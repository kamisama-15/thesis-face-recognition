############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
from PIL import Image, ImageTk
############################################# FUNCTIONS ################################################
import firebase_admin
from firebase_admin import credentials, firestore,auth
cam = cv2.VideoCapture(0)
# Replace 'path/to/your/credentials.json' with the path to your Firebase Admin SDK credentials file
cred = credentials.Certificate('login-9ed8b-firebase-adminsdk-fk6z4-89d69e63ee.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()
#######################
def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
#################
def set_background_image():
    img = Image.open('sksu_bg.jpg')
    img = ImageTk.PhotoImage(img)
    background_label = tk.Label(window, image=img)
    background_label.image = img
    background_label.place(relwidth=1, relheight=1)
#################################################################################

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)

###################################################################################
def on_closing(capture, root):
    capture.release()
    root.destroy()

##################################################################################
def contact():
    mess._show(title='Contact us', message="Please contact us on : 'bokuwakamida@gmail.com' ")

###################################################################################

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

###################################################################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

###################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Enter Old Password',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#3ece48", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#####################################################################################
def clear_form():
    txt.delete(0, 'end')
    txt_fname.delete(0, 'end')
    txt_mname.delete(0, 'end')
    txt_lname.delete(0, 'end')
    txt_department.set("Select Department")
    txt_course.set("Select Course")
    txt_year.set("Select Year Level")
    txt_gmail.delete(0, 'end')
    message1.configure(text="1) Take Images \u2192  2) Save Profile")
#######################################################################################
def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')
    clear_form()


######################################################################################

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

def clear_txt():
    txt.delete(0, 'end')
def clear_txt_department():
    txt_department.set("Select Department")


#######################################################################################
columns = ['SERIAL NO.', '', 'ID', '', 'Last Name','','First Name','','Middle Name', '', 'COURSE', '', 'DEPARTMENT','','Year','','GMAIL']


