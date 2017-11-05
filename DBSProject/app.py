from flask import Flask,render_template,session,request,jsonify,json,redirect,url_for
from hashlib import md5
import MySQLdb

cus_info = "Hello"
emp_info = ""
addr_info = ""
app = Flask(__name__)
app.secret_key = "aw456787uioSHUI4w5eQuighepuihqetoghRUIGHQEOh"

db = MySQLdb.connect("localhost","root","password","hsh2" )


@app.route("/register")
def register():
	return render_template('register.html')

@app.route("/reg",methods=['GET','POST'])
def reg():
	if not session.get('cusid'):	
		fname = request.form["f_name"]
		mname = request.form["m_name"]
		lname = request.form["l_name"]
		mail = request.form["email_id"]
		cont = int(request.form["contact"])
		building = request.form["building"]
		street = request.form["street"]
		city = request.form["city"]
		state = request.form["state"]
		password = request.form["password"]
		cur = db.cursor()
		cur.execute("INSERT INTO Name(first_name,middle_name,last_name) VALUES (%s,%s,%s)",(fname,mname,lname))
		db.commit()
		nameid = cur.lastrowid
		cur.execute("INSERT INTO Address(building_name,street_name,city,state) VALUES (%s,%s,%s,%s)",(building,street,city,state))
		db.commit()
		addrid = cur.lastrowid
		# cur.execute("SELECT name_id FROM Name where first_name = %s and middle_name = %s and last_name = %s",(fname,mname,lname))
		# nameid=int(cur.fetchone()[0])
		# cur.execute("SELECT addr_id FROM Address where building_name = %s and street_name = %s and city = %s and state = %s",(building,street,city,state))
		# addrid=int(cur.fetchone()[0])
		cur.execute("INSERT INTO Customer(password,cus_name_id,cus_email_id,addr_id) VALUES (%s,%s,%s,%s)",(password,nameid,mail,addrid))
		cusid = cur.lastrowid


		# cur.execute("SELECT cus_id FROM Customer where cus_name_id = %s and addr_id = %s",(nameid,addrid))
		# cusid=int(cur.fetchone()[0])
		cur.execute("INSERT INTO Customer_contact VALUES (%s,%s)",(cusid,cont))
		print cusid
		return render_template('login.html',cusid = session['cusid'])
	else:
		return redirect("/index")

@app.route("/")
@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/login_test", methods=['POST'])
def login_test():
	userkey = request.form["username"]
	passkey = request.form["password"]
	try:
		error = None
		cur = db.cursor()
		print 1
		cur.execute("SELECT * FROM Customer WHERE cus_id = %s" %userkey);
		print 3
		if cur.fetchone():
			print 4
			cur.execute("SELECT password FROM Customer where cus_id = %s",[userkey]);
			for row in cur.fetchall():	
				print 2
				if passkey == row[0]:
					session['cusid'] = userkey
					print "loggedin" 
					print session['cusid']
					return render_template("index.html")
				else:
					error = "Wrong Password"
					print error
					return render_template('login.html', error=error)
		else:
			error = "User Not Registered"
			print "error"
			return render_template('login.html', error=error)
	except Exception as e:
		print e
		return render_template("login.html",error=e)

@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/home")
def home():
	return render_template("index.html",cusid=session['cusid'])

@app.route("/appliance")
def appliance():
	if session.get("cusid"):
		return render_template("appliances.html",cusid=session['cusid'])
	else:
		return redirect("/login")

@app.route("/added", methods=['POST'])
def added():
	try:
		aname = request.form["a_name"]
		wdate = request.form["w_date"]
		wduration = int(request.form["w_duration"])
		currentstate = request.form["cur_state"]
		try:
			cur = db.cursor()
			try:
				print session.get('cusid')
				cur.execute("INSERT INTO Appliance(cus_id,appliance_name,warranty_start_date, warranty_duration, current_state) VALUES (%s,%s,%s,%s,%s)",(session.get("cusid"),aname, wdate,wduration,currentstate))
				db.commit()
				return render_template('appliances.html')
			except Exception as e:
				return render_template('addappliance.html', error = "Query could not be run.")
		except Exception as e:
			print e
			return "Could not connect to database"
	except Exception as e:
		return "Form values not submitted properly."

@app.route("/add_app")
def add_app():
	return render_template("addappliance.html",cusid=session['cusid'])

@app.route("/del_app")
def del_app():
	try:
		cur = db.cursor()
		cur.execute("SELECT appliance_id, appliance_name, current_state FROM Appliance WHERE cus_id = %s" % session.get("cusid"))
		appl_li = cur.fetchall()
		print appl_li
		print type(appl_li)
		return render_template("delappliance.html",cusid=session['cusid'],del_app_li = appl_li)
	except Exception as e:
		print e
		return render_template('appliances.html', error = e)
	


@app.route("/ctrl_app")
def ctrl_app():
	try:
		cur = db.cursor()
		cur.execute("SELECT appliance_id, appliance_name, current_state FROM Appliance WHERE cus_id = %s" % session.get("cusid"))
		appl_li = cur.fetchall()
		print appl_li
		print type(appl_li)
		return render_template("ctrlappliance.html",cusid=session['cusid'],del_app_li = appl_li)
	except Exception as e:
		print e
		return render_template('appliances.html', error = e)

@app.route("/rep_app")
def rep_app():
	return render_template("repappliance.html")

@app.route("/logout")
def logout():
	session.pop("cusid",None)
	return redirect("/")

# @app.route("/elec")
# def elec():
# 	return render_template("electricity.html")

# @app.route("/perinfo")
# def perinfo():
# 	return render_template("personalinfo.html")

@app.route("/comp")
def comp():
	return render_template("complaint.html")

@app.route("/about")
def about():
	return render_template("aboutus.html")

@app.route("/contact")
def contact():
	return render_template("contactus.html")


if __name__ == '__main__':
	app.run(debug=True)