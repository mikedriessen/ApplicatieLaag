#importing Libraries

from tkinter import * # Import GUI
import random, string
import pyperclip



###initialize window

root =Tk()

root.geometry("400x200")
root.resizable(0,0) #not resizable
root.title("Mike-PassGen")


#heading
heading = Label(root, text = 'Password Generator' , font ='arial 15 bold').pack()
Label(root, text ='Mike-PassGen', font ='arial 15 bold').pack(side = BOTTOM)



###select password length
pass_label = Label(root, text = 'Password Length', font = 'arial 10 bold').pack()
pass_len = IntVar()
length = Spinbox(root, from_ = 8, to_ = 32 , textvariable = pass_len , width = 15).pack()



#####define function

pass_str = StringVar()

def Generator():
    password = ''
    for x in range (0,4):
        password = random.choice(string.ascii_uppercase)+random.choice(string.ascii_lowercase)+random.choice(string.digits)+random.choice(string.punctuation)
    for y in range(pass_len.get()- 4):
        password = password+random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation)
    pass_str.set(password)
   


###button

Button(root, text = "Generate Password" , command = Generator ).pack(pady= 5)

Entry(root , textvariable = pass_str).pack()

########function to copy

def Copy_password():
    pyperclip.copy(pass_str.get())

Button(root, text = 'Copy Password', command = Copy_password).pack(pady=5)




# loop to run program
root.mainloop()
