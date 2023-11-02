class HydraBased:
    def __init__(self,
                 name: str = None,
                 input=None,
                 output=None):
        self.name = name
        self.input = input
        self.output = self.add()

