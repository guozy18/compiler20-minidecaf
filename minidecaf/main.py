"""实例：真·main"""
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
import argparse
import sys
from .generator.MiniDecafLexer import MiniDecafLexer
from .generator.MiniDecafParser import MiniDecafParser
from .ir.irgen import *
from .ir.irset import *
from .asm.asmgen import *
from .ir.nameresolution import *
from .ir.typer import *

# 输入语法分析树，返回中间码，以列表的形式进行存储
def irGenerator(tree):
    tmpName = NameVisitor()
    tmpName.visit(tree)
    tmpType = Typer(tmpName.nameResolution)
    tmpType.visit(tree)
    irStr = irResult()
    irGen(irStr,tmpName.nameResolution,tmpType.typeAnalysis).visit(tree)
    return irStr.getResult()


def asmGenerator(myIr, outfile):
    if outfile is not None:
        with open(outfile, 'w') as fout:
            out = asmFileout(fout)
    else:
        out = asmFileout(sys.stdout)
    asmGen(myIr,out).riscvGen()
    out.close()

def parseArg():
    parser = argparse.ArgumentParser(description="MiniDecaf compiler")
    parser.add_argument("infile", type=str, help="Input C-type files")
    parser.add_argument("outfile",nargs="?", type=str, help="Output RISC-V files")
    parser.add_argument("-ir", action="store_true", help="Output ir rather than RISC-V")
    return parser.parse_args()

class BailErrorListener:
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise MiniDecafError(f"lexer error at {line},{column}")

class ParsErrorListener(ErrorListener):
    def __init__(self):
        super(ParsErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception("Oh no!!")

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        pass

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        pass

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        pass

def main():
    try:
        args = parseArg()
        # 使用Anltr4读取输入文件转化为输入流，使用词法分析进行解析
        inStream = FileStream(args.infile)
        #inStream = FileStream("assign.c")
        lexer = MiniDecafLexer(inStream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(BailErrorListener())
        tokenStream = CommonTokenStream(lexer)
        parser = MiniDecafParser(tokenStream)
        #parser.removeErrorListeners();
        parser.addErrorListener(ParsErrorListener())
        # lexer，parser分别为通过Anltr4解析出来的词法分析和语法分析结果
        tree = parser.prog()
        # 获得IR中间码
        myIr = irGenerator(tree)
        if args.ir:
            print(myIr)
        else:
            # 获得最终的汇编代码并且将其写入文件
            asmGenerator(myIr,args.outfile)
        #asmGenerator(myIr, "output.s")
        #print(myIr)
    except MiniDecafError as e:
        print(e, file=sys.stderr)
        return 1


