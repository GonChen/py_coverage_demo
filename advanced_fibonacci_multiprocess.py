#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import argparse
import multiprocessing as mp
from functools import lru_cache
import os
import psutil


# 斐波那契计算方法 - 开始
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


# 动态规划方法
def fibonacci_dp(n):
    """动态规划方式计算斐波那契数列"""
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]


# 斐波那契计算方法 - 结束

# 获取所有可用的斐波那契计算方法
def get_available_methods():
    methods = {
        'recursive': fibonacci_recursive,
        'memoization': fibonacci_memoization,
        'iterative': fibonacci_iterative,
        'matrix': fibonacci_matrix,
        'formula': fibonacci_formula,
        'dp': fibonacci_dp
    }
    return methods


def worker_process(method, n, result_queue, process_name, process_id):
    """工作进程函数，计算斐波那契数并将结果放入队列"""
    # 设置进程亲和性（如果可能）
    try:
        process = psutil.Process(os.getpid())
        process.cpu_affinity([process_id % os.cpu_count()])
    except:
        pass  # 如果不支持设置CPU亲和性，则忽略
    
    start_time = time.time()
    
    # 获取进程内存使用前
    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # 计算斐波那契数
    result = method(n)
    
    # 获取进程内存使用后
    memory_after = process.memory_info().rss / 1024 / 1024  # MB
    memory_used = memory_after - memory_before
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    result_queue.put({
        'process_id': process_id,
        'process_name': process_name,
        'method': method.__name__,
        'n': n,
        'result': result,
        'time': execution_time,
        'memory': memory_used
    })


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='多进程计算斐波那契数列')
    parser.add_argument('-n', type=int, default=35, help='要计算的斐波那契数 (默认: 35)')
    parser.add_argument('-m', '--methods', nargs='+', choices=get_available_methods().keys(), 
                        default=['recursive', 'memoization', 'iterative', 'matrix', 'formula', 'dp'],
                        help='要使用的计算方法 (默认: 全部)')
    parser.add_argument('-r', '--recursive-limit', type=int, default=30, 
                        help='递归方法的最大n值 (默认: 30)')
    parser.add_argument('-p', '--processes', type=int, default=None,
                        help='要使用的进程数量 (默认: 与方法数量相同)')
    parser.add_argument('-b', '--benchmark', action='store_true',
                        help='运行基准测试模式，对每种方法运行多次并取平均值')
    parser.add_argument('-c', '--benchmark-count', type=int, default=3,
                        help='基准测试模式下每种方法运行的次数 (默认: 3)')
    
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_arguments()
    
    # 获取要计算的斐波那契数
    n = args.n
    
    # 获取所有可用的计算方法
    all_methods = get_available_methods()
    
    # 筛选用户指定的方法
    selected_methods = {name: method for name, method in all_methods.items() if name in args.methods}
    
    # 如果指定了递归方法，确保n不超过递归限制
    if 'recursive' in selected_methods and n > args.recursive_limit:
        print(f"警告: 递归方法限制为最大计算第{args.recursive_limit}项，对于递归方法将使用n={args.recursive_limit}")
    
    # 确定进程数量
    process_count = args.processes if args.processes is not None else len(selected_methods)
    
    # 创建结果队列
    result_queue = mp.Queue()
    
    if args.benchmark:
        print(f"运行基准测试模式，每种方法运行{args.benchmark_count}次...")
        run_benchmark(selected_methods, n, args.recursive_limit, args.benchmark_count, result_queue)
    else:
        print(f"开始计算斐波那契数 F({n})...")
        run_single(selected_methods, n, args.recursive_limit, result_queue)


def run_single(methods, n, recursive_limit, result_queue):
    """运行单次计算"""
    processes = []
    
    # 创建并启动进程
    process_id = 0
    for method_name, method in methods.items():
        # 对于递归方法，限制n的大小
        actual_n = min(n, recursive_limit) if method_name == 'recursive' else n
        
        p = mp.Process(
            target=worker_process,
            args=(method, actual_n, result_queue, f"{method_name}进程", process_id)
        )
        processes.append(p)
        process_id += 1
    
    # 启动所有进程
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
    print("-" * 100)
    print(f"{'进程名称':<15} {'实现方法':<20} {'n值':<5} {'结果':<15} {'执行时间(秒)':<15} {'内存使用(MB)':<15}")
    print("-" * 100)
    
    for r in results:
        print(f"{r['process_name']:<15} {r['method']:<20} {r['n']:<5} {r['result']:<15} {r['time']:<15.6f} {r['memory']:<15.6f}")


def run_benchmark(methods, n, recursive_limit, count, result_queue):
    """运行基准测试模式"""
    benchmark_results = {}
    
    for i in range(count):
        print(f"运行第 {i+1}/{count} 轮...")
        
        processes = []
        process_id = 0
        
        # 创建并启动进程
        for method_name, method in methods.items():
            # 对于递归方法，限制n的大小
            actual_n = min(n, recursive_limit) if method_name == 'recursive' else n
            
            p = mp.Process(
                target=worker_process,
                args=(method, actual_n, result_queue, f"{method_name}进程", process_id)
            )
            processes.append(p)
            process_id += 1
        
        # 启动所有进程
        for p in processes:
            p.start()
        
        # 等待所有进程完成
        for p in processes:
            p.join()
        
        # 收集结果
        while not result_queue.empty():
            result = result_queue.get()
            method_name = result['method']
            
            if method_name not in benchmark_results:
                benchmark_results[method_name] = {
                    'process_name': result['process_name'],
                    'method': method_name,
                    'n': result['n'],
                    'result': result['result'],
                    'times': [],
                    'memories': []
                }
            
            benchmark_results[method_name]['times'].append(result['time'])
            benchmark_results[method_name]['memories'].append(result['memory'])
    
    # 计算平均值并打印结果
    print("\n基准测试结果:")
    print("-" * 120)
    print(f"{'实现方法':<20} {'n值':<5} {'结果':<15} {'平均执行时间(秒)':<20} {'最短时间(秒)':<15} {'最长时间(秒)':<15} {'平均内存(MB)':<15}")
    print("-" * 120)
    
    # 按平均执行时间排序
    sorted_results = sorted(benchmark_results.values(), key=lambda x: sum(x['times'])/len(x['times']))
    
    for r in sorted_results:
        avg_time = sum(r['times']) / len(r['times'])
        min_time = min(r['times'])
        max_time = max(r['times'])
        avg_memory = sum(r['memories']) / len(r['memories'])
        
        print(f"{r['method']:<20} {r['n']:<5} {r['result']:<15} {avg_time:<20.6f} {min_time:<15.6f} {max_time:<15.6f} {avg_memory:<15.6f}")


if __name__ == "__main__":
    # 设置启动方法为spawn，确保跨平台兼容性
    mp.set_start_method('spawn', force=True)
    main() 