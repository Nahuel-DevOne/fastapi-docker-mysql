from fastapi import APIRouter, HTTPException, Depends
from models import Movie, get_db
from typing import List

router = APIRouter()

# Método para obtener una película por su ID
@router.get("/movies/{movie_id}", response_model=Movie)
def read_movie(movie_id: int, db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM my_movies WHERE id = %s", (movie_id,))
        movie_data = cursor.fetchone()

    if movie_data is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    print(movie_data)

    # Convierte la tupla a un diccionario
    movie_dict = {
        "id": movie_data[0],
        "autor": movie_data[1],
        "descripcion": movie_data[2],
        "fecha_de_estreno": movie_data[3].strftime("%Y-%m-%d")  # Formatea la fecha como string si es necesario
    }

    movie = Movie(**movie_dict)
    return movie


# Método para leer varias películas
@router.get("/movies", response_model=List[Movie])
def read_movies(skip: int = 0, limit: int = 10, db=Depends(get_db)):
    movies = []

    with db.cursor() as cursor:
        sql_query = "SELECT id, autor, descripcion, fecha_de_estreno FROM my_movies LIMIT %s OFFSET %s"
        cursor.execute(sql_query, (limit, skip))
        columns = [column[0] for column in cursor.description]

        print("SQL Query:", cursor.mogrify(sql_query, (limit, skip)))

        for row in cursor.fetchall():
            movie_data = dict(zip(columns, row))

            # Imprimir datos obtenidos de la base de datos
            print("Database Data:", movie_data)

            # Crear un diccionario para los campos opcionales
            optional_fields = {}
            for field in Movie.__annotations__:
                if field in movie_data and movie_data[field] is not None:
                    optional_fields[field] = movie_data[field]

            # Crear un diccionario con todos los campos (requeridos y opcionales)
            all_fields = {**dict.fromkeys(Movie.__annotations__, None), **optional_fields}

            movies.append(Movie(**all_fields))

    return movies


# Método para agregar una nueva película
@router.post("/movies", response_model=Movie)
def create_movie(movie: Movie, db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute("INSERT INTO my_movies (autor, descripcion, fecha_de_estreno) VALUES (%s, %s, %s)",
                       (movie.autor, movie.descripcion, movie.fecha_de_estreno))
        db.commit()

    return movie


# Método para actualizar una película por su ID
@router.put("/movies/{movie_id}", response_model=Movie)
def update_movie(movie_id: int, movie: Movie, db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute("UPDATE my_movies SET autor = %s, descripcion = %s, fecha_de_estreno = %s WHERE id = %s",
                       (movie.autor, movie.descripcion, movie.fecha_de_estreno, movie_id))
        db.commit()

    return movie

# Método para borrar una película por su ID
@router.delete("/movies/{movie_id}", status_code=204)
def delete_movie(movie_id: int, db=Depends(get_db)):
    with db.cursor() as cursor:
        # Verificar si la película existe
        cursor.execute("SELECT * FROM my_movies WHERE id = %s", (movie_id,))
        deleted_movie_data = cursor.fetchone()

        if deleted_movie_data is None:
            raise HTTPException(status_code=404, detail="No se encontró ninguna película con el ID proporcionado")

        # Eliminar la película
        cursor.execute("DELETE FROM my_movies WHERE id = %s", (movie_id,))
        db.commit()

