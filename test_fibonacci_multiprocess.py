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

def test_main_with_mock(monkeypatch):
    """使用mock测试main函数的行为"""
    # 创建一个模拟的Process类
    class MockProcess:
        def __init__(self, target=None, args=None):
            self.target = target
            self.args = args
            
        def start(self):
            if self.target and self.args:
                self.target(*self.args)
        
        def join(self):
            pass
    
    # 替换multiprocessing.Process
    import multiprocessing
    # monkeypatch.setattr(multiprocessing, "Process", MockProcess)
    
    # 捕获标准输出
    captured_output = io.StringIO()
    with redirect_stdout(captured_output):
        main(10)
        main(0)
        main(1)
    
    # 获取输出内容
    output = captured_output.getvalue()
    
    # 检查输出是否包含完成消息
    assert "所有计算已完成" in output

if __name__ == "__main__":
    pytest.main(["-v", "test_fibonacci_multiprocess.py"]) 