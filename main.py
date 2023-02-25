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
        cursor.execute("SELECT * FROM  fitness.members  WHERE username = %s and password = %s" ,(username,password))
        account = cursor.fetchone()



        #if account exists in accounts table in out database 
        if account:
        # Create session data , for acess this  data in other route
            session['loggedin'] = True
            session['id'] = account['id']
            #we will compare  user in mysql and session input form html 
            session['username'] = account['username']

            # Redirect to homepage

            return redirect(url_for("home"))


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
            cursor.execute("SELECT * FROM fitness.members  WHERE username = %s", (username,))
            account = cursor.fetchone()

            if account:
                msg = 'An account with this username already exists!'
            else:
                cursor.execute('INSERT INTO fitness.members  VALUES (NULL, %s, %s, %s)', (username, password, email))
                mysql.connection.commit()
                msg = 'Account created successfully!'

    return render_template('register.html', msg=msg)

    

#Home page 
@app.route('/home')
def home():
    #chekc if user is loggedin 
    if 'loggedin' in session :
        # user is loggedin show them the home 
        return render_template('home.html', username = session['username'])
    # User is not login   redirect to login page
    return redirect(url_for("login"))



#Product buy 
@app.route('/buy',methods = [ "GET" , "POST"])
def buy():
    #ใช้ในขณะเราอยู่ที่หน้า buy สินค้า ทำการ login หรือไม่ก็ตาม
    
    if 'loggedin' in session:
        if request.method == "POST": 
            #Get item id from the form submission
            item_id = request.form['item_id']
    

            #Qurey the database to get the item information
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM fitness.products where id = %s " ,(item_id,))
            #ทำการ fetchone กรองข้อมุลออกมาแบบเลือกเป็นตัวๆ 
            item = cursor.fetchone()


            #Add the item to user order history 
            #ต้องทำการสร้างตารางเข้ามาเพิ่มเพื่อเก็บข้อมูลของ user
            #ภายใน Column ต้องมี user_id   item_id และข้อมูลที่ทำการร้องของของ session['id'], item['id']
            cursor.execute("INSEART INTO fitness.purcheses  (user_id , item_id) VALUES (%s , %s ) ",session['id'], item['id'] )
            mysql.connection.commit()

            return render_template('buy.html' , message = "Thank you for your purchase" )

        else : 
            #Query the database to get all the avaliable product 
            #ถ้าเกิดข้อมูลมีการจองไว้อยู่แล้ว

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM  fitness.products")
            items = cursor.fetchall()


            return render_template('buy.html' , items = items )


    else:
        # Redirect page user to the login page if they are not loggedin 
        return redirect(url_for('login'))






# @app.route('/buy' , methods = ["GET" , "POST"])
# def buy_product():

#     if 'loggedin' in session : 
#     #Get ID from the request from Data

#         item_id  = request.form.get("item_id")

#         #Get the current user' ID from the session 
#         user_id = session["id"]

#        #check Item id for purches on Database
#        # ยังไม่จำเป็นที่ต้องใช้
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute("SELECT * FROM fitness.product WHERE id = %s ",(item_id , ))
#         items = cursor.fetchone()

#         #Inseart Data into database 
#         cursor.execute("INSEART  INTO purchases  (user_id , item_id ) VALUES (%s , %s )", (user_id , item_id))
#         mysql.connection.commit()


#         return render_template('buy.html')
         




if __name__ == "__main__":
    app.run(debug= True)
