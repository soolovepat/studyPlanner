from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

# import datetime as dt
from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.efcklz9.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

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

# # 날짜
# @app.route("/datedata")
# def date_time():
#     date_receive = dt.datetime.today().year
#     date_receive = dt.datetime.today().month
#     date_receive = dt.datetime.today().day
#     date_receive = dt.datetime.today().year

#     date_DayOfWeek = dt.datetime.weekday()


#     return jsonify({'date':date_receive},{'dayofweek':date_DayOfWeek})

if __name__ == '__main__':

    app.run('0.0.0.0', port=5000, debug=True)