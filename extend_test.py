import json

class Dog:
    def __init__(self, name):
        self.name = name
        self.age = 0
        
    def print_name(slef):
        print(slef.name)
    
    def toString(slef):
        return slef.to_dict()
    
    def to_dict(self):
        return self.__dict__
    

class ElectricDog(Dog):
    def __init__(self, name):
        self.name = name
        self.print_name()


if __name__=="__main__":
    dog = ElectricDog('ElectricDog')
    dog.age = 10
    print(dog.toString())
    