class PairRowCol:
    def __init__(self,row,col):
        self.ROW = row
        self.COL = col

    def __eq__(self, other):
        if not isinstance(other,PairRowCol): return False
        return self.ROW == other.ROW and self.COL == other.COL

    def __hash__(self):
        return hash((self.ROW,self.COL))

