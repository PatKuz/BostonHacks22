from flask import Flask, request
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

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    print('got a request')
    if request.method == 'GET':
        x = 1
    else:
        # Do stuff here
        print('in here')

        # try:
        #     ret = request.get_json()
        # except:
        #     print('could not get json')
        #     return render_template('index.html')
        # print('got here')
        # if ret == None:
        #     return render_template('index.html')

        # number = ret['number']

        number = request.values.get('phone')
        print(request.values)
        print(number)

        if not verify_phone(number):
            print('could not verify number')

        #for a test try to insert number into sql table
        with conn.cursor() as cur:
            id = 43
            name = 'Pat'
            # sql = f'''INSERT into Users values('{id}','{name}','{number}');'''
            sql = '''SELECT * FROM Users;'''
            # sql = '''CREATE TABLE Users(id int,name varchar, number varchar);'''
            cur.execute(sql)
            res = cur.fetchall()
            conn.commit()
            print(res)


        # Check to see if the number is in the data base
        # docs = users.where(u'number', u'==', '5').stream()
        # print(number)

        # size = 0
        # for doc in docs:
        #     if size > 0:
        #         print('something is wrong')
        #     else:
        #         size += 1
        #         # maybe unpack some things about the user


        # need to verify number either way



def verify_phone(num):
    print('calling the verify method')
    import re
    regex = re.compile(r'^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')
    return regex.search(str(num))