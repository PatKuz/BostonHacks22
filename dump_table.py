import yaml, psycopg2, os

def dump_rows():
    creds = yaml.safe_load(open("creds.yaml", "r"))
    conn = psycopg2.connect(creds["DATABASE_URL"])
    table_name = 'USERS'
    with conn.cursor() as c:
        c.execute(f'SELECT * FROM {table_name}')
        users = c.fetchall()
        conn.commit()
        f = open('temp.csv', 'w')
        f.write('NUMBER,NAME,SCHOOL,ECON\n')
        for user in users:
            f.write('{},{},{},{}\n'.format(user[0],user[1],user[2],user[3]))
        
def cleanup():
    if os.path.exists("temp.csv"):
        os.remove("temp.csv")
    else:
        return
