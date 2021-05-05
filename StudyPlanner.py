import pandas as pd
import numpy as np
from tkinter import *
from tkinter import ttk
import tkinter as tk


window = tk.Tk() #open window
window.configure(bg = 'white')
window.title('Virtual Study Plan Advisor')
window.geometry("700x900")

#variables for input from user 
studentFile_var = tk.StringVar()
catalogFile_var = tk.StringVar()
selected = IntVar()

#path: /Users/stacyfortes/Documents/cps3320/CS_Student2.xlsx
#path: /Users/stacyfortes/Documents/cps3320/CS_Student.xlsx

#path for electives: /Users/stacyfortes/Documents/cps3320/CS_Electives.xlsx
#path for requirements: /Users/stacyfortes/Documents/cps3320/CS_Requirements.xlsx

#functions 
def submit():
	#retrieve user input
	typeOfCourses = selected.get()
	studentFile = studentFile_var.get()
	catalogFile = catalogFile_var.get()

	#call function to dataframe from paths entered
	student_df = createDFfromPath(studentFile)
	catalog_df = createDFfromPath(catalogFile)

	#reset labels each time 
	creditTotalLbl.config(text ="")
	creditNeededLbl.config(text ="")

	#different options based on which recommendation user wants to see 
	if (typeOfCourses == 1): #if major requirements are selected 
		courseList = generateReqList(student_df, catalog_df)
		creditTotal = totalCredits(student_df)
		creditsNeeded = creditsLeft(creditTotal, catalog_df)
		creditTotalLbl.config(text = "Total Credits You've Taken: " + str(creditTotal))
		creditNeededLbl.config(text = "Credits Left to Graduate: " + str(creditsNeeded))
	elif (typeOfCourses == 2): #if major electives are selected
		courseList = generateReqList(student_df, catalog_df)

	studentFile_var.set(studentFile)
	catalogFile_var.set(catalogFile)

#open each excel file and create a dataframe from it 
def createDFfromPath(filePath):
	df = pd.read_excel(filePath)
	return df

#compare the student's taken courses and comes up with list of what they can take 
def generateReqList(studentDf, catalogDf):
	student_df = studentDf
	requirements_df = catalogDf

	#checks to see if student has taken any of the prerequisites
	requirements_df = requirements_df.assign(Prereq_Taken = requirements_df.Prerequisite.isin(student_df.Course_ID).astype(int))
	#create column of courses that are already taken 
	requirements_df = requirements_df.assign(Course_Taken = requirements_df.Course_ID.isin(student_df.Course_ID).astype(int))

	#selecting only rows with prerequisite met or no prerquisite and course not already taken
	allowedClasses_df = requirements_df[((requirements_df['Prereq_Taken'] == 1) | (requirements_df['Prerequisite'].isnull())) & (requirements_df['Course_Taken'] == 0)]
	display_df = allowedClasses_df[['Course_ID', 'Course_Name', 'Credits']]
	
	generateTreeView(display_df)


#prompt user to enter catalog path 
def enterCatalogPath():
	catalogFileLbl.config(text = "Path to Catalog File: ")
	catalogInfoLbl.config(text = "**Please make sure you enter the file that corresponds with your selection**")
	#display labels and entries 
	catalogFileLbl.grid() 
	cFileEntry.grid()
	catalogInfoLbl.grid()  


#find how many credits user has taken
def totalCredits(df):
	total = df['Credits'].sum()
	return total


#find how many credits user still needs to graduate 
def creditsLeft(completedCredits, df):
	#requirements_df = pd.read_excel(r'/Users/stacyfortes/Documents/cps3320/CS_Requirements.xlsx')
	majorTotal = df['Total_Req_Credits'].iloc[0]
	creditDiff = majorTotal - completedCredits
	return creditDiff


