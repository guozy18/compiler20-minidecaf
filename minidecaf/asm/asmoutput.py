from .asmstr import *

# 将生成的RISC-V文件内容输出到指定的文件中
class asmFileout:
    def __init__(self, fout):
        self.outfile = fout

    def fileout(self, outContent:asmBaseStr):
        print(f"{outContent}",file=self.outfile)

    def close(self):
        self.outfile.close()

    def __call__(self, commands:[asmBaseStr]):
        for command in commands:
            self.fileout(command)
