import pytest
import io
import sys
import tempfile
import os
from contextlib import redirect_stdout
from fibonacci_multiprocess import main


def test_main_function_runs():
    """测试main函数能否正常运行（不测试输出）"""
    # 使用较小的n值以加快测试速度
    try:
        main(5)
        main(30)
        main(0)
        main(1)
        # 如果没有异常，则测试通过
        assert True
    except Exception as e:
        pytest.fail(f"main函数运行失败: {e}")

if __name__ == "__main__":
    pytest.main(["-v", "test_fibonacci_multiprocess.py"]) 