class Node():
    def __init__(self , num = 0 , cx = 0.0 , cy = 0.0):
        self.num = num
        self.cx = cx
        self.cy = cy
    def get_num(self):
        return self.num
    def get_x(self):
        return self.cx
    def get_y(self):
        return self.cy