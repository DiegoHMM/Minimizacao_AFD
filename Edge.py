class Edge(object):
    def __init__(self, origin, destiny, symbol):
        self.origin = origin
        self.destiny = destiny
        self.symbol = symbol

    def print_edge(self):
        print("\t" + self.origin.name + "\t ->"+ self.symbol  + "\t" + self.destiny.name)
    