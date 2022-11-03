from typing import Tuple


class Stack (object):

    def __init__(self):

        self._p = []

    def getStack(self):

        return self._p

    def __getitem__(self,i):

        if i >= len(self):
            print("Posicio incorecte")

        else:
            return self.getStack()[i]

    def __delitem__(self,i):

        del self.getStack()[i]

    def push(self,e):

        self.getStack().append(e)


    def pop(self,Prioritat=3):

        if not(len(self)):
            print("Cua buida")

        else:
            for i in range(len(self)):
                if self.getStack()[i]["prioritat"] == Prioritat:
                    data = self.getStack()[i]
                    del self.getStack()[i]
                    return data
        
                self.pop(Prioritat-1)

    def top(self):
        return self._p[-1]

    def __len__(self):
        return len(self.getStack())

    def __iter__(self):
        return iter(self.getStack())

    def isEmpty(self):
        return not(len(self))

