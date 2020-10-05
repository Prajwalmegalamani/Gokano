
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

pfile = 'encryptedpassword.bin'
efile = 'encryptedemail.bin'
        
def write_key():
    key = Fernet.generate_key()
    with open("Gkey.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("Gkey.key", "rb").read()
        
def get_info():
    email = input("email:")
    password = input("password:")
    browser = input("browser:")
    gpu = input("gpu:")
    write_key()
    encrypt_write(email, efile)
    encrypt_write(password, pfile)
    file = open("browserdetails.txt", "w")
    file.write("%s\n" %(browser))
    file.write("%s\n" %(gpu))
    file.close()
    run()
    
def encrypt_write(data,file):
    data = bytes(data ,'utf-8')
    key = load_key()
    f = Fernet(key)
    encrypteddata = f.encrypt(data)
    f = open(file,"wb")
    f.write(encrypteddata)
    f.close()
    
def read_decrypt(file):
    f = open(file,"rb")
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
    print(cemail)
    print(cpassword)
    with open("browserdetails.txt", "r") as f:
        data = [line.rstrip('\n') for line in f]
    browser = data[0].lower()
    gpu = data[1].lower()
    
    if browser == 'edge':
        try:
            requests.get("http://www.google.com")
            print ('Connection Found')
            options = EdgeOptions()
            options.use_chromium = True
            options.add_argument("--start-maximized")
            if gpu == 'no':
                options.add_argument("window-size=1920,1080")
                options.add_argument("--headless")
                options.add_argument("disable-gpu")
                options.add_argument("-inprivate")
            driver = Edge(executable_path='msedgedriver.exe', options=options)
            driver.get('https://gokano.com/')
            try:
                email = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, 'email')))
                print ("Page is ready!")
                email.send_keys(cemail)
                password = driver.find_element_by_name('password')
                password.send_keys(cpassword)
                time.sleep(3)
                button = driver.find_element_by_class_name('submit')
                button.click()
                print('Login sucessful')
            except TimeoutException:
                print ("Error logining in")            #bowib95650@gomaild.com
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
                time.sleep(3)
                driver.quit()
            print('Automation completed')
            time.sleep(3)
            driver.quit()
        except requests.ConnectionError:
            print ('Could not connect')
            
def write_time():
    Cdatetime = datetime.now()
    file = open("timedetails.txt", "w")
    file.write("%s" %(Cdatetime))
    file.close()
    
def check_time():
    with open("timedetails.txt", "r") as f:
        for line in f:
            data = line
    cdatetime = datetime.now()
    rdatetime = datetime.strptime(data,'%Y-%m-%d %H:%M:%S.%f')  
    ddatetime = cdatetime - rdatetime
    if (ddatetime.days) > 0:
        return True
    else:
        return False
        
    
if os.path.exists('timedetails.txt') == False or os.path.exists('Gkey.key') == False:
        get_info()
if os.path.exists('Gkey.key') == True and os.path.exists('timedetails.txt') == True:
        print('Data found')
        ctime = check_time()
        if ctime == True:
            run()
        else:
            print('Time needs to go')
        



            

