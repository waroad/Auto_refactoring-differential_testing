# return boolean statement
def func(A, B):
    if A:
        print(1)
        return True
    # elif B:
    #     return False
    else:
        return False
    
A, B = 1, 1
func(1,1)
# changed
def func(A):
    return A