def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'Last Name', '', 'First Name', '', 'Middle Name', '', 'COURSE', '',
               'DEPARTMENT', '', 'Year', '', 'GMAIL']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails/StudentDetails.csv")

    if exists:
        with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
    else:
        with open("StudentDetails/StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1

    Id = txt.get()
    fname = txt_fname.get()
    mname = txt_mname.get()
    lname = txt_lname.get()
    course = txt_course.get()
    department = txt_department.get()
    year = txt_year.get()
    gmail = txt_gmail.get()

    if (fname.isalpha() or ' ' in fname) and (mname.isalpha() or ' ' in mname) and (
            lname.isalpha() or ' ' in lname) and department and course and year and gmail:
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum = sampleNum + 1
                img_name = f"TrainingImage/{fname}{lname}.{serial}.{Id}.{sampleNum}.jpg"
                cv2.imwrite(img_name, gray[y:y + h, x:x + w])

                cv2.imshow('Taking Images', img)

            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 100:
                break

        cam.release()
        cv2.destroyAllWindows()
        res = f"Images Taken for ID: {Id}"
        row = [serial, '', Id, '', lname, '', fname, '', mname, '', course, '', department, '', year, '', gmail]

        # Get the user UID generated by Firebase Authentication
        user_email = gmail
        user_password = "123456"  # Default password
        user = auth.create_user(email=user_email, password=user_password)
        uid = user.uid

        # Save data to Firestore with the user's UID as the document ID
        student_data = {
            "ID": Id,
            "Last Name": lname,
            "First Name": fname,
            "Middle Name": mname,
            "COURSE": course,
            "DEPARTMENT": department,
            "Year": year,
            "GMAIL": gmail
        }

        db.collection("users").document(uid).set(student_data)

        with open('StudentDetails/StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)

        csvFile.close()
        message1.configure(text=res)

    else:
        res = "Enter Correct name, course, department, year, and gmail"
        message.configure(text=res)
########################################################################################

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids
###########################################################################################
def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")

    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return

    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    col_names = ['Serial No.','ID', 'Last Name', 'First Name', 'Middle Name', 'Course', 'Date',
                 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")

    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        df = pd.DataFrame(columns=col_names)
        df.to_csv("StudentDetails\StudentDetails.csv", index=False)
        mess._show(title='Details Missing', message='Students details are missing, a new file has been created.')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
        return

    marked_students = set()

    try:
        while True:
            ret, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
                serial, conf = recognizer.predict(gray[y:y + h, x:x + w])

                if conf < 50 and serial not in marked_students:
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

                    # Extracting First, Middle, and Last Names
                    aa = df.loc[df['SERIAL NO.'] == serial][['First Name', 'Middle Name', 'Last Name']].values
                    fname, mname, lname = aa[0]

                    # Extracting Course
                    if 'COURSE' in df.columns:
                        course = df['COURSE'].loc[df['SERIAL NO.'] == serial].values
                        if len(course) > 0:
                            course = str(course[0])
                        else:
                            course = 'N/A'
                    else:
                        course = 'N/A'

                    ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                    ID = str(ID)
                    ID = ID[1:-1]

                    # Increment the serial number for each attendance
                    serial_no = len(marked_students) + 1

                    # Move the attendance-related code outside the loop
                    attendance_data = {
                        'Serial No.': serial_no,
                        'ID': str(ID),
                        'Last Name': str(lname),
                        'First Name': str(fname),
                        'Middle Name': str(mname),
                        'Course': str(course),
                        'Date': str(date),
                        'Time': str(timeStamp)
                    }

                    # Update Firestore with attendance data
                    db.collection('attendance').add(attendance_data)

                    # Update Treeview with attendance data
                    tv.insert('', 'end', text=str(serial_no), values=(
                        str(ID), str(fname + " " + mname + " " + lname), str(course), str(date), str(timeStamp)))

                    marked_students.add(serial)  # Mark the student as attended

                    # Display the name continuously while saving attendance only once
                if marked_students:
                    cv2.putText(im, f"Attendance Recorded for: {fname} {mname} {lname}", (10, 30), font, 1, (0, 255, 0),
                                2)

                cv2.imshow('Taking Attendance', im)

            key = cv2.waitKey(1)
            if key == ord('q'):
                # Save attendance data to a file with the date in the "Attendance" folder
                filename = f"Attendance/Attendance_{date}.csv"

                # Remove empty columns
                df = df.dropna(axis=1, how='all')

                df.to_csv(filename, index=False)
                mess._show(title='Attendance Saved', message=f'Attendance data saved to {filename}')
                break

    finally:
        cam.release()
        cv2.destroyAllWindows()

######################################## USED STUFFS ############################################

global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.geometry("1280x720")
window.resizable(True, False)
window.title("Attendance System")

# Set the background image
set_background_image()

frame1 = tk.Frame(window, bg="#5cb85c")
frame1.place(relx=0, rely=0.17, relwidth=0.50, relheight=0.80)

frame2 = tk.Frame(window, bg="gray")
frame2.place(relx=0.5, rely=0.17, relwidth=0.70, relheight=0.80)

message3 = tk.Label(window, text="Face Recognition Based Attendance System" ,fg="white",bg="#262523" ,width=53 ,height=1,font=('arial', 29, ' bold '))
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="#F3EEEA")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="#F3EEEA")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text=day + "-" + mont[month] + "-" + year + "  |  ", fg="orange", bg="#739072",
                 width=100, height=2, font=('times',15, ' bold '))
datef.pack(fill='both',expand=1)

clock = tk.Label(frame3,fg="orange",bg="#739072" ,width=55 ,height=1,font=('times', 22, ' bold '))
clock.pack(fill='both',expand=1)
tick()

head2 = tk.Label(frame2, text="                       For New Registrations                       ", fg="black",bg="#fffffF" ,font=('arial', 17, ' bold '), width=50 )
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="                       For Already Registered                       ", fg="black",bg="#fffffF" ,font=('arial', 17, ' bold '), width=50)
head1.place(x=0,y=0)


