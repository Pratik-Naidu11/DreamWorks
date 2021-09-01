from tkinter import *
from tkinter.messagebox import *
import requests
import bs4
from sqlite3 import *
import matplotlib.pyplot as plt 
from tkinter.scrolledtext import *
  
try:
	wal = "https://ipinfo.io"
	resl = requests.get(wal)
	data = resl.json()
	#print(data)
	location = data['city']		#-->value for location label

	city_name = location
	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + city_name
	a3 = "&appid=" + "c6e315d09197cec231495138183954bd"

	waT = a1+a2+a3
	resT = requests.get(waT)
	dataT = resT.json()
	main = dataT['main']
	temperature = main['temp'] 	#-->Value for temp label
	temperature = str(temperature)


	waq = "https://www.brainyquote.com/quote_of_the_day"
	resq = requests.get(waq)
	
	dataq = bs4.BeautifulSoup(resq.text ,'html.parser')
	
	info = dataq.find('img',{'class':'p-qotd'})
	qotd = info['alt']	#-->Value for qotd

	#print(location)
	#print(temperature)
	#print(msg)
	
except Exception as e:
	print("Issue",e)



#******************************************Main Window**********************************
mainwindow = Tk()
mainwindow.title("StudentManagementSytem")
mainwindow.geometry("700x700+500+10")

def validate(r,n,m):
	rno = r
	name = n
	marks = m
	verified_rno , verified_name,verified_marks = None,None,None
	if rno =="":
		showwarning("Warning","Roll no. can't be blank.")
		ent_rno.focus()
		return(None,None,None)
	else:
		if not rno.isdigit():
			showwarning("Warning","Roll has to be numeric.")
			ent_rno.focus()
			return(None,None,None)
		elif int(rno) <1:
			showwarning("Warning","Roll has to greater than 0.")
			ent_rno.focus()	
			return(None,None,None)
		elif (not(name.isalpha())) or (len(name) < 2):
			showwarning("Warning","Invalid Name")
			ent_name.focus()
			return(None,None,None)
		elif marks =="":
			showwarning("Warning","Marks can't be blank.")
			ent_marks.focus()
			return(None,None,None)
		elif not marks.isdigit():
			showwarning("Warning","Marks has to be numeric.")
			ent_marks.focus()
			return(None,None,None)	
		elif int(marks) not in range(0,101):
			showwarning("Warning","Marks must be in range 0-100 only.")
			ent_marks.focus()
			return(None,None,None)
		else:
			verified_name = name.title()
			verified_marks = int(marks)
			verified_rno = int(rno)
			print(verified_name)
			return (verified_rno,verified_name, verified_marks)
	

def display(n):
	pg =n
	if pg ==1:
		add_window.deiconify()
		mainwindow.withdraw()
	elif pg==2:
		view_window.deiconify()
		mainwindow.withdraw()
		showRecords()
	elif pg==3:
		upd_window.deiconify()
		mainwindow.withdraw()
	elif pg==4:
		del_window.deiconify()
		mainwindow.withdraw()
	elif pg==5:
		create_graph()


	
def back(n):
	op = n
	if op ==1:
		mainwindow.deiconify()
		add_window.withdraw()
	elif op==2:
		mainwindow.deiconify()
		upd_window.withdraw()
	elif op==3:
		mainwindow.deiconify()
		del_window.withdraw()
	elif op==4:
		mainwindow.deiconify()
		view_window.withdraw()
		

f=('Calibri',20,'bold')
#**********************buttons***********************
btn_add = Button(mainwindow,text="ADD",font=f,width=10,command=lambda:display(1))
btn_add.pack(pady=10)
btn_view = Button(mainwindow,text="View",font=f,width=10,command=lambda:display(2))
btn_view.pack(pady=10)
btn_update = Button(mainwindow,text="Update",font=f,width=10,command=lambda:display(3))
btn_update.pack(pady=10)
btn_delete = Button(mainwindow,text="Delete",font=f,width=10,command=lambda:display(4))
btn_delete.pack(pady=10)
btn_charts = Button(mainwindow,text="Charts",font=f,width=10,command=lambda:display(5))
btn_charts.pack(pady=10)

#**********************Labels***********************
f1=('Calibri',20,'bold')
lbl_loc = Label(mainwindow,text="Location: " + location,font = f1,width=20)
lbl_loc.place(x=10,y=450)


