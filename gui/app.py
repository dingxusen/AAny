"""
语音控制助手 - GUI界面
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from main import VoiceControlAssistant
import logging

logger = logging.getLogger(__name__)

class VoiceControlGUI:
    """语音控制助手GUI界面"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.assistant = None
        self.is_running = False
        
        self.setup_ui()
        self.setup_logging()
    
    def setup_ui(self):
        """设置用户界面"""
        self.root.title("语音控制助手 v1.0.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # 状态显示区域
        self.create_status_frame(main_frame)
        
        # 控制按钮区域
        self.create_control_frame(main_frame)
        
        # 日志显示区域
        self.create_log_frame(main_frame)
        
        # 命令列表区域
        self.create_commands_frame(main_frame)
    
    def create_status_frame(self, parent):
        """创建状态显示区域"""
        status_frame = ttk.LabelFrame(parent, text="系统状态", padding="5")
        status_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 运行状态
        ttk.Label(status_frame, text="运行状态:").grid(row=0, column=0, sticky=tk.W)
        self.status_label = ttk.Label(status_frame, text="未启动", foreground="red")
        self.status_label.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # 麦克风状态
        ttk.Label(status_frame, text="麦克风:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.mic_status_label = ttk.Label(status_frame, text="未检测", foreground="gray")
        self.mic_status_label.grid(row=0, column=3, sticky=tk.W, padx=(5, 0))
        
        # 语音反馈状态
        ttk.Label(status_frame, text="语音反馈:").grid(row=0, column=4, sticky=tk.W, padx=(20, 0))
        self.tts_status_label = ttk.Label(status_frame, text="未配置", foreground="gray")
        self.tts_status_label.grid(row=0, column=5, sticky=tk.W, padx=(5, 0))
    
    def create_control_frame(self, parent):
        """创建控制按钮区域"""
        control_frame = ttk.LabelFrame(parent, text="控制面板", padding="5")
        control_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 启动/停止按钮
        self.start_button = ttk.Button(
            control_frame, 
            text="启动助手", 
            command=self.start_assistant,
            style="Accent.TButton"
        )
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_button = ttk.Button(
            control_frame, 
            text="停止助手", 
            command=self.stop_assistant,
            state="disabled"
        )
        self.stop_button.grid(row=0, column=1, padx=(0, 10))
        
        # 测试按钮
        ttk.Button(
            control_frame, 
            text="测试麦克风", 
            command=self.test_microphone
        ).grid(row=0, column=2, padx=(0, 10))
        
        ttk.Button(
            control_frame, 
            text="测试语音反馈", 
            command=self.test_voice_feedback
        ).grid(row=0, column=3, padx=(0, 10))
        
        # 清空日志按钮
        ttk.Button(
            control_frame, 
            text="清空日志", 
            command=self.clear_log
        ).grid(row=0, column=4)
    
    def create_log_frame(self, parent):
        """创建日志显示区域"""
        log_frame = ttk.LabelFrame(parent, text="运行日志", padding="5")
        log_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # 日志文本框
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            height=15, 
            wrap=tk.WORD,
            state="disabled"
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def create_commands_frame(self, parent):
        """创建命令列表区域"""
        commands_frame = ttk.LabelFrame(parent, text="可用命令", padding="5")
        commands_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        commands_frame.columnconfigure(0, weight=1)
        commands_frame.rowconfigure(0, weight=1)
        
        # 命令列表
        self.commands_text = scrolledtext.ScrolledText(
            commands_frame, 
            height=10, 
            wrap=tk.WORD,
            state="disabled"
        )
        self.commands_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 初始化命令列表
        self.update_commands_list()
    
    def setup_logging(self):
        """设置日志显示"""
        # 创建自定义日志处理器
        class GUILogHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget
            
            def emit(self, record):
                msg = self.format(record)
                def append():
                    self.text_widget.config(state="normal")
                    self.text_widget.insert(tk.END, msg + "\n")
                    self.text_widget.config(state="disabled")
                    self.text_widget.see(tk.END)
                self.text_widget.after(0, append)
        
        # 添加GUI日志处理器
        gui_handler = GUILogHandler(self.log_text)
        gui_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(gui_handler)
    
    def start_assistant(self):
        """启动语音助手"""
        try:
            if self.is_running:
                messagebox.showwarning("警告", "助手已在运行中")
                return
            
            # 在新线程中启动助手
            self.assistant_thread = threading.Thread(
                target=self._start_assistant_thread,
                daemon=True
            )
            self.assistant_thread.start()
            
        except Exception as e:
            logger.error(f"启动助手失败：{e}")
            messagebox.showerror("错误", f"启动助手失败：{str(e)}")
    
    def _start_assistant_thread(self):
        """在新线程中启动助手"""
        try:
            self.assistant = VoiceControlAssistant()
            
            # 更新UI状态
            self.root.after(0, self._update_starting_status)
            
            # 启动助手
            if self.assistant.start():
                self.is_running = True
                self.root.after(0, self._update_running_status)
                logger.info("语音助手启动成功")
            else:
                self.root.after(0, self._update_error_status)
                logger.error("语音助手启动失败")
                
        except Exception as e:
            logger.error(f"启动助手线程失败：{e}")
            self.root.after(0, self._update_error_status)
    
    def stop_assistant(self):
        """停止语音助手"""
        try:
            if not self.is_running or not self.assistant:
                messagebox.showwarning("警告", "助手未在运行")
                return
            
            # 停止助手
            self.assistant.stop()
            self.is_running = False
            
            # 更新UI状态
            self._update_stopped_status()
            logger.info("语音助手已停止")
            
        except Exception as e:
            logger.error(f"停止助手失败：{e}")
            messagebox.showerror("错误", f"停止助手失败：{str(e)}")
    
    def test_microphone(self):
        """测试麦克风"""
        try:
            if not self.assistant:
                self.assistant = VoiceControlAssistant()
            
            # 在新线程中测试麦克风
            def test_thread():
                try:
                    if self.assistant.voice_input.test_microphone():
                        self.root.after(0, lambda: messagebox.showinfo("测试结果", "麦克风测试成功"))
                    else:
                        self.root.after(0, lambda: messagebox.showerror("测试结果", "麦克风测试失败"))
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("测试结果", f"麦克风测试异常：{str(e)}"))
            
            threading.Thread(target=test_thread, daemon=True).start()
            
        except Exception as e:
            logger.error(f"测试麦克风失败：{e}")
            messagebox.showerror("错误", f"测试麦克风失败：{str(e)}")
    
    def test_voice_feedback(self):
        """测试语音反馈"""
        try:
            if not self.assistant:
                self.assistant = VoiceControlAssistant()
            
            self.assistant.voice_feedback.test_speech()
            logger.info("语音反馈测试已发送")
            
        except Exception as e:
            logger.error(f"测试语音反馈失败：{e}")
            messagebox.showerror("错误", f"测试语音反馈失败：{str(e)}")
    
    def clear_log(self):
        """清空日志"""
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")
    
    def update_commands_list(self):
        """更新命令列表"""
        try:
            if not self.assistant:
                self.assistant = VoiceControlAssistant()
            
            commands = self.assistant.command_parser.get_available_commands()
            
            self.commands_text.config(state="normal")
            self.commands_text.delete(1.0, tk.END)
            
            for category, command_list in commands.items():
                self.commands_text.insert(tk.END, f"{category}：\n")
                for command in command_list:
                    self.commands_text.insert(tk.END, f"  • {command}\n")
                self.commands_text.insert(tk.END, "\n")
            
            self.commands_text.config(state="disabled")
            
        except Exception as e:
            logger.error(f"更新命令列表失败：{e}")
    
    def _update_starting_status(self):
        """更新启动中状态"""
        self.status_label.config(text="启动中...", foreground="orange")
        self.start_button.config(state="disabled")
        self.stop_button.config(state="disabled")
    
    def _update_running_status(self):
        """更新运行中状态"""
        self.status_label.config(text="运行中", foreground="green")
        self.start_button.config(state="disabled")
        self.stop_button.config(state="enabled")
        self.mic_status_label.config(text="已激活", foreground="green")
        self.tts_status_label.config(text="已配置", foreground="green")
    
    def _update_stopped_status(self):
        """更新已停止状态"""
        self.status_label.config(text="已停止", foreground="red")
        self.start_button.config(state="enabled")
        self.stop_button.config(state="disabled")
        self.mic_status_label.config(text="未激活", foreground="gray")
    
    def _update_error_status(self):
        """更新错误状态"""
        self.status_label.config(text="启动失败", foreground="red")
        self.start_button.config(state="enabled")
        self.stop_button.config(state="disabled")
    
    def run(self):
        """运行GUI应用"""
        try:
            # 设置关闭事件处理
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # 启动GUI主循环
            self.root.mainloop()
            
        except Exception as e:
            logger.error(f"GUI运行异常：{e}")
    
    def on_closing(self):
        """处理窗口关闭事件"""
        try:
            if self.is_running and self.assistant:
                self.assistant.stop()
            
            self.root.destroy()
            
        except Exception as e:
            logger.error(f"关闭应用失败：{e}")

def main():
    """GUI主函数"""
    try:
        app = VoiceControlGUI()
        app.run()
    except Exception as e:
        print(f"GUI应用启动失败：{e}")

if __name__ == "__main__":
    main()
