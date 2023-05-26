from syntax_utils import *


class SyntaxAnalyser:
    def __init__(self, rerun=False):
        if rerun is False:
            self.dyd = []
        self.errs = []

        self.cur_line = 1
        self.cur = 0
        self.cur_var = 1
        self.cur_process = Process(p_name='main', p_type='procedure', p_lev=0)

    def load_dyd(self, dyd_path):
        with open(dyd_path, "r") as f:
            for line in f:
                word, word_id = line.split()
                word_id = int(word_id)
                self.dyd.append((word, word_id))

    def write(self, dyd_path):
        prefix = dyd_path.split('.')[0]
        dys_path = prefix + ".dys"
        var_path = prefix + ".var"
        pro_path = prefix + ".pro"
        err_path = prefix + ".err"

        err_strings = []
        last_line = 0
        for error in self.errs:
            if error[0] == last_line:
                continue
            last_line = error[0]
            err_string = f"***LINE:{error[0]}  ERR00{error[1]}:{error[2]}\n"
            err_strings.append(err_string)
        with open(err_path, "w") as f:
            for string in err_strings:
                f.write(string)

        with open(dys_path, "w") as f:
            for dyd in self.dyd:
                string = f"{dyd[0].rjust(16)} {dyd[1]}\n"
                f.write(string)

        var_strings = self.cur_process.vars_to_strings()
        with open(var_path, "w") as f:
            for string in var_strings:
                f.write(string)

        pro_strings = self.cur_process.pros_to_strings()
        with open(pro_path, "w") as f:
            for string in pro_strings:
                f.write(string)

        if len(err_strings) == 0:
            return False
        return True

    def __advance(self):
        self.cur += 1
        while self.dyd[self.cur][0] == "ELON":
            self.cur += 1
            self.cur_line += 1

    def __current(self):
        return self.dyd[self.cur]

    def __next(self):
        pos = 1
        while self.dyd[self.cur + pos][0] == "ELON":
            pos += 1
        return self.dyd[self.cur + pos]

    def __error(self, error_code, error_info):
        self.errs.append((self.cur_line, error_code, error_info))

    def run(self):
        self.__init__(rerun=True)
        while self.__current()[0] == "ELON":
            self.cur_line += 1
            self.__advance()
        self.__program()

    def __program(self):
        """
        <program>-><subprogram>
        """
        self.__subprogram()

    def __subprogram(self):
        """
        <subprogram>->begin<declarations>;<executions>end
        """
        if self.__current()[0] == "begin":
            self.__advance()
            self.__declarations()
            if self.__current()[0] == ";":
                self.__advance()
                self.__executions()
                if self.__current()[0] == "end":
                    self.__advance()
                else:
                    self.__error(1, "Symbol \"end\" not found; Symbol \"begin\" must match the symbol \"end\"")
            else:
                self.__error(0, "Symbol \";\" not found!")
        else:
            self.__error(0, "Symbol \"begin\" not found")

    def __declarations(self):
        """
        <declarations> -> <declaration>|<declarations>;<declaration>
        
        <declarations> -> <declaration><declarations1>
        <declarations1> -> epsilon|;<declaration><declarations1>
        """
        self.__declaration()
        self.__declarations1()
        pass

    def __declarations1(self):
        if self.__current()[0] == ";" and self.__next()[0] == 'integer':
            self.__advance()
            self.__declaration()
            self.__declarations1()
        else:
            pass

    def __declaration(self):
        """
        <declaration>-><variable_declaration>|<function_declaration>
        """
        if self.__current()[0] == "integer":
            if self.__next()[1] == 10:
                self.__variable_declaration()
            elif self.__next()[0] == "function":
                self.__function_declaration()
            else:
                self.__error(1, "Invalid declaration: symbol \"integer\" must match an identifier of the symbol "
                                "\"function\"")
        else:
            self.__error(0, "Neither variable nor function declaration!")

    def __variable_declaration(self):
        """
        <variable_declaration> -> integer <variable>
        <variable> -> <identifier>
        """
        if self.__current()[0] == "integer":
            self.__advance()
            if self.__current()[1] == 10:  # TOKEN
                var = Variable(v_name=self.__current()[0],
                               v_proc=self.cur_process.p_name,
                               v_kind=0,
                               v_type='integer',
                               v_lev=self.cur_process.p_lev,
                               v_adr=self.cur_var
                               )
                if var.v_name == self.cur_process.param:
                    var.v_kind = 1
                flag = self.cur_process.insert(var)
                self.__advance()
                if flag is False:
                    self.__error(2, f"Variable or function \"{self.__current()[0]}\" is defined!")  # �ظ�����
                else:
                    self.cur_var += 1
            else:
                self.__error(1, f"Invalid identifier \"{self.__current()[0]}\"!")
        else:
            pass

    def __function_declaration(self):
        """
        <function_declaration> -> integer function <identifier> (<parameter>) ; <function_block>
        """
        if self.__current()[0] == "integer":
            self.__advance()
            if self.__current()[0] == "function":
                self.__advance()
                if self.__current()[1] == 10:
                    p_name = self.__current()[0]
                    self.__advance()
                    if self.__current()[0] == "(":
                        self.__advance()
                        param = self.__parameter()
                        if self.__current()[0] == ")":
                            self.__advance()
                            if self.__current()[0] == ";":
                                self.__advance()
                                flag = self.cur_process.create(p_name=p_name,
                                                               p_type='integer',
                                                               p_param=param.v_name)
                                if flag is False:
                                    self.__error(2, f"Identifier \"{p_name}\" is defined!")
                                self.cur_process = self.cur_process.son_dict[p_name]
                                self.__function_block()
                                self.cur_process = self.cur_process.father
                            else:
                                self.__error(0, "Symbol \";\" is not found!")
                        else:
                            self.__error(1, "Symbol \")\" is not found: symbol \"(\" must match the symbol \")\"")
                    else:
                        self.__error(0, "Symbol \"(\" is not found!")
                else:
                    self.__error(1, f"Invalid identifier f{self.__current()[0]}")
            else:
                self.__error(0, f"Invalid function definition!")
        else:
            pass

    def __parameter(self):
        """
        <parameter> -> <variable>
        (�β�)
        """
        var = Variable(v_name=self.__current()[0],
                       v_proc=self.cur_process.p_name,
                       v_kind=1,
                       v_type='integer',
                       v_lev=self.cur_process.p_lev,
                       v_adr=self.cur
                       )
        flag = self.cur_process.find_var(var.v_name)
        if flag is True:
            self.__error(2, f"Variable or function \"{self.__current()[0]}\" is defined!")
        self.__advance()
        return var

    def __function_block(self):
        """
        <function_block> -> begin <declarations>;<executions> end
        """
        if self.__current()[0] == "begin":
            self.__advance()
            self.__declarations()
            if self.__current()[0] == ";":
                self.__advance()
                self.__executions()
                if self.__current()[0] == "end":
                    self.__advance()
                else:
                    self.__error(1, "Symbol \"end\" not found; Symbol \"begin\" must match the symbol \"end\"")
            else:
                self.__error(0, "Symbol \";\" not found!")
        else:
            self.__error(0, "Symbol \"begin\" not found")

    def __executions(self):
        """
        <executions> -> <execution> | <executions> ; <execution>

        <executions> -> <execution> <executions1>
        <executions1> -> ; <execution> <executions1> | epsilon
        """
        self.__execution()
        self.__executions1()

    def __executions1(self):
        if self.__current()[0] == ";" and self.__next()[1] in [4, 8, 9, 10]:
            self.__advance()
            self.__execution()
            self.__executions1()
        else:
            pass

    def __execution(self):
        """
        <execution> -> <reading>|<writing>|<assignment>|<conditional_sentence>
        """
        cur = self.__current()
        if cur[0] == "read":
            self.__reading()
        elif cur[0] == "write":
            self.__writing()
        elif cur[1] == 10:
            self.__assignment()
        elif cur[0] == "if":
            self.__conditional_sentence()
        else:
            pass

    def __reading(self):
        """
        <reading> -> read(<variable>)
        """
        self.__advance()
        if self.__current()[0] == "(":
            self.__advance()
            if self.__current()[1] == 10:
                v_name = self.__current()[0]
                self.__advance()
                if self.cur_process.find_var(v_name) is False:
                    self.__error(2, f"Variable \"{v_name}\" is not defined!")
                if self.__current()[0] == ")":
                    self.__advance()
                else:
                    self.__error(1, "Symbol \")\" is not found: symbol \"(\" must match the symbol \")\"")

            else:
                self.__error(1, f"Invalid identifier f{self.__current()[0]}")
        else:
            self.__error(0, "Symbol \")\" is not found!")

    def __writing(self):
        """
        <writing> -> write(<variable>)
        """
        self.__advance()
        if self.__current()[0] == "(":
            self.__advance()
            if self.__current()[1] == 10:
                v_name = self.__current()[0]
                self.__advance()
                if self.cur_process.find_var(v_name) is False:
                    self.__error(2, f"Variable \"{v_name}\" is not defined!")
                if self.__current()[0] == ")":
                    self.__advance()
                else:
                    self.__error(1, "Symbol \")\" is not found: symbol \"(\" must match the symbol \")\"")
            else:
                self.__error(1, f"Invalid identifier f{self.__current()[0]}")
        else:
            self.__error(0, "Symbol \")\" is not found!")

    def __assignment(self):
        """
        <assignment> -> <variable> := <arithmetic_expression>
        """
        if self.__current()[1] == 10:
            v_name = self.__current()[0]
            self.__advance()
            if self.cur_process.find_var(v_name) is False:
                self.__error(2, f"Variable \"{v_name}\" is not defined!")
            if self.__current()[0] == ":=":
                self.__advance()
                self.__arithmetic_expression()
            else:
                self.__error(0, "Symbol \":=\" is not found!")
        else:
            self.__error(1, f"Invalid identifier f{self.__current()[0]}")

    def __arithmetic_expression(self):
        """
        <arithmetic_expression> -> <arithmetic_expression> - <item> | <item>

        <arithmetic_expression> -> <item> | <arithmetic_expression1>
        <arithmetic_expression1> -> epsilon | - <item> <arithmetic_expression1>
        """
        self.__item()
        self.__arithmetic_expression1()
        pass

    def __arithmetic_expression1(self):
        if self.__current()[0] == "-":
            self.__advance()
            self.__item()
            self.__arithmetic_expression1()
        else:
            pass

    def __item(self):
        """
        <item> -> <item> * <multiplier> | <multiplier>

        <item> -> <multiplier> | <item1>
        <item1> -> epsilon | * <multiplier> <item1>
        """
        self.__multiplier()
        self.__item1()
        pass

    def __item1(self):
        if self.__current()[0] == "*":
            self.__advance()
            self.__multiplier()
            self.__item1()
        else:
            pass

    def __multiplier(self):
        """
        <multiplier> -> <variable> | <constant> | <function_call>
        """
        if self.__current()[1] == 10:
            identifier = self.__current()[0]
            if self.__next()[0] == "(":
                self.__advance()
                if self.cur_process.find_pro(identifier) is False:
                    self.__error(2, f"Function \"{identifier}\" is not defined!")
                self.__function_call()
            else:
                self.__advance()
                if self.cur_process.find_var(identifier) is False:
                    self.__error(2, f"Variable \"{identifier}\" is not defined!")
        elif self.__current()[1] == 11:
            self.__advance()
        else:
            self.__error(0, "Invalid expression!")

    def __function_call(self):
        """
        <function_call> -> <identifier>(<arithmetic_expression>)
        """
        if self.__current()[0] == "(":
            self.__advance()
            self.__arithmetic_expression()
            if self.__current()[0] == ")":
                self.__advance()
            else:
                self.__error(1, "Symbol \")\" is not found: symbol \"(\" must match the symbol \")\"")
        else:
            self.__error(0, "Symbol \"(\" is not found!")

    def __conditional_sentence(self):
        """
        <conditional_sentence> -> if <conditional_expression> then <execution> else <execution>
        """
        if self.__current()[0] == "if":
            self.__advance()
            self.__conditional_expression()
            if self.__current()[0] == "then":
                self.__advance()
                self.__execution()
                if self.__current()[0] == "else":
                    self.__advance()
                    self.__execution()
            else:
                self.__error(1, "Symbol \"then\" is not found: Symbol \"if\" must match the symbol \"then\"!")
        else:
            self.__error(0, "Symbol \"if\" is not found!")

    def __conditional_expression(self):
        """
        <conditional_expression> -> <arithmetic_expression> <relative_operator> <arithmetic_expression>
        """
        self.__arithmetic_expression()
        if self.__current()[0] in ["<", ">", "<=", ">=", "=", "<>"]:
            self.__advance()
            self.__arithmetic_expression()
        else:
            self.__error(0, "Relative operator is not found!")
