from clases.modificador import ModificadorPositivo, ModificadorNegativo
from clases.arbol import Arbol
from clases.ramas import Rama, get_branch_class
from clases.game import Game

from utils.input import read_input, read_inputs

from parametros import SAVES_FOLDER

from pathlib import Path


def read_branches(
    amount: int, positive_modifier_name_by_id, negative_modifier_name_by_id, file
) -> Rama:
    parents = dict()
    branch_by_id = dict()
    branches = []

    main_branch: Rama = None

    for _ in range(amount):
        (
            id,
            name,
            parent_id,
            modifiers_amount,
            salud,
            vida_maxima,
            defensa,
            dano_base,
        ) = read_input([int, str, int, int, int, int, float, int], ";", file.readline())

        branch = get_branch_class(name)(id, [])
        branches.append(branch)

        branch_by_id[id] = branch
        parents[id] = parent_id

        if parent_id == -1:
            main_branch = branch

        branch._salud = salud
        branch._vitalidad_maxima = vida_maxima
        branch._defensa = defensa
        branch.dano_base = dano_base

        if modifiers_amount > 0:
            ids = read_inputs(int, ";", file.readline())

            # Reverse for FIFO
            ids.reverse()

            for id in ids:
                if id in positive_modifier_name_by_id:
                    name = positive_modifier_name_by_id[id]

                    if hasattr(branch, "_modificadores"):
                        branch._modificadores.append(ModificadorPositivo(name))
                    else:
                        branch.modificador = ModificadorPositivo(name)
                else:
                    name = negative_modifier_name_by_id[id]

                    if hasattr(branch, "_modificadores"):
                        branch._modificadores.append(ModificadorNegativo(name))
                    else:
                        branch.modificador = ModificadorNegativo(name)

    for branch in branches:
        if parents[branch.id] == -1:
            continue

        parent = branch_by_id[parents[branch.id]]
        parent.ramas_hijas.append(branch)

    return main_branch


def read_save(filename: str) -> Game:
    with Path(SAVES_FOLDER, filename).open("r") as file:
        positive_modifiers_amount = int(file.readline())

        positive_modifier_name_by_id = dict()

        for _ in range(positive_modifiers_amount):
            id, name = read_input([int, str], ";", file.readline())

            positive_modifier_name_by_id[id] = name

        negative_modifiers_amount = int(file.readline())

        negative_modifier_name_by_id = dict()

        for _ in range(negative_modifiers_amount):
            id, name = read_input([int, str], ";", file.readline())

            negative_modifier_name_by_id[id] = name

        dinero, round = read_input([int, int], ";", file.readline())

        player_tree_name, player_branches_amount = read_input(
            [str, int], ";", file.readline()
        )

        main_player_branch = read_branches(
            player_branches_amount,
            positive_modifier_name_by_id,
            negative_modifier_name_by_id,
            file,
        )

        player_tree = Arbol(main_player_branch, player_tree_name)

        enemy_tree_name, enemy_branches_amount = read_input(
            [str, int], ";", file.readline()
        )

        main_enemy_branch = read_branches(
            enemy_branches_amount,
            positive_modifier_name_by_id,
            negative_modifier_name_by_id,
            file,
        )

        enemy_tree = Arbol(main_enemy_branch, enemy_tree_name)

        game = Game(player_tree, enemy_tree)

        game.dinero = dinero
        game.round = round

        return game
