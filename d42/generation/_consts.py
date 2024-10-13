import string

INT_MIN = -(2 ** 63)
INT_MAX = 2 ** 63 - 1
FLOAT_MIN = float(INT_MIN)
FLOAT_MAX = float(INT_MAX)
STR_ALPHABET = string.digits + string.ascii_letters + " -_"
STR_LEN_MIN = 0
STR_LEN_MAX = 32
LIST_LEN_MIN = 0
LIST_LEN_MAX = 16
BYTES_LEN_MIN = 0
BYTES_LEN_MAX = 32
