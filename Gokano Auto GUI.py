import time
import os.path
import requests
from datetime import datetime
from msedge.selenium_tools import Edge
from cryptography.fernet import Fernet
from selenium.webdriver.common.by import By
from msedge.selenium_tools import EdgeOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
import threading
import sys

top = tk.Tk()

canvas = tk.Canvas(top, width=400, height=500, bg='white', relief='raised')
canvas.pack()

Mainlabel = tk.Label(top, text=" Gokano Automation ", bg='white')
Mainlabel.config(font=('helvetica', 25, "bold"))
canvas.create_window(200, 50, window=Mainlabel)

Label = tk.Label(top, text="Email:", bg='white')
Label.config(font=('helvetica', 10, "bold"))
canvas.create_window(110, 100, window=Label)

entry1 = tk.Entry(top)
canvas.create_window(200, 100, window=entry1)

Label = tk.Label(top, text="Password:", bg='white')
Label.config(font=('helvetica', 10, "bold"))
canvas.create_window(100, 140, window=Label)

entry2 = tk.Entry(top)
canvas.create_window(200, 140, window=entry2)

Label = tk.Label(top, text="Browser:", bg='white')
Label.config(font=('helvetica', 10, "bold"))
canvas.create_window(100, 180, window=Label)

entry3 = tk.Entry(top)
canvas.create_window(200, 180, window=entry3)

Label = tk.Label(top, text="GPU:", bg='white')
Label.config(font=('helvetica', 10, "bold"))
canvas.create_window(110, 220, window=Label)

entry4 = tk.Entry(top)
canvas.create_window(200, 220, window=entry4)

top.title("Gokano Automator")

a = entry1.bind("<Return>", lambda funct1: entry2.focus())
b = entry2.bind("<Return>", lambda funct1: entry3.focus())
c = entry3.bind("<Return>", lambda funct1: entry4.focus())

pfile = 'encryptedpassword.bin'
efile = 'encryptedemail.bin'

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def write_key():
    key = Fernet.generate_key()
    with open("Gkey.key", "wb") as key_file:
        key_file.write(key)

path = '.'
def load_key():
    return open("Gkey.key", "rb").read()


def get_info():
    # email = input("email:")
    email = entry1.get()
    # password = input("password:")
    password = entry2.get()
    # browser = input("browser:")
    browser = entry3.get()
    # gpu = input("gpu:")
    gpu = entry4.get()
    write_key()
    encrypt_write(email, efile)
    encrypt_write(password, pfile)
    file = open("browserdetails.txt", "w")
    file.write("%s\n" % browser)
    file.write("%s\n" % gpu)
    file.close()
    t2 = threading.Thread(target=run)
    t2.start()
    # run()


def encrypt_write(data, file):
    data = bytes(data, 'utf-8')
    key = load_key()
    f = Fernet(key)
    encrypteddata = f.encrypt(data)
    f = open(file, "wb")
    f.write(encrypteddata)
    f.close()


def read_decrypt(file):
    f = open(file, "rb")
    data = f.readline()
    f.close()
    key = load_key()
    f = Fernet(key)
    decrypted_encrypted = f.decrypt(data)
    decrypted_encrypted = str(decrypted_encrypted)[2:-1]
    return decrypted_encrypted


def run():
    email = read_decrypt(efile)
    password = read_decrypt(pfile)
    cemail = str(email)
    cpassword = str(password)
    with open("browserdetails.txt", "r") as f:
        data = [line.rstrip('\n') for line in f]
    browser = data[0].lower()
    gpu = data[1].lower()

    if browser == 'edge':
        try:
            requests.get("http://www.google.com")
            print('Connection Established.')
            l1 = tk.Label(top, text=" Connection Established. ", bg='white')
            l1.config(font=('helvetica', 15, "bold"))
            canvas.create_window(200, 410, window=l1)
            options = EdgeOptions()
            options.use_chromium = True
            options.add_argument("--start-maximized")
            if gpu == 'no':
                options.add_argument("window-size=1920,1080")
                options.add_argument("--headless")
                options.add_argument("disable-gpu")
                options.add_argument("-inprivate")
            driver = Edge(resource_path('msedgedriver.exe'), options=options)
            driver.get('https://gokano.com/')
            try:
                email = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, 'email')))
                print("Page is ready!")
                l1 = tk.Label(top, text="           Page is Ready.           ", bg='white')
                l1.config(font=('helvetica', 15, "bold"))
                canvas.create_window(200, 410, window=l1)
                email.send_keys(cemail)
                password = driver.find_element_by_name('password')
                password.send_keys(cpassword)
                time.sleep(3)
                button = driver.find_element_by_class_name('submit')
                button.click()        
                try:
                    driver.find_element_by_class_name('gokan-alert-error')
                    print("Invalid Credintials")
                    l1 = tk.Label(top, text=" Invalid Credintials. ", bg='white')
                    l1.config(font=('helvetica', 15, "bold"))
                    canvas.create_window(200, 410, window=l1)
                    time.sleep(3)
                    driver.quit()
                except NoSuchElementException:
                    print('Login sucessful')
                    l1 = tk.Label(top, text=" Login Successful. ", bg='white')
                    l1.config(font=('helvetica', 15, "bold"))
                    canvas.create_window(200, 410, window=l1)
            except TimeoutException:
                print("Login Error!")
                l1 = tk.Label(top, text=" Login Error! ", bg='white')
                l1.config(font=('helvetica', 15, "bold"))
                canvas.create_window(200, 410, window=l1)
                # bowib95650@gomaild.com
                time.sleep(3)
                driver.quit()
            time.sleep(3)
            try:
                cdp = driver.find_element_by_link_text('Collect daily points')
                cdp.click()
                write_time()
                time.sleep(3)
                driver.quit()
            except NoSuchElementException:
                print('Already collected')
                l1 = tk.Label(top, text=" Points Already Collected. ", bg='white')
                l1.config(font=('helvetica', 15, "bold"))
                canvas.create_window(200, 410, window=l1)
                time.sleep(3)
                driver.quit()
            print('Automation completed')
            l1 = tk.Label(top, text=" Automation Completed. ", bg='white')
            l1.config(font=('helvetica', 15, "bold"))
            canvas.create_window(200, 410, window=l1)
            time.sleep(3)
            write_time()
            driver.quit()
        except requests.ConnectionError:
            print('Could not connect')
            l1 = tk.Label(top, text=" Couldn't Connect. ", bg='white')
            l1.config(font=('helvetica', 15, "bold"))
            canvas.create_window(200, 410, window=l1)
            driver.quit()


