"""
命令解析模块测试
"""
import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.command_parser import CommandParser

class TestCommandParser(unittest.TestCase):
    """命令解析器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.parser = CommandParser()
    
    def test_direct_match_volume_increase(self):
        """测试音量增加命令的直接匹配"""
        test_cases = [
            "声音大一点",
            "音量调高",
            "声音增加",
            "音量调大"
        ]
        
        for voice_text in test_cases:
            with self.subTest(voice_text=voice_text):
                result = self.parser.parse_voice_command(voice_text)
                self.assertIsNotNone(result)
                self.assertEqual(result["command"], "adjust_volume")
                self.assertEqual(result["parameters"]["action"], "increase")
    
    def test_direct_match_volume_decrease(self):
        """测试音量减少命令的直接匹配"""
        test_cases = [
            "声音小一点",
            "音量调低",
            "声音减少",
            "音量调小"
        ]
        
        for voice_text in test_cases:
            with self.subTest(voice_text=voice_text):
                result = self.parser.parse_voice_command(voice_text)
                self.assertIsNotNone(result)
                self.assertEqual(result["command"], "adjust_volume")
                self.assertEqual(result["parameters"]["action"], "decrease")
    
    def test_direct_match_music_control(self):
        """测试音乐控制命令的直接匹配"""
        # 播放音乐
        play_cases = ["播放音乐", "放首歌", "听音乐"]
        for voice_text in play_cases:
            with self.subTest(voice_text=voice_text):
                result = self.parser.parse_voice_command(voice_text)
                self.assertIsNotNone(result)
                self.assertEqual(result["command"], "play_music")
        
        # 暂停音乐
        pause_cases = ["暂停音乐", "停止播放", "暂停播放"]
        for voice_text in pause_cases:
            with self.subTest(voice_text=voice_text):
                result = self.parser.parse_voice_command(voice_text)
                self.assertIsNotNone(result)
                self.assertEqual(result["command"], "pause_music")
    
    def test_direct_match_system_control(self):
        """测试系统控制命令的直接匹配"""
        # 锁屏
        result = self.parser.parse_voice_command("锁屏")
        self.assertIsNotNone(result)
        self.assertEqual(result["command"], "lock_screen")
        
        # 打开记事本
        result = self.parser.parse_voice_command("打开记事本")
        self.assertIsNotNone(result)
        self.assertEqual(result["command"], "open_app")
        self.assertEqual(result["parameters"]["app_name"], "notepad")
        
        # 打开计算器
        result = self.parser.parse_voice_command("打开计算器")
        self.assertIsNotNone(result)
        self.assertEqual(result["command"], "open_app")
        self.assertEqual(result["parameters"]["app_name"], "calculator")
    
    def test_command_validation(self):
        """测试命令验证功能"""
        # 有效命令
        valid_command = {
            "command": "play_music",
            "parameters": {}
        }
        is_valid, message = self.parser.validate_command(valid_command)
        self.assertTrue(is_valid)
        self.assertEqual(message, "命令验证通过")
        
        # 无效命令 - 缺少字段
        invalid_command = {
            "command": "play_music"
            # 缺少 parameters 字段
        }
        is_valid, message = self.parser.validate_command(invalid_command)
        self.assertFalse(is_valid)
        self.assertIn("缺少必需字段", message)
        
        # 无效命令 - 命令为空
        invalid_command = {
            "command": None,
            "parameters": {}
        }
        is_valid, message = self.parser.validate_command(invalid_command)
        self.assertFalse(is_valid)
        self.assertIn("命令类型不能为空", message)
    
    def test_get_available_commands(self):
        """测试获取可用命令列表"""
        commands = self.parser.get_available_commands()
        self.assertIsInstance(commands, dict)
        self.assertIn("媒体控制", commands)
        self.assertIn("系统控制", commands)
        self.assertIn("应用操作", commands)
        self.assertIn("文件操作", commands)
        
        # 检查每个类别都有命令
        for category, command_list in commands.items():
            self.assertIsInstance(command_list, list)
            self.assertGreater(len(command_list), 0)
    
    def test_empty_voice_input(self):
        """测试空语音输入"""
        result = self.parser.parse_voice_command("")
        self.assertIsNotNone(result)
        self.assertIsNone(result["command"])
        self.assertIn("无语音输入", result["error"])
        
        result = self.parser.parse_voice_command(None)
        self.assertIsNotNone(result)
        self.assertIsNone(result["command"])
        self.assertIn("无语音输入", result["error"])

if __name__ == "__main__":
    unittest.main()
