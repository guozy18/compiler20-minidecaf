# 代码与产生IR代码的中间阶段，用于对生成的产生树增加一些性质
from ..generator.MiniDecafParser import MiniDecafParser
from ..generator.MiniDecafVisitor import MiniDecafVisitor
from copy import deepcopy
from ..utils import *


class FunctionResolution:
    def __init__(self, isDefine=True):
        self.variable = {}
        self.position = {}
        self.blockSlot = {}
        self.isDefine = isDefine

    def nameBind(self,tmp,variable,position):
        self.variable[tmp] = variable
        self.position[tmp] = position

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        if item in self.variable:
            return self.variable[item]
        else:
            raise MyMiniDecafError(f"{test(item)}  undefined")


class NameResolution:
    def __init__(self):
        self.functionInformation = {}
        # self.parameterListInformation = {}
        self.globalInformation = {}
        self.variable = {}

    def freeze(self):
        for functionName in self.functionInformation.values():
            self.variable.update(functionName.variable)

    def __getitem__(self, ctx):
        return self.variable[ctx]


class NameVisitor(MiniDecafVisitor):
    def __init__(self):
        self.countSlots = []
        self.currentSlot = 0
        self.nameResolution = NameResolution()
        self.currentFunctionResolution = None
        self.variableSet = [{}]
        self.variableDictory = [{}]

    def enterScope(self, ctx):
        self.variableSet.append(deepcopy(self.variableSet[-1]))
        self.variableDictory.append({})
        self.countSlots.append(self.currentSlot)

    def exitScope(self,ctx):
        self.currentFunctionResolution.blockSlot[ctx] = self.currentSlot - self.countSlots[-1]
        self.currentSlot = self.countSlots[-1]
        assert len(self.variableSet)>1
        self.variableSet.pop()
        self.variableDictory.pop()
        self.countSlots.pop()

    def defineVar(self,ctx,key,intNum = 1):
        self.currentSlot += intNum
        tmp = test(key)
        self.variableDictory[-1][tmp] = self.variableSet[-1][tmp] = MyVariable(tmp,-4*self.currentSlot,4*intNum)
        var = self.variableSet[-1][tmp]
        pos = (ctx.start.line, ctx.start.column)
        self.currentFunctionResolution.nameBind(key,var,pos)

    def numberLimit(self,ctx:MiniDecafParser.DeclContext):
        var = [int(test(i)) for i in ctx.Integer()]
        ans = 1
        for j in var:
            ans *= j
        if ans <= 0:
            raise MyMiniDecafError("array size cannot <=0")
        if ans >= MAX_INT:
            raise MyMiniDecafError("array size is larger than max_length")
        return ans

    def useVar(self,ctx,key):
        var = self.variableSet[-1][test(key)]
        position = (ctx.start.line,ctx.start.column)
        self.currentFunctionResolution.nameBind(key, var, position)

    def visitBlock(self, ctx: MiniDecafParser.BlockContext):
        self.enterScope(ctx)
        self.visitChildren(ctx)
        self.exitScope(ctx)

    def visitDecl(self, ctx: MiniDecafParser.DeclContext):
        if ctx.expr() is not None:
            ctx.expr().accept(self)
        var = test(ctx.Indentifier())
        if var in self.variableDictory[-1]:
            raise MyMiniDecafError("redefinition1")
        self.defineVar(ctx, ctx.Indentifier(),self.numberLimit(ctx))

    def visitForDeclStmt(self, ctx:MiniDecafParser.ForDeclStmtContext):
        self.enterScope(ctx)
        self.visitChildren(ctx)
        self.exitScope(ctx)

    def visitPrimaryIndentifier(self, ctx: MiniDecafParser.PrimaryIndentifierContext):
        var = test(ctx.Indentifier())
        if var not in self.variableSet[-1]:
            raise MyMiniDecafError("Variable undeclared")
        self.useVar(ctx, ctx.Indentifier())

    def visitFuncDef(self, ctx: MiniDecafParser.FuncDefContext):
        func = test(ctx.Indentifier())
        # if func in self.nameResolution.functionInformation and self.nameResolution.functionInformation[func].isDefine:
        #     raise MyMiniDecafError(f"redefinition: {func}")
        functionInformation = FunctionResolution(isDefine=True)
        self.currentFunctionResolution = self.nameResolution.functionInformation[func] = functionInformation
        self.enterScope(ctx.block())
        ctx.parameterList().accept(self)
        self.visitChildren(ctx.block())
        self.exitScope(ctx.block())
        self.currentFunctionResolution = None

    def visitFuncDecl(self, ctx: MiniDecafParser.FuncDeclContext):
        func = test(ctx.Indentifier())
        if func in self.nameResolution.globalInformation:
            raise MyMiniDecafError(f"{func} redeclared function")
        functionName = FunctionResolution(isDefine=True)
        if func not in self.nameResolution.functionInformation:
            self.nameResolution.functionInformation[func] = functionName

    def visitDeclExternalDecl(self, ctx:MiniDecafParser.DeclExternalDeclContext):
        ctx = ctx.decl()
        myInit = None
        if ctx.expr() is None:
            myInit = None
        else:
            try:
                myInit = safeEval(test(ctx.expr()))
            except:
                raise MyMiniDecafError("global initializers error")

        varString = test(ctx.Indentifier())
        if varString in self.nameResolution.functionInformation:
            raise MyMiniDecafError("function redeclared")
        var = MyVariable(varString, None , 4*self.numberLimit(ctx))
        globInfo = GlobalInformation(var, 4*self.numberLimit(ctx) , myInit)

        if varString in self.variableDictory[-1]:
            preGlobal = self.nameResolution.globalInformation[varString]
            if preGlobal.init is not None and globInfo.init is not None:
                raise MyMiniDecafError(f"redefine of {varString}")
            if globInfo.init is not None:
                self.nameResolution.globalInformation[varString].init = myInit
        else:
            self.nameResolution.globalInformation[varString] = globInfo
            self.variableSet[-1][varString] = var
            self.variableDictory[-1][varString] = var

    def visitProg(self, ctx:MiniDecafParser.ProgContext):
        self.visitChildren(ctx)
        self.nameResolution.freeze()
