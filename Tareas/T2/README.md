# Tarea 2: DCConquista de Yggdrasil 🌳

## Consideraciones generales :octocat:

### Programación Orientada a Objetos

- ✅ Incluye y aplica herencia en un contexto correcto de la tarea.

- ✅ Incluye y aplica clases abstractas en un contexto correcto de la tarea.

- ✅ Incluye y aplica polimorfismo en un contexto correcto de la tarea.

- ✅ Incluye y aplica decoradores que definen properties en un contexto correcto de la tarea.

#### Preparación programa

- ✅ El programa recibe correctamente la dificultad como argumento por consola.

- ✅ El programa muestra correctamente la interfaz de Selección Inicial, y es cosistente con la dificultad ingresada por el jugador.

- ✅ El jugador comienza con el Arbol selecciónado.

- ✅ El Arbol del oponente es elegido de la forma pedida.

- ✅ Se muestra un cuadro de resumen con la información del Arbol del jugador y el Arbol del oponente. Ademas se muestra un mensaje de bienvenida.

#### Entidades

##### Árbol

- ✅ Modela correctamente la clase Arbol, utilizando los contenidos de OOP que corresponden

- ✅ Modela correctamente los atributos de Arbol.

- ✅ El método Cargar Item está implementado correctamente.

- ✅ El método Atacar está implementado correctamente.

- ✅ El método Pasar ronda está implementado correctamente.

- ✅ El método Resumir Arbol está implementado correctamente.

- ✅ El método Presentarse está implementado correctamente.

##### Rama

- ✅ Modela correctamente la clase Rama, utilizando los contenidos de OOP que corresponden

- ✅ Modela correctamente los atributos de Rama.

- ✅ El método Cargar Item está implementado correctamente.

- ✅ El método Pasar ronda está implementado correctamente.

- ✅ El método Atacar está implementado correctamente.

- ✅ El método Recibir daño está implementado correctamente.

- ✅ El método Presentarse está implementado correctamente.

- ✅ Cuando se asigna un Modificador, se carga correctamente en caso de que la rama estuviera vacía, o se reemplaza de acuerdo con la mecánica de la Rama.

##### Modificadores

- ✅ Modela correctamente la clase Modificadores, utilizando los contenidos de OOP que corresponden.

- ✅ Modela correctamente los atributos de Modificadores.

- ✅ Se modela correctamente la utilización de Modificadores en Ramas.

- ✅ Los modificadores afectan positivamente o negativamente a una Rama, según la caracteristica de la Rama.

#### Flujo del programa

##### Menú principal

- ✅ Se muestran todas las opciones pedidas en el menú principal.

- ✅ Se muestran todas las opciones pedidas en el menú principal.

- ✅ Al seleccionar 'Salir', se imprime un mensaje para el usuario y se termina el programa

##### Menú tienda

- ✅ Se muestra toda la información pedida en el menú tienda.

- ✅ Se muestran todos los modificadores para el menú tienda, según el archivo correspondiente.

- ✅ Al comprar un modificador, se adjunta correctamente a la Rama indicada por el jugador.

- ✅ La opción 'Volver al menú de inicio' funciona correctamente

##### Mecánica de juego

- ✅ El orden de los eventos al pasar ronda sigue el orden pedido en el enunciado.

- ✅ El juego finaliza inmediatamente en caso de derrota de cualquiera de los árboles, y muestra el mensaje pedido según el caso.

##### Robustez

- ✅ Todos los menús son a prueba de cualquier tipo de input.

#### Combate

##### Ataque

- ✅ Al atacar, se puede seleccionar una rama de su propio Arbol, la cual está disponible y viva.

- ✅ Se maneja correctamente la selección de la rama del Arbol Enemigo.

##### Cálculo de daño

- ✅ El jugador puede seleccionar la rama desde la cuál atacará.

- ✅ La rama que recibe el daño se selecciona en base a su profundidad.

- ✅ La rama que recibe el daño se selecciona en base a su profundidad.

- ✅ El daño se resta correctamente a la vida de la rama, considerando su defensa, para ambos árboles.

##### Recepción de daño

- ✅ Se respeta el orden pedido para la recepción de daño.

#### Archivos

##### Archivos.txt

- ✅ Se trabaja correctamente con los tres archivos de dificultad.

- ✅ Se trabaja correctamente con el archivo de ramas.txt