#creates the dataframe display in the Window
def generateTreeView(df):
	clear_data()
	tv1["column"] = list(df.columns)
	tv1["show"] = "headings"
	for column in tv1["columns"]:
		tv1.heading(column, text=column)

	df_rows = df.to_numpy().tolist()
	for row in df_rows:
		tv1.insert("", "end", values=row)

	return None


#function to clear data from display when resubmiting
def clear_data():
	tv1.delete(*tv1.get_children())




#GUI SPECIFICS 

#labels -- labels for each section 
welcome = Label(window, text="Welcome to Virtual Study Plan Advisor!", 
	fg='black', font=("Helvetica bold", 20))
welcome.pack(pady=10)

instructions = Label(window, text="Below, enter the path to the file which contains an excel sheet of all the courses you've completed.", 
					fg='black', font=("Helvetica", 12))
instructions.pack()

instructions2 = Label(window, text="Then select which type of course catalog you'd like to get recommendations from.", 
					fg='black', font=("Helvetica", 12))
instructions2.pack()

instructions3 = Label(window, text="The Study Plan Advisor will then recommend courses you are allowed to take based on prerequisites you've taken.", 
					fg='black', font=("Helvetica", 12))
instructions3.pack()

#frame for course list 
#frame1 = tk.LabelFrame(window, text = "Course Options")
#frame1.place(height = 250, width = 500)

#for spacing purposes 
entryFrame = Frame(window)
entryFrame.pack(pady=20)

#labels 
studentFileLbl = Label(entryFrame, text="Path To Courses Taken File:", fg='black', font=("Helvetica", 16))
studentFileLbl.grid(row = 0, column = 0, padx = 20)

#entry -- where user will enter their file path 
sFileEntry = Entry(entryFrame, textvariable = studentFile_var, bd = 3)
sFileEntry.grid(row = 0, column = 1, padx = 20)  

catalogFileLbl = Label(entryFrame, text="", fg='black', font=("Helvetica", 16))
catalogFileLbl.grid(row = 2, column = 0, padx = 20)
catalogFileLbl.grid_remove() #to hide file

cFileEntry = Entry(entryFrame, textvariable = catalogFile_var, bd = 3)
cFileEntry.grid(row = 2, column = 1, padx = 20)  
cFileEntry.grid_remove() #hide entry

catalogInfoLbl = Label(entryFrame, text="", fg = 'red', font = ("Helvetica", 10))
catalogInfoLbl.grid(row = 3, column = 1, padx = 20)
catalogInfoLbl.grid_remove() #hide


#radio buttons 
reqButton = Radiobutton(entryFrame,text='Major Requirements', value=1, variable = selected, command = enterCatalogPath)
reqButton.grid(row = 1, column = 0, padx = 20, pady = 10)

elecButton = Radiobutton(entryFrame,text='Major Electives', value=2, variable = selected, command = enterCatalogPath)
elecButton.grid(row = 1, column = 1, padx = 20, pady = 10)

#submit button
btn = Button(window, text="Submit", fg='black', command = submit)
btn.pack(pady = 20)

# resultsLbl = Label(window, text="", fg = 'Black', font = ("Helvetica", 16))
# resultsLbl.pack(pady = 20)
# resultsLbl.pack_forget() #hide

#Treeview -- for displaying dataframe  
tv1 = ttk.Treeview(window)
tv1.pack(pady = 20)
treescrolly = tk.Scrollbar(window, orient="vertical", command = tv1.yview)
treescrollx = tk.Scrollbar(window, orient="horizontal", command = tv1.xview)
tv1.configure(xscrollcommand = treescrollx.set, yscrollcommand = treescrolly.set)
treescrollx.pack(side="bottom", fill="x")
treescrolly.pack(side="right", fill="y")

creditTotalLbl=Label(window, text="", fg='blue', font=("Helvetica", 16))
creditTotalLbl.pack()

creditNeededLbl=Label(window, text="", fg='red', font=("Helvetica", 16))
creditNeededLbl.pack()


window.mainloop()

