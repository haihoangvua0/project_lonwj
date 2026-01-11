"""class Gồm có:
- Định thức -> Vuông
- Chuyển vị -> Vuông
- Đơn vị -> Vuông
- Nhân (có hướng, vô hướng)
- Cộng, trừ
- Bình, lập phương -> Vuông
Các hàm gồm:
- Det -> Định thức
- Trn -> Chuyển vị
- Inv -> Đảo.
"""
from process_front_end import *
from fractions import Fraction as frac

class MatrixError(Exception):
        """
        Lỗi tổng quát liên quan tới ma trận
        """
        pass
class MatrixShapeError(MatrixError):
        """
        Lỗi do kích thước / shape ma trận không hợp lệ \n
        Ví dụ:
        - Nhân hai ma trận khác kích thước
        - Cộng / trừ ma trận khác shape
        """
        pass
class MatrixPowerError(MatrixError):
        """
        Lỗi liên quan tới phép lũy thừa ma trận\n
        Ví dụ:
        - Ma trận ^ ma trận
        - Ma trận ^ số không nguyên
        - Ma trận không vuông mà đòi mũ
        """
        pass
class Matrix:
        def __init__(self, data: list):
                self.data = data
                # Check valid:
                if len(self.data) == 1:
                        pass
                elif not all(len(self.data[i]) == len(self.data[i+1]) for i in range(len(self.data)-1)):
                        raise MatrixShapeError("The matrix get error with its built-in size")
                if any(not isinstance(i, list) for i in self.data):
                        raise MatrixError("Matrix got ")
                self.m = len(self.data)
                self.n = len(self.data[0])
        def Id(self, size):
                res = [[0 for _ in range(size)] for _ in range(size)]
                for i in range(size):
                        res[i][i] = 1
                return Matrix(res)
        def det(self):
                if self.m != self.n:
                        raise MatrixShapeError("Determinant only defined for square matrices")
        
                n = self.m
                a = [row[:] for row in self.data]
        
                # 1x1
                if n == 1:
                        return returning(a[0][0], "S")
        
                # 2x2
                if n == 2:
                        return returning(a[0][0]*a[1][1] - a[0][1]*a[1][0], "S")
        
                # 3x3
                if n == 3:
                        return returning(
                                a[0][0]*(a[1][1]*a[2][2] - a[1][2]*a[2][1])
                              - a[0][1]*(a[1][0]*a[2][2] - a[1][2]*a[2][0])
                              + a[0][2]*(a[1][0]*a[2][1] - a[1][1]*a[2][0])
                        , "S")
        
                # 4x4 — Laplace theo hàng 0
                if n == 4:
                        res = 0
                        for j in range(4):
                                sign = (-1) ** j
                                minor = self._minor(0, j)
                                res += sign * a[0][j] * minor.det()
                        return returning(res, "S")
        
                raise MatrixError("Only support 1 <= (int) n <= 4")
        def _minor(self, row, col):
                data = [
                        [returning(self.data[i][j], "S") for j in range(self.n) if j != col]
                        for i in range(self.m) if i != row
                ]
                return Matrix(data)
        def adjugate(self):
                n = self.m
                cof = [[0]*n for _ in range(n)]
                
                for i in range(n):
                        for j in range(n):
                                minor = self._minor(i, j)
                                cof[i][j] = returning(((-1)**(i+j)) * minor.det(), "S")

                # transpose
                adj = [[returning(cof[j][i], "S") for j in range(n)] for i in range(n)]
                return Matrix(adj)
        def inverse(self):
                if self.m != self.n:
                        raise MatrixPowerError("Inverse only exists for square matrices")
                
                d = self.det()
                if d == 0:
                        raise MatrixPowerError("Matrix is singular (det = 0)")
            
                adj = self.adjugate()
                res = [[returning(adj.data[i][j] / d, "S") \
                        for j in range(self.n)] \
                        for i in range(self.m)]
                return Matrix(res)
        def transpose(self):
                """
                Ma trận chuyển vị (Trn)
                """
                new_data = [[0 for _ in range(self.m)] for _ in range(self.n)]
        
                for i in range(self.m):
                        for j in range(self.n):
                                new_data[j][i] = self.data[i][j]
                return Matrix(new_data)
        def __len__(self):
                return (len(t := self.data), len(t[0]))
        def __getitem__(self, idx):
                if not isinstance(idx, (int)): raise MatrixError("Index must be int.")
                if not self.data or not self.data[0]:
                        raise MatrixError("Matrix is empty")
                if isinstance(idx, tuple):
                        i, j = idx
                        if i < 0 or i >= self.m or j < 0 or j >= self.n:
                                raise IndexError("Matrix index out of range")
                        return self.data[i][j]
                if idx < 0 or idx >= self.m:
                        raise IndexError("Matrix row index out of range")
                return self.data[idx]
        def __add__(self, other):
                if not isinstance(other, Matrix): raise MatrixError("Cannot plus Matrix with number")
                if not self.m == other.m or not self.n == other.n:
                        raise MatrixShapeError("Cannot plus 2 matrix as they are not in the same size")
                new_mat = [[0 for _ in range(self.n)] for _ in range(self.m)]
                for i in range(self.m):
                        for j in range(self.n):
                                new_mat[i][j] = self.data[i][j] + other.data[i][j]
                return Matrix(new_mat)
        def __sub__(self, other):
                if not isinstance(other, Matrix): raise MatrixError("Cannot subtract Matrix with number")
                if not self.m == other.m or not self.n == other.n:
                        raise MatrixShapeError("Cannot subtract 2 matrix as they are not in the same size")
                new_mat = [[0 for _ in range(self.n)] for _ in range(self.m)]
                for i in range(self.m):
                        for j in range(self.n):
                                new_mat[i][j] = self.data[i][j] + other.data[i][j]
                return Matrix(new_mat)
        def __eq__(self, other):
                if not isinstance(other, Matrix):
                        raise MatrixError("Comparison must be at same type")
                if not (self.__len__() == other.__len__()):
                        return False
                return all(self.data[i][j] == other.data[i][j] \
                            for i in range(self.m) \
                            for j in range(self.n))
        def __mul__(self, other):
                if isinstance(other, Matrix):
                        if not self.n == other.m:
                                raise MatrixShapeError("Cannot multiply two other matrix incorrectly.")
                        # create new matrix for result.
                        res = [[0 for _ in range(other.n)] for _ in range(self.m)]
                        muls = 0
                        for i in range(self.m):
                                for j in range(other.n):
                                        muls = 0
                                        for k in range(self.n):
                                                muls += self.data[i][k] * other.data[k][j]
                                        res[i][j] = muls
                        return Matrix(res)
                elif isinstance(other, (int, float, frac)):
                        new = [[0 for _ in range(self.n)] for _ in range(self.m)]
                        for i in range(self.m):
                                for j in range(self.n):
                                        new[i][j] = self.data[i][j] * other
                        return Matrix(new)
        def __pow__(self, other):
                if other == 1: return self
                if not self.m == self.n:
                        raise MatrixPowerError("Expected row = column")
                if isinstance(other, Matrix):
                        raise MatrixPowerError("Cannot make matrix A powered to matrix B")
                elif isinstance(other, (float, frac, complex)):
                       raise MatrixPowerError("Cannot power up to a(n) float number.")
                elif isinstance(other, int):
                        if other >= 4:  raise MatrixPowerError("The exponent is too high")
                        elif other == -1: return self.inverse()
                        elif other == 0: return self.Id(self.m)
                        elif other == 2: return self * self
                        elif other == 3: return self * self * self
                else: 
                        raise MatrixPowerError(f"Cannot make matrix A powered to {type(other)}")
        def __repr__(self):
                return f"Matrix({self.data})"
        def __str__(self):
                lines = []
                for row in self.data:
                        line =  "\t".join(f"{(x)}" for x in row)
                        lines.append(line)
                return "\n".join(lines)

Det = Matrix.det
Trn = Matrix.transpose
Inv = Matrix.inverse # matA ** -1
if __name__ == "__main__":
        matA = Matrix([[1, 2, 3], [4, 5, 6]])
        matB = Matrix([[11, 15, 20], [25, 30, 35]])
        print(matB - matA)
