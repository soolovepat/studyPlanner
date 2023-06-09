from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests



app = Flask(__name__)

# import datetime as dt
from pymongo import MongoClient
client = MongoClient('mongodb+srv://powerlife145:test@cluster0.yg0ur8n.mongodb.net/')
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

#---------------------------------------------D-DAY,날씨 플랜 DB
# dday plan DB post(save)
@app.route("/study_ddayplan", methods=["POST"])
def ddayplan_post():
    dday_plan = request.form['ddayplan_give']
    dday_input = request.form['ddayinput_give']
    doc = {
        'ddplan': dday_plan,
        'd-day' : dday_input
    }
    db.dday_plan.insert_one(doc)
    return jsonify({'msg': 'dday 저장 완료!'})

# dday plan DB get
@app.route("/study_ddayplan", methods=["GET"])
def ddayplan_get():
    ddplans = list(db.dday_plan.find({},{'_id':False}))
    return jsonify({'ddayResult': ddplans})
#---------------------------------------------D-DAY 플랜 DB END

@app.route("/study_ddayplan", methods=["GET"])
def weather_get():
    html = requests.get('https://search.naver.com/search.naver?query=날씨')
    soup = bs(html.text,'html.parser')

    data1 = soup.find('span',{'class':'blind'})

    ## 뭐지
    return jsonify({'weatherResult': data1})

if __name__ == '__main__':

    app.run('0.0.0.0', port=5000, debug=True)

    