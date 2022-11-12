from flask import Flask
import yaml
import psycopg2


creds = yaml.safe_load(open("creds.yaml", "r"))

app = Flask(__name__)


conn = psycopg2.connect(creds["DATABASE_URL"])

# with conn.cursor() as cur:
#     cur.execute("SELECT now()")
#     res = cur.fetchall()
#     conn.commit()
#     print(res)

@app.route('/')
def test():
    print('got a request here')
