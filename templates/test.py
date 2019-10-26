#python web main
#by David
#2018/11/7
#数据库：
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__ , template_folder='../templates')
@app.route('/')
def welcome():
    return render_template('main.html')
if __name__=="__main__":
    app.run(debug=True)