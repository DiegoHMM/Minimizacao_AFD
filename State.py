class State(object):
    def __init__(self, name, final=False, initial=False ):
        self.name = name
        self.final = final
        self.initial = initial

    def is_initial(self):
        if(self.initial == True):
            return True

    def is_final(self):
        if(self.final == True):
            return True

    def print_state(self):
        if(self.is_initial()):
            print("\n\t Name:" + self.name + "\n\t Type: Initial")
        elif(self.is_final()):
            print("\n\t Name:" + self.name + "\n\t Type: Final")
        else:
            print("\n\t Name:" + self.name)