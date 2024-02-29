import pymysql
from pydantic import BaseModel
from typing import Optional
from datetime import date
from decouple import config

class Movie(BaseModel):
    id: Optional[int]
    autor: Optional[str]
    descripcion: Optional[str]
    fecha_de_estreno: Optional[date]
    
# Configuración de la conexión a la base de datos
db_params = {
    'host': '127.0.0.1',
    'port': 33306,
    'user': config('MYSQL_USER'),
    'password': config('MYSQL_PASSWORD'),
    'database': config('MYSQL_DB'),
}

# Función para obtener una conexión de la base de datos
def get_db():
    connection = pymysql.connect(**db_params)
    print("Database connection successful")
    return connection


