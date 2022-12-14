from flask import Flask, request, render_template, url_for, redirect, session
import yaml
import psycopg2
from auth import start_verify, check_verify
from PIL import Image
import base64
import io
from flask import Response as FlaskResponse
from flask import jsonify
import json
from dump_table import dump_rows as dr
import numpy as np
import cv2
from tensorflow import keras
from send_msg import send_message
from decimal import *


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
def getOldTime(number):
    with conn.cursor() as c:
        #get the old amount of time driven
        table_name = 'LEADERBOARD'
        c.execute(f'SELECT time FROM {table_name} WHERE number=\'{number}\';')
        time = c.fetchall()
        # print(user)
        conn.commit()
        oldTime = float(time[0][0])
    return oldTime

def updateLeaderboard(hoursDriven, oldTime, number):
    # number = str(session['number'])
    updatedHours = hoursDriven + oldTime
    with conn.cursor() as c:
        table_name = 'LEADERBOARD'
        c.execute(f'UPDATE {table_name} SET time = \'{updatedHours}\'WHERE number=\'{number}\';')
        c.execute(f'UPDATE {table_name} SET numdrives = numdrives + 1 WHERE number=\'{number}\';')
        # c.execute(f'UPDATE {table_name} SET numdrives = \'{updatedHours}\'WHERE number=\'{number}\';')
        # time = c.fetchall()
        # print(user)
        conn.commit()
    with conn.cursor() as c:
        table_name = 'LEADERBOARD'
        #THIS DOESNT WORK BECAUSE TIME IS A VARCHAR AND NOT AN INT/DOUBLE
        c.execute(f'SELECT COUNT(name) FROM {table_name} WHERE number!=\'{number}\' AND time > \'{updatedHours}\';')
        result = c.fetchall()
        # print(user)
        conn.commit()
        print(result)
        above = result[0][0]
        hoursDriven /= 60000
        toSend = f'You added {hoursDriven} seconds of safe driving. There are now {above} people ahead of you on the leaderboard! Keep it up!'
        send_message(toSend, number)

def send_warning(num):
    print('sending warning for')
    with conn.cursor() as c:
        table_name = 'USERS'
        num = num.strip()
        sql = f'''SELECT name, econ1 FROM {table_name} WHERE number='{num}';'''
        print(sql)
        c.execute(sql)
        # c.execute(f'UPDATE {table_name} SET numdrives = numdrives + 1 WHERE number=\'{number}\';')
        # c.execute(f'UPDATE {table_name} SET numdrives = \'{updatedHours}\'WHERE number=\'{number}\';')
        res = c.fetchall()
        print(res)
        # print(user)
        conn.commit()
        name = res[0][0]
        econ1 = res[0][1]
        print(f'name: {name}, econ1: {econ1}')
        econ1='4845385080'

        to_send = f'We have detected that {name} is potentially driving drowsy, you may want to contact them to make sure that they are not making bad decisions'
        send_message(to_send, econ1)
    

@app.route('/end_drive', methods = ["POST"])
def end():
    number = str(session['number'])
    print('ending the drive')
    # number = "7817388373"
    hoursDriven = request.json['hoursDriven']
    print(f'ending drive for: {number}, with hoursDriven: {hoursDriven}')
    # badTime = request.json['hoursDriven']
    oldTime = getOldTime(number)
    #update leaderboard
    updateLeaderboard(hoursDriven, oldTime, number)

@app.route('/landing', methods = ["GET"])
def landing():
    table_name = 'USERS'
    number = str(session['number'])
    with conn.cursor() as c:
        c.execute(f'SELECT * FROM {table_name} WHERE number=\'{number}\';')
        user = c.fetchall()
        # print(user)
        conn.commit()
        name = user[0][1]
    return render_template('landing.html',name=name)

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
            query = 'INSERT INTO Users (number, name, school, econ1) VALUES (\'{}\', \'{}\', \'{}\', \'{}\');'.format(number, uname, school, econ1)
            cur.execute(query)
            conn.commit()
        return None

