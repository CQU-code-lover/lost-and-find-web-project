from flask import *
import mysql.connector
import re

app = Flask(__name__, template_folder='../templates')
@app.route('/')
def a():
        return render_template('fabu.html')
if __name__=="__main__":
    app.run(debug=True)