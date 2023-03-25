import http.client, urllib.parse
import json

def operate(data: str, left: int):
    dict = json.loads(data)
    if dict['operation'] == 'sum':
        return left + int(dict['number'])
    if dict['operation'] == 'sub':
        return left - int(dict['number'])
    if dict['operation'] == 'mul':
        return left * int(dict['number'])
    if dict['operation'] == 'div':
        return left / int(dict['number'])

    return left

# Результирующее число
result = 0

# Задание 1.11
conn = http.client.HTTPConnection("167.172.172.227:8000")
conn.request("GET", "/number/11")

r1 = conn.getresponse().read().decode()
number1 = json.loads(r1)
result += int(number1['number'])
print("Первое число:", number1['number'])


# Задание 2.11
conn = http.client.HTTPConnection("167.172.172.227:8000")
conn.request("GET", "/number/?option=11")

r1 = conn.getresponse().read().decode()
number2 = json.loads(r1)
result = operate(r1, result)


print("Второе число:", number2['operation'], number2['number'])
print("Результат операции:", int(result))


# Задание 3.11
headers = {'Content-type': 'application/x-www-form-urlencoded'}
conn.request("POST", "/number/", "option=11", headers)

r1 = conn.getresponse().read().decode()
number3 = json.loads(r1)
result = operate(r1, result)

print("Третье число:", number3['operation'], number3['number'])
print("Результат операции:", int(result))


# Задание 4.11
headers = {'Content-type': 'application/json'}
body = {"option": 11}
conn.request("PUT", "/number/", json.dumps(body), headers)

r1 = conn.getresponse().read().decode()
number4 = json.loads(r1)
result = operate(r1, result)

print("Четвертое число:", number4['operation'], number4['number'])
print("Результат операции:", int(result))


# Задание 5.11
headers = {'Content-type': 'application/json'}
body = {"option": 11}
conn.request("DELETE", "/number/", json.dumps(body), headers)

r1 = conn.getresponse().read().decode()
number5 = json.loads(r1)
result = operate(r1, result)

print("Пятое число:", number5['operation'], number5['number'])
print("Результат операции:", int(result))
