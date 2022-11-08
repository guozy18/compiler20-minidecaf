# 中间码的存储类
from .irstr import *

# 定义每个临时函数，其中irList存储每个函数自己的ir指令列表
class irFunction:
    def __init__(self , functionName:str, parameterNum:int , irList):
        self.functName = functionName
        self.parameterNum = parameterNum
        self.irList = irList

    def myStr(self,instr):
        if type(instr) is irComment:
            return f"\t\t\t\t{instr}"
        if type(instr) is irLabel:
            return f"{instr}"
        return f"\t{instr}"

    def __str__(self):
        tmp = '\n'.join(map(self.myStr, self.irList))
        return f"{self.functName}({self.parameterNum}):\n{tmp}"


class Global:
    def __init__(self,symbol:str,size:int,init = None,align = 4):
        self.symbol = symbol
        self.size = size
        self.init = init
        self.align = align

    def fromGlobInfo(globalInformation: GlobalInformation):
        assert globalInformation.variable.offset is None
        return Global(globalInformation.variable.identifier, globalInformation.size, globalInformation.init)

    def initStr(self):
        if self.init is None:
            return "uninitialized"
        else:
            return f"initializer={self.init}"


# 定义所有函数的集合，其中irLists存储所有函数
class irStore:
    def __init__(self, irList,irGlobal):
        self.irLists = irList
        self.irGlobals = irGlobal

    def __str__(self):
        return "\n\n".join(map(str, self.irLists))


# 用于最终的IR的列表存储
class irResult:
    def __init__(self):
        self.irList = []
        self.irGlobal = []
        self.irLists = []
        self.functionName = None
        self.parameterNum = None

    # 进入一个新的函数调用
    def enterFunction(self,functionName:str,paramterNum:int):
        self.irList = []
        self.functionName = functionName
        self.parameterNum = paramterNum

    # 离开函数时调用
    def exitFunction(self):
        self.irLists.append(irFunction(self.functionName,self.parameterNum,self.irList))

    def expandList(self, nextIr: [irBaseStr]):
        self.irList += nextIr

    def expandGlobal(self,globalInfomation:GlobalInformation):
        self.irGlobal += [Global.fromGlobInfo(globalInfomation)]

    def __call__(self, nextIr: [irBaseStr]):
        self.expandList(nextIr)

    # 此函数用于得到最终的结果
    def getResult(self):
        return irStore(self.irLists,self.irGlobal)