lbl_temp = Label(mainwindow,text="Temperature: "+ temperature+"\u2103",font = f1,width=20)
lbl_temp.place(x=400,y=450)


lbl_qotd = Label(mainwindow,text="QOTD: "+ qotd,font =('Calibri',15))
lbl_qotd.place(x=50,y=500)


#*************************ADD Window***************************
def submit():

	rno = ent_rno.get()
	name = ent_name.get()
	marks = ent_marks.get()
	vf_rno,vf_name,vf_marks = validate(rno,name,marks)
	if vf_rno == None:
		pass
	else:
		con = None	
		try:
			con = connect('studentdata.db')
			cur = con.cursor()
			sql = "insert into students values('%d','%s','%d')"
			cur.execute(sql %(vf_rno,vf_name,vf_marks))
			showinfo("Info","Record added successfully")
			con.commit()
			sql = 'select * from students'
			cur.execute(sql)
			ent_rno.delete(0,END)
			ent_name.delete(0,END)
			ent_marks.delete(0,END)
			data = cur.fetchall()
			print(data)
		except Exception as e:
			print(e)
			con.rollback()
			showerror("Error",e)
		finally:
			if con is not None:
				con.close()
				print("Closed")
					
			

	

add_window = Toplevel(mainwindow)
add_window.title("Add Student")
add_window.geometry("500x700+500+10")


lbl_rno = Label(add_window,text="Enter Roll No.: ",font=f)
lbl_rno.pack(pady=10)
lbl_rno.focus()

ent_rno = Entry(add_window, bd=4, font=f,width=30,highlightthickness=2)
ent_rno.pack()

lbl_name = Label(add_window,text="Enter Name: ",font=f)
lbl_name.pack(pady=10)

ent_name = Entry(add_window, bd=4, font=f,width=30,highlightthickness=2)
ent_name.pack()


lbl_marks = Label(add_window,text="Enter Marks: ",font=f)
lbl_marks.pack(pady=10)

ent_marks = Entry(add_window, bd=4, font=f,width=30,highlightthickness=2)
ent_marks.pack()

btn_save = Button(add_window,text="Save",font=f,width=20,command=submit)
btn_save.pack(pady = 20)

btn_back = Button(add_window,text="Back",font=f,width=20,command=lambda:back(1))
btn_back.pack(pady = 20)

#******************************Update Window*********************************
upd_window = Toplevel(mainwindow)
upd_window.title("Update Student")
upd_window.geometry("500x700+500+10")

def update():

	rno = ent_urno.get()
	name = ent_uname.get()
	marks = ent_umarks.get()
	db_rno=[]
	vf_rno,vf_name,vf_marks = validate(rno,name,marks)
	
	con = None	
	try:
		con = connect('studentdata.db')
		cur = con.cursor()
		get_rno = "select rno from students"
		cur.execute(get_rno)
		data = cur.fetchall()
		for d in data:
			db_rno.append(d[0])
		if vf_rno in db_rno:
			sql = "update students set name='%s' , marks='%d' where rno='%d'"
			cur.execute(sql %(vf_name,vf_marks,vf_rno))
			showinfo("Info","Record updated successfully")
		else:
			showwarning("Warning","Record does not exist")	
			ent_uname.delete(0,END)	
			ent_umarks.delete(0,END)	
		con.commit()
		sql = 'select * from students'
		cur.execute(sql)
		data = cur.fetchall()
		print(data)
	except Exception as e:
		print(e)
		con.rollback()
		showerror("Error",e)
	finally:
		if con is not None:
			con.close()
			print("Closed")


lbl_urno = Label(upd_window,text="Enter Roll No.: ",font=f)
lbl_urno.pack(pady=10)
lbl_urno.focus()

ent_urno = Entry(upd_window, bd=4, font=f,width=30,highlightthickness=2)
ent_urno.pack()

lbl_uname = Label(upd_window,text="Enter Name: ",font=f)
lbl_uname.pack(pady=10)

ent_uname = Entry(upd_window, bd=4, font=f,width=30,highlightthickness=2)
ent_uname.pack()


lbl_umarks = Label(upd_window,text="Enter Marks: ",font=f)
lbl_umarks.pack(pady=10)

ent_umarks = Entry(upd_window, bd=4, font=f,width=30,highlightthickness=2)
ent_umarks.pack()

btn_upd = Button(upd_window,text="Update",font=f,width=20,command=update)
btn_upd.pack(pady = 20)

