# 中间码的不同的指令，不同指令分别对应不同的类
from ..utils import *


# 定义各种生成IR所需要的类
class irBaseStr:
    def __repr__(self):
        self.__str__()


# 定义IR中的push
class irPush(irBaseStr):
    def __init__(self, var: int):
        assert MIN_INT < var < MAX_INT
        self.var = var

    def __str__(self):
        return f"push {self.var}"


class irConst(irBaseStr):
    def __init__(self, var:int):
        assert MIN_INT < var < MAX_INT
        self.var = var

    def __str__(self):
        return f"const {self.var}"

# 返回语句指令
class irRet(irBaseStr):
    def __init__(self):
        super()

    def __str__(self):
        return f"ret"


class irUnary(irBaseStr):
    def __init__(self,op:str):
        assert op in unary
        self.op = op

    def __str__(self):
        return unaryMap[self.op]


class irBinary(irBaseStr):
    def __init__(self,op:str):
        assert op in binary
        self.op = op

    def __str__(self):
        return binaryMap[self.op]


class irLoad(irBaseStr):
    def __str__(self):
        return f"load"


class irAsmStore(irBaseStr):
    def __str__(self):
        return f"store"


class irPop(irBaseStr):
    def __str__(self):
        return f"pop"


class irFrameAddr(irBaseStr):
    def __init__(self,offset:int):
        assert offset < 0
        self.offset = offset

    def __str__(self):
        return f"frameslot {self.offset}"


class irComment(irBaseStr):
    def __init__(self,message:str):
        self.message = message

    def __str__(self):
        return f"# {self.message}"


class irBranch(irBaseStr):
    def __init__(self,oper,label:str):
        assert oper in branch
        self.oper = oper
        self.label = label

    def __str__(self):
        return f"{self.oper} {self.label}"


class irLabel(irBaseStr):
    def __init__(self,label:str):
        self.label  = label

    def __str__(self):
        return f"{self.label}"


class irCall(irBaseStr):
    def __init__(self,functionName:str):
        self.functionName = functionName

    def __str__(self):
        return f"call {self.functionName}"


class irGlobalSymbol(irBaseStr):
    def __init__(self,symbol:str):
        self.symbol = symbol

    def __str__(self):
        return f"Global Symbol: {self.symbol}"