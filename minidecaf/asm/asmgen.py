from .asmstr import *
from .asmoutput import *
from ..ir.irset import *
from ..utils import *

def convert(commands: list):
    return [asmInstruction(command) for command in commands]


def pop(reg):
    return ([f"lw {reg}, 0(sp)"] if reg is not None else []) + [f"addi sp, sp, 4"]


def popAll(*regs):
    return flatten(map(pop,regs))


def push(reg):
    if type(reg) is int:
        return [f"addi sp, sp, -4", f"li t1, {reg}", f"sw t1, 0(sp)"]
    else:
        return [f"addi sp, sp, -4", f"sw {reg}, 0(sp)"]


def pushAll(*regs):
    return flatten(map(push,regs))


def binaryAsmGen(op:str):
    if op in binaryMap1:
        return popAll("t2", "t1") + [f"{binaryMap1[op]} t1, t1, t2"] + push("t1")
    if op in binaryMap2:
        return popAll("t2", "t1") + [f"sub t1, t1, t2", f"{binaryMap2[op]} t1, t1"] + push("t1")
    if op in binaryMap3:
        return popAll("t2", "t1") + [f"{binaryMap3[op]} t1, t1, t2"] + push("t1")
    if op == "||":
        return popAll("t2", "t1") + [f"or t1, t1, t2", f"snez t1, t1"] + push("t1")
    if op == "&&":
        return pop("t2") + unaryAsmGen("!") + push("t2") + unaryAsmGen("!") + binaryAsmGen("||") + unaryAsmGen("!")
    if op == "<=":
        return binaryAsmGen(">") + unaryAsmGen("!")
    if op == ">=":
        return binaryAsmGen("<") + unaryAsmGen("!")

def myRetAsmGen(var:str):
    return [f"beqz x0, {var}_exit"]


def frameSlotAsmGen(offset):
    return pushAll("fp", offset) + binaryAsmGen("+")


def unaryAsmGen(op:str):
    if op in unaryNew:
        return pop("t1") + [f"{unaryAsmMap[op]} t1, t1"] + push("t1")


def branchAsmGen(oper , label:str):
    if oper in branchMap:
        index, oper = branchMap[oper]
        return pushAll(*[0]*index) + branchAsmGen(oper, label)
    return popAll("t2", "t1") + [f"{oper} t1, t2, {label}"]


def labelAsmGen(label:str):
    return [f"{label}:"]


def callAsmGen(function:str,parameterNumber:int):
    return [f"call {function}"] + popAll(*[None]*parameterNumber) + push("a0")


def globalAsmGen(symbol:str):
    return [f"la t1,{symbol}"] + push("t1")


class asmGen:
    def __init__(self, myIr: irStore, out: asmFileout):
        self.myIr = myIr
        self.out = out
        self.ir2asm = {irPush:self.riscvPush,irRet:self.riscvRet,
                       irBinary:self.riscvBinary,irUnary:self.riscvUnary,
                       irPop:self.riscvPop,irLoad:self.riscvLoad,
                       irFrameAddr:self.riscvFrameSlot,irAsmStore:self.riscvStore,
                       irBranch:self.riscvBranch,irLabel:self.riscvLabel,irConst:self.riscvConst,
                       irCall:self.riscvCall,irGlobalSymbol:self.riscvGlobalSymbol}
        self.functionName = None
        self.parameter = None


    def riscvPush(self, instr: irPush):
        returnValue= instr.var
        asmPush = convert(push(returnValue))
        self.out(asmPush)

    def riscvRet(self, instr: irBaseStr):
        asmRet = convert(myRetAsmGen(self.functionName))
        self.out(asmRet)

    def riscvConst(self, instr:irConst):
        self.out(convert(push(instr.var)))

    def riscvBinary(self,instr: irBinary):
        binaryOperation = instr.op
        buffer = binaryAsmGen(binaryOperation)
        asmBinary = convert(buffer)
        self.out(asmBinary)

    def riscvUnary(self,instr: irUnary):
        unaryOperation = instr.op
        buffer = unaryAsmGen(unaryOperation)
        asmUnary = convert(buffer)
        self.out(asmUnary)

    def riscvFrameSlot(self, instr: irFrameAddr):
        buffer = frameSlotAsmGen(instr.offset)
        asmFrameSlot = convert(buffer)
        self.out(asmFrameSlot)

    def riscvLoad(self,instr: irLoad):
        asmLoad = convert(pop("t1") + [f"lw t1, 0(t1)"] + push("t1"))
        self.out(asmLoad)

    def riscvStore(self,instr:irAsmStore):
        asmStore = convert(popAll("t2", "t1") + [f"sw t1, 0(t2)"] + push("t1"))
        self.out(asmStore)

    def riscvPop(self,instr:irPop):
        asmPop = convert(pop(None))
        self.out(asmPop)

    def riscvBranch(self,instr:irBranch):
        buffer = branchAsmGen(instr.oper,instr.label)
        asmBranch = convert(buffer)
        self.out(asmBranch)

    def riscvLabel(self,instr:irLabel):
        buffer = labelAsmGen(instr.label)
        asmLabel = convert(buffer)
        self.out(asmLabel)

    def riscvCall(self,instr:irCall):
        tmp , function = inList(lambda function: function.functName == instr.functionName, self.myIr.irLists)
        buffer = callAsmGen(function.functName,function.parameterNum)
        asmCall = convert(buffer)
        self.out(asmCall)

    def riscvGlobalSymbol(self,instr:irGlobalSymbol):
        buffer = globalAsmGen(instr.symbol)
        asmGlobal = convert(buffer)
        self.out(asmGlobal)

    def prologueGen(self, func:irFunction):
        self.out([
            asmInstruction(".text"), asmInstruction(f".globl {func.functName}"),
            asmLabel(f"{func.functName}:")] +convert(pushAll("ra", "fp")) +
            [ asmInstruction("mv fp, sp")])
        for i in range(func.parameterNum):
            start = 4*(i+2)
            end = -4*(i+1)
            self.out([asmInstruction(f"lw t1, {start}(fp)")] + convert(push("t1")))

    # def out2file(self,outputCommands:[]):
    def epilogueGen(self, func: irFunction):
        self.out( convert(push(0)) +
                 [asmLabel(f"{func.functName}_exit:") , asmInstruction("lw a0, 0(sp)"), asmInstruction("mv sp, fp")] +
                convert(popAll("fp", "ra")) + [ asmInstruction("jr ra")])

    def riscvGen(self):
        for globals in self.myIr.irGlobals:
            if globals.init is None:
                self.out([asmInstruction(f".comm {globals.symbol},{globals.size},{globals.align}")])
            else:
                self.out([asmInstruction(".data"), asmInstruction(f".globl {globals.symbol}"),
                          asmInstruction(f".align {globals.align}"),
                          asmInstruction(f".size {globals.symbol}, {globals.size}"),
                          asmLabel(f"{globals.symbol}:"), asmInstruction(f".quad {globals.init}")])

        for irList in self.myIr.irLists:
            self.functionName = irList.functName
            self.prologueGen(irList)
            for instr in irList.irList:
                self.ir2asm[type(instr)](instr)
            self.epilogueGen(irList)

