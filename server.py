from flask import Flask,render_template,request,send_file
import os
import attendancemarker

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('attendance.html')

@app.route('/upload',methods = ['GET', 'POST'])
def attendance():
    if request.method == 'POST' and 'photos' in request.files:
        for f in request.files.getlist('photos'):
            f.save( "newinput/"+f.filename)
        attendancemarker.get_attendance("newinput/")
        return send_file('newinput/attendance.xlsx')

if __name__ == '__main__':
    app.run()