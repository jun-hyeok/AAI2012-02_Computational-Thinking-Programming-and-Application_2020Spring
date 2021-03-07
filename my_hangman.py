import random

guesses = ""
turns = 10

infile = open("words.txt", "r")
lines = infile.readlines()
# readlines()로 읽어들인 *.txt 파일의 word는 whitespace를 포함한다.
# 띄어쓰기(" "), 탭("\t"), 줄 바꿈("\n") 등이 whitespace에 속한다.
# word의 tailling white space(이 문제에서는 "\n")가 char로 받아들여져서 발생한 문제이다.
# .strip() method는 leading, tailing의 whitespace를 제거해 준다.
# 기존의 word에서 word.strip()으로 tailing whitespace를 제거한다.
word = random.choice(lines).strip()

while turns > 0:
    blank = 0
    for char in word:
        if char in guesses:
            print(char, end="")
        else:
            print("_", end="")
            blank += 1
    if blank == 0:
        print("\nYou Win!")
        break
    guess = input("\nGuess the word: ")
    guesses += guess
    if guess not in word:
        turns -= 1
        print("Wrong!")
        print(str(turns) + " times left!")
        if turns == 0:
            print("You lose, the answer is " + word)
infile.close()
