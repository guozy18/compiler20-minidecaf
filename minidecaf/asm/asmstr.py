# 定义几种RISCV输出时的格式
class asmBaseStr:
    def __init__(self,str):
        self.str = str

    def __repr__(self):
        self.__str__()


class asmLabel(asmBaseStr):
    def __str__(self):
        return f"{self.str}"


class asmInstruction(asmBaseStr):
    def __str__(self):
        return f"\t{self.str}"


class asmComment(asmBaseStr):
    def __str__(self):
        return f"\t#{self.str}"


class asmBlank(asmBaseStr):
    def __init__(self):
        pass

    def __str__(self):
        return f""
