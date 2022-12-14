import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

from flask import Flask, render_template, request
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>黃鈺慈的vercel</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/today>顯示日期時間</a><br>"
    homepage += "<a href=/welcome?nick=育慈>傳送使用者暱稱</a><br>"
    homepage += "<a href=/about>育慈簡介網頁</a><br>"
    homepage += "<br><a href=/read>讀取Firestore資料</a><br>"
    return homepage

@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
    now = datetime.now()
    return render_template("today.html", datetime = str(now))

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    user = request.values.get("nick")
    return render_template("welcome.html", name=user)

@app.route("/about")
def about():
    return render_template("aboutme.html")

@app.route("/read", methods=["GET", "POST"])
def read():
    if request.method == "POST":
        cond = request.form["keyword"]
        result = "您輸入的課程關鍵字是："+ cond  
        db = firestore.client()   
        collection_ref = db.collection("1111")    
        docs = collection_ref.get()
        result = ""    
        for doc in docs:
            dict = doc.to_dict()
            if cond in dict["Course"]:         
                result += dict["Leacture"]+"老師開的"+dict["Course"]+"課程，每周"+dict["Time"]+"於"+dict["Room"]+"上課<br>"  
        return result
    else:
        return render_template("read.html")

#if __name__ == "__main__":
#    app.run()