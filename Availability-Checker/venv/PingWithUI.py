## importing socket module
from tkinter import * # Import GUI
import platform
import subprocess

###initialize window

root =Tk()

root.geometry("400x200") #size of windows
root.resizable(0,0) #not resizable
root.title("Mike-StatusLogger") #name

#heading
heading = Label(root, text = 'StatusLog' , font ='arial 15 bold').pack()
Label(root, text ='Mike-Pinger', font ='arial 15 bold').pack(side = BOTTOM)



def ping(ipAddr, timeout=100):

    if platform.system().lower() == 'windows':
        numFlag = '-n'
    else:
        numFlag = '-c'
    completedPing = subprocess.run(['ping', numFlag, '1', '-w', str(timeout), ipAddr],
                                   stdout=subprocess.PIPE,    # Capture standard out
                                   stderr=subprocess.STDOUT)  # Capture standard error
    # print(completedPing.stdout)
    return (completedPing.returncode == 0) and (b'TTL=' in completedPing.stdout)
## printing the status
str = StringVar() #variable str contains StringVar
def Generator():
    ip = ("Online =",ping('google.com'))
    str.set(ip)
###button
Button(root, text = "Check" , command = Generator ).pack(pady= 5)

Entry(root , textvariable = str).pack(ipadx=20,ipady=20) #Builds string cointaner field.
root.mainloop() #calls main loop of tkinter