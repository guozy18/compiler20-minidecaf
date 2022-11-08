# Generated from MiniDecaf.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MiniDecafParser import MiniDecafParser
else:
    from MiniDecafParser import MiniDecafParser

# This class defines a complete listener for a parse tree produced by MiniDecafParser.
class MiniDecafListener(ParseTreeListener):

    # Enter a parse tree produced by MiniDecafParser#prog.
    def enterProg(self, ctx:MiniDecafParser.ProgContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#prog.
    def exitProg(self, ctx:MiniDecafParser.ProgContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#funcExternalDecl.
    def enterFuncExternalDecl(self, ctx:MiniDecafParser.FuncExternalDeclContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#funcExternalDecl.
    def exitFuncExternalDecl(self, ctx:MiniDecafParser.FuncExternalDeclContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#declExternalDecl.
    def enterDeclExternalDecl(self, ctx:MiniDecafParser.DeclExternalDeclContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#declExternalDecl.
    def exitDeclExternalDecl(self, ctx:MiniDecafParser.DeclExternalDeclContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#funcDef.
    def enterFuncDef(self, ctx:MiniDecafParser.FuncDefContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#funcDef.
    def exitFuncDef(self, ctx:MiniDecafParser.FuncDefContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#funcDecl.
    def enterFuncDecl(self, ctx:MiniDecafParser.FuncDeclContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#funcDecl.
    def exitFuncDecl(self, ctx:MiniDecafParser.FuncDeclContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#parameterList.
    def enterParameterList(self, ctx:MiniDecafParser.ParameterListContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#parameterList.
    def exitParameterList(self, ctx:MiniDecafParser.ParameterListContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#ptrType.
    def enterPtrType(self, ctx:MiniDecafParser.PtrTypeContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#ptrType.
    def exitPtrType(self, ctx:MiniDecafParser.PtrTypeContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#intType.
    def enterIntType(self, ctx:MiniDecafParser.IntTypeContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#intType.
    def exitIntType(self, ctx:MiniDecafParser.IntTypeContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#blockItemStmt.
    def enterBlockItemStmt(self, ctx:MiniDecafParser.BlockItemStmtContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#blockItemStmt.
    def exitBlockItemStmt(self, ctx:MiniDecafParser.BlockItemStmtContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#blockItemDecl.
    def enterBlockItemDecl(self, ctx:MiniDecafParser.BlockItemDeclContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#blockItemDecl.
    def exitBlockItemDecl(self, ctx:MiniDecafParser.BlockItemDeclContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#block.
    def enterBlock(self, ctx:MiniDecafParser.BlockContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#block.
    def exitBlock(self, ctx:MiniDecafParser.BlockContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#returnCont.
    def enterReturnCont(self, ctx:MiniDecafParser.ReturnContContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#returnCont.
    def exitReturnCont(self, ctx:MiniDecafParser.ReturnContContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#exprStmt.
    def enterExprStmt(self, ctx:MiniDecafParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#exprStmt.
    def exitExprStmt(self, ctx:MiniDecafParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#nullstmt.
    def enterNullstmt(self, ctx:MiniDecafParser.NullstmtContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#nullstmt.
    def exitNullstmt(self, ctx:MiniDecafParser.NullstmtContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#ifStmt.
    def enterIfStmt(self, ctx:MiniDecafParser.IfStmtContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#ifStmt.
    def exitIfStmt(self, ctx:MiniDecafParser.IfStmtContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#blockStmt.
    def enterBlockStmt(self, ctx:MiniDecafParser.BlockStmtContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#blockStmt.
    def exitBlockStmt(self, ctx:MiniDecafParser.BlockStmtContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#forDeclStmt.
    def enterForDeclStmt(self, ctx:MiniDecafParser.ForDeclStmtContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#forDeclStmt.
    def exitForDeclStmt(self, ctx:MiniDecafParser.ForDeclStmtContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#forStmt.
    def enterForStmt(self, ctx:MiniDecafParser.ForStmtContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#forStmt.
    def exitForStmt(self, ctx:MiniDecafParser.ForStmtContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#whileStmt.
    def enterWhileStmt(self, ctx:MiniDecafParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#whileStmt.
    def exitWhileStmt(self, ctx:MiniDecafParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#doWhileStmt.
    def enterDoWhileStmt(self, ctx:MiniDecafParser.DoWhileStmtContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#doWhileStmt.
    def exitDoWhileStmt(self, ctx:MiniDecafParser.DoWhileStmtContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#breakStmt.
    def enterBreakStmt(self, ctx:MiniDecafParser.BreakStmtContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#breakStmt.
    def exitBreakStmt(self, ctx:MiniDecafParser.BreakStmtContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#continueStmt.
    def enterContinueStmt(self, ctx:MiniDecafParser.ContinueStmtContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#continueStmt.
    def exitContinueStmt(self, ctx:MiniDecafParser.ContinueStmtContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#expr.
    def enterExpr(self, ctx:MiniDecafParser.ExprContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#expr.
    def exitExpr(self, ctx:MiniDecafParser.ExprContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#decl.
    def enterDecl(self, ctx:MiniDecafParser.DeclContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#decl.
    def exitDecl(self, ctx:MiniDecafParser.DeclContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#tAsgn.
    def enterTAsgn(self, ctx:MiniDecafParser.TAsgnContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#tAsgn.
    def exitTAsgn(self, ctx:MiniDecafParser.TAsgnContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#cAssign.
    def enterCAssign(self, ctx:MiniDecafParser.CAssignContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#cAssign.
    def exitCAssign(self, ctx:MiniDecafParser.CAssignContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#tCond.
    def enterTCond(self, ctx:MiniDecafParser.TCondContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#tCond.
    def exitTCond(self, ctx:MiniDecafParser.TCondContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#cCond.
    def enterCCond(self, ctx:MiniDecafParser.CCondContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#cCond.
    def exitCCond(self, ctx:MiniDecafParser.CCondContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#cLor.
    def enterCLor(self, ctx:MiniDecafParser.CLorContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#cLor.
    def exitCLor(self, ctx:MiniDecafParser.CLorContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#tLor.
    def enterTLor(self, ctx:MiniDecafParser.TLorContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#tLor.
    def exitTLor(self, ctx:MiniDecafParser.TLorContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#tLand.
    def enterTLand(self, ctx:MiniDecafParser.TLandContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#tLand.
    def exitTLand(self, ctx:MiniDecafParser.TLandContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#cLand.
    def enterCLand(self, ctx:MiniDecafParser.CLandContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#cLand.
    def exitCLand(self, ctx:MiniDecafParser.CLandContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#tEq.
    def enterTEq(self, ctx:MiniDecafParser.TEqContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#tEq.
    def exitTEq(self, ctx:MiniDecafParser.TEqContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#cEq.
    def enterCEq(self, ctx:MiniDecafParser.CEqContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#cEq.
    def exitCEq(self, ctx:MiniDecafParser.CEqContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#tRel.
    def enterTRel(self, ctx:MiniDecafParser.TRelContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#tRel.
    def exitTRel(self, ctx:MiniDecafParser.TRelContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#cRel.
    def enterCRel(self, ctx:MiniDecafParser.CRelContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#cRel.
    def exitCRel(self, ctx:MiniDecafParser.CRelContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#cAdd.
    def enterCAdd(self, ctx:MiniDecafParser.CAddContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#cAdd.
    def exitCAdd(self, ctx:MiniDecafParser.CAddContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#tAdd.
    def enterTAdd(self, ctx:MiniDecafParser.TAddContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#tAdd.
    def exitTAdd(self, ctx:MiniDecafParser.TAddContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#tMul.
    def enterTMul(self, ctx:MiniDecafParser.TMulContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#tMul.
    def exitTMul(self, ctx:MiniDecafParser.TMulContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#cMul.
    def enterCMul(self, ctx:MiniDecafParser.CMulContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#cMul.
    def exitCMul(self, ctx:MiniDecafParser.CMulContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#tCast.
    def enterTCast(self, ctx:MiniDecafParser.TCastContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#tCast.
    def exitTCast(self, ctx:MiniDecafParser.TCastContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#cCast.
    def enterCCast(self, ctx:MiniDecafParser.CCastContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#cCast.
    def exitCCast(self, ctx:MiniDecafParser.CCastContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#tUnary.
    def enterTUnary(self, ctx:MiniDecafParser.TUnaryContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#tUnary.
    def exitTUnary(self, ctx:MiniDecafParser.TUnaryContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#cUnary.
    def enterCUnary(self, ctx:MiniDecafParser.CUnaryContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#cUnary.
    def exitCUnary(self, ctx:MiniDecafParser.CUnaryContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#postfixArray.
    def enterPostfixArray(self, ctx:MiniDecafParser.PostfixArrayContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#postfixArray.
    def exitPostfixArray(self, ctx:MiniDecafParser.PostfixArrayContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#postfixCall.
    def enterPostfixCall(self, ctx:MiniDecafParser.PostfixCallContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#postfixCall.
    def exitPostfixCall(self, ctx:MiniDecafParser.PostfixCallContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#tPostfix.
    def enterTPostfix(self, ctx:MiniDecafParser.TPostfixContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#tPostfix.
    def exitTPostfix(self, ctx:MiniDecafParser.TPostfixContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#primaryInteger.
    def enterPrimaryInteger(self, ctx:MiniDecafParser.PrimaryIntegerContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#primaryInteger.
    def exitPrimaryInteger(self, ctx:MiniDecafParser.PrimaryIntegerContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#primaryIndentifier.
    def enterPrimaryIndentifier(self, ctx:MiniDecafParser.PrimaryIndentifierContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#primaryIndentifier.
    def exitPrimaryIndentifier(self, ctx:MiniDecafParser.PrimaryIndentifierContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#primaryParen.
    def enterPrimaryParen(self, ctx:MiniDecafParser.PrimaryParenContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#primaryParen.
    def exitPrimaryParen(self, ctx:MiniDecafParser.PrimaryParenContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#argmentList.
    def enterArgmentList(self, ctx:MiniDecafParser.ArgmentListContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#argmentList.
    def exitArgmentList(self, ctx:MiniDecafParser.ArgmentListContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#unaryList.
    def enterUnaryList(self, ctx:MiniDecafParser.UnaryListContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#unaryList.
    def exitUnaryList(self, ctx:MiniDecafParser.UnaryListContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#addList.
    def enterAddList(self, ctx:MiniDecafParser.AddListContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#addList.
    def exitAddList(self, ctx:MiniDecafParser.AddListContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#assignList.
    def enterAssignList(self, ctx:MiniDecafParser.AssignListContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#assignList.
    def exitAssignList(self, ctx:MiniDecafParser.AssignListContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#mulList.
    def enterMulList(self, ctx:MiniDecafParser.MulListContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#mulList.
    def exitMulList(self, ctx:MiniDecafParser.MulListContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#relationList.
    def enterRelationList(self, ctx:MiniDecafParser.RelationListContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#relationList.
    def exitRelationList(self, ctx:MiniDecafParser.RelationListContext):
        pass


    # Enter a parse tree produced by MiniDecafParser#equalList.
    def enterEqualList(self, ctx:MiniDecafParser.EqualListContext):
        pass

    # Exit a parse tree produced by MiniDecafParser#equalList.
    def exitEqualList(self, ctx:MiniDecafParser.EqualListContext):
        pass



del MiniDecafParser