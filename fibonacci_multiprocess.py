import multiprocessing
import time

# 方法1：递归实现
def fib_recursive(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib_recursive(n - 1) + fib_recursive(n - 2)

# 方法2：循环实现
def fib_iterative(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# 方法3：动态规划实现
def fib_dynamic(n):
    if n <= 0:
        return 0
    
    dp = [0] * (n + 1)
    if n >= 1:
        dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]

# 方法4：矩阵幂实现
def matrix_multiply(A, B):
    C = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_power(A, n):
    if n == 1:
        return A
    if n % 2 == 0:
        half_pow = matrix_power(A, n // 2)
        return matrix_multiply(half_pow, half_pow)
    else:
        half_pow = matrix_power(A, (n - 1) // 2)
        return matrix_multiply(matrix_multiply(half_pow, half_pow), A)

def fib_matrix(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    A = [[1, 1], [1, 0]]
    result = matrix_power(A, n - 1)
    return result[0][0]

# 方法5：使用黄金比例公式实现（闭式公式）
import math

def fib_formula(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    golden_ratio = (1 + math.sqrt(5)) / 2
    return int(round((golden_ratio ** n - (1 - golden_ratio) ** n) / math.sqrt(5)))

# 进程执行函数，计算并打印结果
def process_function(func, n, name):
    start_time = time.time()
    result = func(n)
    end_time = time.time()
    
    print(f"方法: {name}, 结果: fib({n}) = {result}, 用时: {end_time - start_time:.6f}秒")

def main(n=30):
    """
    主函数，使用多进程方式计算斐波那契数列
    
    参数:
        n: 要计算的斐波那契数列项数，默认为30
    """
    # 创建进程
    processes = []
    
    # 定义要运行的函数和它们的名称
    functions = [
        (fib_recursive, "递归方法"),
        (fib_iterative, "循环方法"),
        (fib_dynamic, "动态规划方法"),
        (fib_matrix, "矩阵幂方法"),
        (fib_formula, "黄金比例公式方法")
    ]
    
    # 创建并启动进程
    for func, name in functions:
        p = multiprocessing.Process(target=process_function, args=(func, n, name))
        processes.append(p)
        p.start()
    
    # 等待所有进程完成
    for p in processes:
        p.join()
        
    print("所有计算已完成！")

if __name__ == "__main__":
    # 调用主函数
    main(30) 