btn_back = Button(upd_window,text="Back",font=f,width=20,command=lambda:back(2))
btn_back.pack(pady = 20)

#*******************************************Delete Window***************************************
del_window = Toplevel(mainwindow)
del_window.title("Delete Student")
del_window.geometry("500x700+400+100")

def delete_record():
	rno = ent_drno.get()
	vf_rno = None
	db_rno=[]
	if rno =="":
		showwarning("Warning","Roll no. can't be blank.")
		ent_drno.focus()
		vf_rno = None
	else:
		if not rno.isdigit():
			showwarning("Warning","Roll has to be numeric.")
			ent_drno.focus()
			vf_rno = None
		elif int(rno) <1:
			showwarning("Warning","Roll has to greater than 0.")
			ent_drno.focus()		
			vf_rno = None
		else:
			rno = int(rno)
			vf_rno = rno
	if vf_rno == None:
		pass
	else:
		con = connect('studentdata.db')
		cur = con.cursor()
		get_rno = "select rno from students"
		cur.execute(get_rno)
		data = cur.fetchall()
		for d in data:
			db_rno.append(d[0])
		#print(db_rno)
		if vf_rno in db_rno:
			sql = "delete from students where rno='%d'"
			cur.execute(sql %(vf_rno))
			showinfo("Info","Record Deleted successfully")
			ent_drno.delete(0,END)
		else:
			showwarning("Warning","Record does not exist")		
		con.commit()
		

lbl_drno = Label(del_window,text="Enter Roll No.: ",font=f)
lbl_drno.pack(pady=10)
lbl_drno.focus()

ent_drno = Entry(del_window, bd=4, font=f,width=30,highlightthickness=2)
ent_drno.pack()

btn_del = Button(del_window,text="Delete",font=f,width=20,command=delete_record)
btn_del.pack(pady = 20)

btn_back = Button(del_window,text="Back",font=f,width=20,command=lambda:back(3))
btn_back.pack(pady = 20)

#*************************************Graph Window************************************************
def create_graph():	
	rno_lst = []
	marks_lst = []
	strt =[]
	con = None	
	try:
		con = connect('studentdata.db')
		cur = con.cursor()
		sql = 'select * from students order by rno'
		cur.execute(sql)
		data = cur.fetchall()
		print(data)
		for d in data:
			rno_lst.append(d[0])
			marks_lst.append(int(d[2]))
		#print(len(students_lst))
		#print(len(marks_lst))
		#rno_lst.sort()
	except Exception as e:
		showerror("Error",e)
	finally:
		if con is not None:
			con.close()
			print("Closed")
 
	for count in range(1,len(rno_lst)+1):
		strt.append(count)
	height = marks_lst
 
	tick_label = rno_lst
  
	plt.bar(strt, height, tick_label = tick_label, 
	        width = 0.8, color = ['purple', 'orange'])   

	plt.xlabel('Roll Number') 

	plt.ylabel('Marks') 

	plt.title('Student Perfomance') 
  
	plt.show() 
#************************************View Window*********************************
view_window = Toplevel(mainwindow)
view_window.title('View Student Records')
view_window.geometry("700x700+200+10")

def showRecords():
	text_area.delete(1.0,END)
	st_records=""	
	header ="\t"+ "Rno."+"\t"+"Name"+"\t\t"+"Marks"+"\n\n"
	con = None
	try:
		con = connect('studentdata.db')
		cur = con.cursor()
		sql = "select * from students order by rno"
		cur.execute(sql)
		data = cur.fetchall()
		print(data)
		text_area.insert(INSERT,header)
		for d in data:
			st_records+= "\t"+str(d[0])+"\t" + str(d[1])+"\t\t" + str(d[2]) + "\n"
		text_area.insert(INSERT,st_records)
		text_area.configure(state='disabled')
	except Exception as e:
		showerror("Error",e)
	finally:
		if con is not None:
				con.close()



lbl_records = Label(view_window,text="Student Records",font=f)
lbl_records.pack(pady=5)
text_area = ScrolledText(view_window, width = 50, height = 15,font = ("Times New Roman",18))
text_area.pack(pady=10)
btn_back = Button(view_window,text="Back",width=20,font=f,command=lambda:back(4))
btn_back.pack(pady=10)



add_window.withdraw()
upd_window.withdraw()
del_window.withdraw()
view_window.withdraw()
mainwindow.mainloop()








