#-*-coding:utf-8-*-
import mysql.connector as mysql
import shaonutil
import os
from utility import *
from shaonutil.mysqlDB import MySQL
"""
go to mysql folder > aria_chk -r
delete araia_log.### files in mysql data folder
change the port=3306 to anything else in line 20,28 in my.ini in mysql data folder
if anything didn't recover then, go to mysqsl/backup, copy everything and go to mysql/data folder , delete everything and past here.
"""



if os.path.isfile('private/config.ini'):
	print("Configurations found !")
else:
	print("Creating configurations ...")
	create_configuration('gui')

# start mysql server
config = shaonutil.file.read_configuration_ini('private/config.ini')
process = shaonutil.process.start_mysql_server(config['MYSQL']['mysql_bin_folder'],"private/my.ini")
print(process.pid)	


time.sleep(1)

myNowMYSQL = MySQL(config._sections['DB_INITIALIZE'])

if not myNowMYSQL.is_mysql_user_exist(config['DB_AUTHENTICATION']['user']):
	myNowMYSQL.createMySQLUser(config['DB_AUTHENTICATION']['host'], config['DB_AUTHENTICATION']['user'], config['DB_AUTHENTICATION']['password'])
	myNowMYSQL.grantMySQLUserAllPrivileges(config['DB_AUTHENTICATION']['host'], config['DB_AUTHENTICATION']['user'])
	myNowMYSQL.listMySQLUsers()

if not myNowMYSQL.is_db_exist(config['DB_AUTHENTICATION']['database']):
	myNowMYSQL.create_db(config['DB_AUTHENTICATION']['database'])


_ = shaonutil.file.read_configuration_ini('private/db_structure.ini')
column_info = eval(_['DB']['column_info'])


myNowMYSQL.config = config._sections['DB_AUTHENTICATION']

if not myNowMYSQL.is_table_exist(config['DB_AUTHENTICATION']['table']):
	myNowMYSQL.create_table(config['DB_AUTHENTICATION']['table'],column_info)


myNowMYSQL.close_connection()


def insertion_form():
	window = Tk()
	window.title("BookRack v1.0")
	window.geometry('400x400')
	window.configure(background = "grey");



	# Label fb_authentication
	FB_LABEL = Label(window ,text = "Book Details").grid(row = 0,column = 0,columnspan=2)
	a = Label(window ,text = "Name").grid(row = 1,column = 0)
	c = Label(window ,text = "Writer").grid(row = 2,column = 0)
	d = Label(window ,text = "Publisher").grid(row = 3,column = 0)

	name_ = tk.StringVar(window)
	writer_ = tk.StringVar(window)
	publisher_ = tk.StringVar(window)

	Entry(window,textvariable=name_).grid(row = 1,column = 1)
	Entry(window,textvariable=writer_).grid(row = 2,column = 1)
	Entry(window,textvariable=publisher_).grid(row = 3,column = 1)
	

	def clicked():
		myNowMYSQL.reopen_connection()
		sid = myNowMYSQL.get_unique_id_from_field(8,'book_sid')
		name = name_.get().encode('utf-8')
		writer = writer_.get().encode('utf-8')
		publisher = publisher_.get().encode('utf-8')
		myNowMYSQL.insert_data((sid,name,writer,publisher))
		
		# entry to database
		window.destroy()



	btn = ttk.Button(window ,text="Submit",command=clicked).grid(row=9,column=0)
	window.mainloop()

insertion_form()

#Name+Writer+Publisher> convert to barcode/qrcode
#Barcode/QRCode > Name+Writer+Publisher