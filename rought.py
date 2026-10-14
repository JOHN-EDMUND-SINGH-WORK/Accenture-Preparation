a=input()
sum2=0
list1=list(range(1,27))

for i in range(len(a)):
    
    if i==0:
        sum2=sum2+list1[ord(a[i])-97]+list1[ord(a[i+1])-97]
    elif i==len(a)-1:
        sum2=sum2+list1[ord(a[i])-97]+list1[ord(a[i-1])-97]
    else:
        sum2=sum2+list1[ord(a[i])-97]+list1[ord(a[i-1])-97]+list1[ord(a[i+1])-97]
print(sum2)
    

