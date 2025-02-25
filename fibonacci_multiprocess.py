#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import multiprocessing as mp
from functools import lru_cache


def fibonacci_recursive(n):
    """递归方式计算斐波那契数列"""
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)


@lru_cache(maxsize=None)
def fibonacci_memoization(n):
    """带有记忆化的递归方式计算斐波那契数列"""
    if n <= 1:
        return n
    return fibonacci_memoization(n-1) + fibonacci_memoization(n-2)


def fibonacci_iterative(n):
    """迭代方式计算斐波那契数列"""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fibonacci_matrix(n):
    """矩阵方式计算斐波那契数列 - 时间复杂度 O(log n)"""
    if n <= 1:
        return n
    
    def matrix_multiply(A, B):
        a = A[0][0] * B[0][0] + A[0][1] * B[1][0]
        b = A[0][0] * B[0][1] + A[0][1] * B[1][1]
        c = A[1][0] * B[0][0] + A[1][1] * B[1][0]
        d = A[1][0] * B[0][1] + A[1][1] * B[1][1]
        return [[a, b], [c, d]]
    
    def matrix_power(A, n):
        if n == 1:
            return A
        if n % 2 == 0:
            return matrix_power(matrix_multiply(A, A), n // 2)
        else:
            return matrix_multiply(A, matrix_power(matrix_multiply(A, A), (n - 1) // 2))
    
    result = matrix_power([[1, 1], [1, 0]], n)
    return result[0][1]


def fibonacci_formula(n):
    """使用公式计算斐波那契数列 - 黄金比例法"""
    import math
    phi = (1 + math.sqrt(5)) / 2
    return round((phi ** n - (1 - phi) ** n) / math.sqrt(5))


def worker_process(method, n, result_queue, process_name):
    """工作进程函数，计算斐波那契数并将结果放入队列"""
    start_time = time.time()
    result = method(n)
    end_time = time.time()
    execution_time = end_time - start_time
    
    result_queue.put({
        'process_name': process_name,
        'method': method.__name__,
        'n': n,
        'result': result,
        'time': execution_time
    })


def main():
    # 要计算的斐波那契数
    n = 35
    
    # 创建结果队列
    result_queue = mp.Queue()
    
    # 创建进程列表
    processes = [
        mp.Process(
            target=worker_process,
            args=(fibonacci_recursive, min(n, 30), result_queue, "递归进程")
        ),
        mp.Process(
            target=worker_process,
            args=(fibonacci_memoization, n, result_queue, "记忆化递归进程")
        ),
        mp.Process(
            target=worker_process,
            args=(fibonacci_iterative, n, result_queue, "迭代进程")
        ),
        mp.Process(
            target=worker_process,
            args=(fibonacci_matrix, n, result_queue, "矩阵进程")
        ),
        mp.Process(
            target=worker_process,
            args=(fibonacci_formula, n, result_queue, "公式进程")
        )
    ]
    
    # 启动所有进程
    print(f"开始计算斐波那契数 F({n})...")
    for p in processes:
        p.start()
    
    # 等待所有进程完成
    for p in processes:
        p.join()
    
    # 收集并打印结果
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    
    # 按执行时间排序
    results.sort(key=lambda x: x['time'])
    
    print("\n计算结果:")
    print("-" * 80)
    print(f"{'进程名称':<15} {'实现方法':<20} {'n值':<5} {'结果':<15} {'执行时间(秒)':<15}")
    print("-" * 80)
    
    for r in results:
        print(f"{r['process_name']:<15} {r['method']:<20} {r['n']:<5} {r['result']:<15} {r['time']:<15.6f}")


if __name__ == "__main__":
    # 设置启动方法为spawn，确保跨平台兼容性
    mp.set_start_method('spawn', force=True)
    main() 