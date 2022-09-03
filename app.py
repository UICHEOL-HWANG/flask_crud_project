from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# #파워쉘 커맨트에서 python 입력 후 Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:59:51) [MSC v.1914 64 bit (AMD64)] on win32
# >>> from app import app, db, User, Post
# >>> db.create_all() 데이터 베이스 초기화 시키면 해당 디렉토리 안으로 site.db가 만들어짐 

class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email =db.Column(db.String(100))
    number =db.Column(db.String(100))
    def __init__(self,name,email,number):
        self.name = name
        self.email = email
        self.number = number
    


@app.route('/')
def index():
    all_data = Data.query.all()
    return render_template('index.html',employees = all_data)

@app.route('/insert' , methods =['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        
        my_data = Data(name,email,number)
        db.session.add(my_data)
        db.session.commit()
        
        flash("노예추가가 완료되었습니다.")

        return redirect(url_for('index')) # 새로운 db 값을 저장해주는 함수

@app.route('/update' ,methods = ['GET','POST'])
def update():
    if request.method == "POST":
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.number = request.form['number']
        
        db.session.commit()

        flash("노예 수정이 완료되었습니다.")
        return redirect(url_for('index')) # 수정된 db 값을 저장해주는 함수

@app.route('/delete/<id>/',methods = ['GET','POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("노예명단 삭제가 완료되었습니다")
    return redirect(url_for('index')) # 삭제할 db값을 지정하는 함수.

if __name__ == "__main__":
    app.run()