import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="26032000"
)

# Создание курсора
cur = conn.cursor()

# Выполнение запроса
cur.execute("SELECT * FROM employees")

# Получение результата
result = cur.fetchall()
print(result)

# Закрытие курсора и соединения с базой данных
cur.close()
conn.close()