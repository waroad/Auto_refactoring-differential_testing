a=2
b=3
c=5
d=7

if a<=b  and b<=c:
    print("changed")
elif b>a and c>b:
    print("changed")
elif b<a and b<c:
    print("not changed")
elif b>=c and d<=c:
    print("changed")
else:
    print("ignore")

# 변환 후
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
