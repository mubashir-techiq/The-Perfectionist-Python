import PyQt5.QtWidgets as w
from PyQt5.uic import loadUi
import sys
from functools import partial
import random as rd
import os
from PyQt5.QtCore import Qt
from User import User
import shutil


# Linked List
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
class LinkedList:
    def __init__(self):
        self.head = None
    
    def insertAtEnd(self,val):
        if self.head == None:
            self.head = Node(val)
        else:
            ptr = self.head
            while ptr.next != None:
                ptr = ptr.next
            ptr.next = Node(val)

    def deleteStart(self):
        if not (self.head == None):
            val = self.head
            self.head = self.head.next
            return val

# Stack
class Stack:
    list = LinkedList()

    def push(val):
        list.insertAtEnd(val)
    
    def pop():
        return list.deleteStart()

# files
AdminFile = 'files\Admin.txt'
WorkerFile = 'files\Worker.txt'
CustomerFile = 'files\Customer.txt'
temp = 'temp.txt'
ServiceFile = 'files\Services.txt'
BookServiceFile = 'files\BookServices.txt'

#Widgets
class Appointment2(w.QWidget):
    def __init__(self,price, name, gender):
        super(Appointment2,self).__init__()
        loadUi('Widgets/Appointment 2.ui', self)
        self.price.setText(price)
        self.name.setText(name)
        self.gender.setText(gender)
        self.setFixedHeight(250)
        self.setFixedWidth(300)
    
    def mousePressEvent(self, event,clas):
        if event.button() == Qt.LeftButton:
            clas.exec_()

class Appointment1(w.QWidget):
    def __init__(self,price, name, service):
        super(Appointment1,self).__init__()
        loadUi('Widgets/Appointment 1.ui', self)
        self.price.setText(price)
        self.name.setText(name)
        self.service.setText(service)
        self.setFixedHeight(250)
        self.setFixedWidth(300)

class Review1(w.QWidget):
    def __init__(self,price, name, service,rate,review):
        super(Review1,self).__init__()
        loadUi('Widgets\\review 1.ui', self)
        self.price.setText(price)
        self.name.setText(name)
        self.service.setText(service)
        self.rate.setText(rate)
        self.review.setText(review)
        self.setFixedHeight(250)
        self.setFixedWidth(900)

class Review2(w.QWidget):
    def __init__(self,name, id, rate,review):
        super(Review2,self).__init__()
        loadUi('Widgets\\REVIEW.ui', self)
        self.name.setText(name)
        self.id.setText(id)
        self.rate.setText(rate)
        self.review.setText(review)
        self.setFixedHeight(250)
        self.setFixedWidth(900)

class WorkersWid(w.QWidget):
    def __init__(self,id, name,rate):
        super(WorkersWid,self).__init__()
        loadUi('Widgets\\workers.ui', self)
        self.id.setText(id)
        self.name.setText(name)
        self.rate.setText(rate)
        self.setFixedHeight(200)
        self.setFixedWidth(1000)

