# Tarea 2: DCC 🗣️❔❔

## Consideraciones generales :octocat:

### Carga de datos

#### cargar_usuarios()

- ✅ Pasan todos los tests para validar el correcto funcionamiento de esta consulta.

#### cargar_productos()

- ✅ Pasan todos los tests para validar el correcto funcionamiento de esta consulta.

#### cargar_ordenes()

- ✅ Pasan todos los tests para validar el correcto funcionamiento de esta consulta.

#### cargar_ordenes_items()

- ✅ Pasan todos los tests para validar el correcto funcionamiento de esta consulta.

#### cargar_proveedores()

- ✅ Pasan todos los tests para validar el correcto funcionamiento de esta consulta.

#### cargar_proveedores_productos()

- ✅ Pasan todos los tests para validar el correcto funcionamiento de esta consulta.

### Consultas Simples

#### productos_desde_fecha()

- ✅ Pasan todos los tests de correctitud, los cuales validan el correcto funcionamiento de esta consulta.
- ✅ Pasan todos los tests de cargar, los cuales validan que la consulta termina en un tiempo adecuado.

#### buscar_orden_por_contenido()

- ✅ Pasan todos los tests de correctitud, los cuales validan el correcto funcionamiento de esta consulta.
- ✅ Pasan todos los tests de cargar, los cuales validan que la consulta termina en un tiempo adecuado.

#### proveedores_por_estado()

- ✅ Pasan todos los tests de correctitud, los cuales validan el correcto funcionamiento de esta consulta.
- ✅ Pasan todos los tests de cargar, los cuales validan que la consulta termina en un tiempo adecuado.

#### ordenes_segun_estado_orden()

- ✅ Pasan todos los tests de correctitud, los cuales validan el correcto funcionamiento de esta consulta.
- ✅ Pasan todos los tests de cargar, los cuales validan que la consulta termina en un tiempo adecuado.

#### ordenes_entre_fechas()

- ✅ Pasan todos los tests de correctitud, los cuales validan el correcto funcionamiento de esta consulta.
- ✅ Pasan todos los tests de cargar, los cuales validan que la consulta termina en un tiempo adecuado.

#### modificar_estado_orden_ordenes_previas_fecha()

- ✅ Pasan todos los tests de correctitud, los cuales validan el correcto funcionamiento de esta consulta.
- ✅ Pasan todos los tests de cargar, los cuales validan que la consulta termina en un tiempo adecuado.

### Consultas Complejas

#### producto_mas_popular()

- ✅ Pasan todos los tests de correctitud, los cuales validan el correcto funcionamiento de esta consulta.
- ✅ Pasan todos los tests de cargar, los cuales validan que la consulta termina en un tiempo adecuado.

#### ordenes_usuario()

- ✅ Pasan todos los tests de correctitud, los cuales validan el correcto funcionamiento de esta consulta.
- ✅ Pasan todos los tests de cargar, los cuales validan que la consulta termina en un tiempo adecuado.

#### valor_orden()

- ✅ Pasan todos los tests de correctitud, los cuales validan el correcto funcionamiento de esta consulta.
- ✅ Pasan todos los tests de cargar, los cuales validan que la consulta termina en un tiempo adecuado.

#### proveedores_segun_precio_productos()

- ✅ Pasan todos los tests de correctitud, los cuales validan el correcto funcionamiento de esta consulta.
- ✅ Pasan todos los tests de cargar, los cuales validan que la consulta termina en un tiempo adecuado.

#### precio_promedio_segun_estado_orden()

- ✅ Pasan todos los tests de correctitud, los cuales validan el correcto funcionamiento de esta consulta.
- ✅ Pasan todos los tests de cargar, los cuales validan que la consulta termina en un tiempo adecuado.

#### cantidad_vendida_productos()

- ✅ Pasan todos los tests de correctitud, los cuales validan el correcto funcionamiento de esta consulta.
- ✅ Pasan todos los tests de cargar, los cuales validan que la consulta termina en un tiempo adecuado.

#### ordenes_dirigidas_al_estado()

- ✅ Pasan todos los tests de correctitud, los cuales validan el correcto funcionamiento de esta consulta.
- ✅ Pasan todos los tests de cargar, los cuales validan que la consulta termina en un tiempo adecuado.

