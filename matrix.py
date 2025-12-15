from process_front_end import *
class Matrix:
        def __init__(self, data: list):
                self.data = data
                # Check valid:
                if not all(len(self.data[i]) == len(self.data[i-1]) for i in range(len(self.data))):
                        raise TypeError("The matrix get error with its built-in")
        def __len__(self):
                return len(self.data)
        #def __getitem__(self):
                
        def __eq__(self, other):
                if not isinstance(other, Matrix):
                        raise NotImplemented
                if not (self.__len__() == other.__len__()):
                        return False
                
                return all(self.data[i][j] == other.data[i][j] for i, j in range(len(self.data)))
        def __mul__(self, self1):
                if isinstance(self1, Matrix):
                        pass
                else:
                        pass
