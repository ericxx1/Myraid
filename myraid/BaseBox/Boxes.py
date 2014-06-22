from rply.token import BaseBox

class BoxInt(BaseBox):
    def __init__(self, value):
        self.value = value

    def getint(self):
        return self.value
        
class BoxStr(BaseBox):
    def __init__(self, value):
        self.value = value

    def get_str(self):
        return self.value
        

