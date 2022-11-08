from ..generator.MiniDecafParser import MiniDecafParser
from ..generator.MiniDecafVisitor import MiniDecafVisitor
from ..utils import *
from .alltype import *
from .nameresolution import *
from .irstr import *


# 种类信息的类
class TypeAnalysis:
    def __init__(self):
        self.functionType = {}
        self.type = {}
        self.location = {}

    def setLValue(self, ctx, location):
        self.location[ctx] = location

    def lvalueLocation(self,ctx):
        return self.location[ctx]

    def __getitem__(self, item):
        return self.type[item]


class Locator(MiniDecafVisitor):
    def __init__(self, nameResolution:NameResolution, typeAnalysis:TypeAnalysis):
        self.nameResolution = nameResolution
        self.typeAnalysis = typeAnalysis

    def locate(self, function:str, ctx):
        self.function = function
        res = ctx.accept(self)
        self.function = None
        return res

    def visitPrimaryIndentifier(self, ctx:MiniDecafParser.PrimaryIndentifierContext):
        var = self.nameResolution[ctx.Indentifier()]
        if var.offset is None:
            return [irGlobalSymbol(var.identifier)]
        else:
            return [irFrameAddr(var.offset)]

    def visitCUnary(self, ctx:MiniDecafParser.CUnaryContext):
        op = test(ctx.unaryList())
        if op == '*':
            return [ctx.cast()]

    def visitPostfixArray(self, ctx:MiniDecafParser.PostfixArrayContext):
        tmp = self.typeAnalysis[ctx.postfix()].base.sizeof()
        return [ctx.postfix(), ctx.expr(), irConst(tmp), irBinary('*'), irBinary('+')]

    def visitPrimaryParen(self, ctx:MiniDecafParser.PrimaryParenContext):
        return ctx.expr().accept(self)


