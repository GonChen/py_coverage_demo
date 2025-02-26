# 多进程斐波那契计算示例

这个Python程序展示了如何使用多进程并行计算斐波那契数列，每个进程使用不同的算法实现。

## 功能特点

- 使用Python的`multiprocessing`模块创建多个并行进程
- 实现了多种不同的斐波那契数列计算方法：
  1. 递归方法 (时间复杂度: O(2^n))
  2. 带记忆化的递归方法 (时间复杂度: O(n))
  3. 迭代方法 (时间复杂度: O(n))
  4. 矩阵幂方法 (时间复杂度: O(log n))
  5. 数学公式方法 (时间复杂度: O(1)，但有浮点数精度问题)
  6. 动态规划方法 (时间复杂度: O(n))
- 比较不同算法的执行时间和效率
- 使用进程间通信（队列）收集结果

## 运行要求

- Python 3.6+
- 基础版本无需额外依赖库
- 高级版本需要安装psutil库：`pip install -r requirements.txt`

## 程序版本

本仓库包含两个版本的斐波那契多进程计算程序：

### 1. 基础版本 (fibonacci_multiprocess.py)

简单的多进程斐波那契计算程序，固定计算第35项斐波那契数。

```bash
python fibonacci_multiprocess.py
```

### 覆盖率测试方法

```
COVERAGE_PROCESS_START=.coveragerc coverage run -m pytest test_fibonacci.py
coverage combine
coverage report
coverage html
```