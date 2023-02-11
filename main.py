from flask import Flask, render_template, request,url_for,session,redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re



app = Flask(__name__)

app.secret_key = 'Thismydatabase'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '02749'
app.config['MYSQL_DB'] = 'fitness'

#Intialize mysql
mysql = MySQL(app)





@app.route('/' , methods = ['GET', 'POST'])
def login():
    msg = ''
    # check if username and password POST {request  exit user submit from}
    if request.method == "POST" and "username" in request.form  and 'password' in request.form:
        #Create variable for easy acess
        username = request.form['username']
        password = request.form['password']

        #check if accoutnt exists using in mysql 
        # MySQLdb.cursors.DictCursor เราจะใช้ก็ต่อเมื่อค่าของ input ที่รับเข้ามานั้นมี type ที่แตกต่างกัน 
        cursor  = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM fitness.member WHERE user = %s and password = %s" ,(username,password))
        account = cursor.fetchone()



        #if account exists in accounts table in out database 
        if account:
        # Create session data , for acess this  data in other route
            session['loggedin'] = True
            session['id'] = account['id']
            #we will compare  user in mysql and session input form html 
            session['username'] = account['user']

            # Redirect to homepage

            return 'Logged in successfully!!'


        else: 
            # if account is not exit 
            msg = 'Incorrect Username/Password'

    return render_template('index.html', msg = msg)




@app.route('/logout')
def logout():

    #Remove session data , this will log the userout
    session.pop('loggedin' , None)
    session.pop('id',None)
    session.pop('username' , None)

    # ทำการ redirect หน้าออกไป
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email  = request.form['email']
        #ทำการเช็คข้อมูลว่า มีปัญาตนงไหนเช่นการซ้ำ username password email
        if not username or not password or not email:
            msg = 'Please fill out all the fields!'

        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'

        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM fitness.member_test WHERE user = %s", (username,))
            account = cursor.fetchone()

            if account:
                msg = 'An account with this username already exists!'
            else:
                cursor.execute('INSERT INTO fitness.member_test VALUES (NULL, %s, %s, %s)', (username, password, email))
                mysql.connection.commit()
                msg = 'Account created successfully!'

    return render_template('register.html', msg=msg)

    





if __name__ == "__main__":
    app.run(debug= True)