class SyntaxAnalyser:
    def __init__(self):
        self.dyd = []
        self.vars = []
        self.pros = []
        self.errs = []

        self.cur_line = 0
        self.cur = 0

    def load_dyd(self, dyd_path):
        with open(dyd_path, "r") as f:
            for line in f:
                word, word_id = line.split()
                word_id = int(word_id)
                self.dyd.append((word, word_id))

    def write(self, dyd_path):
        pass

    def __advance(self):
        self.cur += 1
        if self.dyd[self.cur][0] == "ELON":
            self.cur += 1
            self.cur_line += 1

    def __error(self, error_code, error_info):
        raise NotImplementedError

    def run(self):
        self.__program()

    def __program(self):
        pass

    def __subprogram(self):
        pass

    def __declarations(self):
        pass

    def __declaration(self):
        pass

    def __variable_declaration(self):
        pass

    def __variable(self):
        pass

    def __identifier(self):
        pass

    def __letter(self):
        pass

    def __number(self):
        pass

    def __function_declaration(self):
        pass

    def __parameter(self):
        pass

    def __function_block(self):
        pass

    def __executions(self):
        pass

    def __execution(self):
        pass

    def __reading(self):
        pass

    def __writing(self):
        pass

    def __assignment(self):
        pass

    def __arithmetic_expression(self):
        pass

    def __item(self):
        pass

    def __multiplier(self):
        pass

    def __constant(self):
        pass

    def __unsigned_integer(self):
        pass

    def __function_call(self):
        pass

    def __conditional_sentence(self):
        pass

    def __conditional_expression(self):
        pass

    def __relative_operator(self):
        pass
