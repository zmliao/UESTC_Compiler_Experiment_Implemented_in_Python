from lexical import LexicalAnalyzer
import argparse


def get_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", type=str, default="test.pas")
    parser.add_argument("--lexical_only", type=bool, default=True)
    return parser.parse_args()


def run_lexical(filepath):
    filename = filepath.split()[-1]
    filename = filename.split('.')[0]
    dyd_name = filename + '.dyd'
    err_name = filename + '.err'

    lexical = LexicalAnalyzer()
    lexical.load_program(filepath)
    lexical.run()
    lexical.write(dyd_path=dyd_name,
                  err_path=err_name)
    return filename


def run_syntax(filename):
    raise NotImplementedError


if __name__ == '__main__':
    opts = get_opts()
    filename = run_lexical(filepath=opts.file_path)
    if not opts.lexical_only:
        run_syntax(filename=filename)


