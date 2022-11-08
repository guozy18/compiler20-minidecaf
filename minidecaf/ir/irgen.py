# 中间码的产生
from .irset import *
from ..generator.MiniDecafParser import MiniDecafParser
from ..generator.MiniDecafVisitor import MiniDecafVisitor
from .nameresolution import NameResolution
from .typer import TypeAnalysis
from .alltype import *

# 用于更新最新产生的ir中间码到irResult中
class irGen(MiniDecafVisitor):
    def __init__(self, irEmitter: irResult, nameResolution: NameResolution , typeAnalysis:TypeAnalysis):
        self.irEmitter = irEmitter
        self.offsetManager = OffsetManager()
        self.labelManager = LabelManager()
        self.nameResolution = nameResolution
        self.currentFunction = None
        self.typeAnalysis = typeAnalysis

    '''def visitExpr(self, ctx: MiniDecafParser.ExprContext):
        nodeVal = int(test(ctx.Integer()))
        self.irEmitter(irPush(nodeVal))'''

    def genVar(self,variable:MyVariable):
        if variable.offset is None:
            self.irEmitter([irGlobalSymbol(variable.identifier)])
        else:
            self.irEmitter([irFrameAddr(variable.offset)])

    def visitReturnCont(self, ctx:MiniDecafParser.ReturnContContext):
        self.visitChildren(ctx)
        self.irEmitter([irRet()])

    def visitBlock(self,ctx:MiniDecafParser.BlockContext):
        self.visitChildren(ctx)
        self.irEmitter([irPop()]*self.nameResolution.functionInformation[self.currentFunction].blockSlot[ctx])

    def visitPrimaryInteger(self,ctx:MiniDecafParser.PrimaryIntegerContext):
        nodeVal = int(test(ctx.Integer()))
        self.irEmitter([irPush(nodeVal)])

    def visitCUnary(self,ctx:MiniDecafParser.CUnaryContext):
        oper = test(ctx.unaryList())
        if oper == '&':
            location = self.typeAnalysis.lvalueLocation(ctx.cast())
            for loc in location:
                if isinstance(loc,irBaseStr):
                    self.irEmitter([loc])
                else:
                    loc.accept(self)
        elif oper == '*':
            self.visitChildren(ctx)
            self.irEmitter([irLoad()])
        else:
            self.visitChildren(ctx)
            self.irEmitter([irUnary(oper)])

    def visitCLor(self,ctx:MiniDecafParser.CLorContext):
        lor_true = self.labelManager.newLabel("lor_true")
        lor_exit = self.labelManager.newLabel("lor_exit")
        ctx.logical_or().accept(self)
        self.irEmitter([irBranch("bnez", lor_true)])
        ctx.logical_and().accept(self)
        self.irEmitter([irBranch("bnez", lor_true), irConst(0), irBranch("br", lor_exit),
                 irLabel(lor_true), irConst(1), irLabel(lor_exit)])

    def visitCLand(self,ctx:MiniDecafParser.CLandContext):
        land_false = self.labelManager.newLabel("land_false")
        land_exit = self.labelManager.newLabel("land_exit")
        ctx.logical_and().accept(self)
        self.irEmitter([irBranch("beqz", land_false)])
        ctx.equality().accept(self)
        self.irEmitter([irBranch("beqz", land_false), irConst(1), irBranch("br", land_exit),
                 irLabel(land_false), irConst(0), irLabel(land_exit)])

    def visitCEq(self, ctx: MiniDecafParser.CEqContext):
        self.visitChildren(ctx)
        self.irEmitter([irBinary(test(ctx.equalList()))])

    def visitCRel(self,ctx:MiniDecafParser.CRelContext):
        self.visitChildren(ctx)
        self.irEmitter([irBinary(test(ctx.relationList()))])

    def visitCAdd(self,ctx:MiniDecafParser.CAddContext):
        if isinstance(self.typeAnalysis[ctx.additive()] , pointerType):
            sizeOf = self.typeAnalysis[ctx.additive()].sizeof()
            if isinstance(self.typeAnalysis[ctx.multiplicative()], pointerType): # ptr - ptr
                ctx.additive().accept(self)
                ctx.multiplicative().accept(self)
                self.irEmitter([irBinary(test(ctx.addList())) , irConst(sizeOf) , irBinary('/')])
            else: # ptr +- int
                ctx.additive().accept(self)
                ctx.multiplicative().accept(self)
                self.irEmitter([irConst(sizeOf),irBinary('*'),irBinary(test(ctx.addList()))])
        else:
            sizeOf = self.typeAnalysis[ctx.multiplicative()].sizeof()
            if isinstance(self.typeAnalysis[ctx.multiplicative()], pointerType): # int +- ptr
                ctx.additive().accept(self)
                self.irEmitter([irConst(sizeOf), irBinary('*')])
                ctx.multiplicative().accept(self)
                self.irEmitter([irBinary(test(ctx.addList()))])
            else: # int +- int
                self.visitChildren(ctx)
                self.irEmitter([irBinary(test(ctx.addList()))])

    def visitCMul(self,ctx:MiniDecafParser.CMulContext):
        self.visitChildren(ctx)
        self.irEmitter([irBinary(test(ctx.mulList()))])

    def visitBlockItemDecl(self,ctx:MiniDecafParser.BlockItemDeclContext):
        self.visitChildren(ctx)

    def visitExprStmt(self,ctx:MiniDecafParser.ExprStmtContext):
        self.visitChildren(ctx)
        self.irEmitter([irPop()])

    # def _var(self, term):
    #     return self.ni[term]

    def visitDecl(self,ctx:MiniDecafParser.DeclContext):
        var = self.nameResolution[ctx.Indentifier()]
        if ctx.expr() is not None:
            ctx.expr().accept(self)
        else:
            self.irEmitter([irConst(0)] * (var.size//4) )
        '''
        if var not in self.offsetManager.offset.keys():
            self.offsetManager.newVar(var)
        else:
            raise MyMiniDecafError(var, f"{test(var)} is Redefined")
        '''


    def visitPrimaryIndentifier(self,ctx:MiniDecafParser.PrimaryIndentifierContext):
        var = self.nameResolution[ctx.Indentifier()]
        self.genVar(var)
        if not isinstance(self.typeAnalysis[ctx],arrayType):
            self.irEmitter([irLoad()])

    def visitCAssign(self,ctx:MiniDecafParser.CAssignContext):
        ctx.asgn().accept(self)
        # self.computeAddress(ctx.unary())
        location = self.typeAnalysis.lvalueLocation(ctx.unary())
        for loc in location:
            if isinstance(loc,irBaseStr):
                self.irEmitter([loc])
            else:
                loc.accept(self)
        self.irEmitter([irAsmStore()])

    def visitIfStmt(self,ctx:MiniDecafParser.IfStmtContext):
        ctx.expr().accept(self)
        label1 = self.labelManager.newLabel("if_end")
        label2 = self.labelManager.newLabel("if_else")
        if ctx.el is not None:
            self.irEmitter([irBranch("beqz", label2)])
            ctx.th.accept(self)
            self.irEmitter([irBranch("br", label1), irLabel(label2)])
            ctx.el.accept(self)
            self.irEmitter([irLabel(label1)])
        else:
            self.irEmitter([irBranch("beqz", label1)])
            ctx.th.accept(self)
            self.irEmitter([irLabel(label1)])

    def visitCCond(self, ctx: MiniDecafParser.CCondContext):
        ctx.logical_or().accept(self)
        label1 = self.labelManager.newLabel("cond_end")
        label2 = self.labelManager.newLabel("cond_else")
        self.irEmitter([irBranch("beqz",label2)])
        ctx.expr().accept(self)
        self.irEmitter([irBranch("br", label1), irLabel(label2)])
        ctx.cond().accept(self)
        self.irEmitter([irLabel(label1)])

    # def computeAddress(self,var:irUnary):
    #     if isinstance(var, MiniDecafParser.TUnaryContext):
    #         return self.computeAddress(var.postfix())
    #     if isinstance(var, MiniDecafParser.TPostfixContext):
    #         return self.computeAddress(var.primary())
    #     if isinstance(var, MiniDecafParser.PrimaryParenContext):
    #         return self.computeAddress(var.expr())
    #     if isinstance(var,MiniDecafParser.PrimaryIndentifierContext):
    #         tmp1 = self.currentFunction[var.Indentifier()]
    #         tmp = self.genVar(tmp1)
    #         return tmp
    #     raise MyMiniDecafError(f"{test(var)} is not Left Value")

    def forLoop(self, name, myInit, condition, myBody, post):
        enterlabel = self.labelManager.newLabel(f"{name}_entry")
        if post is not None:
            labelContinue = self.labelManager.newLabel(f"{name}_continue")
        else:
            labelContinue = enterlabel
        exitLabel = self.labelManager.newLabel(f"{name}_exit")

        self.labelManager.enterLoop(labelContinue, exitLabel)
        if myInit is not None:
            myInit.accept(self)
            if isinstance(myInit, MiniDecafParser.ExprContext):
                self.irEmitter([irPop()])

        self.irEmitter([irLabel(enterlabel)])
        if condition is not None:
            condition.accept(self)
        else:
            self.irEmitter([irConst(1)])

        self.irEmitter([irBranch("beqz", exitLabel)])
        myBody.accept(self)
        if post is not None:
            self.irEmitter([irLabel(labelContinue)])
            post.accept(self)
            if isinstance(post, MiniDecafParser.ExprContext):
                self.irEmitter([irPop()])
        self.labelManager.exitLoop()
        self.irEmitter([irBranch("br", enterlabel), irLabel(exitLabel)])

    def whileNoinitLoop(self, name, condition, myBody):
        enterlabel = self.labelManager.newLabel(f"{name}_entry")
        labelContinue = enterlabel
        exitLabel = self.labelManager.newLabel(f"{name}_exit")
        self.labelManager.enterLoop(labelContinue, exitLabel)
        self.irEmitter([irLabel(enterlabel)])
        condition.accept(self)
        self.irEmitter([irBranch("beqz", exitLabel)])
        myBody.accept(self)
        self.labelManager.exitLoop()
        self.irEmitter([irBranch("br", enterlabel), irLabel(exitLabel)])

    def whileLoop(self, name, myInit, condition, myBody):
        enterlabel = self.labelManager.newLabel(f"{name}_entry")
        labelContinue = enterlabel
        exitLabel = self.labelManager.newLabel(f"{name}_exit")
        self.labelManager.enterLoop(labelContinue, exitLabel)
        myInit.accept(self)
        if isinstance(myInit, MiniDecafParser.ExprContext):
            self.irEmitter([irPop()])
        self.irEmitter([irLabel(enterlabel)])
        condition.accept(self)
        self.irEmitter([irBranch("beqz", exitLabel)])
        myBody.accept(self)
        self.labelManager.exitLoop()
        self.irEmitter([irBranch("br", enterlabel), irLabel(exitLabel)])

    def visitForDeclStmt(self, ctx:MiniDecafParser.ForDeclStmtContext):
        self.forLoop("for", ctx.init, ctx.control, ctx.stmt(), ctx.post)
        self.irEmitter([irPop()] * self.nameResolution.functionInformation[self.currentFunction].blockSlot[ctx])

    def visitForStmt(self, ctx:MiniDecafParser.ForStmtContext):
        self.forLoop("for", ctx.init, ctx.control, ctx.stmt(), ctx.post)

    def visitWhileStmt(self, ctx:MiniDecafParser.WhileStmtContext):
        self.whileNoinitLoop("while", ctx.expr(), ctx.stmt())

    def visitDoWhileStmt(self, ctx:MiniDecafParser.DoWhileStmtContext):
        self.whileLoop("dowhile", ctx.stmt(), ctx.expr(), ctx.stmt())

    def visitBreakStmt(self, ctx:MiniDecafParser.BreakStmtContext):
        self.irEmitter([irBranch("br", self.labelManager.MyBreak())])

    def visitContinueStmt(self, ctx:MiniDecafParser.ContinueStmtContext):
        self.irEmitter([irBranch("br", self.labelManager.MyContinue())])

    # 函数定义语句
    def visitFuncDef(self,ctx:MiniDecafParser.FuncDefContext):
        functionName = test(ctx.Indentifier())
        parameterNum = len(self.typeAnalysis.functionType[functionName].parameterType)
        self.currentFunction = functionName
        self.irEmitter.enterFunction(functionName,parameterNum)
        ctx.block().accept(self)
        self.irEmitter.exitFunction()
        self.currentFunction = None

    def visitFuncDecl(self,ctx:MiniDecafParser.FuncDeclContext):
        pass

    # 函数调用语句
    def visitPostfixCall(self, ctx:MiniDecafParser.PostfixCallContext):
        argmentList = reversed(ctx.argmentList().expr())
        for argment in argmentList:
            argment.accept(self)
        function = test(ctx.Indentifier())
        self.irEmitter([irCall(function)])

    def visitDeclExternalDecl(self, ctx: MiniDecafParser.DeclExternalDeclContext):
        pass

    def visitProg(self, ctx: MiniDecafParser.ProgContext):
        for globalInformation in self.nameResolution.globalInformation.values():
            self.irEmitter.expandGlobal(globalInformation)
        self.visitChildren(ctx)

    def visitPostfixArray(self, ctx:MiniDecafParser.PostfixArrayContext):
        fixUp = self.typeAnalysis[ctx.postfix()].base.sizeof()
        ctx.postfix().accept(self)
        ctx.expr().accept(self)
        self.irEmitter([irConst(fixUp), irBinary('*'), irBinary('+')])
        if not isinstance(self.typeAnalysis[ctx] , arrayType):
            self.irEmitter([irLoad()])