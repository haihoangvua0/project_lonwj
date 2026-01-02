def format_complex_output(s: str) -> str:
    import re
    # 1j, -1j, +1j -> i, -i, +i
    s = re.sub(r'(?<![\w.])1j\b', 'i', s)
    s = re.sub(r'(?<![\w.])\-1j\b', '-i', s)
    s = re.sub(r'(?<![\w.])\+1j\b', '+i', s)

    # còn lại: 2j, 3.5j, (a+b)j → 2i, 3.5i, (a+b)i
    s = re.sub(r'j\b', 'i', s)
    return s
print(format_complex_output("20+3j"))
