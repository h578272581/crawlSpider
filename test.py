class A:
    def fun(self, num):
        print('funIn: %s'%num)

def fun(num):
    print('funOut: %s'%num)

a = A()
a.fun = fun
a.fun(3)

