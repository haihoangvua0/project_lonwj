from process_front_end import *
from fractions import Fraction as frac
"""class Gồm có:
Định thức -> Vuông
Chuyển vị -> Vuông
Đơn vị -> Vuông
Nhân (có hướng, vô hướng)
Cộng, trừ
Bình, lập phương -> Vuông
"""
class MatrixError(Exception):
        """
        Lỗi tổng quát liên quan tới ma trận
        """
        pass
class MatrixShapeError(MatrixError):
        """
        Lỗi do kích thước / shape ma trận không hợp lệ
        Ví dụ:
        - Nhân hai ma trận khác kích thước
        - Cộng / trừ ma trận khác shape
        """
        pass
class MatrixPowerError(MatrixError):
        """
        Lỗi liên quan tới phép lũy thừa ma trận
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
                a = self.data.copy()
        
                # 1x1
                if n == 1:
                        return a[0][0]
        
                # 2x2
                if n == 2:
                        return a[0][0]*a[1][1] - a[0][1]*a[1][0]
        
                # 3x3
                if n == 3:
                        return (
                                a[0][0]*(a[1][1]*a[2][2] - a[1][2]*a[2][1])
                              - a[0][1]*(a[1][0]*a[2][2] - a[1][2]*a[2][0])
                              + a[0][2]*(a[1][0]*a[2][1] - a[1][1]*a[2][0])
                        )
        
                # 4x4 — Laplace theo hàng 0
                if n == 4:
                        res = 0
                        for j in range(4):
                                sign = (-1) ** j
                                minor = self._minor(0, j)
                                res += sign * a[0][j] * minor.det()
                        return res
        
                raise MatrixError("Only support 1 <= (int) n <= 4")
        def inverse(self):
                def adjugate(self):
                        def _minor(self, row, col):
                                data = [
                                        [self.data[i][j] for j in range(self.n) if j != col]
                                        for i in range(self.m) if i != row
                                ]
                                return Matrix(data)
                        n = self.m
                        cof = [[0]*n for _ in range(n)]
                    
                        for i in range(n):
                                for j in range(n):
                                        minor = self._minor(i, j)
                                        cof[i][j] = ((-1)**(i+j)) * minor.det()

                        # transpose
                        adj = [[cof[j][i] for j in range(n)] for i in range(n)]
                        return Matrix(adj)
                if self.m != self.n:
                        raise MatrixPowerError("Inverse only exists for square matrices")
                
                d = self.det()
                if d == 0:
                        raise MatrixPowerError("Matrix is singular (det = 0)")
            
                adj = self.adjugate()
                res = [[adj.data[i][j] / d \
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
                return len(self.data)
        def __add__(self, other):
                if not self.m == other.m or not self.n == other.n:
                        raise MatrixShapeError("Cannot plus 2 matrix as they are not in the same size")
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
                        MatrixPowerError("Cannot power up to a(n) float number.")
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
                        line =  "\t".join(str(x) for x in row)
                        lines.append(line)
                return "\n".join(lines)

Det = Matrix.det
Trn = Matrix.transpose
A = Matrix([[1, 2, 3], [4, 5, 6]])
B = Matrix([[10, 15, 20], [25, 30, 35], [40, 45, 50]])
print(pow(A, 1))