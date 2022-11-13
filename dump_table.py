import yaml, psycopg2, os

def dump_rows():
    creds = yaml.safe_load(open("creds.yaml", "r"))
    conn = psycopg2.connect(creds["DATABASE_URL"])
    table_name = 'LEADERBOARD'
    with conn.cursor() as c:
        c.execute(f'SELECT * FROM {table_name} ORDER BY time DESC LIMIT 5;')
        users = c.fetchall()
        conn.commit()
        f = open('temp.csv', 'w')
        f.write('NAME,SCHOOL,NUM_DRIVES,TIME\n')
        for user in users:
            f.write('{},{},{},{}\n'.format(user[1],user[2],user[3],user[4]))