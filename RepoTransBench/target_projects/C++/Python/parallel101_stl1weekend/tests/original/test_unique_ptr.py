class Animal:
    def speak(self):
        raise NotImplementedError
    def __del__(self):
        pass

class Dog(Animal):
    def __init__(self, age):
        self.age = age
    def speak(self):
        return f"Bark! I'm {self.age} Year Old!"

class Cat(Animal):
    def __init__(self, age_ref):
        self.age_ref = age_ref
    def speak(self):
        return f"Meow! I'm {self.age_ref[0]} Year Old!"

def makeUnique(cls, arg):
    return cls(arg)

def test_zoo_animals():
    zoo = []
    age = [3]
    zoo.append(Cat(age))
    zoo.append(Dog(age[0]))
    barks = [a.speak() for a in zoo]
    assert barks[0].startswith("Meow")
    assert barks[1].startswith("Bark")
    age[0] += 1
    barks2 = [a.speak() for a in zoo]
    assert barks2[0].startswith("Meow") and "4" in barks2[0]
    assert barks2[1].startswith("Bark") and "3" in barks2[1]