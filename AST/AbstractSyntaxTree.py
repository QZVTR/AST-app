class AbstractSyntaxTree:
    def __init__(self, path):
        self.path = path
        self.dicItems = {}
        self.parse()
        

    def parse(self):
        with open(self.path, "r") as file:
            for idx, line in enumerate(file):
                if line == '\n':
                    continue
                else:
                    self.dicItems[idx + 1] = line
        print(self.dicItems)
