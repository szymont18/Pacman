file = open("resources/maps/level02.txt")
lines = file.readlines()
cnt = 0
for line in lines:
    for chr in line.split():
        if int(chr) == 0: cnt += 1
print(cnt)