lbl = tk.Label(frame2, text="Enter ID", width=10, height=1, fg="black", bg="#A9A9A9", font=('arial', 10, ' bold '))
lbl.place(x=80, y=60)
lbl.configure(bg=frame2.cget("bg"))
txt = tk.Entry(frame2, width=35, fg="black", font=('arial', 10, ' bold '))
txt.place(x=30, y=88)

# Entry for First Name
lbl_fname = tk.Label(frame2, text="Enter First Name", width=15, fg="black", bg="#A9A9A9", font=('arial', 10, ' bold '))
lbl_fname.place(x=380, y=55)
lbl_fname.configure(bg=frame2.cget("bg"))
txt_fname = tk.Entry(frame2, width=35, fg="black", font=('arial', 10, ' bold '))
txt_fname.place(x=350, y=88)

# Entry for Middle Name
lbl_mname = tk.Label(frame2, text="Enter Middle Name", width=15, fg="black", bg="#A9A9A9", font=('arial', 10, ' bold '))
lbl_mname.place(x=80, y=120)
lbl_mname.configure(bg=frame2.cget("bg"))
txt_mname = tk.Entry(frame2, width=35, fg="black", font=('arial', 10, ' bold '))
txt_mname.place(x=30, y=150)

# Entry for Last Name
lbl_lname = tk.Label(frame2, text="Enter Last Name", width=15, fg="black", bg="#A9A9A9", font=('arial', 10, ' bold '))
lbl_lname.place(x=380, y=120)
lbl_lname.configure(bg=frame2.cget("bg"))
txt_lname = tk.Entry(frame2, width=35, fg="black", font=('arial', 10, ' bold '))
txt_lname.place(x=350, y=150)

# Department dropdown
departments = ["COE", "CSS", "NABA"]
lbl_department = tk.Label(frame2, text="Select Department", width=15, fg="black", bg="#ECE3CE",
                          font=('arial', 10, ' bold '))
lbl_department.place(x=380, y=180)
lbl_department.configure(bg=frame2.cget("bg"))
txt_department = ttk.Combobox(frame2, values=departments, width=33, state="readonly", style="Custom.TCombobox")
txt_department.set("Select Department")
txt_department.place(x=350, y=210)
# Combobox for Course
courses = ["BSCPE", "BSECE", "BSCE", "BSIT", "BSCS","BSIT-Drafting"]
lbl_course = tk.Label(frame2, text="Select Course", width=15, fg="black", bg="#ECE3CE", font=('arial', 10, ' bold '))
lbl_course.place(x=80, y=180)
lbl_course.configure(bg=frame2.cget("bg"))
txt_course = ttk.Combobox(frame2, values=courses, width=33, state="readonly", style="Custom.TCombobox")
txt_course.set("Select Course")
txt_course.place(x=30, y=210)
#for year level
year_level = ["1st Year", "2nd Year", "3rd Year", "4th Year",]
lbl_year = tk.Label(frame2, text="Select Year Level", width=15, fg="black", bg="#ECE3CE", font=('arial', 10, ' bold '))
lbl_year.place(x=80, y=240)
lbl_year.configure(bg=frame2.cget("bg"))
txt_year = ttk.Combobox(frame2, values=year_level, width=33, state="readonly", style="Custom.TCombobox")
txt_year.set("Select Year Level")
txt_year.place(x=30, y=265)
#gmail
lbl_gmail = tk.Label(frame2, text="Enter Your SKSU Gmail", width=20, fg="black", bg="#A9A9A9", font=('arial', 10, ' bold '))
lbl_gmail.place(x=380, y=240)
lbl_gmail.configure(bg=frame2.cget("bg"))
txt_gmail = tk.Entry(frame2, width=35, fg="black", font=('arial', 10, ' bold '))
txt_gmail.place(x=350, y=265)
# Message Labels
message1 = tk.Label(frame2, text="1) Take Images \u2192  2) Save Profile", bg="#00aeff", fg="black", width=39, height=1, activebackground="yellow", font=('arial', 12, ' bold '))
message1.place(x=120, y=300)
message1.configure(bg=frame2.cget("bg"))
message = tk.Label(frame2, text="", bg="#00aeff", fg="black", width=39, height=1, activebackground="yellow", font=('arial', 16, ' bold '))
message.place(x=50, y=450)
message.configure(bg=frame2.cget("bg"))

