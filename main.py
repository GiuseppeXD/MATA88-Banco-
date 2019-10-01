file = open("banco.txt", "r+")
file.seek(4)
file.truncate()