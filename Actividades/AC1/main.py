from collections import defaultdict
from os.path import join
from utilidades import Anime  # Debes utilizar esta nametupled


#####################################
#       Parte 1 - Cargar datos      #
#####################################
def cargar_animes(ruta_archivo: str) -> list:

    animes = []

    with open(ruta_archivo, encoding="utf-8") as file:
        for line in file:
            name, chaptersText, scoreText, yearText, study, genresText = (
                line.strip().split(",")
            )

            genres = set(genresText.split(";"))

            anime = Anime(
                nombre=name,
                capitulos=int(chaptersText),
                puntaje=int(scoreText),
                estreno=int(yearText),
                estudio=study,
                generos=genres,
            )

            animes.append(anime)

    return animes


#####################################
#        Parte 2 - Consultas        #
#####################################
def animes_por_estreno(animes: list) -> dict:
    animes_by_year = defaultdict(list)

    for anime in animes:
        animes_by_year[anime.estreno].append(anime.nombre)

    return animes_by_year


def descartar_animes(generos_descartados: set, animes: list) -> list:
    animes_filtrados = []

    for anime in animes:
        if generos_descartados & anime.generos:
            continue

        animes_filtrados.append(anime.nombre)

    return animes_filtrados


def resumen_animes_por_ver(*animes: Anime) -> dict:
    results = {"puntaje promedio": 0, "capitulos total": 0, "generos": set()}

    for anime in animes:
        results["puntaje promedio"] += round(anime.puntaje / len(animes), 1)
        results["capitulos total"] += anime.capitulos
        results["generos"] |= anime.generos

    return results


def estudios_con_genero(genero: str, **estudios: list) -> list:
    studies = []

    for study, animes in estudios.items():
        has_genre = False

        for anime in animes:
            if genero in anime.generos:
                has_genre = True
                break

        if has_genre:
            studies.append(study)

    return studies


if __name__ == "__main__":
    #####################################
    #       Parte 1 - Cargar datos      #
    #####################################
    animes = cargar_animes(join("data", "ejemplo.chan"))
    indice = 0
    for anime in animes:
        print(f"{indice} - {anime}")
        indice += 1

    #####################################
    #        Parte 2 - Consultas        #
    #####################################
    # Solo se usará los 2 animes del enunciado.
    datos = [
        Anime(
            nombre="Hunter x Hunter",
            capitulos=62,
            puntaje=9,
            estreno=1999,
            estudio="Nippon Animation",
            generos={"Aventura", "Comedia", "Shonen", "Acción"},
        ),
        Anime(
            nombre="Sakura Card Captor",
            capitulos=70,
            puntaje=10,
            estreno=1998,
            estudio="Madhouse",
            generos={"Shoujo", "Comedia", "Romance", "Acción"},
        ),
    ]

    # animes_por_estreno
    estrenos = animes_por_estreno(datos)
    print(estrenos)

    # descartar_animes
    animes = descartar_animes({"Comedia", "Horror"}, datos)
    print(animes)

    # resumen_animes_por_ver
    resumen = resumen_animes_por_ver(datos[0], datos[1])
    print(resumen)

    # estudios_con_genero
    estudios = estudios_con_genero(
        "Shonen",
        Nippon_Animation=[datos[0]],
        Madhouse=[datos[1]],
    )
    print(estudios)
