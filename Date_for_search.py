import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Параметры подключения к базе данных из переменных окружения
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# SQL-запрос для получения данных
SQL_QUERY = """
    SELECT MAX(code) AS "Код", name_ru AS "Текст"
    FROM dict_enstru
    GROUP BY name_ru
"""

# Функция для извлечения данных из PostgreSQL
def fetch_data_from_postgres():
    try:
        # Подключаемся к базе данных
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        # Выполняем SQL-запрос и загружаем результат в DataFrame
        df = pd.read_sql(SQL_QUERY, conn)
        
        # Закрываем соединение
        conn.close()

        # Сохраняем полученные данные в CSV-файл
        df.to_csv('product_names_with_codes.csv', index=False)
        print("Данные успешно сохранены в product_names_with_codes.csv")
        
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")

# Вызываем функцию
if __name__ == "__main__":
    fetch_data_from_postgres()
