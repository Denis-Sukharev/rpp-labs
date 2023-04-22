import sqlite3

def create_users_table():

    # Установка соединения с базой данных
    conn = sqlite3.connect('database.db')
    
    # Создание объекта курсора
    cursor = conn.cursor()
    
    # Создание таблицы "users"
    cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
    
    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()


# функция для добавления нового пользователя в таблицу "users"
def add_user(name, email):
    # Установка соединения с базой данных
    conn = sqlite3.connect('database.db')
    
    # Создание объекта курсора
    cursor = conn.cursor()
    
    # Добавление пользователя в таблицу "users"
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    
    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()


# функция для получения всех пользователей из таблицы "users"
def get_all_users():
    # Установка соединения с базой данных
    conn = sqlite3.connect('database.db')
    
    # Создание объекта курсора
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()
    
    # закрытие соединения
    conn.close()
    
    return all_users


# функция для получения пользователя по id из таблицы "users"
def get_user_by_id(user_id):
    # Установка соединения с базой данных
    conn = sqlite3.connect('database.db')
    
    # Создание объекта курсора
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    
    # закрытие соединения
    conn.close()
    
    return user


# функция для удаления пользователя по id из таблицы "users"
def delete_user_by_id(user_id):
    # Установка соединения с базой данных
    conn = sqlite3.connect('database.db')
    
    # Создание объекта курсора
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    
    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()
    

# Создание таблицы "users"
# create_users_table()

# добавление нового пользователя
user_id = add_user("Иван", "ivan@example.com")
print(f"Добавлен пользователь с id {user_id}")

# получение всех пользователей из таблицы
all_users = get_all_users()
for user in all_users:
    print(user)

# получение пользователя по id
user = get_user_by_id(user_id)
print(f"Пользователь {user}")

# удалить пользователя по id
delete_user_by_id(6)

