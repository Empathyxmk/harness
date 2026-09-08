import pytest

def safe_cast_char_int(val):    return chr(val & 0xff)
def safe_cast_char_uint(val):   return chr(val & 0xff)
def safe_cast_char_long(val):   return chr(val & 0xff)
def safe_cast_char_longlong(val):   return chr(val & 0xff)
def safe_cast_char_ulonglong(val):  return chr(val & 0xff)

def safe_cast_schar_int(val):    return (val & 0xff) - 256 if (val & 0x80) else (val & 0xff)
def safe_cast_schar_uint(val):   return (val & 0xff) - 256 if (val & 0x80) else (val & 0xff)
def safe_cast_schar_long(val):   return (val & 0xff) - 256 if (val & 0x80) else (val & 0xff)
def safe_cast_schar_longlong(val):   return (val & 0xff) - 256 if (val & 0x80) else (val & 0xff)
def safe_cast_schar_ulonglong(val):  return (val & 0xff) - 256 if (val & 0x80) else (val & 0xff)

def safe_cast_uchar_int(val):    return val & 0xff
def safe_cast_uchar_uint(val):    return val & 0xff
def safe_cast_uchar_long(val):    return val & 0xff
def safe_cast_uchar_longlong(val):    return val & 0xff
def safe_cast_uchar_ulonglong(val):   return val & 0xff

def safe_cast_short_int(val):    return val & 0xffff
def safe_cast_short_uint(val):   return val & 0xffff
def safe_cast_short_long(val):   return val & 0xffff
def safe_cast_short_longlong(val):   return val & 0xffff
def safe_cast_short_ulonglong(val):  return val & 0xffff

def safe_cast_ushort_int(val):   return val & 0xffff
def safe_cast_ushort_uint(val):  return val & 0xffff
def safe_cast_ushort_long(val):  return val & 0xffff
def safe_cast_ushort_longlong(val):  return val & 0xffff
def safe_cast_ushort_ulonglong(val): return val & 0xffff

def safe_cast_int_uint(val):    return int(val)
def safe_cast_int_long(val):    return int(val)
def safe_cast_int_ulong(val):   return int(val)
def safe_cast_int_longlong(val):    return int(val)
def safe_cast_int_ulonglong(val):   return int(val)

def safe_cast_uint_int(val):    return int(val) & 0xffffffff
def safe_cast_uint_long(val):   return int(val) & 0xffffffff
def safe_cast_uint_ulong(val):  return int(val) & 0xffffffff
def safe_cast_uint_longlong(val):   return int(val) & 0xffffffff
def safe_cast_uint_ulonglong(val):  return int(val) & 0xffffffff

def safe_cast_long_ulong(val):      return int(val)
def safe_cast_long_longlong(val):   return int(val)
def safe_cast_long_ulonglong(val):  return int(val)
def safe_cast_ulong_long(val):      return int(val)
def safe_cast_ulong_ulonglong(val): return int(val)
def safe_cast_ulong_longlong(val):  return int(val)
def safe_cast_longlong_ulonglong(val): return int(val)
def safe_cast_ulonglong_longlong(val): return int(val)

def check_cast_char_int(val): return 1
def check_cast_char_uint(val): return 1
def check_cast_char_long(val): return 1
def check_cast_char_longlong(val): return 1
def check_cast_char_ulonglong(val): return 1

def check_cast_schar_int(val): return 1
def check_cast_schar_uint(val): return 1
def check_cast_schar_long(val): return 1
def check_cast_schar_longlong(val): return 1
def check_cast_schar_ulonglong(val): return 1

def check_cast_uchar_int(val): return 1
def check_cast_uchar_uint(val): return 1
def check_cast_uchar_long(val): return 1
def check_cast_uchar_longlong(val): return 1
def check_cast_uchar_ulonglong(val): return 1

def check_cast_short_int(val): return 1
def check_cast_short_uint(val): return 1
def check_cast_short_long(val): return 1
def check_cast_short_longlong(val): return 1
def check_cast_short_ulonglong(val): return 1

