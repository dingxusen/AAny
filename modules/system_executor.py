"""
系统执行模块
负责执行解析后的命令
"""
import os
import subprocess
import platform
import logging
import time
import threading
from config.settings import APPLICATION_PATHS, COMMAND_TIMEOUT
import psutil

logger = logging.getLogger(__name__)

class SystemExecutor:
    def __init__(self):
        self.platform = platform.system()
        self.applications = APPLICATION_PATHS.copy()
        self.running_processes = {}
        
    def execute_command(self, command_data):
        """
        执行解析后的命令
        返回格式：{"success": True/False, "message": "执行结果", "data": {}}
        """
        if not command_data or not command_data.get("command"):
            return {"success": False, "message": "无效的命令数据"}
        
        command_type = command_data.get("command")
        parameters = command_data.get("parameters", {})
        
        logger.info(f"执行命令：{command_type}, 参数：{parameters}")
        
        try:
            # 根据命令类型执行相应操作
            if command_type == "play_music":
                return self.play_music(parameters)
            elif command_type == "pause_music":
                return self.pause_music(parameters)
            elif command_type == "adjust_volume":
                return self.adjust_volume(parameters)
            elif command_type == "adjust_brightness":
                return self.adjust_brightness(parameters)
            elif command_type == "open_app":
                return self.open_application(parameters)
            elif command_type == "close_app":
                return self.close_application(parameters)
            elif command_type == "lock_screen":
                return self.lock_screen()
            elif command_type == "open_folder":
                return self.open_folder(parameters)
            elif command_type == "search_file":
                return self.search_file(parameters)
            else:
                return {"success": False, "message": f"未知命令类型：{command_type}"}
                
        except Exception as e:
            logger.error(f"命令执行失败：{e}")
            return {"success": False, "message": f"执行失败：{str(e)}"}
    
    def play_music(self, params):
        """播放音乐"""
        try:
            if self.platform == "Windows":
                # Windows系统播放音乐
                # 这里可以集成具体的音乐播放器
                result = subprocess.run(
                    ["powershell", "-Command", "Get-Process | Where-Object {$_.ProcessName -eq 'wmplayer'}"],
                    capture_output=True, text=True, timeout=COMMAND_TIMEOUT
                )
                
                if "wmplayer" in result.stdout:
                    # 如果Windows Media Player正在运行，发送播放命令
                    subprocess.run(
                        ["powershell", "-Command", "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{SPACE}')"],
                        timeout=COMMAND_TIMEOUT
                    )
                    return {"success": True, "message": "音乐播放命令已发送"}
                else:
                    # 启动Windows Media Player
                    subprocess.Popen(["wmplayer.exe"], shell=True)
                    return {"success": True, "message": "正在启动音乐播放器"}
            
            elif self.platform == "Darwin":  # macOS
                os.system("osascript -e 'tell application \"Music\" to play'")
                return {"success": True, "message": "开始播放音乐"}
            
            else:
                return {"success": False, "message": f"不支持的操作系统：{self.platform}"}
                
        except Exception as e:
            logger.error(f"播放音乐失败：{e}")
            return {"success": False, "message": f"播放音乐失败：{str(e)}"}
    
    def pause_music(self, params):
        """暂停音乐"""
        try:
            if self.platform == "Windows":
                # 发送空格键暂停/播放
                subprocess.run(
                    ["powershell", "-Command", "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{SPACE}')"],
                    timeout=COMMAND_TIMEOUT
                )
                return {"success": True, "message": "音乐暂停/播放命令已发送"}
            
            elif self.platform == "Darwin":
                os.system("osascript -e 'tell application \"Music\" to pause'")
                return {"success": True, "message": "音乐已暂停"}
            
            else:
                return {"success": False, "message": f"不支持的操作系统：{self.platform}"}
                
        except Exception as e:
            logger.error(f"暂停音乐失败：{e}")
            return {"success": False, "message": f"暂停音乐失败：{str(e)}"}
    
    def adjust_volume(self, params):
        """调节音量"""
        try:
            action = params.get("action", "increase")
            amount = params.get("amount", 10)
            
            if self.platform == "Windows":
                # 使用Windows音量控制
                if action == "increase":
                    for _ in range(amount // 2):  # 每次增加2%
                        subprocess.run(["powershell", "-Command", "[Audio]::Volume += 0.02"], shell=True)
                elif action == "decrease":
                    for _ in range(amount // 2):  # 每次减少2%
                        subprocess.run(["powershell", "-Command", "[Audio]::Volume -= 0.02"], shell=True)
                
                return {"success": True, "message": f"音量已{action}"}
            
            elif self.platform == "Darwin":
                # macOS音量控制
                current_volume = self._get_current_volume_mac()
                if action == "increase":
                    new_volume = min(100, current_volume + amount)
                else:
                    new_volume = max(0, current_volume - amount)
                
                os.system(f"osascript -e 'set volume output volume {new_volume}'")
                return {"success": True, "message": f"音量已调节至{new_volume}%"}
            
            else:
                return {"success": False, "message": f"不支持的操作系统：{self.platform}"}
                
        except Exception as e:
            logger.error(f"调节音量失败：{e}")
            return {"success": False, "message": f"调节音量失败：{str(e)}"}
    
    def adjust_brightness(self, params):
        """调节亮度"""
        try:
            action = params.get("action", "increase")
            amount = params.get("amount", 10)
            
            if self.platform == "Windows":
                # Windows亮度控制需要额外的库支持
                return {"success": False, "message": "Windows亮度控制需要额外配置"}
            
            elif self.platform == "Darwin":
                # macOS亮度控制
                if action == "increase":
                    os.system("osascript -e 'tell application \"System Events\" to key code 144'")  # F2键
                else:
                    os.system("osascript -e 'tell application \"System Events\" to key code 145'")  # F1键
                
                return {"success": True, "message": f"亮度已{action}"}
            
            else:
                return {"success": False, "message": f"不支持的操作系统：{self.platform}"}
                
        except Exception as e:
            logger.error(f"调节亮度失败：{e}")
            return {"success": False, "message": f"调节亮度失败：{str(e)}"}
    
    def open_application(self, params):
        """打开应用程序"""
        try:
            app_name = params.get("app_name")
            if not app_name:
                return {"success": False, "message": "未指定应用程序名称"}
            
            if app_name in self.applications:
                app_path = self.applications[app_name]
                
                # 检查应用程序是否已经在运行
                if self._is_app_running(app_name):
                    return {"success": True, "message": f"{app_name}已经在运行"}
                
                # 启动应用程序
                if self.platform == "Windows":
                    subprocess.Popen([app_path], shell=True)
                else:
                    subprocess.Popen([app_path])
                
                # 记录运行状态
                self.running_processes[app_name] = time.time()
                
                return {"success": True, "message": f"正在打开{app_name}"}
            else:
                return {"success": False, "message": f"找不到应用程序：{app_name}"}
                
        except Exception as e:
            logger.error(f"打开应用程序失败：{e}")
            return {"success": False, "message": f"打开应用程序失败：{str(e)}"}
    
    def close_application(self, params):
        """关闭应用程序"""
        try:
            app_name = params.get("app_name")
            if not app_name:
                return {"success": False, "message": "未指定应用程序名称"}
            
            if app_name in self.applications:
                app_path = self.applications[app_name]
                process_name = os.path.basename(app_path).replace('.exe', '')
                
                # 查找并关闭进程
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['name'].lower() == process_name.lower():
                        proc.terminate()
                        proc.wait(timeout=5)
                        
                        if app_name in self.running_processes:
                            del self.running_processes[app_name]
                        
                        return {"success": True, "message": f"{app_name}已关闭"}
                
                return {"success": True, "message": f"{app_name}未在运行"}
            else:
                return {"success": False, "message": f"找不到应用程序：{app_name}"}
                
        except Exception as e:
            logger.error(f"关闭应用程序失败：{e}")
            return {"success": False, "message": f"关闭应用程序失败：{str(e)}"}
    
    def lock_screen(self):
        """锁定屏幕"""
        try:
            if self.platform == "Windows":
                subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], timeout=COMMAND_TIMEOUT)
                return {"success": True, "message": "屏幕已锁定"}
            
            elif self.platform == "Darwin":
                os.system("osascript -e 'tell application \"System Events\" to keystroke \"q\" using {command down, control down}'")
                return {"success": True, "message": "屏幕已锁定"}
            
            else:
                return {"success": False, "message": f"不支持的操作系统：{self.platform}"}
                
        except Exception as e:
            logger.error(f"锁定屏幕失败：{e}")
            return {"success": False, "message": f"锁定屏幕失败：{str(e)}"}
    
    def open_folder(self, params):
        """打开文件夹"""
        try:
            folder_path = params.get("path", "")
            
            if self.platform == "Windows":
                if folder_path:
                    subprocess.Popen(["explorer.exe", folder_path])
                    return {"success": True, "message": f"正在打开文件夹：{folder_path}"}
                else:
                    subprocess.Popen(["explorer.exe"])
                    return {"success": True, "message": "正在打开文件管理器"}
            
            elif self.platform == "Darwin":
                if folder_path:
                    subprocess.Popen(["open", folder_path])
                else:
                    subprocess.Popen(["open", "/"])
                return {"success": True, "message": "正在打开文件夹"}
            
            else:
                return {"success": False, "message": f"不支持的操作系统：{self.platform}"}
                
        except Exception as e:
            logger.error(f"打开文件夹失败：{e}")
            return {"success": False, "message": f"打开文件夹失败：{str(e)}"}
    
    def search_file(self, params):
        """搜索文件"""
        try:
            filename = params.get("filename", "")
            if not filename:
                return {"success": False, "message": "未指定搜索文件名"}
            
            if self.platform == "Windows":
                # 使用Windows搜索功能
                subprocess.run(
                    ["powershell", "-Command", f"Get-ChildItem -Path C:\\ -Name \"{filename}\" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 10"],
                    timeout=30
                )
                return {"success": True, "message": f"正在搜索文件：{filename}"}
            
            elif self.platform == "Darwin":
                # 使用Spotlight搜索
                subprocess.Popen(["open", "-a", "Spotlight"])
                return {"success": True, "message": f"正在搜索文件：{filename}"}
            
            else:
                return {"success": False, "message": f"不支持的操作系统：{self.platform}"}
                
        except Exception as e:
            logger.error(f"搜索文件失败：{e}")
            return {"success": False, "message": f"搜索文件失败：{str(e)}"}
    
    def _is_app_running(self, app_name):
        """检查应用程序是否正在运行"""
        try:
            if app_name in self.applications:
                process_name = os.path.basename(self.applications[app_name]).replace('.exe', '')
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'].lower() == process_name.lower():
                        return True
            return False
        except Exception:
            return False
    
    def _get_current_volume_mac(self):
        """获取macOS当前音量"""
        try:
            result = subprocess.run(
                ["osascript", "-e", "output volume of (get volume settings)"],
                capture_output=True, text=True, timeout=5
            )
            return int(result.stdout.strip())
        except Exception:
            return 50  # 默认音量
    
    def get_system_info(self):
        """获取系统信息"""
        try:
            info = {
                "platform": self.platform,
                "running_apps": list(self.running_processes.keys()),
                "available_commands": list(self.applications.keys())
            }
            return {"success": True, "data": info}
        except Exception as e:
            return {"success": False, "message": f"获取系统信息失败：{str(e)}"}
