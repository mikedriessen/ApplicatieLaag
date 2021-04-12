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

lines = ["Baas, neem een racecar, neem een Saab.", "A man, a plan, a canal: Panama.",
    "A Toyota. Race fast, safe car. A Toyota.",
    "Cigar? Toss it in a can. It is so tragic.",
    "Dammit, I'm mad!",
    "Delia saw I was ailed.",
    "Desserts, I stressed!",
    "Draw, O coward!",
    "Lepers repel.",
    "Live not on evil.",
    "Lonely Tylenol.",
    "Murder for a jar of red rum.",
    "Never odd or even.",
    "No lemon, no melon.",
    "Senile felines.",
    "So many dynamos!",
    "Step on no pets.",
    "Was it a car or a cat I saw?",
    "Dot Net Perls is not a palindrome.",
    "Why are you reading this?",
    "This article is not useful."]

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