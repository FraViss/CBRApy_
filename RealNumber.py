class RealNumber:
    def __init__(self, value):
        self.value = float(value)

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        if isinstance(other, RealNumber):
            return RealNumber(self.value + other.value)
        elif isinstance(other, (int, float)):
            return RealNumber(self.value + float(other))
        else:
            raise ValueError("Unsupported operand type for +")

    def __sub__(self, other):
        if isinstance(other, RealNumber):
            return RealNumber(self.value - other.value)
        elif isinstance(other, (int, float)):
            return RealNumber(self.value - float(other))
        else:
            raise ValueError("Unsupported operand type for -")

    def __mul__(self, other):
        if isinstance(other, RealNumber):
            return RealNumber(self.value * other.value)
        elif isinstance(other, (int, float)):
            return RealNumber(self.value * float(other))
        else:
            raise ValueError("Unsupported operand type for *")

    def __truediv__(self, other):
        if isinstance(other, RealNumber):
            if other.value != 0:
                return RealNumber(self.value / other.value)
            else:
                raise ZeroDivisionError("Division by zero")
        elif isinstance(other, (int, float)):
            if other != 0:
                return RealNumber(self.value / float(other))
            else:
                raise ZeroDivisionError("Division by zero")
        else:
            raise ValueError("Unsupported operand type for /")

    def __eq__(self, other):
        if isinstance(other, RealNumber):
            return self.value == other.value
        elif isinstance(other, (int, float)):
            return self.value == float(other)
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, RealNumber):
            return self.value < other.value
        elif isinstance(other, (int, float)):
            return self.value < float(other)
        else:
            raise ValueError("Unsupported operand type for <")

    def __gt__(self, other):
        if isinstance(other, RealNumber):
            return self.value > other.value
        elif isinstance(other, (int, float)):
            return self.value > float(other)
        else:
            raise ValueError("Unsupported operand type for >")

    def __le__(self, other):
        if isinstance(other, RealNumber):
            return self.value <= other.value
        elif isinstance(other, (int, float)):
            return self.value <= float(other)
        else:
            raise ValueError("Unsupported operand type for <=")

    def __ge__(self, other):
        if isinstance(other, RealNumber):
            return self.value >= other.value
        elif isinstance(other, (int, float)):
            return self.value >= float(other)
        else:
            raise ValueError("Unsupported operand type for >=")