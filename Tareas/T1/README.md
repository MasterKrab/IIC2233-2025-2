# Tarea 1: DCCortaRamas 🌳✂️

## Consideraciones generales :octocat:

### Automatización `dccortaramas.py`

- ✅ `Bonsai.cargar_bonsai_de_archivo`

- ✅ `Bonsai.visualizar_bonsai`

- ✅ `DCCortaRamas.modificar_nodo`

- ✅ `DCCortaRamas.quitar_nodo`

- ✅ `DCCortaRamas.es_simetrico`

- ✅ `DCCortaRamas.emparejar_bonsai`

- ✅ `DCCortaRamas.emparejar_bonsai_ahorro`

- ✅ `DCCortaRamas.comprobar_solucion`

#### Menú

- ✅ Consola

- ✅ Menú de Inicio

- ✅ Menú de Acciones

#### Aspectos Generales

- ✅ Modularización

- ✅ PEP8

## Ejecución :computer:

El módulo principal a ejecutar es `main.py`, que inicia un menú. Además, se debe crear los siguientes archivos y directorios adicionales:

1. Módulo `dccortaramas.py` en la raíz `./`
2. Carpeta `data` en la raíz `./`

**Para agregar archivos con los bonsáis para la lectura del programa se deben colocar como un `.txt` siguiendo el formato de bonsái en una carpeta dentro de `data`.**

## Librerías :books:

### Librerías externas utilizadas

Se utilizaron las siguientes librerías externas:

1. `pathlib`: `Path`
2. `PrettyPrintTree`
3. `utilidades`: `visualizar_bonsai`

### Librerías propias

Por otro lado, los módulos que fueron creados fueron los siguientes:

1. `dccortaramas`: Contiene a las clases `Bonsai` y `DCCortaRamas`. También las constantes `READ_FOLDER`, `WRITE_FOLDER`, `NOT_ALLOWED`, `DONE`, `NOT_FOUND`, `FAILS`, `MODIFY_FLOWER` y `REMOVE_NODE`.

## Supuestos y consideraciones adicionales :thinking:

Los supuestos considerados son:

1. El costo de cortar un nodo y modificar un nodo deben ser valores no negativos, debido que si son negativos estaríamos ganando, entonces no es un costo. Un costo igual a cero tiene sentido porque representaría que esa acción es gratis, esto no afecta al funcionamiento del código, incluso con costos cero. También se asume que el costo siempre es entero según enunciado.

2. En los tests públicos la cantidad de nodos es a lo más 50, entonces, se podría asumir que ese el tamaño máximo. Aunque para asegurarme creé mis propios casos de prueba con árboles de hasta 1000 nodos y me aseguré de que el código tardara menos de 10 segundos en emparejar.

## Implementación del programa

El programa fue implementado en el idioma inglés, conservando los nombres de los métodos ya entregados en el idioma español.

A la clase `Bonsai` añadí los siguientes métodos explicados en el código mismo con comentarios:

- `Bonsai.find_node_index`
- `Bonsai.find_node`
- `Bonsai.find_parent`
- `Bonsai.remove_node`
- `Bonsai.copy`
- `Bonsai.get_nodes`

A la clase `DCCortaRamas` añadí los siguientes métodos explicados en el código mismo con comentarios:

- `DCCortaRamas.can_remove_node`
- `DCCortaRamas.balance`
- `DCCortaRamas.calculate_cost`
- `DCCortaRamas.apply_solution`
