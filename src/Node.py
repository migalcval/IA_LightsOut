class Node:
    def __init__(self, value, father=None, action=None):
        self.value = value
        self.father = (father, action)

    def set_father(self, father, action):
        self.father = (father, action)

    def __eq__(self, other):
        return self.value == other.value
    
    def __hash__(self):
        return hash(self.value)