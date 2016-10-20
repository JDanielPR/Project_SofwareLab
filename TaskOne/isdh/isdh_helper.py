class IsdhHelper:
    def __init__(self):
        self.i_s = []
        self.d_h = []
        self.ood = dict()

    def save_ood(self):
        self.d_h.append(self.ood)
    
        