#### ganancias_dadas_por_clientes()

- ✅ Pasan todos los tests de correctitud, los cuales validan el correcto funcionamiento de esta consulta.
- ✅ Pasan todos los tests de cargar, los cuales validan que la consulta termina en un tiempo adecuado.

#### modificar_estados_ordenes_dirigidas_al_estado()

- ✅ Pasan todos los tests de correctitud, los cuales validan el correcto funcionamiento de esta consulta.
- ✅ Pasan todos los tests de cargar, los cuales validan que la consulta termina en un tiempo adecuado.

#### agrupar_items_por_maximo_pedido()

- ✅ Pasan todos los tests de correctitud, los cuales validan el correcto funcionamiento de esta consulta.
- ✅ Pasan todos los tests de cargar, los cuales validan que la consulta termina en un tiempo adecuado.

### Interfaz Gráfica e Interacción

#### Ventana de Entrada

- ✅  Se muestran todos los elementos mínimos solicitados en el enunciado, sin superponerse entre sí.

#### Ventana Principal

- ✅ Se implementa correctamente un input de texto que recibe el path relativo del subset de datos sobre el cual se ejecutarán las consultas.

- ✅ Se implementa correctamente un Drop-down con la lista de consultas disponibles. Permite seleccionar una consulta a ejecutar.

- ✅ Se implementa correctamente un botón con el nombre “Ejecutar Consulta” que se encarga de cargar los datos indicados en el input de texto y ejecutar la consulta seleccionada en el drop-down.
- ✅ Se implementa correctamente un elemento de texto que posea -por lo menos- un scroll de tipo vertical. Este elemento debe permitir ver la cantidad de datos -que corresponden al resultado de la consulta ejecutada- acordes a la página actual. En caso de que no se puedan apreciar todos los datos dentro del elemento, se debe poder acceder a ella por medio del scroll.
- ✅ Se implementa correctamente un botón con el nombre “Siguiente Página”, el cual tiene como funcionalidad poder avanzar en la paginación

- ✅ Se implementa correctamente un sistema de paginación. Se espera que los resultados generados por las consultas sean seccionados en batches (o bloques) de una cierta cantidad de datos y en la ventana solo se puedan ver esa cantidad de resultados por página.

#### Flujo

- ✅ El usuario puede moverse sin problemas a lo largo de toda la aplicación implementada.

## Ejecución :computer:

El módulo principal a ejecutar es `main.py`, que inicia un menú. Además, se debe crear los siguientes archivos y directorios adicionales:

1. Carpeta `data` en la raíz `./` con al menos una subcarpeta con los archivos  `ordenes.csv`, `productos.csv`, `proveedores.csv`, `proveedores_productos.csv`, `usuarios.csv` y `ordenes_items.csv` con los datos de la tarea en el formato válido.

2. Carpetas `utils`, `frontend` y `backend` con los archivos específicados en la sección de librerías propias.

3. Archivo `constants.py` en la carpeta raíz `./` con las constantes utilizadas en el programa.

## Librerías :books:

### Librerías externas utilizadas

Se utilizaron las siguientes librerías externas:

1. `PyQt5`: `QtWidgets`, `QtCore` y `QtGui`
2. `pathlib`: `Path`
3. `sys`: `argv`
4. `collections`: `defaultdict` y `namedtuple`
5. `typing`: `Generator` e `Iterable`
6. `os`: `listdir`, `path`,  `getcwd`

### Librerías propias

Por otro lado, los módulos que fueron creados fueron los siguientes:

