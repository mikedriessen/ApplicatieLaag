def is_palindrome(value):
    min = 0
    max = len(value) - 1

    # Scan string for letter equality at each end.
    # ... Move indexes closer to the center after each check.
    while True:

        # Return true if all characters were checked.
        if min > max:
            return True;

        a = value[min]
        b = value[max]

        # Return false is characters are not equal.
        if a != b:
            return False;

        # Move inwards.
        min += 1
        max -= 1

lines = ["Baas, neem een racecar, neem een Saab."]

# Use to translate punctuation to spaces.
# ... Changes uppercase to lowercase.
dict = str.maketrans(",:.'!?ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "      abcdefghijklmnopqrstuvwxyz")

for line in lines:
    # Change all punctuation to spaces.
    line = line.translate(dict)

    # Remove all spaces.
    line = line.replace(" ", "")

    # See if line is a palindrome.
    if is_palindrome(line):
        print("Palindrome:    ", line)
    else:
        print("Not palindrome:", line)