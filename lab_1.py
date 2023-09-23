# pip install flask

from flask import Flask, request, jsonify
import psycopg2

# Объект Flask
app = Flask(__name__)
conn = psycopg2.connect(database = 'lab1', user = 'postgres', password = 'postgres', host='localhost')
cursor = conn.cursor()
conn.commit()

# Маршрут для обработки POST-запросов по пути
@app.route('/v1/add/region', methods=['POST'])
def process_json():
    # Получение значения заголовка 'Content-Type' из запроса
    content_type = request.headers.get('Content-Type')
    # Проверка, что 'Content-Type' равен 'application/json'
    if (content_type == 'application/json'):
        # Получение JSON-данных из тела запроса
        json = request.json
        return json # Возвращение полученных данных
    else:
        return 'Content-Type not supported!' # Возвращение ошибки, если Content-Type не поддерживается


    region_code = data['id']
    region_name = data['name']


    # Проверка, существует ли уже запись с переданным кодом региона
    cursor.execute('SELECT * FROM region WHERE id = %s', (region_code,))
    existing_region = cursor.fetchone()
    if existing_region:
        return jsonify({'error': 'Region with id {} already exists'.format(region_code)}), 400


    # Сохранение кода и названия региона в таблицу region
    cur.execute('INSERT INTO region (id, name) VALUES (%s, %s)', (region_code, region_name))
    conn.commit()
    return jsonify({'message': 'Region added successfully'}), 200


@app.route("/v1/add/tax-param", methods=["POST"])
def add_tax_param():
    # Извлечение значений из JSON-запроса
    city_code = request.json.get("city_code")  # кода города
    horse_power_from = request.json.get("horse_power_from")  # начальных лошадиных сил
    horse_power_to = request.json.get("horse_power_to")  # конечных лошадиных сил
    year_from = request.json.get("year_from")  # начального года производства автомобиля
    year_to = request.json.get("year_to")  # конечного года производства автомобиля
    tax_rate = request.json.get("tax_rate")  # ставки налога

    cur = conn.cursor()

    # Проверка существования региона с заданным кодом
    cur.execute("SELECT id FROM regions WHERE code = %s", (city_code,))
    region_id = cur.fetchone()  # Получение результата запроса
    if not region_id:
        cur.close()
        return jsonify({"error": "Регион с указанным кодом не найден"}), 400  # Возврат ошибки, если регион не найден

    # Проверка отсутствия объекта налогообложения для заданного региона, диапазона лошадиных сил и диапазона годов производства автомобиля
    cur.execute("""
        SELECT id 
        FROM tax_param 
        WHERE region_id = %s 
            AND horse_power_from <= %s 
            AND horse_power_to >= %s 
            AND year_from <= %s 
            AND year_to >= %s
    """, (region_id[0], horse_power_to, horse_power_from, year_to, year_from))
    existing_tax_param_id = cur.fetchone() # Получение результата запроса
    if existing_tax_param_id:
        cur.close()
        return jsonify({"error": "Объект налогообложения для заданных параметров уже существует"}), 400 # Возврат ошибки, если объект уже существует

    # Добавление объекта налогообложения в таблицу tax_param
    cur.execute("""
        INSERT INTO tax_param (region_id, horse_power_from, horse_power_to, year_from, year_to, tax_rate) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (region_id[0], horse_power_from, horse_power_to, year_from, year_to, tax_rate))
    conn.commit() # Сохранение изменений в БД
    cur.close()
    return jsonify({"message": "Информация об объекте налогообложения успешно добавлена"})

@app.route("/v1/add/auto", methods=["POST"])
def add_auto():
    city_code = request.json.get("city_code")
    car_name = request.json.get("car_name")
    horse_power = request.json.get("horse_power")
    year = request.json.get("year")

    cur = conn.cursor()

    # Проверка существования региона с заданным кодом
    cur.execute("SELECT id FROM regions WHERE code = %s", (city_code,))
    region_id = cur.fetchone()
    if not region_id:
        cur.close()
        return jsonify({"error": "Регион с указанным кодом не найден"}), 400

    # Проверка существования объекта налогообложения для заданного региона, количества лошадиных сил и года выпуска автомобиля
    cur.execute("""
        SELECT tax_rate 
        FROM tax_param 
        WHERE region_id = %s 
            AND horse_power_from <= %s 
            AND horse_power_to >= %s 
            AND year_from <= %s 
            AND year_to >= %s
    """, (region_id[0], horse_power, horse_power, year, year))
    tax_rate = cur.fetchone()
    if not tax_rate:
        cur.close()
        return jsonify({"error": "Объект налогообложения для заданных параметров не найден"}), 400

    # Вычисление транспортного налога
    transport_tax = tax_rate[0] * horse_power

    # Добавление информации об автомобиле в таблицу auto
    cur.execute("""
        INSERT INTO auto (region_id, car_name, horse_power, year, transport_tax)
        VALUES (%s, %s, %s, %s, %s)
    """, (region_id[0], car_name, horse_power, year, transport_tax))
    conn.commit()
    cur.close()
    return jsonify({"message": "Информация об автомобиле успешно добавлена"})


@app.route("/v1/auto", methods=["GET"])
def get_auto():
    auto_id = request.args.get("auto_id")

    cur = conn.cursor()

    # Получение информации об автомобиле по его идентификатору
    cur.execute("""
        SELECT auto.id, regions.code, auto.car_name, auto.horse_power, auto.year, auto.transport_tax 
        FROM auto 
        JOIN regions ON auto.region_id = regions.id 
        WHERE auto.id = %s
    """, (auto_id,))
    auto_info = cur.fetchone()
    if not auto_info:
        cur.close()
        return jsonify({"error": "Автомобиль с указанным идентификатором не найден"}), 400

    # Формирование ответа в формате JSON информации из БД
    response = {
        "id": auto_info[0],
        "city_code": auto_info[1],
        "car_name": auto_info[2],
        "horse_power": auto_info[3],
        "year": auto_info[4],
        "transport_tax": auto_info[5]
    }

    cur.close()
    return jsonify(response) # Возврат информации об автомобиле в формате JSON
 
if __name__ == "__main__":
    app.run(debug=True) # Запуск приложения Flask


