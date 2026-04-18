class Temperature:
    def __init__(self, celsius):
        self.c = celsius

    def __repr__(self):
        return f"Temperature({self.c}°C)"

    def __str__(self):
        return f"{self.c}°C / {self.to_fahrenheit()}°F"

    def to_fahrenheit(self):
        return round((self.c * 9 / 5) + 32, 1)

    def __add__(self, other):
        if isinstance(other, Temperature):
            return Temperature(self.c + other.c)
        return Temperature(self.c + other)

    def __sub__(self, other):
        if isinstance(other, Temperature):
            return Temperature(self.c - other.c)
        return Temperature(self.c - other)

    def __eq__(self, other):
        return self.c == other.c

    def __lt__(self, other):
        return self.c < other.c

    def __call__(self, scale="C"):
        if scale == "C":
            return self.c
        elif scale == "F":
            return self.to_fahrenheit()
        else:
            raise ValueError("Use 'C' or 'F'")

t1 = Temperature(25)
t2 = Temperature(10)
print(t1)                 
print(t1 + t2)            
print(t1 - 5)             
print(t1 == Temperature(25))
print(t1 < t2)
print(t1("F"))            