from lexical import LexicalAnalyzer
from syntax import SyntaxAnalyser
import argparse


def get_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", type=str, default="test.pas")
    parser.add_argument("--lexical_only", type=bool, default=False)
    return parser.parse_args()


def run_lexical(filepath):
    file_name = filepath.split()[-1]
    file_name = file_name.split('.')[0]
    dyd_name = file_name + '.dyd'
    err_name = file_name + '.err'

    lexical = LexicalAnalyzer()
    lexical.load_program(filepath)
    lexical.run()
    lexica_result = lexical.write(dyd_path=dyd_name, err_path=err_name)
    return lexica_result


def run_syntax(filepath):
    dyd_path = filepath.split('.')[0] + '.dyd'

    syntax_analyser = SyntaxAnalyser()
    syntax_analyser.load_dyd(dyd_path=dyd_path)
    syntax_analyser.run()
    syntax_result = syntax_analyser.write(dyd_path=dyd_path)
    return syntax_result


if __name__ == '__main__':
    opts = get_opts()
    result = run_lexical(filepath=opts.file_path)
    if result is True:
        print("Lexical Analysis Finished!")
    else:
        print("Lexical Analysis Error!")
        exit(0)
    if not opts.lexical_only:
        result = run_syntax(filepath=opts.file_path)
        if result is True:
            print("Syntax Analysis Finished!")
        else:
            print("Syntax Analysis Error!")
