from flask import Flask, redirect, url_for,render_template,request,flash, session
import MySQLdb

app = Flask(__name__)
app.secret_key = '!@#$' # secret key

# connector for database
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythondb'

# access mysql
mysql = MySQLdb.connect (
   host = app.config['MYSQL_HOST'],
   user = app.config['MYSQL_USER'],
   password = app.config['MYSQL_PASSWORD'],
   db = app.config['MYSQL_DB']
)

# fetch all data
def getprocess(data)->str:
	cursor = mysql.cursor()
	cursor.execute(data)
	data = cursor.fetchall()
	cursor.close()
	return data

# changes to databases
def doprocess(data)->str:
	cursor = mysql.cursor()
	cursor.execute(data)
	mysql.commit()
	cursor.close()

# for user login validation
def userLogin(table:str, **kwargs)->list:
	keys = list(kwargs.keys())
	vals = list(kwargs.values())
	query = f"SELECT * FROM `{table}` WHERE `{keys[0]}` = '{vals[0]}' and `{keys[1]}` = '{vals[1]}'"
	return getprocess(query)

# main route   
@app.route('/')
def main():
   return render_template('index.html', title='Home Page')

# login route
@app.route('/login', methods=['POST', 'GET'])
def login():
   if request.method == 'POST':
      usern:str = request.form['username']
      passw:str = request.form['password']

      user = userLogin('account', username=usern,password=passw)

      if len(user) > 0:
         query = f"select firstname from account where username = '{usern}'"
         cursor = mysql.cursor()
         cursor.execute(query)
         data = cursor.fetchall()
         cursor.close()
         session['name'] = data[0][0]
         session['username'] = usern
         return redirect(url_for('dashboard'))
      else:
         flash('Invalid User')
         return redirect(url_for('login'))
      
   else:
      return render_template('login.html', title='Login')

# logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged Out')
    return redirect(url_for('login'))

# dashboard route
@app.route('/dashboard')
def dashboard()->None:
   if 'username' in session:
      name = session['name']
      query = "SELECT * FROM student"
      cursor = mysql.cursor()
      cursor.execute(query)
      data = cursor.fetchall()
      data_desc = cursor.description
      if len(data) > 0:
               return render_template('dashboard.html',data_desc=data_desc, data=data, title='Dashboard', name=name)
      else:
         flash("No Data Available")
         return render_template('dashboard.html')
   
   else:
      flash('Login Properly')
      return redirect(url_for('login'))

# insert route
@app.route('/insert',methods=['POST', 'GET'])
def insert():
   if request.method == 'POST':
      mydict = dict(
        idno = request.form['idno'],
        lastname = request.form['lname'],
        firstname = request.form['fname'],
        course = request.form['course'],
        level = request.form['level']
      )
      keys = mydict.keys()
      vals = mydict.values()
      flds = "`,`".join(keys)
      base:str = "','".join(vals)
      query = f"INSERT INTO student(`{flds}`)VALUES ('{base}')"
      doprocess(query)
      flash("New Record Added")
      return redirect(url_for('dashboard'))
   
   else:
      return render_template('dashboard.html')

 # update route  
@app.route('/update',methods=['POST', 'GET'])
def update():
   if request.method == 'POST':
      idno = request.form['idno']
      mydict = dict(
        lastname = request.form['lname'],
        firstname = request.form['fname'],
        course = request.form['course'],
        level = request.form['level']
      )

      keys = "`,`".join(mydict.keys())
      vals = "','".join(mydict.values())
      flds = keys.split("`,`")
      base = vals.split("','")
      params = []
      for i in range(0,len(flds)):
         params.append(f"`{flds[i]}`='{base[i]}'")
      joint = ",".join(params)
      query = f"UPDATE student SET{joint} WHERE idno = '{idno}'"
      doprocess(query)
      flash("Record Updated")
      return redirect(url_for('dashboard'))
   
   else:
      return render_template('dashboard.html')

# Delete route
@app.route('/delete/<string:idno>')
def delete(idno):
   query = f"DELETE FROM student WHERE idno = '{idno}'"
   doprocess(query)
   flash('Record Deleted')
   return redirect(url_for('dashboard'))


# calling main function
if __name__ == '__main__':
   app.run(debug = True)