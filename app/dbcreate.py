from app import db, User
import csv


def get_add_name(name_str, gpa_str):
    tb = User.query.filter(User.name == name_str).first()
    if not tb:
        tb = Table(name=name_str, gpa=gpa_str)

    return tb


with open('gpa_table.csv', 'r', encoding='utf-8-sig') as f:
    line = csv.DictReader(f, delimiter=';')
    for ro in line:
        if ro['Name'] != '' or ro['GPA'] != '':
            test_rec = get_add_name(str(ro['Name']), str(ro['GPA']))
            db.session.add(test_rec)
    db.session.commit()
