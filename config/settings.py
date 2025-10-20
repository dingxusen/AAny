"""
应用配置文件
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API配置
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
AZURE_SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION', 'eastus')

# 应用配置
APP_NAME = "Voice Control Assistant"
APP_VERSION = "1.0.0"

# 语音配置
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
CHANNELS = 1
AUDIO_FORMAT = 'int16'

# 系统配置
PLATFORM = os.name
SUPPORTED_PLATFORMS = ['nt', 'posix', 'java']

# 日志配置
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# 命令配置
COMMAND_TIMEOUT = 30  # 命令执行超时时间（秒）
MAX_RETRY_ATTEMPTS = 3  # 最大重试次数

# 常用应用程序路径
APPLICATION_PATHS = {
    'notepad': 'notepad.exe',
    'calculator': 'calc.exe',
    'file_explorer': 'explorer.exe',
    'browser': 'chrome.exe',  # 可根据用户安装的浏览器调整
    'music_player': 'wmplayer.exe',
    'task_manager': 'taskmgr.exe'
}

# 语音命令模板
COMMAND_TEMPLATES = {
    'play_music': ['播放音乐', '放首歌', '听音乐', '播放歌曲'],
    'pause_music': ['暂停音乐', '停止播放', '暂停播放'],
    'adjust_volume': ['调节音量', '声音大点', '声音小点', '音量调高', '音量调低'],
    'open_folder': ['打开文件夹', '打开目录', '浏览文件夹'],
    'search_file': ['搜索文件', '查找文件', '找文件'],
    'lock_screen': ['锁屏', '锁定电脑', '锁定屏幕'],
    'adjust_brightness': ['调节亮度', '屏幕亮一点', '屏幕暗一点', '亮度调高', '亮度调低']
}
