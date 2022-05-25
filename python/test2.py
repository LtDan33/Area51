from random import randint
import time
import asyncio


class Animal:
    legs =  2
    print(f'You are an animal!')
    
    def default():
        print(f'You are an default animal!')

        

class Dog(Animal):
    print(f'You are an dog!')

    def default(self):
        super().default()
        print(f'Your a a default dog!')


foo = Dog()
foo.default()