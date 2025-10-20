#!/usr/bin/env python3
"""
语音控制助手安装脚本
"""
import os
import sys
import subprocess
import platform

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("错误：需要Python 3.8或更高版本")
        print(f"当前版本：{sys.version}")
        return False
    print(f"Python版本检查通过：{sys.version}")
    return True

def install_dependencies():
    """安装依赖包"""
    print("正在安装依赖包...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"依赖包安装失败：{e}")
        return False

def setup_environment():
    """设置环境"""
    print("正在设置环境...")
    
    # 创建必要的目录
    directories = ['logs', 'config']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"创建目录：{directory}")
    
    # 检查环境变量文件
    if not os.path.exists('.env'):
        if os.path.exists('env_example.txt'):
            print("请复制 env_example.txt 为 .env 并填入您的API密钥")
        else:
            print("请创建 .env 文件并配置API密钥")
    
    return True

def check_system_requirements():
    """检查系统要求"""
    print("检查系统要求...")
    
    system = platform.system()
    print(f"操作系统：{system}")
    
    # 检查麦克风设备（Windows）
    if system == "Windows":
        try:
            import pyaudio
            audio = pyaudio.PyAudio()
            device_count = audio.get_device_count()
            print(f"音频设备数量：{device_count}")
            audio.terminate()
        except ImportError:
            print("警告：pyaudio未安装，可能影响麦克风功能")
        except Exception as e:
            print(f"音频设备检查失败：{e}")
    
    return True

def main():
    """主函数"""
    print("语音控制助手安装程序")
    print("=" * 40)
    
    # 检查Python版本
    if not check_python_version():
        return 1
    
    # 检查系统要求
    if not check_system_requirements():
        print("系统要求检查失败")
        return 1
    
    # 安装依赖包
    if not install_dependencies():
        return 1
    
    # 设置环境
    if not setup_environment():
        return 1
    
    print("\n安装完成！")
    print("下一步：")
    print("1. 配置 .env 文件中的API密钥")
    print("2. 运行 python start.py --mode gui 启动图形界面")
    print("3. 或运行 python start.py 启动命令行界面")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
