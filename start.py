#!/usr/bin/env python3
"""
语音控制助手启动脚本
"""
import sys
import os
import argparse

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='语音控制助手启动脚本')
    parser.add_argument('--mode', choices=['cli', 'gui'], default='cli',
                       help='运行模式：cli(命令行) 或 gui(图形界面)')
    parser.add_argument('--test', action='store_true',
                       help='运行测试模式')
    parser.add_argument('--debug', action='store_true',
                       help='启用调试模式')
    
    args = parser.parse_args()
    
    # 设置调试模式
    if args.debug:
        os.environ['LOG_LEVEL'] = 'DEBUG'
    
    try:
        if args.test:
            # 运行测试
            import subprocess
            result = subprocess.run([sys.executable, '-m', 'pytest', 'tests/'], 
                                  capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("错误信息：", result.stderr)
            return result.returncode
        
        elif args.mode == 'gui':
            # 启动GUI模式
            from gui.app import main as gui_main
            gui_main()
        
        else:
            # 启动命令行模式
            from main import main as cli_main
            return cli_main()
            
    except ImportError as e:
        print(f"导入错误：{e}")
        print("请确保已安装所有依赖包：pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"启动失败：{e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