detector = cv2.FaceDetectorYN.create(
    'face_detection_yunet_2022mar.onnx',
    "",
    (640, 480),
    0.9, # score threshold
    0.3, # nms threshold
    5000 # top k
)
eyesModel = keras.models.load_model('eyesOpenClose.h5')
yawnModel = keras.models.load_model('yawn.h5')
@app.route('/live', methods=['POST'])
def live():
    #take in the image and compare it to the model
    
    print(f'request: {request}')
    # print(f'request form: {request.form}')
    # print(f'request.values: {request.values}')
    # print(f'request json: {request.get_json()}' )
    # print(f'{request.json["imageSrc"]}')
    # with open('test.json', 'w') as f:
        # f.write(request.json['imageSrc'])

    # ret = json.load(request.json)
    # print(f'ret: {ret}')
    # print(f'{type(request.json["imageSrc"])}')
    b = (request.json['imageSrc'])
    z = b[b.find('/9'):]
    nparr = np.fromstring(base64.b64decode(z), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    frame = cv2.flip(frame, 1) # if your camera reverses your image
    faces = detector.detect(frame)[1]
    
    if faces is not None:
        face_boxes = []
        for face in faces:
            x,y,w,h = face[:4].astype('int')
            face_boxes.append([x,y,x+w,y+h])
            
        lx,ly,la,lb = sorted([[x,y,a,b,(a-x)*(b-y)] for x,y,a,b in face_boxes], key=lambda x: x[4])[-1][:-1]
        face_array = frame[max(0,ly):min(lb,frame.shape[0]), max(0,lx):min(la,frame.shape[1])]
        face_array = cv2.resize(face_array, (100,100)).reshape(-1, 100, 100, 3)

        yawn_pred = yawnModel.predict(face_array/255, verbose=0).item()
        yawn_text = "Mouth: Open" if yawn_pred < 0.2 else "Mouth: Closed"
        cv2.putText(frame, yawn_text, (frame.shape[1]-250,frame.shape[0]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 203, 241), 2)

        eyes_pred = eyesModel.predict(face_array/255, verbose=0).item()
        eyes_text = "Eyes: Closed" if eyes_pred < 0.50 else "Eyes: Open"
        cv2.putText(frame, eyes_text, (25,frame.shape[0]-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 203, 241), 2)

        frame = cv2.rectangle(frame, (lx, ly), (la, lb), (0, 255, 0), 2)
        

        retval, buffer = cv2.imencode('.jpg', frame)

        # z = base64.b64encode(frame.tobytes())
        # b = "data:image/jpeg;base64,/9j/" + z.decode("utf-8") 
        b = base64.b64encode(buffer)
        b = "data:image/jpeg;base64," + b.decode("utf-8") 

    asleep = False
    print(f'yawn_pres: {yawn_pred}, eyes_pred: {eyes_pred}')
    if yawn_pred < 0.2 and eyes_pred < 0.5:
        print('asleep')
        asleep = True
        number = session['number']
        # number='9788065553'
        print(f'number: {number}')
        print('going to send warning')
        send_warning(number)


    response = {
        'asleep': asleep,
        'image': b,
    }
    response = json.dumps(response)
    return response

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
    number = request.values.get('pnum')[2:]
    session['number'] = number
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
                # return render_template('register.html')
                return redirect(url_for('register'))
            else:
                print(f'The user exists, res: {res}')
                #there is a user so send them to logged in page
                return redirect(url_for('landing'))   
    elif status == 'pending':
        #not approved
        print(status)
        print('not approved')
        return render_template('index.html')
    else:
        print('.')     

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    with conn.cursor() as c:
        c.execute(f'SELECT * FROM LEADERBOARD ORDER BY time DESC LIMIT 5;')
        users = c.fetchall()
        conn.commit()
        top5 = {1:{},2:{},3:{},4:{},5:{}}
        i = 1
        for user in users:
            try:
                top5[i] = {'name':user[1],'drives':user[2],'time':user[3]}
            except:
                top5[i] = {'name':'','drives':'','time':''}
            i+=1
            
        one = top5[1]
        two = top5[2]
        three = top5[3]
        four = top5[4]
        five = top5[5]
    return render_template('leaderboard.html',one=one,two=two,three=three,four=four,five=five)


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