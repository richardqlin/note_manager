from datetime import datetime

import pymongo
from flask import Flask, render_template, request, redirect

from datetime import datetime

from bson.objectid import ObjectId


app = Flask(__name__)

client = pymongo.MongoClient('mongodb+srv://richardlin:richardlin@cluster0.3wovn.mongodb.net/myDatabase?retryWrites=true&w=majority')
db = client.notemanager


@app.route('/',methods=['GET','POST'])
def index():
    if request.method =='GET':
        notes = db.notes.find()
        return render_template('index.html', notes = notes)
    if request.method =='POST':
        document = {}
        document['note'] = request.form['note']
        now = datetime.now()
        document['timestamp'] = now.strftime('%m/%d/%Y, %H:%M:%S')

        db.notes.insert_one(document)
        return redirect('/')


@app.route('/delete/<note_id>')
def delete(note_id):
    db.notes.delete_one({'_id':ObjectId(note_id)})
    return redirect('/')

@app.route('/update/<note_id>', methods=['GET','POST'])
def update(note_id):
    note = db.notes.find_one({'_id':ObjectId(note_id)})
    print(note)
    if request.method == 'GET':
        return render_template('update.html', note = note)
    if request.method == 'POST':
        document = {}
        print(request.form)
        document['note'] = request.form['note']
        now = datetime.now()
        document['timestamp'] = now.strftime('%m/%d/%Y, %H:%M:%S')
        db.notes.update_one({'_id':ObjectId(note_id)}, {'$set':document})
        return redirect('/')

app.run(debug = True)