- ✅ Se trabaja correctamente con el archivo de modificadores.txt y modificadores_negativos.txt

##### parametros.py

- ✅ Utiliza e importa correctamente los parámetros del archivo parametros.py.

- ✅ El archivo parametros.py contiene todos los parámetros y constantes que se utilizan a lo largo del programa, además de los especificados en el enunciado.

#### Bonus Guardar Partida

##### README

- ✅ El README de la Tarea en el repositorio personal explicita que se implementó el BONUS.

##### Implementación

- ✅ Al iniciar el programa, el jugador puede dar como argumento el nombre del archivo que tiene la partida guardada.

- ✅ El Menu Principal tiene la opcion Guardar Partida, y puede accionarse.

- ✅ La opción Guardar Partida da la posibilidad al jugador de detener el programa, entendiendo que el jugador abandonaría el juego.

- ✅ La opción Guardar Partida crea un archivo con todos los detalles requeridos en el enunciado, guardando en este toda la información de la partida actual.

- ✅ Es posible guardar la partida las veces que se deseen, siempre considerando la información actualizada al instante de seleccionar la opción.

- ✅ Si se carga una partida guardada al iniciar el programa, el juego se reanuda con la información contenida en el archivo indicado por el jugador.

## Ejecución :computer:

El módulo principal a ejecutar es `main.py`, que inicia un menú. Además, se debe crear los siguientes archivos y directorios adicionales:

1. Carpeta `data` en la raíz `./`
2. Carpeta `saves` en la raíz `./` para guardar las partidas guardadas.
3. Carpetas `utils` y `clases` con los archivos específicados en la sección de librerías propias.

**Para agregar archivos con los árboles, ramas y modificadores para la lectura del programa se deben colocar como un `.txt` siguiendo el formato en una carpeta dentro de `data`.**

## Librerías :books:

### Librerías externas utilizadas

Se utilizaron las siguientes librerías externas:

