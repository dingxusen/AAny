"""
系统工具模块
"""
import os
import platform
import subprocess
import psutil
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class SystemUtils:
    """系统工具类"""
    
    @staticmethod
    def get_system_info() -> Dict:
        """获取系统信息"""
        try:
            info = {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "architecture": platform.architecture()[0],
                "processor": platform.processor(),
                "hostname": platform.node(),
                "python_version": platform.python_version(),
                "cpu_count": psutil.cpu_count(),
                "memory_total": psutil.virtual_memory().total,
                "memory_available": psutil.virtual_memory().available
            }
            return info
        except Exception as e:
            logger.error(f"获取系统信息失败：{e}")
            return {}
    
    @staticmethod
    def get_running_processes() -> List[Dict]:
        """获取正在运行的进程列表"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    proc_info = proc.info
                    processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # 按CPU使用率排序
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            return processes[:20]  # 返回前20个进程
        except Exception as e:
            logger.error(f"获取进程列表失败：{e}")
            return []
    
    @staticmethod
    def is_process_running(process_name: str) -> bool:
        """检查指定进程是否正在运行"""
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() == process_name.lower():
                    return True
            return False
        except Exception as e:
            logger.error(f"检查进程运行状态失败：{e}")
            return False
    
    @staticmethod
    def kill_process(process_name: str) -> bool:
        """终止指定进程"""
        try:
            killed_count = 0
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() == process_name.lower():
                    proc.terminate()
                    killed_count += 1
            
            return killed_count > 0
        except Exception as e:
            logger.error(f"终止进程失败：{e}")
            return False
    
    @staticmethod
    def get_volume_level() -> Optional[int]:
        """获取当前音量级别（仅Windows）"""
        try:
            if platform.system() == "Windows":
                # 使用PowerShell获取音量
                result = subprocess.run(
                    ["powershell", "-Command", "[Audio]::Volume * 100"],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    return int(float(result.stdout.strip()))
            return None
        except Exception as e:
            logger.error(f"获取音量级别失败：{e}")
            return None
    
    @staticmethod
    def set_volume_level(level: int) -> bool:
        """设置音量级别（仅Windows）"""
        try:
            if platform.system() == "Windows":
                level = max(0, min(100, level))  # 限制在0-100之间
                result = subprocess.run(
                    ["powershell", "-Command", f"[Audio]::Volume = {level / 100}"],
                    timeout=5
                )
                return result.returncode == 0
            return False
        except Exception as e:
            logger.error(f"设置音量级别失败：{e}")
            return False
    
    @staticmethod
    def get_brightness_level() -> Optional[int]:
        """获取屏幕亮度级别"""
        try:
            if platform.system() == "Darwin":  # macOS
                result = subprocess.run(
                    ["osascript", "-e", "brightness of (get display settings)"],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    return int(float(result.stdout.strip()) * 100)
            return None
        except Exception as e:
            logger.error(f"获取亮度级别失败：{e}")
            return None
    
    @staticmethod
    def set_brightness_level(level: int) -> bool:
        """设置屏幕亮度级别"""
        try:
            if platform.system() == "Darwin":  # macOS
                level = max(0, min(100, level))  # 限制在0-100之间
                result = subprocess.run(
                    ["osascript", "-e", f"set brightness of (get display settings) to {level / 100}"],
                    timeout=5
                )
                return result.returncode == 0
            return False
        except Exception as e:
            logger.error(f"设置亮度级别失败：{e}")
            return False
    
    @staticmethod
    def get_installed_applications() -> List[str]:
        """获取已安装的应用程序列表"""
        try:
            apps = []
            if platform.system() == "Windows":
                # Windows: 从注册表获取已安装程序
                try:
                    result = subprocess.run(
                        ["powershell", "-Command", 
                         "Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName"],
                        capture_output=True, text=True, timeout=30
                    )
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')[2:]  # 跳过标题行
                        for line in lines:
                            if line.strip():
                                apps.append(line.strip())
                except Exception:
                    pass
            
            elif platform.system() == "Darwin":  # macOS
                # macOS: 从Applications文件夹获取
                try:
                    apps_dir = "/Applications"
                    for item in os.listdir(apps_dir):
                        if item.endswith('.app'):
                            apps.append(item.replace('.app', ''))
                except Exception:
                    pass
            
            return sorted(apps)
        except Exception as e:
            logger.error(f"获取已安装应用程序失败：{e}")
            return []
    
    @staticmethod
    def find_application_path(app_name: str) -> Optional[str]:
        """查找应用程序的安装路径"""
        try:
            if platform.system() == "Windows":
                # Windows: 在PATH和常见安装目录中搜索
                search_paths = [
                    os.environ.get('PROGRAMFILES', 'C:\\Program Files'),
                    os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'),
                    os.path.expanduser('~\\AppData\\Local\\Programs'),
                ]
                
                for search_path in search_paths:
                    if os.path.exists(search_path):
                        for root, dirs, files in os.walk(search_path):
                            for file in files:
                                if file.lower() == f"{app_name.lower()}.exe":
                                    return os.path.join(root, file)
            
            elif platform.system() == "Darwin":  # macOS
                # macOS: 在Applications文件夹中搜索
                apps_dir = "/Applications"
                app_path = os.path.join(apps_dir, f"{app_name}.app")
                if os.path.exists(app_path):
                    return app_path
            
            return None
        except Exception as e:
            logger.error(f"查找应用程序路径失败：{e}")
            return None
    
    @staticmethod
    def create_shortcut(name: str, target: str, description: str = "") -> bool:
        """创建快捷方式（仅Windows）"""
        try:
            if platform.system() == "Windows":
                import winshell
                from win32com.client import Dispatch
                
                desktop = winshell.desktop()
                path = os.path.join(desktop, f"{name}.lnk")
                target = os.path.join(target)
                wDir = os.path.dirname(target)
                icon = target
                
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(path)
                shortcut.Targetpath = target
                shortcut.WorkingDirectory = wDir
                shortcut.IconLocation = icon
                shortcut.Description = description
                shortcut.save()
                
                return True
            return False
        except Exception as e:
            logger.error(f"创建快捷方式失败：{e}")
            return False
