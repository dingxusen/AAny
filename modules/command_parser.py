"""
指令解析模块
负责将语音指令解析为可执行的命令
"""
import re
import json
import logging
from openai import OpenAI
from config.settings import COMMAND_TEMPLATES
from config.api_keys import OPENAI_API_KEY

logger = logging.getLogger(__name__)

class CommandParser:
    def __init__(self):
        self.llm_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
        self.command_patterns = self._build_command_patterns()
        
    def _build_command_patterns(self):
        """构建命令模式匹配字典"""
        patterns = {}
        for command_type, templates in COMMAND_TEMPLATES.items():
            patterns[command_type] = '|'.join(templates)
        return patterns
    
    def parse_voice_command(self, voice_text):
        """
        解析语音指令
        返回格式：{"command": "命令类型", "parameters": {"参数": "值"}, "confidence": 0.9}
        """
        if not voice_text:
            return {"command": None, "parameters": {}, "confidence": 0, "error": "无语音输入"}
        
        logger.info(f"开始解析指令：{voice_text}")
        
        # 首先尝试模式匹配
        direct_match = self._try_direct_match(voice_text)
        if direct_match:
            return direct_match
        
        # 如果模式匹配失败，使用LLM解析
        if self.llm_client:
            return self._parse_with_llm(voice_text)
        else:
            return {"command": None, "parameters": {}, "confidence": 0, "error": "LLM服务未配置"}
    
    def _try_direct_match(self, voice_text):
        """尝试直接模式匹配"""
        voice_text = voice_text.lower().strip()
        
        # 音量调节
        if re.search(r'音量|声音', voice_text):
            if re.search(r'大|高|增加|调高', voice_text):
                return {
                    "command": "adjust_volume",
                    "parameters": {"action": "increase", "amount": 10},
                    "confidence": 0.9
                }
            elif re.search(r'小|低|减少|调低', voice_text):
                return {
                    "command": "adjust_volume",
                    "parameters": {"action": "decrease", "amount": 10},
                    "confidence": 0.9
                }
        
        # 音乐控制
        if re.search(r'播放音乐|放首歌|听音乐', voice_text):
            return {
                "command": "play_music",
                "parameters": {},
                "confidence": 0.9
            }
        elif re.search(r'暂停音乐|停止播放|暂停播放', voice_text):
            return {
                "command": "pause_music",
                "parameters": {},
                "confidence": 0.9
            }
        
        # 系统控制
        if re.search(r'锁屏|锁定电脑|锁定屏幕', voice_text):
            return {
                "command": "lock_screen",
                "parameters": {},
                "confidence": 0.9
            }
        
        # 应用启动
        if re.search(r'打开记事本|启动记事本', voice_text):
            return {
                "command": "open_app",
                "parameters": {"app_name": "notepad"},
                "confidence": 0.9
            }
        elif re.search(r'打开计算器|启动计算器', voice_text):
            return {
                "command": "open_app",
                "parameters": {"app_name": "calculator"},
                "confidence": 0.9
            }
        elif re.search(r'打开文件管理器|打开文件夹|浏览文件', voice_text):
            return {
                "command": "open_app",
                "parameters": {"app_name": "file_explorer"},
                "confidence": 0.9
            }
        
        return None
    
    def _parse_with_llm(self, voice_text):
        """使用LLM解析复杂指令"""
        try:
            prompt = f"""
            请解析以下语音指令并返回可执行的命令：
            指令：{voice_text}
            
            可用命令类型：
            1. 媒体控制：
               - play_music: 播放音乐
               - pause_music: 暂停音乐
               - next_song: 下一首歌
               - previous_song: 上一首歌
            
            2. 系统控制：
               - adjust_volume: 调节音量 (参数: action: "increase/decrease", amount: 数值)
               - adjust_brightness: 调节亮度 (参数: action: "increase/decrease", amount: 数值)
               - lock_screen: 锁定屏幕
            
            3. 应用操作：
               - open_app: 打开应用 (参数: app_name: "应用名称")
               - close_app: 关闭应用 (参数: app_name: "应用名称")
            
            4. 文件操作：
               - open_folder: 打开文件夹 (参数: path: "路径")
               - search_file: 搜索文件 (参数: filename: "文件名")
            
            请返回JSON格式：{{"command": "命令类型", "parameters": {{"参数": "值"}}, "confidence": 0.9}}
            如果无法理解指令，请返回：{{"command": null, "parameters": {{}}, "confidence": 0, "error": "无法理解的指令"}}
            """
            
            response = self.llm_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content.strip()
            logger.info(f"LLM解析结果：{result_text}")
            
            # 尝试解析JSON响应
            try:
                result = json.loads(result_text)
                return result
            except json.JSONDecodeError:
                # 如果JSON解析失败，尝试提取命令信息
                return self._extract_command_from_text(result_text, voice_text)
                
        except Exception as e:
            logger.error(f"LLM解析失败：{e}")
            return {
                "command": None,
                "parameters": {},
                "confidence": 0,
                "error": f"LLM解析失败：{str(e)}"
            }
    
    def _extract_command_from_text(self, llm_text, original_text):
        """从LLM文本响应中提取命令信息"""
        # 简单的文本提取逻辑
        if "play_music" in llm_text.lower():
            return {"command": "play_music", "parameters": {}, "confidence": 0.7}
        elif "pause_music" in llm_text.lower():
            return {"command": "pause_music", "parameters": {}, "confidence": 0.7}
        elif "lock_screen" in llm_text.lower():
            return {"command": "lock_screen", "parameters": {}, "confidence": 0.7}
        else:
            return {
                "command": None,
                "parameters": {},
                "confidence": 0,
                "error": "无法从LLM响应中提取有效命令"
            }
    
    def get_available_commands(self):
        """获取可用命令列表"""
        return {
            "媒体控制": ["播放音乐", "暂停音乐", "下一首歌", "上一首歌"],
            "系统控制": ["调节音量", "调节亮度", "锁定屏幕"],
            "应用操作": ["打开记事本", "打开计算器", "打开文件管理器"],
            "文件操作": ["打开文件夹", "搜索文件"]
        }
    
    def validate_command(self, command_data):
        """验证命令数据的有效性"""
        required_fields = ["command", "parameters"]
        
        if not isinstance(command_data, dict):
            return False, "命令数据必须是字典格式"
        
        for field in required_fields:
            if field not in command_data:
                return False, f"缺少必需字段：{field}"
        
        command = command_data.get("command")
        if command is None:
            return False, "命令类型不能为空"
        
        return True, "命令验证通过"