# Welcome Screens
class Login(w.QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi('Welcome\Login Screen.ui',self)

        types = ['Admin','Worker','Customer']
        for i in types:
            self.type.addItem(i)

        self.signup.clicked.connect(partial(self.changeUi,SignUp()))
        self.login.clicked.connect(self.getLogin)

    def changeUi(self,obj):
        ui = obj
        self.close()
        ui.exec_()

    def getLogin(self):
        mail = self.mail.toPlainText()
        pas = self.pas.toPlainText()
        typ = self.type.currentText()
        
        if mail == '' or pas == '':
            msg = w.QMessageBox.information(None, "Information", "Please Enter All Fields Properly!.", w.QMessageBox.Ok)
        else:
            if typ == 'Admin':
                self.checkLogin(AdminFile,mail,pas)
            elif typ == 'Worker':
                self.checkLogin(WorkerFile,mail,pas)
            else:
                self.checkLogin(CustomerFile,mail,pas)

    def checkLogin(self,filename,mail,pas):
        flag = True
        with open(filename,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[2] == mail and arr[4] == pas:
                    User.id = arr[0]
                    User.name = arr[1]
                    User.mail = arr[2]
                    User.contact = arr[3]
                    User.pas = arr[4]
                    User.type = self.type.currentText()
                    if filename == AdminFile:
                        self.changeUi(AdminConsole())
                    elif filename == WorkerFile:
                        self.changeUi(WorkerConsole())
                    elif filename == CustomerFile:
                        self.changeUi(CustomerConsole())
                        pass
                    flag = False
                    break
        if flag:
            w.QMessageBox.information(None, "Information", "This User Doesn't Exist.", w.QMessageBox.Ok)

class Welcome(w.QDialog):
    def __init__(self):
        super(Welcome,self).__init__()
        loadUi('Welcome\Welcome Screen.ui',self)

        self.start.clicked.connect(self.changeUI)

    def changeUI(self):
        ui = Login()
        self.close()
        ui.exec_()

class SignUp(w.QDialog):
    def __init__(self):
        super(SignUp,self).__init__()
        loadUi('Welcome\SignUp Screen.ui',self)

        self.login.clicked.connect(self.loginui)
        self.signup.clicked.connect(self.addCustomer)

    def loginui(self):
        ui =Login()
        self.close()
        ui.exec_()

    def addCustomer(self):
        name = self.name.toPlainText()
        mail = self.mail.toPlainText()
        contact = self.contact.toPlainText()
        pas = self.pas.toPlainText()
        flag = True
        while flag:
            ids = rd.randrange(1000,9999)
            if os.path.exists(CustomerFile):
                flag2 = False
                with open(CustomerFile,'r') as file:
                    for line in file:
                        line = line.strip()
                        arr = line.split('~')
                        if arr[0] == ids:
                            flag2 = True
                            break
                if flag2 == False:
                    flag = False
            else:
                flag = False                    

        if name == '' or mail == '' or contact == '' or pas == '':
             w.QMessageBox.information(None, "Information", "Please Enter All Fields Properly!.", w.QMessageBox.Ok)
        elif pas != self.conpas.toPlainText():
            w.QMessageBox.information(None, "Information", "Password and Confirm Password Should be Same!.", w.QMessageBox.Ok)
        elif len(contact) != 11:
            w.QMessageBox.information(None, "Information", "Please Enter a Valid Contact Number!.", w.QMessageBox.Ok)
        else:
            if os.path.exists(CustomerFile):
                file = open(CustomerFile,'a')
                file.write(f'{ids}~{name}~{mail}~{contact}~{pas}\n')
            else:
                file = open(CustomerFile,'w')
                file.write(f'{ids}~{name}~{mail}~{contact}~{pas}\n')
            file.close()
            User.id = str(ids)
            User.name = name
            User.mail = mail
            User.pas = pas
            User.contact = contact
            self.changeUi(CustomerConsole())

    def changeUi(self,obj):
        ui = obj
        self.close()
        ui.exec_()

# Admin Screens
class AddingWork(w.QDialog):
    def __init__(self):
        super(AddingWork,self).__init__()
        loadUi('Admin\Adding a Worker.ui',self)

        self.add.clicked.connect(self.addWorker)

    def addWorker(self):
        name = self.name.toPlainText()
        mail = self.mail.toPlainText()
        contact = self.contact.toPlainText()
        cnic = self.cnic.toPlainText()
        pas = self.pas.toPlainText()
        flag = True
        while flag:
            id = rd.randrange(1000,9999)
            if os.path.exists(WorkerFile):
                flag2 = False
                with open(WorkerFile,'r') as file:
                    for line in file:
                        line = line.strip()
                        arr = line.split('~')
                        if arr[0] == id:
                            flag2 = True
                            break
                if flag2 == False:
                    flag = False
            else:
                flag = False                    

        if name == '' or mail == '' or contact == '' or pas == '' or cnic == '':
             w.QMessageBox.information(None, "Information", "Please Enter All Fields Properly!.", w.QMessageBox.Ok)
        elif len(contact) != 11:
            w.QMessageBox.information(None, "Information", "Please Enter a Valid Contact Number!.", w.QMessageBox.Ok)
        else:
            if os.path.exists(WorkerFile):
                file = open(WorkerFile,'a')
                file.write(f'{id}~{name}~{mail}~{contact}~{pas}~{cnic}~0~0\n')
            else:
                file = open(WorkerFile,'w')
                file.write(f'{id}~{name}~{mail}~{contact}~{pas}~{cnic}~0~0\n')
            file.close()
            w.QMessageBox.information(None, "Information", "Worker Added Successfully!.", w.QMessageBox.Ok)
            self.close()
    
class AdminConsole(w.QDialog):
    def __init__(self):
        super(AdminConsole,self).__init__()
        loadUi('Admin\Admin Console.ui',self)
        obj = Dashboard()
        self.stack.addWidget(obj)
        self.stack.setCurrentWidget(obj)
        
        self.home.clicked.connect(partial(self.changeWidget,Dashboard()))
        self.workers.clicked.connect(partial(self.changeWidget,AdminWorkerOption()))
        self.appointments.clicked.connect(partial(self.changeWidget,AdminAppointment()))
        self.services.clicked.connect(partial(self.changeWidget,AdminServiceOption()))
        self.revenue.clicked.connect(partial(self.changeWidget,AdminProfitandLoss()))
        self.logout.clicked.connect(self.changeUi)

    def changeWidget(self,obj):
        self.stack.addWidget(obj)
        self.stack.setCurrentWidget(obj)
        self.changeColor()
    
    def changeColor(self):
        self.workers.setStyleSheet('background-color: rgba(255, 255, 255, 0);font: 25 14pt "Montserrat Light";color: #FFFCF2')
        self.appointments.setStyleSheet('background-color: rgba(255, 255, 255, 0);font: 25 14pt "Montserrat Light";color: #FFFCF2')
        self.services.setStyleSheet('background-color: rgba(255, 255, 255, 0);font: 25 14pt "Montserrat Light";color: #FFFCF2')
        self.revenue.setStyleSheet('background-color: rgba(255, 255, 255, 0);font: 25 14pt "Montserrat Light";color: #FFFCF2')
        btn = self.sender()
        btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);font: 63 14pt "Montserrat SemiBold";color: rgb(235, 94, 40);')

    def changeUi(self):
        ui = Login()
        self.close()
        ui.exec_()

class AddService(w.QDialog):
    def __init__(self):
        super(AddService,self).__init__()
        loadUi('Admin\Add Service.ui',self)

        self.add.clicked.connect(self.addservice)

    def addservice(self):
        flag = True
        while flag:
            id = rd.randrange(1000,9999)
            if os.path.exists(ServiceFile):
                flag2 = False
                with open(ServiceFile,'r') as file:
                    for line in file:
                        line = line.strip()
                        arr = line.split('~')
                        if arr[0] == id:
                            flag2 = True
                            break
                if flag2 == False:
                    flag = False
            else:
                flag = False

        name = self.name.toPlainText()
        price = self.price.toPlainText()
        gender = ''
        if self.male.isChecked():
            gender = 'Male'
        elif self.female.isChecked():
            gender = 'Female'

        if name == '' or price == '' or gender == '':
            w.QMessageBox.information(None,'Information','Please Enter All Fields!',w.QMessageBox.Ok)
        else:
            if os.path.exists(ServiceFile):
                file = open(ServiceFile,'a')
                file.write(f'{id}~{name}~{price}~{gender}\n')
            else:
                file = open(ServiceFile,'w')
                file.write(f'{id}~{name}~{price}~{gender}\n')
            file.close()
            w.QMessageBox.information(None,'Information','Service Added Successfully!',w.QMessageBox.Ok)
            self.close()

class AdminAppointment(w.QDialog):
    def __init__(self):
        super(AdminAppointment,self).__init__()
        loadUi('Admin\Admin Appointment Approval.ui',self)

        scroll = self.load
        layout = w.QVBoxLayout()
        widget = w.QWidget()
        widget.setLayout(layout)
        row_layout = w.QHBoxLayout()

        i = 0
        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[1] == 'Pending':
                    label = Appointment1(arr[9],arr[3],arr[8])
                    label.setObjectName(f's{arr[0]}')
                    label.btn.clicked.connect(partial(self.uiExec,arr[0]))
                    row_layout.addWidget(label)
                    if (i+1) % 3 == 0:
                        layout.addLayout(row_layout)
                        row_layout = w.QHBoxLayout()
                    i+=1
        
        if row_layout.count() > 0:
            layout.addLayout(row_layout)

        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def uiExec(self,id):
        ui = AppointmentPage(id)
        ui.exec_()

class AdminProfitandLoss(w.QDialog):
    def __init__(self):
        super(AdminProfitandLoss,self).__init__()
        loadUi('Admin\Admin Profit and Loss.ui',self)

        scroll = self.load
        layout = w.QHBoxLayout()
        widget = w.QWidget()
        widget.setLayout(layout)

        total = 0
        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[1] == 'Completed':
                    total += int(arr[9])
                    name = str(arr[8])
                    cname = str(arr[3])
                    label = Appointment1(arr[9],'Completed',arr[8])
                    label.setObjectName(f's{arr[0]}')
                    layout.addWidget(label)

        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        

        self.total.setText(str(total))

class AdminServiceOption(w.QDialog):
    def __init__(self):
        super(AdminServiceOption,self).__init__()
        loadUi('Admin\Admin service Options.ui',self)

        scroll = self.load
        layout = w.QVBoxLayout()
        widget = w.QWidget()
        widget.setLayout(layout)
        row_layout = w.QHBoxLayout()
        
        i = 0
        with open(ServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                name = str(arr[1])
                gender = str(arr[3])
                label = Appointment2(arr[2],name,gender)
                label.setObjectName(f's{arr[0]}')
                row_layout.addWidget(label)

                if (i+1) % 3 == 0:
                    layout.addLayout(row_layout)
                    row_layout = w.QHBoxLayout()
                i+=1
        
        if row_layout.count() > 0:
            layout.addLayout(row_layout)

        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.add.clicked.connect(partial(self.changeUi,AddService()))
        
    def changeUi(self,obj):
        ui = obj
        ui.exec_()

class AdminWorkerOption(w.QDialog):
    def __init__(self):
        super(AdminWorkerOption,self).__init__()
        loadUi('Admin\Admin Worker Options.ui',self)

        scroll = self.load
        layout = w.QVBoxLayout()
        widget = w.QWidget()
        widget.setLayout(layout)
        with open(WorkerFile, 'r') as file:
            # Read data into a list
            worker_list = []
            for line in file:
                line = line.strip()
                arr = line.split('~')
                worker_list.append(arr)

            # Bubble Sort on the basis of arr[1] (names)
            n = len(worker_list)
            for i in range(n - 1):
                for j in range(0, n - i - 1):
                    if worker_list[j][1] > worker_list[j + 1][1]:
                        worker_list[j], worker_list[j + 1] = worker_list[j + 1], worker_list[j]

        # Update the layout with sorted labels
        for worker_data in worker_list:
            label = WorkersWid(worker_data[0], worker_data[1], worker_data[7])
            label.setObjectName(f's{worker_data[0]}')
            label.btn.clicked.connect(partial(self.uiExec, worker_data[0]))
            layout.addWidget(label)

        
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)


        self.addWorker.clicked.connect(partial(self.changeUi,AddingWork()))

    def changeUi(self,obj):
        ui = obj
        ui.exec_()

    def uiExec(self,id):
        ui = DetailsofWorker(id)
        ui.exec_()

class Dashboard(w.QDialog):
    def __init__(self):
        super(Dashboard,self).__init__()
        loadUi('Admin\Dashboard.ui',self)
        file = open(AdminFile,'r')
        for line in file:
            line = line.strip()
            arr = line.split('~')
        self.name.setText(arr[1])
        file.close()
        wcount = 0
        ccount = 0
        with open(WorkerFile,'r') as file:
            for line in file:
                wcount+=1
        with open(CustomerFile,'r') as file:
            for line in file:
                ccount+=1

        self.wt.setText(str(wcount))
        self.ct.setText(str(ccount))
        scroll_area = self.pics
        scroll_area.setWidgetResizable(True)
        
        scroll_content = w.QWidget(scroll_area)
        scroll_area.setWidget(scroll_content)
        scroll_layout = w.QHBoxLayout(scroll_content)

        scroll_layout.setAlignment(Qt.AlignLeft) 

        for i in range(6):
            label = w.QLabel(f"Label {i+1}")
            label.setObjectName("label")
            label.setText('')
            label.setFixedWidth(300)
            
            label.setStyleSheet(f'''
                    border-radius: 20%;
                    border: 2px solid gray;
                    border-image: url(images/b{i+1}) 10 10 10 10 stretch stretch;
                    padding: 5px;
                    margin: 5px;
            ''')
            scroll_layout.addWidget(label)

class DetailsofWorker(w.QDialog):
    def __init__(self,id):
        super(DetailsofWorker,self).__init__()
        loadUi('Admin\Details of Worker.ui',self)

        self.remove.clicked.connect(partial(self.removeWorker,id))
        with open(WorkerFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[0] == id:
                    self.name.setText(arr[1])
                    self.mail.setText(arr[2])
                    self.contact.setText(arr[3])
                    self.cnic.setText(arr[5])
                    self.rating.setText(arr[7])
                    self.service.setText(arr[6])

        scroll = self.load
        layout = w.QHBoxLayout()
        widget = w.QWidget()
        widget.setLayout(layout)
        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if len(arr) > 10:
                    if arr[10] == id and arr[1]== 'Completed':
                        label = Review1(arr[9],arr[3],arr[8],arr[14],arr[15])
                        label.setObjectName(f's{arr[0]}')
                        layout.addWidget(label)

        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def removeWorker(self,id):
        file2 = open(temp,'w')
        with open(WorkerFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[0] != id:
                    file2.write(f'{line}\n')
        file2.close()
        shutil.move(temp,WorkerFile)
        w.QMessageBox.information(None,'Information','Worker Removed Successfully!',w.QMessageBox.Ok)
        self.close()

class AppointmentPage(w.QDialog):
    def __init__(self,id):
        super(AppointmentPage,self).__init__()
        loadUi('Admin\Appointment Page.ui',self)

        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[0] == id:
                    self.name.setText(arr[3])
                    self.mail.setText(arr[4])
                    self.contact.setText(arr[5])
                    self.gender.setText(arr[7])
                    self.service.setText(arr[8])
                    self.price.setText(arr[9])
                    break
        self.workers = []
        with open(WorkerFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                arr2 = []
                arr2.append(arr[0])
                arr2.append(arr[1])
                self.workers.append(arr2)
                self.worker.addItem(arr[1])

        day = ['Monday','Tuesday','Wednessday','Thursday','Friday']
        slot = ['09:00AM to 12:00PM','01:00PM to 03:00PM']

        for i in day:
            self.day.addItem(i)
        
        for i in slot:
            self.slot.addItem(i)

        self.rejec.clicked.connect(self.rejectApp)
        self.approve.clicked.connect(partial(self.approveApp,id))

    def rejectApp(self):
        file2 = open(temp,'w')
        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[0] != id:
                    file2.write(f'{line}\n')

        file2.close()
        shutil.move(temp,BookServiceFile)
        w.QMessageBox.information(None,'Information','Appointment Rejected Successfully!',w.QMessageBox.Ok)
        self.close()

    def approveApp(self,id):
        for i in self.workers:
            if i[1] == self.worker.currentText():
                wid = i[0]
        file2 = open(temp,'w')
        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[0] == id:
                    file2.write(f'{arr[0]}~Approved~{arr[2]}~{arr[3]}~{arr[4]}~{arr[5]}~{arr[6]}~{arr[7]}~{arr[8]}~{arr[9]}~{wid}~{self.worker.currentText()}~{self.day.currentText()}~{self.slot.currentText()}\n')
                else:
                    file2.write(f'{line}\n')
                    
        file2.close()
        shutil.move(temp,BookServiceFile)
        w.QMessageBox.information(None,'Information','Appointment Approved Successfully!',w.QMessageBox.Ok)
        self.close()

# Customer Screens
class CustomerConsole(w.QDialog):
    def __init__(self):
        super(CustomerConsole,self).__init__()
        loadUi('Customer\Customer Console.ui',self)

        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[1] == 'Billed' and arr[2] == User.id:
                    ui = PaymentPending(arr[0])
                    ui.exec_()
                    self.close()
                    break
        obj = CustomerDashboard()
        self.stack.addWidget(obj)
        self.stack.setCurrentWidget(obj)

        self.home.clicked.connect(partial(self.changeWidget,CustomerDashboard()))
        self.book.clicked.connect(partial(self.changeWidget,Appointment()))
        self.perform.clicked.connect(partial(self.changeWidget,LeftAppointment()))
        self.review.clicked.connect(partial(self.changeWidget,YourPreviousReview()))
        self.pending.clicked.connect(partial(self.changeWidget,OldAppointment()))
        self.logout.clicked.connect(self.changeUi)
    
    def changeWidget(self,obj):
        self.stack.addWidget(obj)
        self.stack.setCurrentWidget(obj)
        self.changeColor()
    
    def changeColor(self):
        self.book.setStyleSheet('background-color: rgba(255, 255, 255, 0);font: 25 14pt "Montserrat Light";color: #FFFCF2')
        self.perform.setStyleSheet('background-color: rgba(255, 255, 255, 0);font: 25 14pt "Montserrat Light";color: #FFFCF2')
        self.review.setStyleSheet('background-color: rgba(255, 255, 255, 0);font: 25 14pt "Montserrat Light";color: #FFFCF2')
        self.pending.setStyleSheet('background-color: rgba(255, 255, 255, 0);font: 25 14pt "Montserrat Light";color: #FFFCF2')
        btn = self.sender()
        btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);font: 63 14pt "Montserrat SemiBold";color: rgb(235, 94, 40);')

    def changeUi(self):
        ui = Login()
        self.close()
        ui.exec_()

class Appointment(w.QDialog):
    def __init__(self):
        super(Appointment,self).__init__()
        loadUi('Customer\Appointment.ui',self)

        gender = 'Male'
        self.getServices(gender)
        self.male.toggled.connect(partial(self.getServices,'Male'))
        self.female.toggled.connect(partial(self.getServices,'Female'))
    
    def getServices(self,types):
        gender = types

        scroll = self.load
        layout = w.QVBoxLayout()
        widget = w.QWidget()
        widget.setLayout(layout)
        row_layout = w.QHBoxLayout()

        i = 0
        with open(ServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                
                if arr[3] == gender:
                    name = str(arr[1])
                    gender = str(arr[3])
                    label = Appointment2(arr[2],name,gender)
                    label.setObjectName(f's{arr[0]}')
                    label.btn.clicked.connect(partial(self.uiExec,name,arr[2],gender)) 
                    row_layout.addWidget(label)

                    if (i+1) % 3 == 0:
                        layout.addLayout(row_layout)
                        row_layout = w.QHBoxLayout()
                    i+=1

        if row_layout.count() > 0:
            layout.addLayout(row_layout)

        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def uiExec(self,name,price,gender,id):
        ui = Booking(name,price,gender,id)
        ui.exec_()

class Booking(w.QDialog):
    def __init__(self,name,price,gender,id):
        super(Booking,self).__init__()
        loadUi('Customer\Booking.ui',self)

        self.id = id
        self.gender.setText(gender)
        self.service.setText(name)
        self.price.setText(price)

        self.book.clicked.connect(self.addService)

    def addService(self):
        name = self.name.toPlainText()
        mail = self.mail.toPlainText()
        contact = self.contact.toPlainText()
        gender = self.gender.text()
        service = self.service.text()
        price = self.price.text()

        flag = True
        while flag:
            aid = rd.randrange(1000,9999)
            if os.path.exists(CustomerFile):
                flag2 = False
                with open(BookServiceFile,'r') as file:
                    for line in file:
                        line = line.strip()
                        arr = line.split('~')
                        if arr[0] == aid:
                            flag2 = True
                            break
                if flag2 == False:
                    flag = False
            else:
                flag = False       

        file = open(BookServiceFile,'a')
        file.write(f'{aid}~Pending~{User.id}~{name}~{mail}~{contact}~{self.id}~{gender}~{service}~{price}\n')
        file.close()
        w.QMessageBox.information(None,'Information','Booking Done Successfully!',w.QMessageBox.Ok)
        self.close()

class CustomerDashboard(w.QDialog):
    def __init__(self):
        super(CustomerDashboard,self).__init__()
        loadUi('Customer\Customer Dashboard.ui',self)

        sapcount = 0
        remcount = 0
        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[1] == 'Completed' and arr[2] == User.id:
                    sapcount+=1

        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[1] == 'Approved' and arr[2] == User.id:
                    remcount+=1

        self.name.setText(User.name)
        self.mail.setText(User.mail)
        self.contact.setText(User.contact)
        self.cid.setText(User.id)
        self.sap.setText(str(sapcount))
        self.rem.setText(str(remcount))
        self.edit.clicked.connect(partial(self.changeUi,EditInfo()))

    def changeUi(self,obj):
        ui = obj
        ui.exec_()

class LeftAppointment(w.QDialog):
    def __init__(self):
        super(LeftAppointment,self).__init__()
        loadUi('Customer\left Appointment.ui',self)

        scroll = self.load
        layout = w.QVBoxLayout()
        widget = w.QWidget()
        widget.setLayout(layout)
        row_layout = w.QHBoxLayout()

        i = 0
        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[1] == 'Approved' and arr[2] == User.id:
                    name = str(arr[8])
                    wname = str(arr[11])
                    label = Appointment1(arr[9],wname,name)
                    label.setObjectName(f's{arr[0]}')
                    label.btn.clicked.connect(partial(self.PerformAppointment,arr[0]))
                    row_layout.addWidget(label)

                    if (i+1) % 3 == 0:
                        layout.addLayout(row_layout)
                        row_layout = w.QHBoxLayout()
                    i+=1
        
        if row_layout.count() > 0:
            layout.addLayout(row_layout)

        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    

    def PerformAppointment(self,aid):
        file2 = open(temp,'w')
        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[0] == aid:
                    for i in range(len(arr)):
                        if i == 1:
                            file2.write('Payment Pending~')
                        elif i == len(arr)-1:
                            file2.write(f'{arr[i]}\n')
                        else:
                            file2.write(f'{arr[i]}~')
                else:
                    file2.write(f'{line}\n')
        file2.close()
        shutil.move(temp,BookServiceFile)
        w.QMessageBox.information(None,'Information','Service Performed Successfully!',w.QMessageBox.Ok)
    
class EditInfo(w.QDialog):
    def __init__(self):
        super(EditInfo,self).__init__()
        loadUi('Customer\Edit Info.ui',self)

        self.name.setText(User.name)
        self.mail.setText(User.mail)
        self.contact.setText(User.contact)
        self.pas.setText(User.pas)
        self.save.clicked.connect(self.updateInfo)

    def updateInfo(self):
        name = self.name.toPlainText()
        mail = self.mail.toPlainText()
        contact = self.contact.toPlainText()
        pas = self.pas.toPlainText()
        file = open(temp,'w')
        with open(CustomerFile,'r') as file2:
            for line in file2:
                line = line.strip()
                arr = line.split('~')
                if arr[0] == User.id:
                    file.write(f'{User.id}~{name}~{mail}~{contact}~{pas}\n')
                else:
                    file.write(f'{line}\n')

        file.close()
        shutil.move(temp,CustomerFile)
        w.QMessageBox.information(None,'Information','Information Updated Successfully!',w.QMessageBox.Ok)
        self.close()

class OldAppointment(w.QDialog):
    def __init__(self):
        super(OldAppointment,self).__init__()
        loadUi('Customer\Old Appointment.ui',self)

        scroll = self.load
        layout = w.QVBoxLayout()
        widget = w.QWidget()
        widget.setLayout(layout)
        row_layout = w.QHBoxLayout()

        i = 0
        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[1] == 'Completed' and arr[2] == User.id:
                    name = str(arr[8])
                    wname = str(arr[11])
                    label = Appointment1(arr[9],wname,name)
                    label.setObjectName(f's{arr[0]}')
                    row_layout.addWidget(label)

                    if (i+1) % 3 == 0:
                        layout.addLayout(row_layout)
                        row_layout = w.QHBoxLayout()
                    i+=1
        
        if row_layout.count() > 0:
            layout.addLayout(row_layout)

        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

class PaymentPending(w.QDialog):
    def __init__(self,aid):
        super(PaymentPending,self).__init__()
        loadUi('Customer\Payment Pending Page.ui',self)

        self.pay.clicked.connect(partial(self.paymentDone,aid))

    def paymentDone(self,aid):
        w.QMessageBox.information(None,'Information','Payment Done Successfully!',w.QMessageBox.Ok)
        ui = GiveRating(aid)
        self.close()
        ui.exec_()

class GiveRating(w.QDialog):
    def __init__(self,aid):
        super(GiveRating,self).__init__()
        loadUi('Customer\\rating.ui',self)

        self.submit.clicked.connect(partial(self.reviewSubmit,aid))

    def reviewSubmit(self,aid):
        rate = self.rate.toPlainText()
        review = self.review.toPlainText()
        if rate == '' or review == '':
            w.QMessageBox.information(None,'Information','Please Enter All Fields!',w.QMessageBox.Ok)
        elif int(rate) > 5:
            w.QMessageBox.information(None,'Information','Rating Should Not Be Greater Than 5!',w.QMessageBox.Ok)
        else:
            file2 = open(temp,'w')
            with open(BookServiceFile,'r') as file:
                for line in file:
                    line = line.strip()
                    arr = line.split('~')
                    if arr[0] == aid:
                        arr[1] = 'Completed'
                        for i in arr:
                            file2.write(f'{i}~')
                        file2.write(f'{rate}~{review}\n')
                    else:
                        file2.write(f'{line}\n')
            file2.close()
            shutil.move(temp,BookServiceFile)

            file2 = open(temp,'w')
            with open(WorkerFile,'r') as file:
                for line in file:
                    line = line.strip()
                    arr = line.split('~')
                    if arr[0] == User.id:
                        arr[6]+=1
                        arr[7]+=rate
                        arr[7] = arr[7]/arr[6]
                        for i in arr:
                            file2.write(f'{i}~')
                        file2.write('\n')
                    else:
                        file2.write(f'{line}\n')
            file2.close()
            shutil.move(temp,WorkerFile)
            ui = CustomerConsole()
            self.close()
            ui.exec_()

class YourPreviousReview(w.QDialog):
    def __init__(self):
        super(YourPreviousReview,self).__init__()
        loadUi('Customer\Your Previous Reviews.ui',self)

        scroll = self.load
        layout = w.QVBoxLayout()
        widget = w.QWidget()
        widget.setLayout(layout)
        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[2] == User.id and arr[1] == 'Completed':
                    label = Review2(arr[11],arr[10],arr[14],arr[15])
                    label.setObjectName(f's{arr[0]}')
                    layout.addWidget(label)
        
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

# Worker Screens
class WorkerConsole(w.QDialog):
    def __init__(self):
        super(WorkerConsole,self).__init__()
        loadUi('Worker\Worker Console.ui',self)
        obj = WorkerDashboard()
        self.stack.addWidget(obj)
        self.stack.setCurrentWidget(obj)
        
        self.home.clicked.connect(partial(self.changeWidget,WorkerDashboard()))
        self.bill.clicked.connect(partial(self.changeWidget,ServicesDone()))
        self.check.clicked.connect(partial(self.changeWidget,CheckAppointment()))
        self.review.clicked.connect(partial(self.changeWidget,CheckReviews()))
        self.logout.clicked.connect(self.changeUi)
    
    def changeWidget(self,obj):
        self.stack.addWidget(obj)
        self.stack.setCurrentWidget(obj)
        self.changeColor()
    
    def changeColor(self):
        self.bill.setStyleSheet('background-color: rgba(255, 255, 255, 0);font: 25 14pt "Montserrat Light";color: #FFFCF2')
        self.check.setStyleSheet('background-color: rgba(255, 255, 255, 0);font: 25 14pt "Montserrat Light";color: #FFFCF2')
        self.review.setStyleSheet('background-color: rgba(255, 255, 255, 0);font: 25 14pt "Montserrat Light";color: #FFFCF2')
        btn = self.sender()
        btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);font: 63 14pt "Montserrat SemiBold";color: rgb(235, 94, 40);')

    def changeUi(self):
        ui = Login()
        self.close()
        ui.exec_()

class BillCustomer(w.QDialog):
    def __init__(self,aid):
        super(BillCustomer,self).__init__()
        loadUi('Worker\Bill Customer.ui',self)

        with open(BookServiceFile,'r') as file:
            cid = 0
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[0] == aid:
                    self.name.setText(arr[3])
                    self.service.setText(arr[8])
                    self.price.setText(arr[9])
                    self.worker.setText(arr[11])
                    self.day.setText(arr[12])
                    self.slot.setText(arr[13])
                    cid = arr[0]
                    break

        self.send.clicked.connect(partial(self.sendReceipt,cid))

    def sendReceipt(self,aid):
        file2 = open(temp,'w')
        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[0] == aid:
                    arr[1] = 'Billed'
                    for i in range(len(arr)-1):
                        file2.write(f'{arr[i]}~')
                    file2.write(f'{len(arr)-1}\n')
                else:
                    file2.write(f'{line}\n')
        
        file2.close()
        shutil.move(temp,BookServiceFile)
        w.QMessageBox.information(None,'Information','Receipt Sent Successfully!',w.QMessageBox.Ok)
        self.close()

class CheckReviews(w.QDialog):
    def __init__(self):
        super(CheckReviews,self).__init__()
        loadUi('Worker\Check Reviews.ui',self)

        scroll = self.load
        layout = w.QVBoxLayout()
        widget = w.QWidget()
        widget.setLayout(layout)

        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if len(arr) > 10:
                    if arr[10] == User.id and arr[1] == 'Completed':
                        label = Review2(arr[3],arr[2],arr[14],arr[15])
                        label.setObjectName(f's{arr[0]}')
                        layout.addWidget(label)
        
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

class CheckAppointment(w.QDialog):
    def __init__(self):
        super(CheckAppointment,self).__init__()
        loadUi('Worker\Check Appointments.ui',self)

        scroll = self.load
        layout = w.QVBoxLayout()
        widget = w.QWidget()
        widget.setLayout(layout)
        row_layout = w.QHBoxLayout()

        i = 0
        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[1] == 'Approved' and arr[10] == User.id:
                    name = str(arr[8])
                    cname = str(arr[3])
                    label = Appointment1(arr[9],cname,name)
                    label.setObjectName(f's{arr[0]}')
                    row_layout.addWidget(label)

                    if (i+1) % 3 == 0:
                        layout.addLayout(row_layout)
                        row_layout = w.QHBoxLayout()
                    i+=1
        
        if row_layout.count() > 0:
            layout.addLayout(row_layout)

        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    
class WEditInfo(w.QDialog):
    def __init__(self):
        super(WEditInfo,self).__init__()
        loadUi('Worker\Edit Info.ui',self)

        self.name.setText(User.name)
        self.mail.setText(User.mail)
        self.contact.setText(User.contact)
        self.pas.setText(User.pas)
        self.save.clicked.connect(self.updateInfo)

    def updateInfo(self):
        name = self.name.toPlainText()
        mail = self.mail.toPlainText()
        contact = self.contact.toPlainText()
        pas = self.pas.toPlainText()
        file = open(temp,'w')
        with open(WorkerFile,'r') as file2:
            for line in file2:
                line = line.strip()
                arr = line.split('~')
                if arr[0] == User.id:
                    file.write(f'{User.id}~{name}~{mail}~{contact}~{pas}~{arr[5]}\n')
                else:
                    file.write(f'{line}\n')

        file.close()
        shutil.move(temp,WorkerFile)
        w.QMessageBox.information(None,'Information','Information Updated Successfully!',w.QMessageBox.Ok)
        self.close()

class ServicesDone(w.QDialog):
    def __init__(self):
        super(ServicesDone,self).__init__()
        loadUi('Worker\Services Done.ui',self)

        scroll = self.load
        layout = w.QVBoxLayout()
        widget = w.QWidget()
        widget.setLayout(layout)
        row_layout = w.QHBoxLayout()

        i = 0
        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[1] == 'Payment Pending' and arr[10] == User.id:
                    name = str(arr[8])
                    cname = str(arr[3])
                    label = Appointment1(arr[9],cname,name)
                    label.setObjectName(f's{arr[0]}')
                    label.btn.clicked.connect(partial(self.uiExec,arr[0]))
                    row_layout.addWidget(label)

                    if (i+1) % 3 == 0:
                        layout.addLayout(row_layout)
                        row_layout = w.QHBoxLayout()
                    i+=1
        
        if row_layout.count() > 0:
            layout.addLayout(row_layout)

        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
      
    def uiExec(self,id):
        ui = BillCustomer(id)
        ui.exec_()

class WorkerDashboard(w.QDialog):
    def __init__(self):
        super(WorkerDashboard,self).__init__()
        loadUi('Worker\Worker Dashboard.ui',self)

        sdcount = 0
        with open(BookServiceFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if len(arr) > 10:
                    if arr[1] == 'Completed' and arr[10] == User.id:
                        sdcount +=1

        ratecount = 0

        with open(WorkerFile,'r') as file:
            for line in file:
                line = line.strip()
                arr = line.split('~')
                if arr[0] == User.id:
                    ratecount = arr[7]
        self.name.setText(User.name)
        self.mail.setText(User.mail)
        self.contact.setText(User.contact)
        self.wid.setText(User.id)
        self.sd.setText(str(sdcount))
        self.rate.setText(str(ratecount))
        self.edit.clicked.connect(partial(self.changeUi,WEditInfo()))

    def changeUi(self,obj):
        ui = obj
        ui.exec_()

if __name__ == "__main__":
    app = w.QApplication(sys.argv)
    ui = Welcome()
    ui.show()
    app.exec_()