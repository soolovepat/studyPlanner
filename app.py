from flask import Flask,session, redirect, url_for, render_template, request, jsonify,flash
app = Flask(__name__)


import datetime as dt
#test 용입니다.
# from pymongo import MongoClient
# client = MongoClient('mongodb+srv://sparta:test@cluster0.efcklz9.mongodb.net/?retryWrites=true&w=majority')
# db = client.dbsparta

from pymongo import MongoClient
import certifi  #테스트 몽고 
ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:test@cluster0.ni7z7tt.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
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
    page_receive = request.form['page_give']
    plan_list = list(db.study_planner.find({}, {'_id': False}))
    count = len(plan_list) + 1
      
    doc = {
        'group':group_receive,
        'plan':plan_receive,
        'num': count,
        'page': page_receive,
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




if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)

    # 테스트입니다 :)
    # test 3
    # test 4