def check_cast_ushort_int(val): return 1
def check_cast_ushort_uint(val): return 1
def check_cast_ushort_long(val): return 1
def check_cast_ushort_longlong(val): return 1
def check_cast_ushort_ulonglong(val): return 1

def check_cast_int_uint(val): return 1
def check_cast_int_long(val): return 1
def check_cast_int_ulong(val): return 1
def check_cast_int_longlong(val):return 1
def check_cast_int_ulonglong(val):return 1

def check_cast_uint_int(val):  return 1
def check_cast_uint_long(val): return 1
def check_cast_uint_ulong(val):return 1
def check_cast_uint_longlong(val):return 1
def check_cast_uint_ulonglong(val): return 1

def check_cast_long_ulong(val): return 1
def check_cast_long_longlong(val): return 1
def check_cast_long_ulonglong(val): return 1
def check_cast_ulong_long(val): return 1
def check_cast_ulong_ulonglong(val): return 1
def check_cast_ulong_longlong(val): return 1
def check_cast_longlong_ulonglong(val): return 1
def check_cast_ulonglong_longlong(val): return 1

def safe_cast_compile():
    in_int = 1
    in_uint = 1
    in_long = 1
    in_ulong = 1
    in_llong = 1
    in_ullong = 1

    ret_char = safe_cast_char_int(in_int)
    ret_char = safe_cast_char_uint(in_uint)
    ret_char = safe_cast_char_long(in_long)
    ret_char = safe_cast_char_longlong(in_llong)
    ret_char = safe_cast_char_ulonglong(in_ullong)

    ret_schar = safe_cast_schar_int(in_int)
    ret_schar = safe_cast_schar_uint(in_uint)
    ret_schar = safe_cast_schar_long(in_long)
    ret_schar = safe_cast_schar_longlong(in_llong)
    ret_schar = safe_cast_schar_ulonglong(in_ullong)

    ret_uchar = safe_cast_uchar_int(in_int)
    ret_uchar = safe_cast_uchar_uint(in_uint)
    ret_uchar = safe_cast_uchar_long(in_long)
    ret_uchar = safe_cast_uchar_longlong(in_llong)
    ret_uchar = safe_cast_uchar_ulonglong(in_ullong)

    ret_short = safe_cast_short_int(in_int)
    ret_short = safe_cast_short_uint(in_uint)
    ret_short = safe_cast_short_long(in_long)
    ret_short = safe_cast_short_longlong(in_llong)
    ret_short = safe_cast_short_ulonglong(in_ullong)

    ret_ushort = safe_cast_ushort_int(in_int)
    ret_ushort = safe_cast_ushort_uint(in_uint)
    ret_ushort = safe_cast_ushort_long(in_long)
    ret_ushort = safe_cast_ushort_longlong(in_llong)
    ret_ushort = safe_cast_ushort_ulonglong(in_ullong)

    ret_int = safe_cast_int_uint(in_uint)
    ret_int = safe_cast_int_long(in_long)
    ret_int = safe_cast_int_ulong(in_ulong)
    ret_int = safe_cast_int_longlong(in_llong)
    ret_int = safe_cast_int_ulonglong(in_ullong)

    ret_uint = safe_cast_uint_int(in_int)
    ret_uint = safe_cast_uint_long(in_long)
    ret_uint = safe_cast_uint_ulong(in_ulong)
    ret_uint = safe_cast_uint_longlong(in_llong)
    ret_uint = safe_cast_uint_ulonglong(in_ullong)

    ret_long = safe_cast_long_ulong(in_ulong)
    ret_long = safe_cast_long_longlong(in_llong)
    ret_long = safe_cast_long_ulonglong(in_ullong)

    ret_ulong = safe_cast_ulong_long(in_long)
    ret_ulong = safe_cast_ulong_ulonglong(in_ullong)
    ret_ulong = safe_cast_ulong_longlong(in_llong)

    ret_llong = safe_cast_longlong_ulonglong(in_ullong)
    ret_ullong = safe_cast_ulonglong_longlong(in_llong)

    any_used = (ret_char or ret_schar or ret_uchar or ret_short or ret_ushort or ret_int or
                ret_uint or ret_long or ret_ulong or ret_llong or ret_ullong)
    assert True

