from typing import List

import uvicorn
import psycopg2 as pg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse
import re

from main import cursor

app = FastAPI()

conn=pg.connect(user='postgres', password='postgres', host='localhost', port='5432', database='lab7')

class Converted(BaseModel):
    code: str
    rate: float

class RequestBody(BaseModel):
    baseCurrency: str
    rates: List[Converted]

def select_one_currency(name):
    cur = conn.cursor()
    cur.execute("""select id from currency_rates 
                            where base_currency = %s""", (name,))
    data_id = cur.fetchall()
    data_id = re.sub(r"[^0-9]", r"", str(data_id))
    print(data_id)
    return (data_id)

@app.post("/load")
async def load_post(RequestBody: RequestBody):
    name = RequestBody.baseCurrency
    rates = RequestBody.rates
    print(name)
    print(rates)
    id_cur = select_one_currency(name)
    try:
        id_cur == []
        cur = conn.cursor()
        cur.execute("""Insert into currency_rates  (base_currency)
                                        values (%s);""", (name,))
        id_cur = select_one_currency(name)
        print(id_cur)
        for i in rates:
            cur = conn.cursor()
            cur.execute("""Insert into currency_rates_values (currency_code, rate, currency_rate_id)
                                         values (%s,%s,%s);""", (i.code, i.rate, id_cur,))
        conn.commit()
        return JSONResponse(content="")
    except Exception as e:
        conn.rollback()
        raise HTTPException(500)

if __name__ == '__main__':
    uvicorn.run(app, port=10611, host='localhost')
