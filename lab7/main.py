import uvicorn
import psycopg2 as pg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse
import re

app = FastAPI()

conn=pg.connect(user='postgres', password='postgres', host='localhost', port='5432', database='lab7')
cursor=conn.cursor()

def convert(base, target, user_sum):
    cursor.execute(
        """
        select %(user_sum)s * crv.rate 
            from currency_rates cr
            JOIN currency_rates_values crv on cr.id = crv.currence_rate_id
        where cr.base_currency = %(base)s AND crv.currency_code = %(target)s
        """, {"base": base, "target": target, "user_sum": user_sum}
    )
    data_id=cursor.fetchone()
    print(data_id)
    return data_id[0]


@app.get("/convert")
def convert_get(baseCurrency: str, convertedCurrency: str, sum: int):
    try:
        return {'converted': convert(base=baseCurrency, target=convertedCurrency, user_sum=sum)}
    except Exception as e:
        print(e)
        raise HTTPException(500, error="Not exists")

if __name__ == '__main__':
    uvicorn.run(app, port=10612, host='localhost')
