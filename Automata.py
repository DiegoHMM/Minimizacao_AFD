class Automata(object):
    def __init__(self, states, edges, symbols):
        self.states = states
        self.edges = edges
        self.symbols = symbols


    def print_automata(self):
        print("SYMBOLS: ")
        for symbol in self.symbols:
            print(symbol)
        print("STATES: ")
        for state in self.states:
            state.print_state()
        print("EDGES: ")
        for edge in self.edges:
            edge.print_edge()
        

    def get_state_by_name(self,name):
        for state in self.states:
            if state.name == name:
                return state



    def get_destiny(self, origin_state, symbol):
        for edge in self.edges:
            if edge.origin.name == origin_state.name and edge.symbol == symbol:
                return edge.destiny