class DiByte:
    def __init__(self, content=None):
        self.DiByte = ["" for i in range(16)]
        self.content = content
        self.fill_bit()
        print(self.DiByte)

    def fill_bit(self):
        index = 0
        for bit in self.DiByte:
            if index == 0 or 1 or 2 or 4 or 8:
                break
            self.DiByte[index] = "1" #str(self.content[index])

a = DiByte(content=[1,0,1,1,1,1,0,0,0,0,1,0,0,1,0,1])
