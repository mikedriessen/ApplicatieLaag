import re

WW= input("Put in your Password:")
x = True
while x:
    if (len(WW)<6 or len(WW)>20):
        break
    elif not re.search("[a-z]",WW):
        break
    elif not re.search("[0-9]",WW):
        break
    elif not re.search("[A-Z]",WW):
        break
    elif not re.search("[#$%&'()*+,/:;<=>?@^_`{|}~]",WW):
        break
    elif re.search("\s",WW):
        break
    else:
        print("Password is SAFE!")
        i=False
        break

if i:
    print("NOT A SAFE PASSWORD!")