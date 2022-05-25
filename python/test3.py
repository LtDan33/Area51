class foo:
    # Toy problem to show how __str__ and __repr__ are used
    def __init__(self, x, y,*args, **kwargs):
        # super(CLASS_NAME, self).__init__(*args, **kwargs)
        self.x = x
        self.y = y
        print('In the init')

    def __repr__(self) -> str:
        return "The repr method. {} {}".format(self.x,self.y)

    def __str__(self) -> str:
        return "The str method. {} {}".format(self.x,self.y)

f = foo(3,4)

print(f)
print(repr(f))