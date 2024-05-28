a=2
b=3
c=5
d=7
e=1

if a<=b  and b<=c:
    print("changed")
elif b>a and c>b:
    print("changed")
elif b<a and b<c:
    print("not changed")
elif (d>e or (b>=c and d<=c and b<a and e>c) or e>10) and c>1 and 0<1:
    print("changed")
else:
    print("ignore")

# changed
# 
# a = 2
# b = 3
# c = 5
# d = 7
#
# if a <= b <= c:
#     print("changed")
# elif a < b < c:
#     print("changed")
# elif b < a and b < c:
#     print("not changed")
# elif b >= c >= d:
#     print("changed")
# else:
#     print("ignore")