1. `pathlib`: `Path`
2. `sys`: `argv`
3. `io`: `TextIOWrapper` para el tipado de una función (autorizado en [está issue](https://github.com/IIC2233/Syllabus/issues/173#issuecomment-2813560523)).
4. `random`: `choices`, `choices`
5. `typing`: `Self`
6. `abc`: `ABC`, `abstractmethod`
7. `copy`: `deepcopy`
8. `datetime`: `datetime` para generar timestamps para los archivos de guardado (autorizado en [está issue](https://github.com/IIC2233/Syllabus/issues/173#issuecomment-2813560523)).

### Librerías propias

Por otro lado, los módulos que fueron creados fueron los siguientes:

1. `parametros`: Contiene a las constantes `EASY`, `NORMAL`, `HARD`, `DIFICULTIES`, `FILES_BY_DIFICULTIES`, `BRANCHES_FILE`, `DATA_FOLDER`, `DINERO_INICIAL`, `DINERO_CACTOOS`, `GANANCIA_POR_RONDA`, `POSITIVE_MODIFIER_FILE`, `NEGATIVE_MODIFIER_FILE`, `SAVES_FOLDER`, `DEFENSA_MINIMA`, `DEFENSA_MAXIMA`.

2. `utils.choice`: Contiene la función `event_happens`.
3. `utils.input`: Contiene la función `read_input`.
4. `utils.menu`: Contiene las funciones `get_number_in_range`, `get_number_in_set`, `print_menu`, `ask_yes_no`.
5. `utils.read_save`: Contiene las funciones `read_branches` y `read_save`.
6. `utils.read`: Contiene las funciones `create_branch`, `read_branches`, `read_trees`.
7. `utils.save_game`: Contiene la función `save_game`.
8. `utils.terminal`: Contiene las funciones `erase_terminal`, `print_title`, `create_table`, `continue_input` y `exit_message`.
9. `clases.ramas`: Contiene las clases `Rama`, `Ficus`, `Celery`, `Hyedrid`, `Paalm`, `Alovelis`, `Pine` y `Cactoos`. También contiene la función `get_branch_class`.
10. `clases.modificador`: Contiene las clases `Modificador`, `ModificadorPositivo` y `ModificadorNegativo`.
11. `clases.game`: Contiene la clase `Game`.
12. `clases.arbol`: Contiene la clase `Arbol`.

## Supuestos y consideraciones adicionales :thinking:

1. El bonus **sí fue implementado** y se detalla su implementación en la sección [bonus](#bonus).

2. Débido a no estar específicado en enunciado, los modificadores que afectan la vitalidad máxima no afectan la salud de la rama, a no ser que el cambio en la vitalidad máxima haga que la salud de la rama supere su vitalidad máxima. En ese caso, la salud de la rama se ajusta a su vitalidad máxima. Este tema fue discutido en [está issue](https://github.com/IIC2233/Syllabus/issues/185#issuecomment-2784199719).

3. En mi código ocupo [_list comprehension_](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions), uso que fue autorizado en [está issue](https://github.com/IIC2233/Syllabus/issues/247).

4. Se reutilizarón partes del código de la tarea 1, algunas fueron copiadas sin cambios y otras fueron modificadas. Los códigos reutilizados fueron citados en el código mismo.

5. Se asume un margen de error para los cálculos que involucren _floats_ debido a [los problemas de presición que conllevan](https://docs.python.org/3/tutorial/floatingpoint.html), por ejemplo que la resistencia a plagar se vea afectaba, si la resistencia es `0.8` y hago el cálculo `1 - 0.8` el resultado es `0.19999999999999996` y no `0.2`. Los _floats_ decidí no redondearlos en los apartados donde no se especifica y no afecta realmente al funcionamiento del problema.

6. La tarea fue desarrollada en un entorno virtual creado con _Conda_ (versión `24.9.2`), instalando _Python_ en su versión `3.11.11`. Se desarrollo en ell sistema operativo `Archcraft x86_64`con _kernel_ `Linux 6.13.8-arch1`.

## Implementación del programa

El programa fue implementado en el idioma inglés, conservando los nombres de los métodos ya entregados en el idioma español.

A la clase `Arbol` añadí los siguientes métodos/properties explicados en el código mismo con comentarios:

- `Arbol.branches`
- `Arbol.branches_by_level`
- `Arbol.max_deep`
- `Arbol.branches_ids`
- `Arbol.get_random_deeper_branch`
- `Arbol.find_parent`
- `Arbol.find_by_id`
- `Arbol.remove_branch`
- `Arbol.copy`

A la clase `Rama` añadí los siguientes métodos/properties explicados en el código mismo con comentarios:

- `Rama.all_subtree_branches`
- `Rama.modificadores`
- `Rama.get_branches`

A la clase Hyedrid, tuve que añadir la propiedad `Hyedrid._modificadores` siendo una lista para implementar el funcionamiento especial de esa rama, el atributo `Hyedrid.modificador` de esa clase queda en desuso por eso mismo. Para las demás ramas el atributo `Rama.modificador` es el valor del modificador equipado y además la property `Rama.modificadores` es una lista de los modificadores que tiene la rama, funcionado para todas las ramas.

A la clase `Modificador`, `ModificadorPositivo` y `ModificadorNegativo` añadí los siguientes métodos/properties explicados en el código mismo con comentarios:

- `Modificador.get_modifiers`
- `ModificadorNegativo.get_modifiers`
- `ModificadorPositivo.get_modifiers`

## Bonus

Las partidas se guardan en la carpeta `saves` con el formato `save-{timestamp}` siendo el timestamp generado en formato `{año}-{mes}-{dia}-{hora}-{segundo}` indicando los números de cada campo usando la librería `datetime` como fue mencionado el la sección de librerías externas.

### Formato

El formato busca ser fácil de entender con la explicación pertinente, ordenado y barato en términos de _bytes_. El formato de los archivos de guardado es el siguiente:

- Una línea con la cantidad de modificadores positivos
- Una línea por cada modificador positivo, con el id creado por el programa y el nombre del modificador separados por un `;`.
- Una línea con la cantidad de modificadores negativos
- Una línea por cada modificador negativo, con el id creado por el programa y el nombre del modificador separados por un `;`.
- Una linea con el dinero del jugador y la ronda, separados por un `;`.
- Una línea con el nombre del árbol del jugador y la cantidad de ramas, separados por un `;`.
- Una línea por cada rama del árbol del jugador, con el id de la rama, el nombre de la rama, el id del padre de la rama, la cantidad de modificadores equipados, la salud de la rama, la vitalidad maxima de la rama, la defensa de la rama y el daño base de la rama separados por `;`. Si la rama es la principal (no tiene padre), el id es igual a `-1` para indicar que no tiene padre.
- Una línea por cada modificador con un `+` si es positivo o un `-` si es negativo, junto con el id creado para el modificador separado por `;`.
- Una línea con el nombre del árbol del emenigo y la cantidad de ramas, separados por un `;`.
- Una línea por cada rama del árbol del emenigo, con el id de la rama, el nombre de la rama, el id del padre de la rama, la cantidad de modificadores equipados, la salud de la rama, la vitalidad maxima de la rama, la defensa de la rama y el daño base de la rama separados por `;`. Si la rama es la principal (no tiene padre), el id es igual a `-1` para indicar que no tiene padre.
- Una línea por cada modificador con un `+` si es positivo o un `-` si es negativo, junto con el id creado para el modificador separado por `;`.

#### Ejemplo

Para una partida en la ronda `8` con dinero `$90`.

El árbol del jugador siendo el siguiente:

```bash
------------------------------
Baobab del Despertar
------------------------------
[1] Alovelis, Vida: 1600/1720, Daño base: 25, Defensa: -20.0%, Resistencia a plagas: 80.0%, Modificadores: Avispas Asesinas (Negativo).
  \--subramas-
  [2] Celery, Vida: 1000/1250, Daño base: 35, Defensa: 0.0%, Resistencia a plagas: 75.0%, Modificadores: Flor (Positivo).
    \--subramas-
    [3] Alovelis, Vida: 1750/1750, Daño base: 25, Defensa: -40.0%, Resistencia a plagas: 80.0%, Modificadores: Hongo Parasitario (Negativo).
      \--subramas-
      [4] Alovelis, Vida: 1600/1700, Daño base: 25, Defensa: 0.0%, Resistencia a plagas: 80.0%, Modificadores: Zancudos (Negativo).
        \--subramas-
        [5] Alovelis, Vida: 1700/1800, Daño base: 25, Defensa: -50.0%, Resistencia a plagas: 80.0%, Modificadores: Termitas (Negativo).
        [6] Cactoos, Vida: 700/700, Daño base: 55, Defensa: -11.0%, Resistencia a plagas: 90.0%, Modificadores: Zancudos (Negativo).
      [7] Celery, Vida: 1150/1150, Daño base: 35, Defensa: -40.0%, Resistencia a plagas: 75.0%, Modificadores: Hongo Parasitario (Negativo).
        \--subramas-
        [8] Paalm, Vida: 2000/2000, Daño base: 40, Defensa: 0.2, Resistencia a plagas: 0.9.
        [9] Hyedrid, Vida: 900/900, Daño base: 75, Defensa: -50.0%, Resistencia a plagas: 95.0%, Modificadores: Espora Tóxica (Positivo), Espora Tóxica (Positivo).
  [10] Paalm, Vida: 1950/1950, Daño base: 40, Defensa: -9.999999999999998%, Resistencia a plagas: 90.0%, Modificadores: Espora Tóxica (Positivo).
  [11] Celery, Vida: 1000/1200, Daño base: 35, Defensa: 0.0%, Resistencia a plagas: 75.0%, Modificadores: Gusano Minador (Negativo).
  [12] Pine, Vida: 800/800, Daño base: 60, Defensa: -20.0%, Resistencia a plagas: 80.0%, Modificadores: Zancudos (Negativo).
  [13] Alovelis, Vida: 1800/1800, Daño base: 25, Defensa: 0.0%, Resistencia a plagas: 80.0%, Modificadores: Gusano Minador (Negativo).
```

Y el árbol del enemigo siendo el siguiente:

```bash
------------------------------
Baobab del Despertar
------------------------------
[14] Alovelis, Vida: 1800/1800, Daño base: 25, Defensa: 0.0, Resistencia a plagas: 0.8.
  \--subramas-
  [15] Celery, Vida: 1000/1000, Daño base: 35, Defensa: 0.0%, Resistencia a plagas: 75.0%, Modificadores: Ácaros Chupadores (Negativo).
    \--subramas-
    [16] Alovelis, Vida: 1700/1700, Daño base: 25, Defensa: -50.0%, Resistencia a plagas: 80.0%, Modificadores: Moho Gris (Negativo).
      \--subramas-
      [17] Alovelis, Vida: 1800/1800, Daño base: 25, Defensa: 0.0, Resistencia a plagas: 0.8.
        \--subramas-
        [18] Alovelis, Vida: 1800/1800, Daño base: 25, Defensa: 0.0%, Resistencia a plagas: 80.0%, Modificadores: Gusano Minador (Negativo).
        [19] Cactoos, Vida: 800/800, Daño base: 55, Defensa: -0.11, Resistencia a plagas: 0.9.
      [20] Celery, Vida: 1000/1000, Daño base: 35, Defensa: 0.0%, Resistencia a plagas: 75.0%, Modificadores: Ácaros Chupadores (Negativo).
        \--subramas-
        [21] Paalm, Vida: 1920/1920, Daño base: 40, Defensa: 0.0%, Resistencia a plagas: 90.0%, Modificadores: Avispas Asesinas (Negativo).
        [22] Hyedrid, Vida: 1000/1000, Daño base: 75, Defensa: -0.1, Resistencia a plagas: 0.95.
  [23] Paalm, Vida: 2000/2000, Daño base: 40, Defensa: 0.2, Resistencia a plagas: 0.9.
  [24] Celery, Vida: 1000/1000, Daño base: 35, Defensa: 0.0%, Resistencia a plagas: 75.0%, Modificadores: Ácaros Chupadores (Negativo).
  [25] Pine, Vida: 900/900, Daño base: 60, Defensa: -0.2, Resistencia a plagas: 0.8.
  [26] Alovelis, Vida: 1600/1600, Daño base: 25, Defensa: 0.0%, Resistencia a plagas: 80.0%, Modificadores: Ácaros Chupadores (Negativo).
```

El contenido del archivo de guardado con nombre de ejemplo `save-2025-04-17-15-59-44.txt` en la carpeta `saves` sería:

```bash
19
1;Flor
2;Flor Dorada
3;Panal de Abejas
4;Nido de Pajaros
5;Espinas Afiladas
6;Savia Curativa
7;Hoja de Roble
8;Veneno Lento
9;Escudo de Corteza
10;Aguijón Venenoso
11;Néctar Dulce
12;Espora Tóxica
13;Raíces Profundas
14;Látigo de Zarzas
15;Fruto Energético
16;Hojas Doradas
17;Polen Alergénico
18;Corteza Reflejante
19;Semilla Explosiva
7
20;Termitas
21;Zancudos
22;Hongo Parasitario
23;Gusano Minador
24;Moho Gris
25;Avispas Asesinas
26;Ácaros Chupadores
90;8
Baobab del Despertar;13
1;Alovelis;-1;1;1600;1800;-0.1;25
-;25
2;Celery;1;1;1000;1200;0.0;35
+;1
3;Alovelis;2;1;1750;1800;-0.2;25
-;22
4;Alovelis;3;1;1600;1800;0.0;25
-;21
5;Alovelis;4;1;1700;1800;-0.3;25
-;20
6;Cactoos;4;1;700;800;-0.11;55
-;21
7;Celery;3;1;1150;1200;-0.2;35
-;22
8;Paalm;7;0;2000;2000;0.2;40
9;Hyedrid;7;2;900;1000;-0.4;75
+;12
+;12
10;Paalm;1;1;1950;2000;0.05000000000000002;40
+;12
11;Celery;1;1;1000;1200;0.0;35
-;23
12;Pine;1;1;800;900;-0.2;60
-;21
13;Alovelis;1;1;1800;1800;0.0;25
-;23
Baobab del Despertar;13
14;Alovelis;-1;0;1800;1800;0.0;25
15;Celery;14;1;1000;1200;0.0;35
-;26
16;Alovelis;15;1;1700;1800;-0.4;25
-;24
17;Alovelis;16;0;1800;1800;0.0;25
18;Alovelis;17;1;1800;1800;0.0;25
-;23
19;Cactoos;17;0;800;800;-0.11;55
20;Celery;16;1;1000;1200;0.0;35
-;26
21;Paalm;20;1;1920;2000;0.1;40
-;25
22;Hyedrid;20;0;1000;1000;-0.1;75
23;Paalm;14;0;2000;2000;0.2;40
24;Celery;14;1;1000;1200;0.0;35
-;26
25;Pine;14;0;900;900;-0.2;60
26;Alovelis;14;1;1600;1800;0.0;25
-;26
```

El comando para iniciar la partida con el archivo de guardado sería `python main.py save-2025-04-17-15-59-44.txt`.
