import mysql.connector as mysql
from tkinter import ttk,Tk,Label,Entry
import tkinter as tk
import shaonutil
import time

import os
import subprocess


def create_configuration(option='cli'):
	if option == 'cli':
		print('Getting your configurations to save it.\n')
		print('\nDatabase configurations -')
		dbhost = input('Give your db host : ')
		dbuser = input('Give your db user : ')
		dbpassword = input('Give your db password : ')
		dbname = input('Give your db name : ')
		dbtable = input('Give your db table : ')

		mysql_bin_folder = input('Give your path of mysql bin folder : ')

		f = open("private/config.ini", "w+")
		f.writelines(["; config file\n", "[db_authentication]\n", "host = "+dbhost+"\n", "user = "+dbuser+"\n", "password = "+dbpassword+"\n", "database = "+dbname+"\n", "table = "+dbtable+"\n","[MYSQL]\n","mysql_bin_folder = "+mysql_bin_folder+"\n","[DB_INITIALIZE]\n","host = localhost\n","usr = root\n","passwd = \n"])
		f.close()
	elif option == 'gui':
		window = Tk()
		window.title("Welcome to DB Config")
		window.geometry('400x400')
		window.configure(background = "grey");

		# Label fb_authentication
		FB_LABEL = Label(window ,text = "MYSQL Config").grid(row = 0,column = 0,columnspan=2)
		a = Label(window ,text = "MYSQL bin folder").grid(row = 1,column = 0)
		
		DB_LABEL = Label(window ,text = "Database Authentication").grid(row = 3,column = 0,columnspan=2)
		c = Label(window ,text = "Host").grid(row = 4,column = 0)
		d = Label(window ,text = "User").grid(row = 5,column = 0)
		d = Label(window ,text = "Password").grid(row = 6,column = 0)
		d = Label(window ,text = "Database").grid(row = 7,column = 0)
		d = Label(window ,text = "Table").grid(row = 8,column = 0)

		mysqlbinfolder_ = tk.StringVar(window)
		fbpassword_ = tk.StringVar(window)
		dbhost_ = tk.StringVar(window)
		dbuser_ = tk.StringVar(window)
		dbpassword_ = tk.StringVar(window)
		dbname_ = tk.StringVar(window)
		dbtable_ = tk.StringVar(window)

		Entry(window,textvariable=mysqlbinfolder_).grid(row = 1,column = 1)
		
		Entry(window,textvariable=dbhost_).grid(row = 4,column = 1)
		Entry(window,textvariable=dbuser_).grid(row = 5,column = 1)
		Entry(window,show="*",textvariable=dbpassword_).grid(row = 6,column = 1)
		Entry(window,textvariable=dbname_).grid(row = 7,column = 1)
		Entry(window,textvariable=dbtable_).grid(row = 8,column = 1)

		def clicked():
			mysql_bin_folder = mysqlbinfolder_.get()
			
			dbhost = dbhost_.get()
			dbuser = dbuser_.get()
			dbpassword = dbpassword_.get()
			dbname = dbname_.get()
			dbtable = dbtable_.get()

			f = open("private/config.ini", "w+")
			f.writelines(["; config file\n", "[db_authentication]\n", "host = "+dbhost+"\n", "user = "+dbuser+"\n", "password = "+dbpassword+"\n", "database = "+dbname+"\n", "table = "+dbtable+"\n","[MYSQL]\n","mysql_bin_folder = "+mysql_bin_folder+"\n","[DB_INITIALIZE]\n","host = localhost\n","usr = root\n","passwd = \n"])
			f.close()
			window.destroy()



		btn = ttk.Button(window ,text="Submit",command=clicked).grid(row=9,column=0)
		window.mainloop()