1. `constants`: Contiene a las constantes: `DATAFOLDER`, `ITEMS_ORDERS_FILE`, `ORDERS_FILE`, `PRODUCTS_FILE`, `SUPPLIERS_PRODUCTS_FILE`, `SUPPLIERS_FILE`, `USERS_FILE` y `DATA_FILES`.
2. `utils.date`: Contiene la función `date_to_days`.
3. `utils.folders`: Contiene la función `search_folders`.
4. `utils.format`: Contiene las funciones `format_field`, `format_header`, `format_namedtuples` y `format_dicts`.
5. `utils.list`: Contiene la función `flatten`.
6. `utils.path`: Contiene la función `normalize_path`.
7. `utils.read`: Contiene la función `read_format`.
8. `utils.state`: Contiene la función `extract_state`.
9. `backend.consultas`: Contiene las funciones:
    - `cargar_usuarios`
    - `cargar_productos`
    - `cargar_ordenes`
    - `cargar_ordenes_items`
    - `cargar_proveedores`
    - `cargar_proveedores_productos`
    - `productos_desde_fecha`
    - `buscar_orden_por_contenido`
    - `proveedores_por_estado`
    - `ordenes_segun_estado_orden`
    - `ordenes_entre_fechas`
    - `modificar_estado_orden_ordenes_previas_fecha`
    - `producto_mas_popular`
    - `ordenes_usuario`
    - `valor_orden`
    - `proveedores_segun_precio_productos`
    - `precio_promedio_segun_estado_orden`
    - `cantidad_vendida_productos`
    - `ordenes_dirigidas_al_estado`
    - `ganancias_dadas_por_clientes`
    - `modificar_estados_ordenes_dirigidas_al_estado`
    - `agrupar_items_por_maximo_pedido`
10. `frontend.handlers` contiene las funciones:
    - `handle_cargar_usuarios`
    - `handle_cargar_productos`
    - `handle_cargar_ordenes`
    - `handle_cargar_ordenes_items`
    - `handle_cargar_proveedores`
    - `handle_cargar_proveedores_productos`
    - `handle_productos_desde_fecha`
    - `handle_buscar_orden_por_contenido`
    - `handle_proveedores_por_estado`
    - `handle_ordenes_segun_estado_orden`
    - `handle_ordenes_entre_fechas`
    - `handle_modificar_estado_orden_ordenes_previas_fecha`
    - `handle_producto_mas_popular`
    - `handle_ordenes_usuario`
    - `handle_valor_orden`
    - `handle_proveedores_segun_precio_productos`
    - `handle_precio_promedio_segun_estado_orden`
    - `handle_cantidad_vendida_productos`
    - `handle_ordenes_dirigidas_al_estado`
    - `handle_ganancias_dadas_por_clientes`
    - `handle_modificar_estados_ordenes_dirigidas_al_estado`
    - `handle_agrupar_items_por_maximo_pedido`
    - `make_query`
11. `frontend.inputs`: Contiene la clase `QueryInput`.
12. `frontend.main_window`: Contiene la clase `MainWindow`.
13. `frontend.welcome`: Contiene la clase `WelcomeWindow`.

## Supuestos y consideraciones adicionales :thinking:

1. Se tiene considerado un margen de error para los cálculos que involucren _floats_ debido a [los problemas de presición que conllevan](https://docs.python.org/3/tutorial/floatingpoint.html),

2. La tarea fue desarrollada en un entorno virtual creado con _Conda_ (versión `24.9.2`), instalando _Python_ en su versión `3.11.11`. Se desarrollo en el sistema operativo `Archcraft x86_64`con _kernel_ `Linux 6.13.8-arch1`.

3. Las funcionalidades de _PyQt5_ usadas en la tarea fueron investigadas en la [documentación de River Bank](https://www.riverbankcomputing.com/static/Docs/PyQt5/).

4. El uso de `namedtuple.as_dict()` fue descubierto en [Stack Overflow](https://stackoverflow.com/questions/26180528/convert-a-namedtuple-into-a-dictionary) y se utilizó en el backend para copiar una `namedtuple` y modificar sus valores sin afectar la original.

5. El archivo `parametros.py` no fue usado en la implementación del programa, puesto que no se consideró necesario ni de ayuda para la implementación de la tarea.

6. En la interfaz para la consultas que requerían más parámetros que la ruta y generadores de los datos de los archivos _csv_ como fecha o cambios de estado se les definió valores fijos puesto que no estaba especificado en el enunciado y fue discutido en esta [issue](https://github.com/IIC2233/Syllabus/issues/339).

7. Si se entregan rutas en la interfaz con `/` o `\` en los extremos o usando ambos tipos de separadores, el programa los normaliza para que no afecte la carga de los archivos, es decir, es esperado que funcione correctamente con rutas como `/M\S/M//`, ya que el programa la considera como `M/S/M` o `M\S\M` dependiendo el sistema operativo.

## Implementación del programa
