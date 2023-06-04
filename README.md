# Update:
本人编译原理检查寄了（A-），老师说我对文法非常不熟悉，所以同学们如果要拿去检查之前先熟悉一下文法

然后程序可能有bug，希望同学们能指出来！

检查就是老师让你不看程序，然后按照老师修改要语法检查的代码，问你会报什么错误，然后运行一下，看报错是否正确。

例如会在某个地方后面加一个分号

或者程序删除得只剩下begin和end

或者把标识符改成常量

或者将函数调用内部的算术表达式删除这种

当然如果同学们还有其他面经也可以上传到这里！

哦对还有如果检查结果不好一定要心态平稳。完成了语法分析至少有8分的，也就相当于期末多错2道选择题的样子，影响不大。我检查之后说了个“cao（四声）",被老师听到了，老师问我cao是什么意思，我当场尬住了。所以同学们心态一定要平稳，输也要输得优雅！

# UESTC_Compiler_Experiment_Implemented_in_Python

电子科技大学 编译原理实验 廖子牧

使用Python实现完成类Pascal语言的词法分析和语法分析


如果需要运行程序
```angular2html
python main.py
```

如果需要分析其他路径下的源码
```angular2html
python main.py --file_path your_source_code_path
```

如果只需要完成词法分析
```angular2html
python main.py --lexical_only True
```