def write_time():
    Cdatetime = datetime.now()
    file = open("timedetails.txt", "w")
    file.write("%s" % Cdatetime)
    file.close()


def check_time():
    with open("timedetails.txt", "r") as f:
        for line in f:
            data = line
    cdatetime = datetime.now()
    rdatetime = datetime.strptime(data, '%Y-%m-%d %H:%M:%S.%f')
    ddatetime = cdatetime - rdatetime
    if ddatetime.days > 0:
        return True
    else:
        return False

def Main():
    if os.path.exists('timedetails.txt') == False or os.path.exists('Gkey.key') == False:
        get_info()
    if os.path.exists('Gkey.key') and os.path.exists('timedetails.txt') == True:
        print('Data found')
        data = tk.Label(top, text=" Data Already Exists! ", bg='white')
        data.config(font=('helvetica', 15, "bold"))
        canvas.create_window(200, 240, window=data)
        entry1.destroy()
        entry2.destroy()
        entry3.destroy()
        entry4.destroy()
        erase1 = tk.Label(top, text="                                   ", bg='white')
        erase1.config(font=('helvetica', 10, "bold"))
        canvas.create_window(110, 100, window=erase1)
        erase2 = tk.Label(top, text="                                   ", bg='white')
        erase2.config(font=('helvetica', 10, "bold"))
        canvas.create_window(100, 140, window=erase2)
        erase3 = tk.Label(top, text="                                   ", bg='white')
        erase3.config(font=('helvetica', 10, "bold"))
        canvas.create_window(100, 180, window=erase3)
        erase4 = tk.Label(top, text="                                   ", bg='white')
        erase4.config(font=('helvetica', 10, "bold"))
        canvas.create_window(110, 220, window=erase4)
        ctime = check_time()
        if ctime:
            run()
        else:
            print('Time needs to go')
            l1 = tk.Label(top, text=" Time Needs To Go. ", bg='white')
            l1.config(font=('helvetica', 15, "bold"))
            canvas.create_window(200, 410, window=l1)


Button1 = tk.Button(text='Run Application', command=Main, bg='brown', fg='white',
                    font=('helvetica', 10, 'bold'))
canvas.create_window(200, 270, window=Button1)

def Reset():
    os.remove('browserdetails.txt')
    os.remove('encryptedemail.bin')
    os.remove('encryptedpassword.bin')
    os.remove('timedetails.txt')
    os.remove('Gkey.key')
    Info = tk.Label(top, text=" Reset Successful! ", bg='white')
    Info.config(font=('helvetica', 15, "bold"))
    canvas.create_window(200, 410, window=Info)
    entry1.delete(0, 'end')
    entry2.delete(0, 'end')
    entry3.delete(0, 'end')
    entry4.delete(0, 'end')
    # get_info()
    # Main()

    top.mainloop()


Button2 = tk.Button(text='Reset', command=Reset, bg='brown', fg='white',
                    font=('helvetica', 10, 'bold'))
canvas.create_window(200, 320, window=Button2)
t1 = threading.Thread(target=Main)
t1.start()


def Information():
    Info = tk.Label(top, text="         Version: 1.0        ", bg='white')
    Info.config(font=('helvetica', 15, "bold"))
    canvas.create_window(200, 410, window=Info)


Button3 = tk.Button(text='Info', command=Information, bg='brown', fg='white',
                    font=('helvetica', 10, 'bold'))
canvas.create_window(200, 370, window=Button3)


def exitApplication():
    top.destroy()


exitButton = tk.Button(top, text='Exit Application', command=exitApplication, bg='red', fg='white',
                       font=('helvetica', 10, 'bold'))
canvas.create_window(200, 450, window=exitButton)

top.mainloop()