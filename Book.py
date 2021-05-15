from flask import Flask, render_template , request , redirect ,url_for ,session
from flask_pymongo import PyMongo 
import bcrypt


app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/Standalone"
mongo = PyMongo(app)



@app.route('/')
def base():
    return render_template('Base.html')

@app.route('/Bookmarks')
def book_page():
    return render_template('book.html')


@app.route('/manage')
def manage_page():
    return render_template('manage.html')
    
@app.route('/deleteall')
def deleteall_page():
    return render_template('deleteall.html') 

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('index.html')
    

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name':request.form['username'], 'password': hashpass,'repeat password': hashpass})
            session['username'] =  request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')


@app.route('/create', methods=['POST','GET'])
def create():
    mongo.db.bookmarks.insert({'Bookmark Title':request.form.get('Bookmark Title'),'Location':request.form.get('Location'),'Labels':request.form.get('Labels'),'Notes':request.form.get('Notes')})
    return 'Bookmark added Successfully!'

@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

@app.route('/Bookmarks/<Labels>')
def bookmarks():
    mongo.db.bookmarks.find_one_or_404({'Labels' : 'labels'})
    return 'Bookmarks'

    

if __name__ == '__main__':
    app.secret_key='secretivekey'
    app.run(debug =True)