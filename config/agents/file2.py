class Operations2:
    """
    Class Operations2 with two arguments (num1 and num2)
    and two methods (multiple and divide)
    """
    def __init__(self,
                 num1: int,
                 num2: float):
        self.num1 = num1
        self.num2 = num2

    # Method to multiply two numbers
    def multiply(self):
        return self.num1 * self.num2

    # Method to divide two numbers
    def divide(self):
        return self.num1 / self.num2
