MAX_INT = 2**31
MIN_INT = -2**31-1


class MiniDecafError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)


class MyMiniDecafError(MiniDecafError):
    def __init__(self, msg:str):
        self.msg = msg

    def __str__(self):
        return self.msg


class MiniDecafTypeError(MyMiniDecafError):
    pass


class MyVariable:
    variableSet = {}

    def __init__(self, identifier:str, offset:int , size:int = 4):
        if identifier in MyVariable.variableSet:
            MyVariable.variableSet[identifier] += 1
        else:
            MyVariable.variableSet[identifier] = 0
        self.id = MyVariable.variableSet[identifier]
        self.identifier = identifier
        self.offset = offset
        self.size = size

    def __eq__(self, item):
        if self.id == item.id and self.identifier == item.identifier and self.offset == item.offset and self.size == item.size:
            return True
        else:
            return False

    def __str__(self):
        return f"{self.identifier}({self.id})"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.identifier, self.id, self.offset,self.size))


# class ParameterList:
#     def __init__(self, variable:[MyVariable]):
#         self.variable = variable
#         self.parameterNumber = len(variable)
#
#     def __str__(self):
#         return f"{self.parameterNumber}"
#
#     def compatible(self, other):
#         return self.parameterNumber == other.parameterNumber


class GlobalInformation:
    def __init__(self, variable:MyVariable, size:int, init=None):
        self.variable = variable
        self.size = size
        self.init = init # not a byte array -- that requires endian info

    def __str__(self):
        return f"{self.variable}, size={self.size}, {self.initStr()}"

    def initStr(self):
        if self.init is None:
            return "uninitialized"
        else:
            return f"initializer={self.init}"

    # def compatible(self, other):
    #     return True


class LabelManager:
    def __init__(self):
        self.labels = {}
        self.enterSet = []
        self.exitSet = []

    def newLabel(self,var = "_L"):
        if var not in self.labels:
            self.labels[var] = 1
        else:
            self.labels[var] += 1
        return f"{var}_{self.labels[var]}"

    def enterLoop(self,enter,exit):
        self.enterSet.append(enter)
        self.exitSet.append(exit)

    def exitLoop(self):
        self.exitSet.pop()
        self.enterSet.pop()

    def MyBreak(self):
        if len(self.exitSet) == 0:
            raise MyMiniDecafError("Error")
        return self.exitSet[-1]

    def MyContinue(self):
        if len(self.exitSet) == 0:
            raise MyMiniDecafError("Error")
        return self.enterSet[-1]


class OffsetManager:
    def __init__(self):
        self.offset = {}
        self.top = 0

    def __getitem__(self, item):
        return self.offset[item]

    def newVar(self,var = None):
        self.top -= 4
        if var is not None:
            self.offset[var]  = self.top
        return self.top


def flatten(myList):
    result = []
    for i in myList:
        if type(i) is list:
            result += flatten(i)
        else:
            result += [i]
    return result


def safeEval(s:str):
    from ast import literal_eval
    return literal_eval(s)


def test(x):
    if type(x) is str:
        return x
    if x is not None:
        return str(x.getText())


def inList(f, l):
    for i, v in enumerate(l):
        if f(v):
            return i, v
    return None


unary = ['-', '~', '!','&','*']
unaryMap = {'-':'neg','~':'not','!':'lnot', '&': 'addrof', '*': 'deref'}
unaryAsmMap = {'-': "neg", '!': "seqz", '~': "not"}
unaryNew = ['-', '~', '!']


binary = ['+','-','*','/','%','==','!=','<=','>=','<','>','&&','||']
binaryMap = {'+':'add','-':'sub','*':'mul','/':'div','%':'rem','==':'eq','!=':'ne','<=':'le','>=':'ge','<':'lt','>':'gt','&&':'land','||':'lor'}

binaryMap1 = { "+": "add", "-": "sub", "*": "mul", "/": "div", "%": "rem" }
binaryMap2 = { "==": "seqz", "!=": "snez" }
binaryMap3 = { "<": "slt", ">": "sgt" }

branch = ["br", "beqz", "bnez", "beq", "bne"]
branchMap = { "br": (2, "beq"), "beqz": (1, "beq"), "bnez": (1, "bne") }