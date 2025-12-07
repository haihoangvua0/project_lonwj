import math
def sqrt_simplify(n: float | int) -> tuple[float | int, float | int, int]:
    """
    Phân tích n thành dạng a + b*sqrt(c) với a, b là số thực hoặc nguyên, c là số nguyên dương (ưu tiên nguyên tố).
    Nếu không phân tích được, trả về (0, 1, int(n)) nghĩa là 0 + 1*sqrt(n).
    Chỉ xử lý trường hợp n là số nguyên dương hoặc số thực dương.
    """
    if n < 0:
        return (0, 1, n)
    # Nếu n là số chính phương
    root = math.isqrt(int(n))
    if abs(root * root - n) < 1e-12:
        return (root, 0, 1)
    # Nếu n là số thực, thử tách phần nguyên và phần thập phân
    if isinstance(n, float) and not n.is_integer():
        a = math.floor(n)
        remain = n - a
        if remain > 1e-12:
            # Không cố tách phần thập phân thành căn, chỉ trả về dạng b*sqrt(c)
            n = remain
            a = int(a)
        else:
            n = int(n)
            a = 0
    else:
        a = 0
        n = int(n)
    # Phân tích n thành b^2 * c với c là số nguyên tố nếu có thể
    b = 1
    c = int(n)
    i = 2
    while i * i <= c:
        count = 0
        while c % (i * i) == 0:
            c //= i * i
            b *= i
            count += 1
        i += 1
    return (a, b, c)

print(sqrt_simplify(6.5 + 2*math.sqrt(3))) # -> (6.5, 1, 2, 3)
print(sqrt_simplify((2.3)*math.sqrt(2))) # -> (0, 0, 2.3, 2)
print(sqrt_simplify(math.sqrt(97))) # -> (0, 0, 0, 97)
print(sqrt_simplify(120*math.sqrt(2))) # -> (0, 0, 0, ~169.7056275)
print(sqrt_simplify())
