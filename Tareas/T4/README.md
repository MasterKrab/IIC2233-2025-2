# Tarea 4: DCCaída de palabras

## Consideraciones generales :octocat:

Esta todo implementado lo del enunciado de la tarea, excepto los bloques de hielo y bruma.

## Ejecución :computer:

### Ejecución Servidor

En la carpeta raíz del proyecto `./` se debe ejecutar el siguiente comando:

```bash
python -m servidor.main
```

### Ejecución Cliente

En la carpeta raíz del proyecto `./` se debe ejecutar el siguiente comando:

```bash
python -m cliente.main
```

### Carpetas y archivos necesarios

* Carpeta `servidor/dcconjuntos` con los archivos de conjuntos en el formato de la tarea.

* Archivos `conexion-socket.json` y `conexion-webservice.json` en la carpeta `cliente` y `servidor`, con puertos distintos para el socket y el webservice.

## Librerías :books:

### Librerías externas utilizadas

Se utilizaron las siguientes librerías externas:

* `PyQt5` (Se debe instalar)
* `flask` (Se debe instalar)
* `pathlib`
* `sys`
* `collections`
* `typing`
* `os`
* `socket`
* `queue`
* `requests`
* `time`
* `functools`
* `wsgiref`
* `json`

### Librerías propias

La tarea requiere de todos los archivos de python presentes en el repositorio, tanto en la raíz como en las carpetas `cliente` y `servidor`. El código presente en la raíz es código compartido entre el cliente y el servidor, por otro lado los archivos en las carpetas `cliente` y `servidor` son específicos de cada uno.

## Supuestos y consideraciones adicionales :thinking:

1. Se tiene considerado un margen de error para los cálculos que involucren _floats_ debido a [los problemas de presición que conllevan](https://docs.python.org/3/tutorial/floatingpoint.html),

2. La tarea fue desarrollada en un entorno virtual creado con _Conda_ (versión `24.9.2`), instalando _Python_ en su versión `3.11.11`. Se desarrollo en el sistema operativo `Archcraft x86_64`con _kernel_ `Linux 6.13.8-arch1`.

3. Las funcionalidades de _PyQt5_ usadas en la tarea fueron investigadas en la [documentación de River Bank](https://www.riverbankcomputing.com/static/Docs/PyQt5/) y [geeksforgeeks](https://www.geeksforgeeks.org/), excepto los códigos que contienen una cita que indica lo contrario.

4. El código de la [experiencia 2 del ramo](https://github.com/IIC2233/Syllabus/tree/main/Experiencias/EX02) fue usado y modificado sustancialmente para la implementación del socket del servidor y el cliente.

5. Se utilizaron 2 archivos de conexión en formato _JSON_ debido que no es posible tener un _socket_ y un _webservice_ en el mismo puerto, por como fue discutido en esta [issue](https://github.com/IIC2233/Syllabus/issues/521).

## Implementación del programa
