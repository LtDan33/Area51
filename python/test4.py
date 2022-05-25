from termcolor import colored

""" Fun with class variables
"""

class MyClass:
    static_elem = 123

    def __init__(self) -> None:
        self.object_elem = 456
        print(colored(f'In the init MyClass.static_elem is: {MyClass.static_elem}\n','red'))

c1 = MyClass()
c2 = MyClass()

print(colored(f'c1 is. static_elem: {c1.static_elem}. object_elem: {c1.object_elem}', 'green'))
print(colored(f'c2 is. static_elem: {c2.static_elem}. object_elem: {c2.object_elem} \n','blue'))


MyClass.static_elem = 999

print(colored(f'c1 is. static_elem: {c1.static_elem}. object_elem: {c1.object_elem}', 'green'))
print(colored(f'c2 is. static_elem: {c2.static_elem}. object_elem: {c2.object_elem}\n ','blue'))

c1.object_elem = 888


print(colored(f'c1 is. static_elem: {c1.static_elem}. object_elem: {c1.object_elem}', 'green'))
print(colored(f'c2 is. static_elem: {c2.static_elem}. object_elem: {c2.object_elem}\n ','blue'))

c1.static_elem = 666

print(colored(f'c1 is. static_elem: {c1.static_elem}. object_elem: {c1.object_elem}', 'green'))
print(colored(f'c2 is. static_elem: {c2.static_elem}. object_elem: {c2.object_elem}\n ','blue'))

print(colored(f'OUTSIDEW the init. MyClass.static_elem is: {c1.__class__.static_elem}\n','red'))