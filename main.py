#-*-coding:utf-8-*-from utility import *
from tkinter import ttk,Tk,Label,Entry
import tkinter as tk
from shaonutil.mysqlDB import MySQL
import shaonutil
import os
import time

if os.path.isfile('private/config.ini'):
	print("Configurations found !")
else:
	print("Creating configurations ...")
	shaonutil.mysqlDB.create_configuration('gui')

# start mysql server
config = shaonutil.file.read_configuration_ini('private/config.ini')
if not shaonutil.process.is_process_exist('mysqld.exe'):
	process = shaonutil.process.start_mysql_server(config['MYSQL']['mysql_bin_folder'],"private/my.ini")
	#shaonutil.process.killProcess_ByAll("mysqld.exe")

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