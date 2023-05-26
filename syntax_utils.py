class Variable:
    def __init__(self, v_name, v_proc, v_kind, v_type, v_lev, v_adr):
        self.v_name = v_name
        self.v_proc = v_proc
        self.v_kind = v_kind
        self.v_type = v_type
        self.v_lev = v_lev
        self.v_adr = v_adr

    def to_string(self):
        return f"{self.v_name} {self.v_proc} {self.v_kind} {self.v_type} {self.v_lev} {self.v_adr}\n"


class Process:
    def __init__(self, p_name, p_type, p_lev):
        self.p_name = p_name
        self.p_type = p_type
        self.p_lev = p_lev
        self.var_dict = {}
        self.son_dict = {}
        self.param = None
        self.father = None

    def to_string(self):
        return f"{self.p_name} {self.p_type} {self.p_lev} {self.get_first_adr()} {self.get_last_adr()}\n"

    def vars_to_strings(self):
        def get_all_vars(root):
            ret = list(root.var_dict.values())
            for son in root.son_dict.values():
                ret.extend(get_all_vars(son))
            ret.sort(key=lambda x: x.v_adr)
            return ret

        variables = get_all_vars(self)
        strings = []
        for var in variables:
            strings.append(var.to_string())
        return strings

    def pros_to_strings(self):
        def get_all_sons(root):
            ret = [root]
            for son in root.son_dict.values():
                ret.extend(get_all_sons(son))
            return ret

        pros = get_all_sons(self)
        strings = []
        for pro in pros:
            strings.append(pro.to_string())
        return strings

    def create(self, p_name, p_type, p_param):  # 在一个过程里面定义一个过程
        flag = True
        if p_name in self.son_dict or p_name in self.var_dict:
            flag = False
        son_process = Process(p_name, p_type, self.p_lev + 1)
        son_process.father = self
        son_process.param = p_param
        self.son_dict[p_name] = son_process
        return flag

    def insert(self, var):  # 在一个过程里面定义一个变量
        if var.v_name in self.var_dict:
            return False
        if var.v_name in self.son_dict:
            return False
        self.var_dict[var.v_name] = var
        return True

    def find_var(self, v_name):  # 在一个过程里面查询该变量是否被定义
        cur_process = self
        if v_name == cur_process.p_name:
            return True
        while cur_process is not None:
            if v_name in cur_process.var_dict:
                return True
            cur_process = cur_process.father
        return False

    def find_pro(self, p_name):
        cur_process = self
        while cur_process is not None:
            if p_name in cur_process.son_dict:
                return True
            cur_process = cur_process.father
        return False

    def get_first_adr(self) -> int:  # 获得该过程第一个定义变量的地址
        ret = 998244353
        for var in self.var_dict.values():
            ret = min(ret, var.v_adr)
        if ret == 998244353:
            ret = 0
        return ret

    def get_last_adr(self) -> int:  # 获得该过程最后一个定义变量的地址
        ret = 0
        for var in self.var_dict.values():
            ret = max(ret, var.v_adr)
        return ret
