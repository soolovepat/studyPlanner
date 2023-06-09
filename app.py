from flask import Flask,session, redirect, url_for, render_template, request, jsonify,flash
app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'
app.config['APPLICATION_ROOT'] = '/'  # 애플리케이션의 루트 경로를 설정합니다.
app.config['PREFERRED_URL_SCHEME'] = 'http'  # URL 스킴을 설정합니다.

import threading
import time

import datetime as dt
from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.efcklz9.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        logged_in = True
        return render_template('index.html', username=username, logged_in=logged_in)
    else:
        return redirect(url_for('login'))

# DB 저장
@app.route("/study_planner", methods=["POST"])
def plan_post():
    group_receive = request.form['group_give']
    plan_receive = request.form['plan_give']
    plan_list = list(db.study_planner.find({}, {'_id': False}))
    count = len(plan_list) + 1
      
    doc = {
        'group':group_receive,
        'plan':plan_receive,
        'num': count,
        'done': 0
    }

    db.study_planner.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})

#DB 수정
@app.route("/study_planner/done", methods=["POST"])
def plan_done():
    num_receive = request.form['num_give']
    db.study_planner.update_one({'num':int(num_receive)},{'$set':{'done':1}})
    return jsonify({'msg': '할일 완료!'})

@app.route("/study_planner/undo", methods=["POST"])
def plan_undo():
    num_receive = request.form['num_give']
    db.study_planner.update_one({'num':int(num_receive)},{'$set':{'done':0}})
    return jsonify({'msg': '취소 완료!'})



# DB가져오기
@app.route("/study_planner", methods=["GET"])
def plan_get():
    all_plans = list(db.study_planner.find({},{'_id':False}))
    return jsonify({'result': all_plans})

# 날짜
@app.route("/datedata")
def date_time():
    date_receive = dt.datetime.today().year
    date_receive = dt.datetime.today().month
    date_receive = dt.datetime.today().day
    date_receive = dt.datetime.today().year

    date_DayOfWeek = dt.datetime.weekday()


    return jsonify({'date':date_receive},{'dayofweek':date_DayOfWeek})



# 서브페이지 - 데이터 저장
@app.route("/input_form", methods=["GET", "POST"])
def input_form():
    if request.method == "POST":
        group_receive = request.form['group_give']
        plan_receive = request.form['plan_give']
        plan_list = list(db.study_planner.find({}, {'_id': False}))
        count = len(plan_list) + 1
        
        # MongoDB에 데이터 저장
        doc = {
        'group':group_receive,
        'plan':plan_receive,
        'num': count,
        'done': 0
        }
        db.study_planner.insert_one(doc)

        # 알림 스레드 시작
        t = threading.Thread(target=show_notification)
        t.start()
        
        return jsonify({"msg": "저장 완료!"})
            
    return render_template("input_form.html")

def show_notification():
    time.sleep(5)
    with app.app_context():
        return redirect(url_for("form_view"))

   
# 뷰페이지 - 데이터 조회
@app.route('/form_view')
def form_view():
    data = list(db.study_planner.find({}, {'_id': False}))
    return render_template('form_view.html', result=data)
    
#로그인 회원가입
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SESSION_TYPE'] = 'filesystem'

users_collection = db['users']
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username})

        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('아이디 또는 비밀번호가 틀렸습니다')
            return redirect(url_for('login'))

    return render_template('login.html')

# 회원가입
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = users_collection.find_one({'username': username})

        if existing_user:
            flash('이미 사용중인 아이디 입니다')
            return redirect(url_for('register'))

        new_user = {'username': username, 'password': password}
        users_collection.insert_one(new_user)

        flash('회원가입성공! 로그인해주세요')
        return redirect(url_for('login'))

    return render_template('register1.html')



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    
    app.run('0.0.0.0', port=5000, debug=True)