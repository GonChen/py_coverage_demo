# 多进程斐波那契计算器

这个项目使用Python实现了多种计算斐波那契数列的方法，并通过多进程技术同时运行它们，比较各种方法的性能差异。

## 实现的方法

1. **递归方法** - 经典的递归实现，时间复杂度为O(2^n)
2. **循环方法** - 使用迭代实现，时间复杂度为O(n)
3. **动态规划方法** - 使用数组存储中间结果，时间复杂度为O(n)
4. **矩阵幂方法** - 使用矩阵幂运算，时间复杂度为O(log n)
5. **黄金比例公式方法** - 使用闭式公式直接计算，时间复杂度为O(1)（不考虑大数运算的开销）

## 多进程实现

程序使用Python的`multiprocessing`模块创建多个进程，每个进程运行一种不同的斐波那契计算方法。这样可以充分利用现代多核处理器的计算能力。

## 代码结构

- **main函数** - 封装了多进程创建和执行的主要逻辑，可以接受一个参数n来指定要计算的斐波那契数
- **process_function** - 在每个进程中执行的函数，负责计时和结果输出
- **五种斐波那契实现函数** - 每个函数使用不同的算法实现斐波那契数列计算

## 运行方法

确保您的系统已安装Python 3.6或更高版本，然后执行以下命令：

```bash
python fibonacci_multiprocess.py
```

您也可以在自己的Python代码中导入并使用main函数：

```python
from fibonacci_multiprocess import main

# 计算第40个斐波那契数
main(40)
```

## 测试

项目包含完整的单元测试，使用pytest框架实现。测试文件为`test_fibonacci_multiprocess.py`，包含以下测试：

1. **test_fibonacci_functions** - 测试各个斐波那契函数的正确性
2. **test_main_function_runs** - 测试main函数能否正常运行
3. **test_main_consistency** - 测试所有方法计算结果的一致性
4. **test_main_with_mock** - 使用mock测试main函数的行为

运行测试：

```bash
# 运行所有测试
python3 -m pytest test_fibonacci_multiprocess.py

# 运行测试并显示详细信息
python3 -m pytest test_fibonacci_multiprocess.py -v

# 运行测试并生成覆盖率报告
python3 -m pytest test_fibonacci_multiprocess.py --cov=fibonacci_multiprocess
```

### 生成HTML覆盖率报告

要生成更详细的HTML格式覆盖率报告，可以使用以下命令：

```bash
# 生成HTML覆盖率报告
python3 -m pytest test_fibonacci_multiprocess.py --cov=fibonacci_multiprocess --cov-report html
```

这将在当前目录下创建一个`htmlcov`文件夹，其中包含详细的覆盖率报告。打开`htmlcov/index.html`文件可以查看报告。

HTML报告的特点：
- 直观显示代码覆盖情况
- 高亮显示未覆盖的代码行
- 提供文件、函数和类级别的覆盖率统计
- 可以交互式浏览代码

当前测试覆盖率：99%（仅有`if __name__ == "__main__"`部分的代码未被测试覆盖）

## 输出说明

程序运行后将显示每种方法计算结果，以及计算所需的时间。由于递归方法效率较低，对于较大的n值（如30）可能需要较长时间。

## 注意事项

- 递归方法对于较大的数字（n > 35）可能会导致栈溢出或运行时间过长
- 在计算非常大的斐波那契数时，所有方法都可能受到整数精度限制 