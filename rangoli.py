import string


def rangoli(size):
    for i in range(size - 1, -size, -1):
        row = ["-"] * (size * 2 - 1)
        for j in range(0, size - abs(i)):
            row[size - 1 + j] = alphabet[abs(i) + j]
            row[size - 1 - j] = alphabet[abs(i) + j]
        print("-".join(row))
    return


alphabet = string.ascii_lowercase
size = int(input("Enter your integer: "))
rangoli(size)
