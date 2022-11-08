from ..utils import *


class Type:
    def __repr__(self):
        return self.__str__()

    def sizeof(self):
        return Exception("abstract type")


class voidType(Type):
    def __init__(self):
        pass

    def __str__(self):
        return "void"

    def __eq__(self, other):
        if isinstance(other, voidType):
            return True
        else:
            return False


class intType(Type):
    def __init__(self):
        pass

    def __eq__(self, other):
        if isinstance(other, intType):
            return True
        else:
            return False

    def sizeof(self):
        return 4

    def __str__(self):
        return "int"


class pointerType(Type):
    def __init__(self, base: Type):
        self.base = base

    def sizeof(self):
        return 4

    def __str__(self):
        return f"{self.base}*"

    def __eq__(self, other):
        if not isinstance(other, pointerType):
            return False
        elif (self.base == other.base):
            return True
        else:
            return False


class arrayType(Type):
    def __init__(self, base, len):
        self.base = base
        self.len = len

    def __str__(self):
        return f"[{self.len}]{self.base}"

    def __eq__(self, other):
        if not isinstance(other, arrayType):
            return False
        return self.base == other.base and self.len == other.len

    def make(base:Type, dimension:list):
        for i in dimension:
            base = arrayType(base, i)
        return base

    def sizeof(self):
        return self.base.sizeof() * self.len


class zeroType(intType, pointerType):
    def __str__(self):
        return "zeroType"

    def __eq__(self, other):
        if (isinstance(other, intType) or isinstance(other, pointerType)):
            return True
        else:
            return False


def typeCheck(ty):
    if type(ty) is str:
        raise MyMiniDecafError(f"{ty}")
    if ty is None:
        raise MyMiniDecafError("Type error")
    return ty


# 函数的参数比较
class FunctionTypeInformation:
    def __init__(self, returnType:Type, parameterType:list):
        self.returnType = returnType
        self.parameterType = parameterType

    def compatible(self, other):
        return self.returnType == other.returnType and self.parameterType == other.parameterType

    def callCheck(self,argmentType:list):
        tmp = None
        if self.parameterType == argmentType:
            tmp = self.returnType
        else:
            tmp = "bad argument types"
        ans = typeCheck(tmp)
        return ans


def condCheck(cond,tr,fal):
    if cond == intType() and tr == fal:
        return tr


def intBinaryCheck(le,ri):
    if le == intType() and ri == intType():
        return intType()
    return "expect integer,but has other"


def intUnaryCheck(ty):
    if ty == intType():
        return intType()
    return "expected integer"


def pointerArithCheck(le,ri):
    if ri == intType() and isinstance(le, pointerType):
        return le
    if le == intType() and isinstance(ri, pointerType):
        return ri
    return "pointer and integer"


def pointerDifferentCheck(le,ri):
    if le == ri and isinstance(ri,pointerType):
        return intType()
    return "the same type"


def stmtCondCheck(ty):
    if ty != intType():
        return f"{ty} found"
    return voidType()


def arrayCheck(arr, index):
    if not isinstance(arr, arrayType) and not isinstance(arr, pointerType):
        return f"array,but {arr} found"
    if index != intType():
        return "index must be an integer"
    return arr.base


def derefCheck(ty):
    if isinstance(ty, pointerType):
        return ty.base
    return f"pointer expected, but {ty}"


def addressCheck(ty):
    if isinstance(ty, arrayType):
        return "cannot take address of array type"
    return pointerType(ty)


def equalCheck(le, ri):
    if le != ri:
        return f"cannot equate or compare {le} to {ri}"
    if le != intType() and not isinstance(le, pointerType):
        return f"expected integer or pointer types, found {le}"
    return intType()


def relationCheck(le, ri):
    if le != intType():
        return f"int expected as relop lhs, found {lhs}"
    if ri != intType():
        return f"int expected as relop rhs, found {rhs}"
    return intType()


def assignCheck(le, ri):
    if le != ri:
        return "cannot assign"
    if isinstance(le, arrayType):
        return "cannot assign to array"
    return le


def returnCheck(returnType, ty):
    if returnType != ty:
        return f"return {returnType} expected, {ty} found"
    return voidType()

