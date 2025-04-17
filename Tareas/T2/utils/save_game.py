from clases.modificador import ModificadorPositivo, ModificadorNegativo
from clases.arbol import Arbol

from utils.id import create_id_generator

from parametros import SAVES_FOLDER

from pathlib import Path


def save_game(
    dinero: int, round: int, player_tree: Arbol, enemy_tree: Arbol, filename: str
):
    generate_id = create_id_generator()

    id_by_positive_modifier_name = dict()
    id_by_negative_modifier_name = dict()

    positive_modifiers = ModificadorPositivo.get_modifiers()
    negative_modifiers = ModificadorNegativo.get_modifiers()

    for name in positive_modifiers:
        id_by_positive_modifier_name[name] = generate_id()

    for name in negative_modifiers:
        id_by_negative_modifier_name[name] = generate_id()

    with Path(SAVES_FOLDER, filename).open("w") as file:
        # Saves positive modifiers types with id
        file.write(f"{len(id_by_positive_modifier_name)}\n")

        for name in positive_modifiers:
            file.write(f"{id_by_positive_modifier_name[name]};{name}\n")

        # Saves negative modifiers types with id
        file.write(f"{len(id_by_negative_modifier_name)}\n")

        for name in negative_modifiers:
            file.write(f"{id_by_negative_modifier_name[name]};{name}\n")

        # Saves player's money
        file.write(f"{dinero};{round}\n")

        # Saves player tree
        file.write(f"{player_tree.nombre};{len(player_tree.branches)}\n")

        for branch in player_tree.branches:
            parent = player_tree.find_parent(branch)

            name_parent_id = parent.id if parent else -1

            file.write(
                f"{branch.id};{branch.nombre};{name_parent_id};{len(branch.modificadores)};{branch.salud};{branch._vitalidad_maxima};{branch.defensa};{branch.dano_base}\n"
            )

            if branch.modificadores:
                ids = []

                for modifier in branch.modificadores:
                    if isinstance(modifier, ModificadorPositivo):
                        ids.append(f"{id_by_positive_modifier_name[modifier.nombre]}")
                    else:
                        ids.append(f"{id_by_negative_modifier_name[modifier.nombre]}")

                file.write(";".join(ids))
                file.write("\n")

        # Saves enemy tree
        file.write(f"{enemy_tree.nombre};{len(enemy_tree.branches)}\n")

        for branch in enemy_tree.branches:
            parent = enemy_tree.find_parent(branch)

            name_parent_id = parent.id if parent else -1

            file.write(
                f"{branch.id};{branch.nombre};{name_parent_id};{len(branch.modificadores)};{branch.salud};{branch._vitalidad_maxima};{branch.defensa};{branch.dano_base}\n"
            )

            if branch.modificadores:
                ids = []

                for modifier in branch.modificadores:
                    if isinstance(modifier, ModificadorPositivo):
                        ids.append(f"{id_by_positive_modifier_name[modifier.nombre]}")
                    else:
                        ids.append(f"{id_by_negative_modifier_name[modifier.nombre]}")

                file.write(";".join(ids))
                file.write("\n")
