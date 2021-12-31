import socket
from sys import flags
import threading
import cryptocode

class Client:
    def __init__(self):
        self.create_connection()

    def create_connection(self): # ساختن کانکشن
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # ساختن سوکت
        
        while 1:
            try: # کانکت شدن به کانکشن سوکت
                host = '192.168.42.69'
                port = 5050
                self.s.connect((host,port))
                break
            except:
                print("Couldn't connect to server")
        
        read_db() # خواندن از پایگاه داده
        print("if you want to login type 1")
        print("if you want to sign up type 2")
        menu = input()
        if(menu == '1'): # ورود به برنامه
            self.username = input('Enter username --> ')
            self.password = input('Enter pass --> ')
            if(check_login(self.username,self.password) == True):
                self.s.send(self.username.encode())

                message_handler = threading.Thread(target=self.handle_messages,args=())
                message_handler.start()

                input_handler = threading.Thread(target=self.input_handler,args=())
                input_handler.start()
            else:
                print("Username or Password Incorrect")
        
        elif(menu == '2'): # برای ثبت نام
            username = input("enter your desired username : ")
            if(check_username(username) == True):
                print("username is already taken")
            else:
                password = input("enter your password : ")
                hashed = cryptocode.encrypt(password ,"ahmad")
                dbuser = open("user.txt","a")
                dbpass = open("pass.txt","a")
                dbuser.write(username + '\n')
                dbpass.write(hashed + '\n')
            

    def handle_messages(self): # ارسال مسیج ها
        while 1:
            print(self.s.recv(1204).decode())

    def input_handler(self): # نمایش پیام چت
        while 1:
            self.s.send((self.username+' : '+input()).encode())


usarray = [""]*50
pwdarray = [""]*50

def read_db(): # خواندن پایگاه داده 
    dbuser = open("user.txt","r")
    dbpass = open("pass.txt","r")

    userdata = dbuser.readlines()
    passdata = dbpass.readlines()
        
    usercount = 0
    passcount = 0

    for i in userdata: # ریختن اطلاعات در یک آرایه
	    usarray[usercount] = i.strip()
	    usercount += 1

    for i in passdata: # ریختن اطلاعات در یک آرایه
	    pwdarray[passcount] = i.strip()
	    passcount += 1

    dbuser.close()
    dbpass.close()

def check_login(username,password): # بررسی درست بودن لاگین
    for i in range(0,50):
        if (usarray[i] == username and cryptocode.decrypt(pwdarray[i],"ahmad") == password):
            return True

def check_username(username): # بررسی بودن یوزر نیم در دیتابیس
    for i in range(0,50):
        if (usarray[i] == username):
            return True

client = Client()