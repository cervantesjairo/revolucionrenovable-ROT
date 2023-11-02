class Operations1:
    """
    A Class object with two arguments (num1 and num2)
    and two methods (add and subtract)
    """

    def __init__(self,
                 num1: int,
                 num2: float):
        self.num1 = num1
        self.num2 = num2

    # Method to add two numbers
    def add(self):
        # print(self.num1 + self.num2)
        return self.num1 + self.num2

    # Method to multiply two numbers
    def subtract(self):
        return self.num1 - self.num2
