from datetime import datetime
import json
import os.path
from flask import Flask, render_template, request, Markup

app = Flask(__name__)
_curTab = ""


@app.route('/', methods=["GET", "POST"])  # TODO: make it load both files
def index():
    if request.method == "POST":
        j = json.JSONEncoder()
        data = j.encode(request.form)
        _curTab = request.form.get("type")
        file = open('./data/'+_curTab[0]+'L.json',
                    "w+", newline="\n", encoding="utf-8")
        json.dump(data, file)
    return render_template('index.html')


@app.route('/vista', methods=["GET", "POST"])
def vista():
    pData = getData(False)
    pForms = getForms(pData)
    qData = getData(True)
    qForms = getForms(qData)
    return render_template('vista.html', otherstat='Палата',
                           pForms=Markup(pForms), qForms=Markup(qForms), pCount=pData.__len__(), qCount=qData.__len__())


def getData(dataType):
    filepath = ""
    lastK = ""
    if (dataType):
        filepath = './data/qL.json'
        lastK = "cause"
    else:
        filepath = './data/pL.json'
        lastK = "bedNumber"

    if os.path.isfile(filepath):
        j = json.JSONDecoder()
        file = open(filepath)
        data = j.decode(json.load(file))
        k = ["historyNumber", "firstName", "lastName",
             "patrName", "birthDate", "diagnosis", lastK]
        l = int(data.keys().__len__()/7)
        result = [None] * l
        for i in range(l):
            v = [None] * 7
            for j in range(7):
                key = "db["+str(i)+"]["+k[j]+"]"
                v[j] = data.get(key)
            result[i] = v
        result.sort()
    return result


def getForms(data):
    result = ""
    l = data.__len__()
    for i in range(l):
        d = data[i]
        num = str(d[0])
        name = str(d[1] + " "+d[2]+" "+d[3])
        birthday = str(getAge(d[4]))
        diagnose = str(d[5])
        other = str(d[6])
        result += "<a onclick='showInfo("+str(i)+")'>\n<div class='formEntry' id='" + \
            str(i) + "'>\n<h3 class='num'>"+num+"</h3>\n<h3 class='name'>" + \
            name + "</h3>\n<h3 class='other'>" + other + \
            "</h3>\n<input type='hidden' bday='"+birthday + \
            "' dgns='"+diagnose+"'></div>\n</a>"
    return result


def getAge(date):
    bday = date.split("-")
    time = datetime.now().strftime("%Y-%m-%d").split("-")
    a = []
    b = []
    for x in time:
        a.append((int)(x))
    for x in bday:
        b.append((int)(x))
    if (a[2]-b[2] < 0):
        b[1] += 1
    if (a[1]-b[1] < 0):
        b[0] += 1
    return a[0]-b[0]


app.run(
    host='127.0.0.1',
    port=1374,
    debug=True,
    load_dotenv=False


)
