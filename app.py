from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///record.db"
app.config['SQLALCHEMY_TRACK_MPDIFICATION'] = False
db = SQLAlchemy(app)



class Record(db.Model):
    no = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self) -> str:
        return f"{self.no} - {self.title}"


@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        record = Record(title=title, desc=desc)
        db.session.add(record)
        db.session.commit()
    allRecord = Record.query.all()    
    return render_template('index.html', allRecord=allRecord)
 
@app.route("/show")
def products():
    allrecord = Record.query.all()
    print(allrecord)
    return "<p>dhananjay.vercel.app</p>"

@app.route("/update/<int:no>",methods=['GET','POST'])
def update(no):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        record = Record.query.filter_by(no=no).first()
        record.title = title
        record.desc = desc
        db.session.add(record)
        db.session.commit()
        return redirect("/")
    record = Record.query.filter_by(no=no).first()    
    return render_template('update.html',record=record)


@app.route('/delete/<int:no>')
def delete(no):
    allrecord = Record.query.filter_by(no=no).first()
    db.session.delete(allrecord)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
