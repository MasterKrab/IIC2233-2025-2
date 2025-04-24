from functools import reduce
from itertools import product
from typing import Generator

from utilidades import Pelicula, Genero


# ----------------------------------------------------------------------------
# Parte I: Cargar dataset
# ----------------------------------------------------------------------------


def cargar_peliculas(ruta: str) -> Generator:
    with open(ruta, encoding="utf-8") as file:

        for line in file.readlines()[1:]:
            id_text, title, director, year_text, average_rating_text = line.split(",")

            id = int(id_text)
            year = int(year_text)
            average_rating = float(average_rating_text)

            movie = Pelicula(id, title, director, year, average_rating)

            yield movie


# ----------------------------------------------------------------------------
# Parte II: Consultas sobre generadores
# ----------------------------------------------------------------------------


def obtener_directores(generador_peliculas: Generator) -> Generator:
    return map(lambda movie: movie.director, generador_peliculas)


def obtener_str_titulos(generador_peliculas: Generator) -> str:
    """
    Genera un str con todos los títulos de las películas separados por ", ".
    """

    return reduce(
        lambda last, new: f"{last}, {new}" if last else new,
        map(lambda movie: movie.titulo, generador_peliculas),
        "",
    )


def filtrar_peliculas(
    generador_peliculas: Generator,
    director: str | None = None,
    rating_min: float | None = None,
    rating_max: float | None = None,
) -> filter:
    """
    Filtra los elementos del generador de Películas según lo indicado en el input.
    """

    if rating_min is None:
        rating_min = -float("inf")

    if rating_max is None:
        rating_max = float("inf")

    return filter(
        lambda movie: (True if director is None else movie.director == director)
        and (movie.rating >= rating_min and movie.rating <= rating_max),
        generador_peliculas,
    )


def filtrar_titulos(
    generador_peliculas: Generator, director: str, rating_min: float, rating_max: float
) -> str:
    """
    Genera un str con todos los títulos de las películas separados
    por ", ". Solo se consideran las películas que tengan el mismo
    director que el indicado, tengan un rating igual o mayor al
    rating_min y un rating igual o menor al rating_max.
    """
    return obtener_str_titulos(
        filtrar_peliculas(generador_peliculas, director, rating_min, rating_max)
    )


def filtrar_peliculas_por_genero(
    generador_peliculas: Generator,
    generador_generos: Generator,
    genero: str | None = None,
) -> Generator:
    """
    Crea un generador con todas las combinaciones posibles entre
    el generador de películas y el generador de géneros.
    Después, filtra las pares obtenidos y mantiene únicamente
    los que presentan el mismo id de película.
    Finalmente, retorna una lista con todos los pares pertenecientes
    a la categoría indicada.
    """

    return filter(
        lambda pair: pair[0].id_pelicula == pair[1].id_pelicula
        and (True if genero is None else pair[1].genero == genero),
        product(generador_peliculas, generador_generos),
    )
