import time
import csv
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)

db = SQLAlchemy(app)


class Challenges(db.Model):
    __tablename__ = "Challenges"
    id = db.Column('id', db.Integer, primary_key=True)
    begin = db.Column(db.DateTime(timezone=True) , default=datetime.utcnow)
    end = db.Column(db.DateTime(timezone=True) , default=datetime.utcnow)
    Duration=db.Column(db.Integer)
    Phone_Number=db.Column(db.Integer, unique=True)

    def __init__(self,begin,end,Duration,Phone_Number):
        self.begin = begin
        self.end = end
        self.Duration=Duration
        self.Phone_Number=Phone_Number



@app.route("/challenges/<int:id_str>/", methods=["GET"])
def get_poluch(id_str):
    # находим id
    data1 = Challenges.query.filter(Challenges.id == id_str).first()
    text_404 = "No such id"
    if data1:
        bg=data1.begin
        bg2=data1.end
        data = { "id" : data1.id, "Начало" : bg.strftime("%m %d %Y %H:%M:%S") ,"Завершене" : bg2.strftime("%m %d %Y %H:%M:%S") ,"Длительность" : data1.Duration , "Телефонный номер" : data1.Phone_Number}
        return jsonify(data), 200
    else:
        #если id нет
        data = {'status': text_404}
        return jsonify(data), 404

@app.route("/all_challenges", methods=["GET"])
def get_all():
    sort = request.args.get("sort")

    datas  = db.session.query(Challenges)
    text_500 = "No such properties"

    # Если сортировка указана
    if sort:
        # Если такое свойство есть у модели
        if hasattr(Challenges, sort):
            datas = datas.order_by(getattr(Challenges,sort))
        # Если такого свойства нет
        else:
            data = {'status': text_500}
            return jsonify(data), 500

    # готовим полученные объекты к выводу
    challs_dict = []
    for data1 in datas:
        bg=data1.begin
        bg2=data1.end
        data = { "id" : data1.id, "Начало" : bg.strftime("%m %d %Y %H:%M:%S") ,"Завершене" : bg2.strftime("%m %d %Y %H:%M:%S") ,"Длительность" : data1.Duration , "Телефонный номер" : data1.Phone_Number}
        challs_dict.append(data)
    return jsonify(challs_dict)



def get_add_name( begin_str,end_str,Duration_data,Phone_Number_str):
    tb = Challenges.query.filter(Challenges.Phone_Number == Phone_Number_str).first()
    if not tb:
        tb = Challenges( begin = begin_str,end = end_str, Duration = Duration_data, Phone_Number = Phone_Number_str )
    return tb


def init_db():
    with open('gpa_table.csv', 'r', encoding='utf-8-sig') as f:
        line = csv.DictReader(f, delimiter=';')
        for ro in line:
            if ro['Начало'] != '' or ro['Завершене'] != '' or ro['Телефон'] != '' or ro['Статус_завершен'] != '' :
                aer=[(thing) for thing in (ro['Начало']).split() ]
                date_begin_data = datetime.strptime(ro['Начало'], '%m-%d-%Y %H::%M::%S')

                date_end_data = datetime.strptime(ro['Завершене'], '%m-%d-%Y %H::%M::%S')
                date_Duration_data =(date_end_data - date_begin_data).total_seconds()

                aert=int(ro['Телефон'])

                test_rec = get_add_name(date_begin_data,date_end_data,date_Duration_data,aert)
                db.session.add(test_rec)
        db.session.commit()


if __name__ == '__main__':
    dbstatus = False
    while not dbstatus:
        try:
            db.create_all()
        except Exception as e:
            time.sleep(1)
        else:
            dbstatus = True
    init_db()
    app.run(debug=True, host='0.0.0.0')
