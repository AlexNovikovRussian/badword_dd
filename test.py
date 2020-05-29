from fuzzywuzzy import fuzz
from fuzzywuzzy import process

with open("badwords.txt") as file:
    badwords = [row.strip().lower() for row in file]

message = input()

mess_arr = message.split(" ")

badword_detected = False
for word in mess_arr:
    word = word.lower()
    if badword_detected:
        break
    for badword in badwords:
        if fuzz.ratio(word, badword) > 60:
            print("bad word detected")
            badword_detected = True
            break
badword_detected = False
