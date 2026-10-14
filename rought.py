s=input()
upper=0
lower=0
number=0
special=0

for i in s:
    if len(s)>=8:
        if i.isupper():
            upper+=1
        if i.islower():
            lower+=1
        if i.isdigit():
            number+=1 
        else:
            special+=1 
if upper>0 and lower>0 and number>0 and special>0:
    print("Strong Password")
else:
    print("Weak Password")