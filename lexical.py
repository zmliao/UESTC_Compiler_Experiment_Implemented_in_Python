class LexicalAnalyzer:
    def __init__(self, rerun=False):
        if rerun is False:
            self.lines = []  # 输入程序

        self.results = []  # 输出字符序列
        self.errors = []  # 输出错误信息

        self.state = 0  # 状态
        self.token = ""  # 已读入的字符序列
        self.cur_line = 0  # 当前行数

        # 存放常量
        self.ITEM_DICT = {"begin": 1,
                          "end": 2,
                          "integer": 3,
                          "if": 4,
                          "then": 5,
                          "else": 6,
                          "function": 7,
                          "read": 8,
                          "write": 9,
                          "=": 12,
                          "<>": 13,
                          "<=": 14,
                          "<": 15,
                          ">=": 16,
                          ">": 17,
                          "-": 18,
                          "*": 19,
                          ":=": 20,
                          "(": 21,
                          ")": 22,
                          ";": 23
                          }
        self.TOKEN = 10
        self.CONSTANT = 11

    def load_program(self, path):
        with open(path, "r") as f:
            for line in f:
                self.lines.append(line)

    def write(self, dyd_path, err_path):
        with open(dyd_path, "w") as f:
            for result in self.results:
                word = result[0]
                word_id = str(result[1])
                output = word.rjust(16) + ' ' + word_id + '\n'
                f.write(output)

        with open(err_path, "w") as f:
            for error in self.errors:
                error_line = error[0]
                error_type = error[1]
                if error_type == 0:
                    error_info = "Invalid Symbol！"
                elif error_type == 1:
                    error_info = "Colon\":\" must be followed by\"=\""
                else:
                    error_info = f"The length of token\"{error[2]}\"exceeds!"
                error_info = "***LINE:" + str(error_line) + "  " + error_info + "\n"
                f.write(error_info)

        return len(self.errors) == 0

    def run(self):
        self.__init__(rerun=True)
        for line in self.lines:
            self.cur_line += 1
            for word in line:
                if word.isalpha():  # 处理字母
                    if self.state in [0, 1]:
                        self.token += word
                        self.state = 1
                    else:
                        self.__retract_and_reserve(word, 1)
                elif word.isdigit():  # 处理数字
                    if self.state in [0, 3]:
                        self.token += word
                        self.state = 3
                    elif self.state == 1:
                        self.token += word
                        self.state = 1
                    else:
                        self.__retract_and_reserve(word, 3)
                elif word == " ":  # 处理空格
                    if self.state != 0:
                        self.__reserve()
                    self.state = 0
                elif word == "=":  # 处理字符
                    if self.state in [0, 10, 14, 17]:
                        self.token += word
                        self.__reserve()
                        self.state = 0
                    else:
                        self.__retract_and_reserve(word, 5)
                elif word == "-":
                    self.__retract_and_reserve(word, 6)
                elif word == "*":
                    self.__retract_and_reserve(word, 7)
                elif word == "(":
                    self.__retract_and_reserve(word, 8)
                elif word == ")":
                    self.__retract_and_reserve(word, 9)
                elif word == "<":
                    self.__retract_and_reserve(word, 10)
                elif word == ">":
                    if self.state == 10:
                        self.token += word
                        self.state = 12
                    else:
                        self.__retract_and_reserve(word, 14)

                elif word == ":":
                    self.__retract_and_reserve(word, 17)
                elif word == ";":
                    self.__retract_and_reserve(word, 20)
                elif word == "\n":
                    self.__elon()
                else:
                    self.__error(0)
        self.__eof()

    def __retract_and_reserve(self, word, next_state):  # 回退一字符，处理保留字，然后读入一字符后转入下一状态
        self.__reserve()
        self.token += word
        self.state = next_state

    def __error(self, error_code, error_info=None):  # 处理出错程序
        """
        :param error_code: 错误类型。0：非法字符，1：冒号不匹配，2：token大于16个字符
        :param error_info: 如果错误类型为2，记录过长的token
        :return:
        """
        self.errors.append((self.cur_line, error_code, error_info))

    def __reserve(self):  # 处理保留字
        if self.token == "":
            return
        if self.state == 1:
            if self.ITEM_DICT.get(self.token):
                self.results.append((self.token, self.ITEM_DICT[self.token]))
            elif len(self.token) > 16:
                self.__error(2, error_info=self.token)
            else:
                self.results.append((self.token, self.TOKEN))
        elif self.state == 3:
            if len(self.token) > 16:
                self.__error(2, error_info=self.token)
            else:
                self.results.append((self.token, self.CONSTANT))
        else:
            if self.ITEM_DICT.get(self.token):
                self.results.append((self.token, self.ITEM_DICT[self.token]))
            else:
                self.__error(1)
        self.token = ""

    def __elon(self):  # 处理换行
        self.__reserve()
        self.results.append(("ELON", 24))
        self.state = 0

    def __eof(self):  # 处理文件结束
        self.__reserve()
        self.results.append(("EOF", 25))