class Typer(MiniDecafVisitor):
    def __init__(self,nameResolution):
        self.variableType = {}
        self.nameResolution = nameResolution
        self.typeAnalysis = TypeAnalysis()
        self.locator = Locator(self.nameResolution, self.typeAnalysis)
        self.currentFunction = None
        self.binaryMap = {'*':intBinaryCheck,'/':intBinaryCheck,'%':intBinaryCheck,'&&':intBinaryCheck,'||':intBinaryCheck,
                          '==':equalCheck,'!=':equalCheck,'<':relationCheck,'<=':relationCheck,
                          '>':relationCheck,'>=':relationCheck,'=':assignCheck,
                          '+':[intBinaryCheck,pointerArithCheck],'-':[intBinaryCheck,pointerArithCheck,pointerDifferentCheck]}

    def visitChildren(self, node):
        ty = MiniDecafVisitor.visitChildren(self,node)
        self.typeAnalysis.type[node] = ty
        return ty

    def visitPtrType(self, ctx:MiniDecafParser.PtrTypeContext):
        return pointerType(ctx.ty().accept(self))

    def visitIntType(self, ctx:MiniDecafParser.IntTypeContext):
        return intType()

    def locate(self, ctx):
        loc = self.locator.locate(self.currentFunction, ctx)
        if loc is None:
            raise MyMiniDecafError("lvalue expected")
        self.typeAnalysis.setLValue(ctx,loc)

    def visitCCast(self, ctx:MiniDecafParser.CCastContext):
        ctx.cast().accept(self)
        ty = ctx.ty().accept(self)
        self.typeAnalysis.type[ctx] = ty
        return ty

    # 自己定义实现unary和locate
    def visitCUnary(self, ctx:MiniDecafParser.CUnaryContext):
        myMap = {'-':intUnaryCheck,'!':intUnaryCheck,'~':intUnaryCheck,'&':addressCheck,'*':derefCheck}
        tmp = myMap[test(ctx.unaryList())](ctx.cast().accept(self))
        ty = typeCheck(tmp)
        if test(ctx.unaryList()) == '&':
            self.locate(ctx.cast())
        self.typeAnalysis.type[ctx] = ty
        return ty

    def visitPrimaryParen(self, ctx:MiniDecafParser.PrimaryParenContext):
        ty = ctx.expr().accept(self)
        self.typeAnalysis.type[ctx] = ty
        return ty

    # 自定义实现checkBinary函数
    def visitCAdd(self, ctx:MiniDecafParser.CAddContext):
        binaryList = self.binaryMap[test(ctx.addList())]
        errs = []
        for f in binaryList:
            try:
                tmp = f(ctx.additive().accept(self), ctx.multiplicative().accept(self))
                typeCheck(tmp)
            except MyMiniDecafError as e:
                errs += [e.msg]
            else:
                tmp = f(ctx.additive().accept(self), ctx.multiplicative().accept(self))
                ty = typeCheck(tmp)
                self.typeAnalysis.type[ctx] = ty
                return ty
        err_message = '\n\t'.join(map(str, errs))
        typeCheck(err_message)

    def visitCMul(self, ctx: MiniDecafParser.CMulContext):
        tmp = self.binaryMap[test(ctx.mulList())](ctx.multiplicative().accept(self),ctx.cast().accept(self))
        ty = typeCheck(tmp)
        self.typeAnalysis.type[ctx] = ty
        return ty

    def visitCRel(self, ctx: MiniDecafParser.CRelContext):
        tmp = self.binaryMap[test(ctx.relationList())](ctx.relational().accept(self), ctx.additive().accept(self))
        ty = typeCheck(tmp)
        self.typeAnalysis.type[ctx] = ty
        return ty

    def visitCEq(self, ctx: MiniDecafParser.CEqContext):
        tmp = self.binaryMap[test(ctx.equalList())](ctx.equality().accept(self), ctx.relational().accept(self))
        ty = typeCheck(tmp)
        self.typeAnalysis.type[ctx] = ty
        return ty

    def visitCLand(self, ctx: MiniDecafParser.CLandContext):
        tmp = self.binaryMap["&&"](ctx.logical_and().accept(self), ctx.equality().accept(self))
        ty = typeCheck(tmp)
        self.typeAnalysis.type[ctx] = ty
        return ty

    def visitCLor(self, ctx: MiniDecafParser.CLorContext):
        tmp = self.binaryMap["||"](ctx.logical_or().accept(self), ctx.logical_and().accept(self))
        ty = typeCheck(tmp)
        self.typeAnalysis.type[ctx] = ty
        return ty

    def visitCCond(self, ctx: MiniDecafParser.CCondContext):
        tmp = condCheck(ctx.logical_or().accept(self),ctx.expr().accept(self), ctx.cond().accept(self))
        ty = typeCheck(tmp)
        self.typeAnalysis.type[ctx] = ty
        return ty

    def visitCAssign(self, ctx: MiniDecafParser.CAssignContext):
        tmp = self.binaryMap[test(ctx.assignList())](ctx.unary().accept(self), ctx.asgn().accept(self))
        ty = typeCheck(tmp)
        self.locate(ctx.unary())
        self.typeAnalysis.type[ctx] = ty
        return ty

    def argType(self, ctx:MiniDecafParser.ArgmentListContext):
        return list(map(lambda x: x.accept(self), ctx.expr()))

    def visitPostfixCall(self, ctx: MiniDecafParser.PostfixCallContext):
        argType = self.argType(ctx.argmentList())
        func = test(ctx.Indentifier())
        ty = self.typeAnalysis.functionType[func].callCheck(argType)
        self.typeAnalysis.type[ctx] = ty
        return ty

    def visitPostfixArray(self, ctx: MiniDecafParser.PostfixArrayContext):
        tmp = arrayCheck(ctx.postfix().accept(self),ctx.expr().accept(self))
        ty = typeCheck(tmp)
        self.typeAnalysis.type[ctx] = ty
        return ty

    def visitPrimaryInteger(self, ctx: MiniDecafParser.PrimaryIntegerContext):
        if safeEval(test(ctx)) == 0:
            ty = zeroType()
            self.typeAnalysis.type[ctx] = ty
            return ty
        else:
            ty = intType()
            self.typeAnalysis.type[ctx] = ty
            return ty

    def var(self,item):
        return self.nameResolution[item]

    def declType(self, ctx:MiniDecafParser.DeclContext):
        base = ctx.ty().accept(self)
        dims = [int(test(x)) for x in reversed(ctx.Integer())]
        if len(dims) == 0:
            return base
        else:
            return arrayType.make(base, dims)

    def paramTy(self, ctx:MiniDecafParser.ParameterListContext):
        ans = []
        for myDecl in ctx.decl():
            if myDecl.expr() is not None:
                raise MyMiniDecafError("parameter cannot initializers")
            parameterType = self.declType(myDecl)
            if isinstance(parameterType, arrayType):
                raise MyMiniDecafError("parameter cannot array types")
            ans += [parameterType]
        return ans

    def visitPrimaryIndentifier(self, ctx:MiniDecafParser.PrimaryIndentifierContext):
        var = self.var(ctx.Indentifier())
        ty = self.variableType[var]
        self.typeAnalysis.type[ctx] = ty
        return ty

    def visitDecl(self, ctx: MiniDecafParser.DeclContext):
        var = self.var(ctx.Indentifier())
        ty = self.declType(ctx)
        self.variableType[var] = ty
        if ctx.expr() is not None:
            initType = ctx.expr().accept(self)
            tmp = assignCheck(ty,initType)
            typeCheck(tmp)

    def checkFunc(self, ctx):
        retTy = ctx.ty().accept(self)
        paramTy = self.paramTy(ctx.parameterList())
        funcType = FunctionTypeInformation(retTy,paramTy)
        func = test(ctx.Indentifier())
        if func in self.typeAnalysis.functionType:
            prevFuncType = self.typeAnalysis.functionType[func]
            if not funcType.compatible(prevFuncType):
                raise MyMiniDecafError(f"conflicting types for {func}")
        else:
            self.typeAnalysis.functionType[func] = funcType

    # ???怎么改变
    def visitFuncDef(self, ctx: MiniDecafParser.FuncDefContext):
        function = test(ctx.Indentifier())
        self.currentFunction = function
        self.checkFunc(ctx)
        self.visitChildren(ctx)
        self.currentFunction = None

    def visitFuncDecl(self, ctx: MiniDecafParser.FuncDeclContext):
        function = test(ctx.Indentifier())
        self.currentFunction = function
        self.checkFunc(ctx)
        self.currentFunction = None

    def visitDeclExternalDecl(self, ctx: MiniDecafParser.DeclExternalDeclContext):
        ctx = ctx.decl()
        var = self.nameResolution.globalInformation[test(ctx.Indentifier())].variable
        ty = self.declType(ctx)
        if var in self.variableType:
            prevalueType = self.variableType[var]
            if prevalueType != ty:
                raise MyMiniDecafError(f"conflicting types for {var.ident}")
        else:
            self.variableType[var] = ty
        if ctx.expr() is not None:
            initType = ctx.expr().accept(self)
            tmp = assignCheck(ty,initType)
            typeCheck(tmp)

    def visitReturnCont(self, ctx: MiniDecafParser.ReturnContContext):
        returnType = self.typeAnalysis.functionType[self.currentFunction].returnType
        ty = ctx.expr().accept(self)
        tmp = returnCheck(returnType, ty)
        typeCheck(tmp)

    def visitIfStmt(self, ctx: MiniDecafParser.IfStmtContext):
        self.visitChildren(ctx)
        tmp = stmtCondCheck(ctx.expr().accept(self))
        typeCheck(tmp)

    def visitForDeclStmt(self, ctx: MiniDecafParser.ForDeclStmtContext):
        self.visitChildren(ctx)
        if ctx.control is not None:
            tmp = stmtCondCheck(ctx.control.accept(self))
            typeCheck(tmp)

    def visitForStmt(self, ctx: MiniDecafParser.ForStmtContext):
        self.visitChildren(ctx)
        if ctx.control is not None:
            tmp = stmtCondCheck(ctx.control.accept(self))
            typeCheck(tmp)

    def visitWhileStmt(self, ctx: MiniDecafParser.WhileStmtContext):
        self.visitChildren(ctx)
        tmp = stmtCondCheck(ctx.expr().accept(self))
        typeCheck(tmp)

    def visitDoWhileStmt(self, ctx: MiniDecafParser.DoWhileStmtContext):
        self.visitChildren(ctx)
        tmp = stmtCondCheck(ctx.expr().accept(self))
        typeCheck(tmp)