lbl3 = tk.Label(frame1, text="Attendance Record", width=20, fg="black", height=1, font=('arial', 15, 'bold'))
lbl3.place(x=170, y=115)
lbl3.configure(bg=frame1.cget("bg"))


res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Total Registrations till now  : '+str(res))

##################### MENUBAR #################################

menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='Change Password', command = change_pass)
filemenu.add_command(label='Contact Us', command = contact)
filemenu.add_command(label='Exit',command = window.destroy)
menubar.add_cascade(label='Help',font=('times', 29, ' bold '),menu=filemenu)

################## TREEVIEW ATTENDANCE TABLE ####################
tv = ttk.Treeview(frame1, height=13, columns=('ID', 'Name', 'Course', 'Date', 'Time'))
tv.column('#0', width=50)
tv.column('ID', width=50)
tv.column('Name', width=200)
tv.column('Course', width=100)
tv.column('Date', width=100)
tv.column('Time', width=100)
tv.grid(row=2, column=0, padx=(0, 0), pady=(150, 0), columnspan=5)
tv.heading('#0', text='No.')
tv.heading('ID', text='ID')
tv.heading('Name', text='NAME')
tv.heading('Course', text='COURSE')
tv.heading('Date', text='DATE')
tv.heading('Time', text='TIME')

###################### SCROLLBAR ################################

scroll = ttk.Scrollbar(frame1, orient='vertical', command=tv.yview)
scroll.grid(row=2, column=5, padx=(0, 100), pady=(150, 0), sticky='ns')  # Updated column
tv.configure(yscrollcommand=scroll.set)

###################### BUTTONS ##################################
# clear_department_btn = tk.Button(frame2, text="Clear Department", command=clear_txt_department, fg="black", bg="gray",
#                                  width=15, height=1, activebackground="white", font=('times', 10, ' bold '))
# clear_department_btn.place(x=500, y=250)
#
# clear_course_btn = tk.Button(frame2, text="Clear Course", command=clear_txt_course, fg="black", bg="gray",
#                               width=15, height=1, activebackground="white", font=('times', 10, ' bold '))
# clear_course_btn.place(x=200, y=250)
# Buttons
takeImg = tk.Button(frame2, text="Take Images", command=TakeImages, fg="white", bg="#5bc0de", width=25, height=1,
                    activebackground="white", font=('times', 10, ' bold '),padx=10,pady=5)
takeImg.place(x=230, y=350)

trainImg = tk.Button(frame2, text="Save Profile", command=psw, fg="white", bg="#5cb85c", width=25, height=1, activebackground="white", font=('times', 10, ' bold '), padx=10,pady=5)
trainImg.place(x=230    , y=400)
trackImg = tk.Button(frame1, text="📷 Take Attendance", command=TrackImages, fg="black", bg="#5bc0de", width=15, height=1, activebackground="white", font=('arial', 12, ' bold '), compound=tk.CENTER, anchor="center", justify="center")
trackImg.place(x=200,y=50)
quitWindow = tk.Button(frame1, text="Quit", command=window.destroy  ,fg="black"  ,bg="#d9534f"  ,width=20 ,height=1, activebackground = "white" ,font=('times', 10, ' bold '),padx=10,pady=5)
quitWindow.place(x=200, y=450)

##################### END ######################################

window.configure(menu=menubar)
window.mainloop()

####################################################################################################
