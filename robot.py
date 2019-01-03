
"""ROBOT CLASS"""
class Robot:
    def __init__(self, name, color, age):
        self.name = name 
        self.color = color
        self.age = age

    def name_self(self):
        print("my name is "+self.name)  

    def color_self(self):
        print("my color is "+self.color)

    def age_self(self):
        print("my age is " + self.age)

R1 = Robot("Tom", "Purple", "2 months")
R2 = Robot("ahmed", "colourless", "1 months")
R3 = Robot("med", "black", "7 months")

R1.name_self()
R1.color_self()
R1.age_self()

R2 = Robot("ahmed", "colourless", "1 months")
R2.name_self()
R2.color_self()
R2.age_self()

R3 = Robot("med", "black", "7 months")
R3.name_self()
R3.color_self()
R3.age_self()
