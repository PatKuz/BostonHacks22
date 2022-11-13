from flask import Flask, request, render_template, url_for, redirect, session
import yaml
import psycopg2
from auth import start_verify, check_verify


creds = yaml.safe_load(open("creds.yaml", "r"))

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' #needed to use sessions


conn = psycopg2.connect(creds["DATABASE_URL"])

@app.route('/')
def test():
    return render_template('index.html')

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
        print(f'request: {request}')
        print(f'request form: {request.form}')
        print(f'request.values: {request.values}')
        print(number)

        if not verify_phone(number):
            print('could not verify number')
            return False

        # session['number'] = number
        # print(f'set the session number, {session["number"]}')
        status = start_verify(number)
        print(f'status: {status}')

        #for a test try to insert number into sql table
        return True


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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        print(f'here, {session["number"]}')
        return render_template('register.html')
    else:
        # print(f'getting request: {request}')
        # print(f'request form: {request.form}')
        print("Request Received!")
        print("Username: " + request.form['name'])
        print("School: "+ request.form['school'])
        print("Emergency Contact1: " + request.form['contact1'])
        uname = request.form['name']
        school = request.form['school']
        econ1 = request.form['contact1']
        number = session['number']
        with conn.cursor() as cur:
            # number='9788065553'
            # sql = f'''SELECT * FROM USERS WHERE number = '5';'''
            query = 'INSERT INTO Users (number, name, school, econ1, econ2) VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\');'.format(number, uname, school, econ1, 'NULL')
            cur.execute(query)
            conn.commit()
        return None

@app.route('/live', methods=['POST'])
def live():
    #take in the image and compare it to the model

    print(f'request: {request}')
    print(f'request form: {request.form}')
    print(f'request.values: {request.values}')
    print(f'request json {request.get_json()}' )
    print('we are here')
    return True

@app.route('/verify', methods=['GET', 'Post'])
def verify():
    '''
    takes in the number and the code and either takes them into the logged
    in page if they already have an account or brings them to the create an account
    page
    '''
    if request.method == 'GET':
        x = 1
        # return render_template('verify.html', new=True, pnum=6)


    print(request.values)

    # new = request.values.get('new')
    number = request.values.get('pnum')
    # number = session['number']
    print('the number is')
    print(number)
    # number = '9788065553'
    print(f'number: {number}')
    code = request.values.get('code')
    print(f'code: {code}')

    status = check_verify(number, code)


    print(f'status: {status}')
    print(f'type: {type(status)}')

    if status == 'approved':
        print(f'the number was approved, checking to see if they already exist')
        #check to see if the phone number is already associated with a user account
        with conn.cursor() as cur:
            # number='9788065553'
            # sql = f'''SELECT * FROM USERS WHERE number = '5';'''
            sql = f'''SELECT * FROM USERS WHERE number='{number}';'''
            cur.execute(sql)
            res = cur.fetchall()
            conn.commit()
            print(res)
            if res == []:
                #no use exists, send them to create account page  
                print(f'the user does not exist')
                print('rendering register')
                # session['number'] = number #store number as session variable
                return render_template('register.html')
                # return redirect(url_for('register'))
            else:
                print(f'The user exists, res: {res}')
                #there is a user so send them to logged in page
                return True       
    else:
        #not approved
        print(status)
        print('not aproved')


    # print('is a new user')
    # print(new)

    # temp_ret = temp_codes.document(number).get().to_dict()
    # actual_num = temp_ret['number']

    # if str(actual_num) == str(code):
    #     print('it worked')
    #     if new == 'True':
    #         # return form
    #         return render_template('survey.html', pnum=number)
    #     else:
    #         print('is not a new user')
    #         # return whatever page we show people who already 
    #         # return render_template('results.html') #will need to give it more 0
    #         return get_group(number)

    # else:
    #     print('actual code')
    #     print(actual_num)
    #     print('inputed code')
    #     print(code)
    #     print('wrong code')
    #     return render_template('verify.html', new=new, pnum=number)


def verify_phone(num):
    print('calling the verify method')
    num = num[2:]
    import re
    regex = re.compile(r'^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')
    return regex.search(str(num))