from time import time
from random import shuffle, randint
from threading import Thread, Lock
from queue import Queue

from servidor.utils.read_sets import read_set_words
from servidor.utils.game import (
    generate_spawn_interval,
    calculate_fall_time,
    calculate_points,
    save_game,
)
from servidor.parametros import (
    DIFICULTAD_BASE,
    INCREMENTO_DIFICULTAD,
    TIEMPO_INCREMENTO_DIFICULTAD,
)
from parametros import VIDAS_INICIALES, CUSTOM
from utils.find import find


class WordBlock:
    def __init__(self, user: dict, word: str, dificulty: int, time: int) -> None:
        self.user = user
        self.word = word
        self.start_time = time
        self.fall_time = calculate_fall_time(dificulty)
        self.horizontal_position = randint(0, 100) / 100
        self.is_confirmed = False

    @property
    def is_active(self) -> bool:
        current_time = time()
        difference = (current_time - self.start_time) * 1e3

        return difference < self.fall_time

    @property
    def user_info(self) -> dict:
        return {
            "word": self.word,
            "horizontal-position": self.horizontal_position,
            "is-confirmed": self.is_confirmed,
            "fall-time": self.fall_time,
            "start-time": self.start_time,
        }


class Game(Thread):
    def __init__(self, id: int, users: list, game_set: str, users_lock: Lock) -> None:
        super().__init__(daemon=True)

        self.users = dict()

        for user_thread in users:
            self.users[user_thread.id] = {
                "name": user_thread.name,
                "thread": user_thread,
                "score": 0,
                "streak": 0,
                "lives": VIDAS_INICIALES,
                "effects": [],
                "words": [],
            }

        self.game_set = game_set
        self.id = id
        self.is_running = True

        self.start_time = time()
        self.current_time = self.start_time
        self.last_spawn_time = self.start_time

        self.users_lock = users_lock

        self.game_actions_queue = Queue()

        self.game_actions_thread = Thread(target=self.proces_game_actions, daemon=True)
        self.game_actions_thread.start()

        self.check_if_game_over_thread = Thread(
            target=self.check_if_game_over, daemon=True
        )
        self.check_if_game_over_thread.start()

        for user_thread in users:
            user_thread.game_actions_queue = self.game_actions_queue

        self.words_queue = []

        if game_set == CUSTOM:
            self.words = set()

            for user_thread in users:
                self.words += set(user_thread.custom_words)
        else:
            self.words = read_set_words(game_set)

        self.spawn_interval = 0

        for user in self.users.values():
            self.send_game_state(user["thread"].id)

        self.ranking = dict()
        self.end_message_user_id = set()

    @property
    def dificulty(self):
        time_elapsed = (self.current_time - self.start_time) * 1e3

        delta = int(time_elapsed / TIEMPO_INCREMENTO_DIFICULTAD)

        return DIFICULTAD_BASE + delta * INCREMENTO_DIFICULTAD

    def update_words_state(self):
        with self.users_lock:
            for user_data in list(self.users.values()):

                made_change = False

                for word in user_data["words"]:
                    if word.is_active:
                        continue

                    if word.is_confirmed:
                        continue

                    user_data["streak"] = 0
                    user_data["lives"] = max(0, user_data["lives"] - 1)
                    user_data["words"].remove(word)
                    made_change = True

                if made_change:
                    self.send_game_state(user_data["thread"].id)

        if self.current_time * 1e3 - self.last_spawn_time < self.spawn_interval:
            return

        if not self.words_queue:
            self.words_queue = list(self.words)
            shuffle(self.words_queue)

        spawn_word = self.words_queue.pop()

        with self.users_lock:
            for user_data in self.users.values():
                word_block = WordBlock(
                    user_data,
                    spawn_word,
                    self.dificulty,
                    self.current_time,
                )

                self.last_spawn_time = self.current_time * 1e3
                self.spawn_interval = generate_spawn_interval(self.dificulty)

                user_data["words"].append(word_block)
                user_data["thread"].pending_messages.put(
                    {
                        "type": "game-state",
                        "action": "new-word",
                        "word": word_block.user_info,
                        "server-time": self.current_time,
                    }
                )

    def save_ranking(self, id: int) -> None:
        if id in self.ranking:
            return

        user = self.users[id]
        thread = user["thread"]

        self.ranking[id] = {
            "nombre": thread.name,
            "supervivencia": time() - self.start_time,
            "puntaje": user["score"],
        }

    def check_if_game_over(self):
        while self.is_running:
            if self.users_lock.locked():
                continue

            with self.users_lock:
                users_alive = 0

                for user in self.users.values():
                    if user["lives"] > 0:
                        users_alive += 1
                        continue

                    self.save_ranking(user["thread"].id)

                if users_alive <= 0:
                    self.is_running = False
                    continue

                for user in self.users.values():
                    if user["lives"] > 0:
                        continue

                    thread = user["thread"]

                    self.end_message_user_id.add(thread.id)
                    thread.pending_messages.put(
                        {
                            "type": "game-state",
                            "action": "loose",
                        }
                    )

    def run(self):
        while self.is_running:
            self.current_time = time()
            self.update_words_state()

            with self.users_lock:
                for user in self.users.values():
                    if not user["thread"].is_connected:
                        user["lives"] = 0

        for user in self.users.values():
            self.save_ranking(user["thread"].id)

        winner_ranking = max(
            self.ranking.values(),
            key=lambda user: user["supervivencia"],
        )

        winner = find(
            lambda user: user["thread"].name == winner_ranking["nombre"],
            self.users.values(),
        )

        winner["thread"].pending_messages.put({"type": "game-state", "action": "win"})

        for user in self.users.values():
            thread = user["thread"]
            id = thread.id

            if id == winner["thread"].id or id in self.end_message_user_id:
                continue

            thread.pending_messages.put(
                {
                    "type": "game-state",
                    "action": "loose",
                }
            )

        save_game(self.id, self.game_set, self.ranking)

    def proces_game_actions(self):
        while self.is_running:
            if not self.game_actions_queue.empty():
                message = self.game_actions_queue.get()

                if message["game-action"] == "word-typed":
                    self.word_typed(message["user-id"], message["word"])

    def word_typed(self, user_id: int, word: str) -> None:
        if user_id not in self.users:
            return

        with self.users_lock:
            user_data = self.users[user_id]

            if user_data["lives"] <= 0:
                return

            word_thread = find(lambda thread: thread.word == word, user_data["words"])

            if word_thread is None:
                user_data["streak"] = 0
                return

            if not word_thread.is_active:
                return

            user_data["score"] += calculate_points(
                word, self.dificulty, user_data["streak"]
            )
            word_thread.is_confirmed = True
            user_data["words"].remove(word_thread)
            user_data["streak"] += 1

            user_data["thread"].pending_messages.put(
                {"type": "game-state", "action": "word-typed", "word": word}
            )
            self.send_game_state(user_id)

    def send_game_state(self, user_id: int) -> None:
        user = self.users[user_id]

        user_thread = user["thread"]

        if not user_thread.is_connected:
            return

        game_state = {
            "type": "game-state",
            "action": "state",
            "name": user["name"],
            "streak": user["streak"],
            "score": user["score"],
            "lives": user["lives"],
            "players": [
                {
                    "name": user["name"],
                    "score": user["score"],
                    "lives": user["lives"],
                    "streak": user["streak"],
                }
                for user in self.users.values()
            ],
        }

        user_thread.pending_messages.put(game_state)
