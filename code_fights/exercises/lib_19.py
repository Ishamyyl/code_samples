from collections import deque


class mystack(deque):

    def add_item(self, *ns):
        for i in ns:
            self.append(i)
        
    def pop_item(self):
        try:
            return self.pop()
        except IndexError as ie:
            pass
    
    def count_items(self):
        return len(self)

mystack = mystack()  # (?) the tests never instantiate the object so here we are