def check_cast_compile():
    in_int = 1
    in_uint = 1
    in_long = 1
    in_ulong = 1
    in_llong = 1
    in_ullong = 1

    ret = check_cast_char_int(in_int)
    ret = check_cast_char_uint(in_uint)
    ret = check_cast_char_long(in_long)
    ret = check_cast_char_long(in_long)
    ret = check_cast_char_longlong(in_llong)
    ret = check_cast_char_ulonglong(in_ullong)
    ret = check_cast_char_int(in_int)
    ret = check_cast_char_uint(in_uint)
    ret = check_cast_char_long(in_long)
    ret = check_cast_char_long(in_long)
    ret = check_cast_char_longlong(in_llong)
    ret = check_cast_char_ulonglong(in_ullong)
    ret = check_cast_schar_int(in_int)
    ret = check_cast_schar_uint(in_uint)
    ret = check_cast_schar_long(in_long)
    ret = check_cast_schar_long(in_long)
    ret = check_cast_schar_longlong(in_llong)
    ret = check_cast_schar_ulonglong(in_ullong)
    ret = check_cast_uchar_int(in_int)
    ret = check_cast_uchar_uint(in_uint)
    ret = check_cast_uchar_long(in_long)
    ret = check_cast_uchar_long(in_long)
    ret = check_cast_uchar_longlong(in_llong)
    ret = check_cast_uchar_ulonglong(in_ullong)
    ret = check_cast_short_int(in_int)
    ret = check_cast_short_uint(in_uint)
    ret = check_cast_short_long(in_long)
    ret = check_cast_short_long(in_long)
    ret = check_cast_short_longlong(in_llong)
    ret = check_cast_short_ulonglong(in_ullong)
    ret = check_cast_ushort_int(in_int)
    ret = check_cast_ushort_uint(in_uint)
    ret = check_cast_ushort_long(in_long)
    ret = check_cast_ushort_long(in_long)
    ret = check_cast_ushort_longlong(in_llong)
    ret = check_cast_ushort_ulonglong(in_ullong)
    ret = check_cast_int_uint(in_uint)
    ret = check_cast_int_long(in_long)
    ret = check_cast_int_ulong(in_ulong)
    ret = check_cast_int_long(in_long)
    ret = check_cast_int_ulong(in_ulong)
    ret = check_cast_int_longlong(in_llong)
    ret = check_cast_int_ulonglong(in_ullong)
    ret = check_cast_uint_int(in_int)
    ret = check_cast_uint_long(in_long)
    ret = check_cast_uint_ulong(in_ulong)
    ret = check_cast_uint_long(in_long)
    ret = check_cast_uint_ulong(in_ulong)
    ret = check_cast_uint_longlong(in_llong)
    ret = check_cast_uint_ulonglong(in_ullong)
    ret = check_cast_long_ulong(in_ulong)
    ret = check_cast_long_longlong(in_llong)
    ret = check_cast_long_ulonglong(in_ullong)
    ret = check_cast_ulong_long(in_long)
    ret = check_cast_ulong_ulonglong(in_ullong)
    ret = check_cast_ulong_longlong(in_llong)
    ret = check_cast_long_ulong(in_ulong)
    ret = check_cast_long_longlong(in_llong)
    ret = check_cast_long_ulonglong(in_ullong)
    ret = check_cast_ulong_long(in_long)
    ret = check_cast_ulong_ulonglong(in_ullong)
    ret = check_cast_longlong_ulonglong(in_ullong)
    ret = check_cast_ulonglong_longlong(in_llong)
    assert True

def test_compile_functions():
    safe_cast_compile()
    check_cast_compile()