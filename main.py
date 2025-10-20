"""
语音控制电脑应用 - 主程序
"""
import sys
import time
import signal
import logging
from modules.voice_input import VoiceInputModule
from modules.command_parser import CommandParser
from modules.system_executor import SystemExecutor
from modules.voice_feedback import VoiceFeedback
from utils.logger import setup_logger, get_log_file_path
from config.settings import APP_NAME, APP_VERSION

# 设置日志
logger = setup_logger(
    name="VoiceControlAssistant",
    log_file=get_log_file_path()
)

class VoiceControlAssistant:
    """语音控制助手主类"""
    
    def __init__(self):
        self.voice_input = VoiceInputModule()
        self.command_parser = CommandParser()
        self.system_executor = SystemExecutor()
        self.voice_feedback = VoiceFeedback()
        self.is_running = False
        
        # 注册信号处理器
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info(f"{APP_NAME} v{APP_VERSION} 初始化完成")
    
    def start(self):
        """启动语音控制助手"""
        try:
            logger.info("正在启动语音控制助手...")
            
            # 测试麦克风
            if not self.voice_input.setup_microphone():
                logger.error("麦克风初始化失败，请检查设备连接")
                self.voice_feedback.speak("麦克风初始化失败，请检查设备连接")
                return False
            
            # 播报欢迎信息
            self.voice_feedback.speak_welcome()
            
            # 开始监听语音输入
            if not self.voice_input.start_listening(self._handle_voice_input):
                logger.error("语音监听启动失败")
                return False
            
            self.is_running = True
            logger.info("语音控制助手已启动，等待语音指令...")
            
            # 主循环
            self._main_loop()
            
            return True
            
        except Exception as e:
            logger.error(f"启动失败：{e}")
            self.voice_feedback.speak_error(f"启动失败：{str(e)}")
            return False
    
    def stop(self):
        """停止语音控制助手"""
        try:
            logger.info("正在停止语音控制助手...")
            self.is_running = False
            
            # 停止语音输入
            self.voice_input.stop_listening_input()
            
            # 清空语音队列
            self.voice_feedback.clear_queue()
            
            # 播报告别信息
            self.voice_feedback.speak_goodbye()
            
            logger.info("语音控制助手已停止")
            
        except Exception as e:
            logger.error(f"停止失败：{e}")
    
    def _main_loop(self):
        """主循环"""
        try:
            while self.is_running:
                time.sleep(0.1)  # 短暂休眠，避免CPU占用过高
                
                # 可以在这里添加其他需要定期执行的任务
                # 例如：检查系统状态、更新配置等
                
        except KeyboardInterrupt:
            logger.info("收到键盘中断信号")
        except Exception as e:
            logger.error(f"主循环异常：{e}")
        finally:
            self.stop()
    
    def _handle_voice_input(self, voice_text, error_message=None):
        """处理语音输入"""
        try:
            if error_message:
                logger.warning(f"语音识别错误：{error_message}")
                self.voice_feedback.speak(f"抱歉，{error_message}")
                return
            
            if not voice_text:
                logger.debug("未识别到语音内容")
                return
            
            logger.info(f"收到语音指令：{voice_text}")
            
            # 解析语音指令
            command_data = self.command_parser.parse_voice_command(voice_text)
            
            if not command_data.get("command"):
                logger.warning(f"无法解析指令：{voice_text}")
                self.voice_feedback.speak("抱歉，我没有理解您的指令，请重试")
                return
            
            # 验证命令
            is_valid, message = self.command_parser.validate_command(command_data)
            if not is_valid:
                logger.warning(f"命令验证失败：{message}")
                self.voice_feedback.speak(f"命令无效：{message}")
                return
            
            # 执行命令
            logger.info(f"执行命令：{command_data}")
            result = self.system_executor.execute_command(command_data)
            
            # 播报执行结果
            self.voice_feedback.speak_command_result(result)
            
        except Exception as e:
            logger.error(f"处理语音输入失败：{e}")
            self.voice_feedback.speak_error(f"处理指令失败：{str(e)}")
    
    def _signal_handler(self, signum, frame):
        """信号处理器"""
        logger.info(f"收到信号 {signum}，正在关闭应用...")
        self.stop()
        sys.exit(0)
    
    def get_status(self):
        """获取应用状态"""
        return {
            "is_running": self.is_running,
            "voice_input_status": self.voice_input.is_listening,
            "voice_feedback_status": self.voice_feedback.get_status(),
            "available_commands": self.command_parser.get_available_commands()
        }

def main():
    """主函数"""
    try:
        print(f"欢迎使用 {APP_NAME} v{APP_VERSION}")
        print("正在初始化...")
        
        # 创建并启动助手
        assistant = VoiceControlAssistant()
        
        # 启动助手
        if assistant.start():
            print("语音控制助手已启动")
            print("请说出您的指令，或按 Ctrl+C 退出")
        else:
            print("语音控制助手启动失败")
            return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n收到中断信号，正在退出...")
        return 0
    except Exception as e:
        print(f"程序运行异常：{e}")
        logger.error(f"程序运行异常：{e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
