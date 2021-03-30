## importing socket module
from tkinter import * # Import GUI
import socket

###initialize window

root =Tk()

root.geometry("400x200") #size of windows
root.resizable(0,0) #not resizable
root.title("Mike-IPFinder") #name

#heading
heading = Label(root, text = 'IP finder' , font ='arial 15 bold').pack()
Label(root, text ='Mike-IPFinder', font ='arial 15 bold').pack(side = BOTTOM)

## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)
## printing the hostname and ip_address
str = StringVar() #variable str contains StringVar
def Generator():
    ip = (f"{hostname}") #resolves hostname
    ip = ip + (f":{ip_address}") #resolves ip adress
    str.set(ip)
###button

Button(root, text = "What's my IP?" , command = Generator ).pack(pady= 5)

Entry(root , textvariable = str).pack(ipadx=20,ipady=20) #Builds string cointaner field.
root.mainloop() #calls main loop of tkinter