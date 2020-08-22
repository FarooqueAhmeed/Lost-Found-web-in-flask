from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
import base64
from datetime import datetime
now = datetime.now()
current_date = now.strftime('%Y-%m-%d %H:%M:%S')


app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'sECRET###!!#%$%#'

# Enter your database connection details below
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yaKhudaKhair'
app.config['MYSQL_DB'] = 'found'
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.getcwd()+'\\Static\\images\\'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config['DEBUG'] = True
TEMPLATES_AUTO_RELOAD=True


"""For adding pdb anywhere"""
"""import pdb;
pdb.set_trace()
"""

# Intialize MySQL
mysql = MySQL(app)


foundlost_id = id



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def homeWithoutLogin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT foundlost.foundOrLost,foundlost.title ,foundlost.whenLostOrFound,foundlost.address,foundlost.otherDetails,users.first_name FROM foundlost natural join users;")
    data = cur.fetchall()

    return render_template('homeWithoutLogin.html',foundlost=data)



@app.route('/users/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form and 'father_name' in request.form and 'age' in request.form and 'mobile' in request.form and 'email' in request.form and 'user_password' in request.form and 'gender' in request.form and 'country' in request.form and 'province' in request.form and 'city' in request.form:
        # Create variables for easy access

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        father_name = request.form['father_name']
        age = request.form['age']
        mobile = request.form['mobile']
        email = request.form['email']
        user_password = request.form['user_password']
        gender = request.form['gender']
        if gender == 'male':
            gender = 1
        else:
            gender = 0
        country = request.form['country']
        province = request.form['province']
        city = request.form['city']


        '''
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('register'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('register'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open(file.filename, "rb") as file:
                return base64.b64encode(file.read()).decode('utf-8')

            print("Save file")
        '''



        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))

        users = cursor.fetchone()
        # If account exists show error and validation checks
        if users:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', email):
            msg = 'Username must contain only characters and numbers!'
        elif not email or not user_password or not email:
            msg = 'Please fill out the form!....'

        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute("INSERT INTO users (user_id,first_name,last_name,father_name,age,mobile,email,user_password,gender,country,province,city)"
                           "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (None,first_name,last_name,father_name,age,mobile,email,user_password,gender,country,province,city))
            session['user_id'] = cursor.lastrowid
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return render_template('Join.html', msg=msg)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData
'''  
@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
'''
# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/users/Join', methods=['GET', 'POST'])
def Join():
    # Output message if something goes wrong...
    msg = ''

    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'user_password' in request.form:

        # Create variables for easy access
        email = request.form['email']
        user_password = request.form['user_password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND user_password = %s', (email, user_password,))
        # Fetch one record and return result
        users = cursor.fetchone()
        # If account exists in accounts table in out database
        if users:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['user_id'] = users['user_id']
            session['first_name'] = users['first_name']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect email/password!'
    # Show the login form with message (if any)
    #return redirect(url_for('homeWithoutLogin'))
    return render_template('Join.html', msg=msg)



@app.route('/users/entry', methods=['GET', 'POST'])
def entry():
    msg = ''
    if request.method == 'POST' and 'foundOrLost' in request.form and 'title' in request.form and 'whenLostOrFound' in request.form and 'address' in request.form and 'otherDetails' in request.form:
        # Create variables for easy access
        #foundlost_id = request.form['foundlost_id']
        foundOrLost= request.form['foundOrLost']
        if foundOrLost == "found":
            foundOrLost = 1
        else:
            foundOrLost = 0
        title= request.form['title']
        whenLostOrFound = request.form['whenLostOrFound']

        address = request.form['address']

        otherDetails= request.form['otherDetails']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('INSERT INTO foundlost VALUES (%s,%s, %s, %s, %s, %s,%s)', (None,foundOrLost, title, whenLostOrFound, address, otherDetails,session['user_id']))

        mysql.connection.commit()

        return redirect(url_for('home'))

    return render_template('entry.html', msg=msg)



@app.route('/users/home', methods=['GET', 'POST'])
def home():
    # Check if user is loggedin
    #if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT foundlost.foundlost_id , foundlost.foundOrLost,foundlost.title ,foundlost.whenLostOrFound,foundlost.address,foundlost.otherDetails,users.first_name FROM foundlost natural join users;")
        data = cur.fetchall()
        # User is loggedin show them the home page
        return render_template('home.html', first_name=session['first_name'], foundlost=data)
    # User is not loggedin redirect to login page
    #return redirect(url_for('Join'))



# http://localhost:5000/python/logout - this will be the logout page
@app.route('/users/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('homeWithoutLogin'))


# http://localhost:5000/pythonlogin/register - this will be the registration page, we need to use both GET and POST requests


# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/users/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE user_id = %s ', (session['user_id'],))
        data = cursor.fetchone()
        return render_template('profile.html', data=data)


@app.route('/foundlost/search', methods=['GET', 'POST'])
def search():
    #if request.method == 'POST' in request.form and 'title' in request.form:
    title = request.form['title']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * from foundlost WHERE title = %s", [title])
    data = cursor.fetchall()
    return render_template('search.html', data=data)
       # all in the search box will return all the tuples
    #else:
    #    return redirect(url_for('entry'))



@app.route('/foundlost/ShowEntry', methods=['GET', 'POST'])
def ShowEntry():
    cur = mysql.connection.cursor()
    cur.execute("select * from foundlost where user_id = %s", (session['user_id'],))
    data = cur.fetchall()
    return render_template('ShowEntry.html',data=data)
    # User is not loggedin redirect to login page
    return redirect(url_for('home'))



@app.route('/users/update', methods=['POST', 'GET'])
def update():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    # if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form and 'father_name' in request.form and 'country' in request.form and 'province' in request.form and 'city' in request.form and 'age' in request.form and 'mobile' in request.form and 'email' in request.form and 'password' in request.form:
    # Create variables for easy access
    #user_id = request.form['user_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    father_name = request.form['father_name']
    age = request.form['age']
    mobile = request.form['mobile']
    email = request.form['email']
    user_password = request.form['user_password']
    gender = request.form['gender']
    if gender == "male":
        gender = 1
    else:
        gender = 0
    country = request.form['country']
    province = request.form['province']
    city = request.form['city']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "UPDATE users SET first_name=%s, last_name=%s,father_name=%s , age=%s , mobile=%s ,email=%s, user_password=%s ,gender=%s,country=%s ,province=%s ,city=%s WHERE user_id=%s",
        (first_name, last_name, father_name, age, mobile, email, user_password, gender, country, province, city,
         session['user_id'],))

    flash("Data Updated Successfully")
    mysql.connection.commit()
    return redirect(url_for('profile'))



@app.route('/users/delete')
def delete():
    if 'loggedin' in session:
        flash("Record Has Been Deleted Successfully")
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE user_id=%s", (session['user_id'],))
        mysql.connection.commit()
        return redirect(url_for('register'))


@app.route('/view/<foundlost_id>' , methods=['POST', 'GET'])
def view(foundlost_id):
    listOfGlobals = globals()
    listOfGlobals['foundlost_id'] = foundlost_id
    cursor = mysql.connection.cursor()



    user_id = session['user_id']
    global Aready_claimed_or_on_product
    global msg
    msg = 'You can claim it !'
    Aready_claimed_or_on_product = True
    cursor.execute('SELECT * FROM claims WHERE user_id = %s AND foundlost_id = %s',(user_id,foundlost_id))
    check = cursor.fetchone()

    user_id = session['user_id']
    cursor.execute('SELECT * FROM foundlost WHERE foundlost_id = %s AND user_id = %s', (foundlost_id, user_id))
    check_entry = cursor.fetchone()

    if check != None :
       Aready_claimed_or_on_product = False
       msg = 'already claimed'
    elif check_entry != None:
         Aready_claimed_or_on_product = False
         msg = 'This is your entry'


    cursor.execute(f'SELECT * FROM foundlost WHERE foundlost_id = {foundlost_id}')
    data = cursor.fetchone()
    cursor.execute("select comments.comment_value, users.first_name FROM comments natural join users WHERE foundlost_id = %s",[foundlost_id])
    comments_data = cursor.fetchall()
    return  render_template ('view.html',data=data,comments_data=comments_data,msg=msg,Aready_claimed_or_on_product=Aready_claimed_or_on_product)

@app.route('/View_Update_Entry/<foundlost_id>' , methods=['get'])
def View_Update_Entry(foundlost_id):
    cursor = mysql.connection.cursor()
    cursor.execute(f'SELECT * FROM foundlost WHERE foundlost_id = {foundlost_id}')
    data = cursor.fetchone()
    return redirect(url_for('ShowEntry'))





@app.route('/users/update_Entry', methods=['POST', 'GET'])
def update_Entry():
    foundOrLost = request.form['foundOrLost']
    if foundOrLost == "found":
        foundOrLost = 1
    else:
        foundOrLost = 0
    title = request.form['title']
    whenLostOrFound = request.form['whenLostOrFound']

    address = request.form['address']

    otherDetails = request.form['otherDetails']
    # Check if account exists using MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("UPDATE foundlost SET foundOrLost=%s, title=%s,whenLostOrFound=%s , address=%s , otherDetails=%s WHERE foundlost_id=%s",(foundOrLost, title, whenLostOrFound, address, otherDetails))

    flash("Data Updated Successfully")
    mysql.connection.commit()
    return redirect(url_for('ShowEntry'))





@app.route('/comments/comment', methods=['GET', 'POST'])
def comment():
    if request.method == 'POST' and 'comment_value' in request.form:
        comment_value = request.form['comment_value']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO comments VALUES (%s,%s,%s,%s,%s)', (None,comment_value,current_date,foundlost_id,session['user_id']))
        mysql.connection.commit()
        return redirect(url_for('view',foundlost_id=foundlost_id))
    else:
        return render_template('view.html')



@app.route('/claims/claim', methods=['GET', 'POST'])
def claim():
    cursor = mysql.connection.cursor()

    cursor.execute('SELECT * FROM claims WHERE foundlost_id = %s', [foundlost_id])
    check = cursor.fetchone()
    if check != None:
        msg='already claimed'
    elif check==None:


        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO claims (user_id,foundlost_id) select user_id,foundlost_id from foundlost WHERE foundlost_id = %s',[foundlost_id])
        mysql.connection.commit()
        return render_template('home.html')
    else:
        return render_template('profile.html')


# cursor.execute('SELECT * FROM users WHERE email = %s AND user_password = %s', (email, user_password,))
# Insert into table2 (field1, field2)  select field1, field2 from table1 where field1=condition

#Insert into table2 (field1, field2)  select field1, field2 from table1 where field1=condition


if __name__ == "__main__":
    app.run(debug=True)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')



''''

databse name : Found
###################333
create user table 
####################

create table users(
    user_id int auto_increment primary key not null,
    first_name varchar(100) not null, 
    last_name varchar(100) not null, 
    father_name varchar(100) not null, 
    age int not null, 
    mobile varchar(100) not null, 
    email varchar(100) not null,
    user_password varchar(100) not null,
    gender boolean not null,
	country varchar(100) not null, 
    province varchar(100) not null, 
    city varchar(100) not null
    )engine=InnoDB;

create table foundlost(
    foundlost_id int auto_increment primary key,
    foundOrLost boolean not null,
    title varchar(100) not null, 
    whenLostOrFound date not null, 
    address varchar(100) not null, 
    otherDetails varchar(100) not null,
    user_id int not null
)engine=InnoDB;

create table claims(
    claim_id int auto_increment primary key,
    user_id int not null,
    foundlost_id int not null
)engine=InnoDB;   


create table comments(
    comment_id int auto_increment primary key,
    comment_value varchar(100) not null,
    comment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    foundlost_id int not null,
    user_id int not null
)engine=InnoDB;

'''
