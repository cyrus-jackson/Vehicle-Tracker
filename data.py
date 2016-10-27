d = ()
with open('data.txt','r') as f:
    for line in f:
        d = line.split(",")
print(d) 
