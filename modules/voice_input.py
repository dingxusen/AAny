"""
语音输入模块
负责录音和语音识别
"""
import speech_recognition as sr
import threading
import time
import logging
from config.settings import SAMPLE_RATE, CHUNK_SIZE
from config.api_keys import AZURE_SPEECH_KEY, AZURE_SPEECH_REGION

logger = logging.getLogger(__name__)

class VoiceInputModule:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.stop_listening = None
        self.callback_function = None
        
        # 配置语音识别参数
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
    def setup_microphone(self):
        """初始化麦克风"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("麦克风初始化成功")
            return True
        except Exception as e:
            logger.error(f"麦克风初始化失败：{e}")
            return False
    
    def start_listening(self, callback=None):
        """开始监听语音输入"""
        if not self.setup_microphone():
            return False
            
        self.callback_function = callback
        self.is_listening = True
        
        def audio_callback(recognizer, audio):
            try:
                if not self.is_listening:
                    return
                    
                # 使用Azure语音识别
                text = recognizer.recognize_azure(
                    audio, 
                    key=AZURE_SPEECH_KEY, 
                    location=AZURE_SPEECH_REGION,
                    language='zh-CN'
                )
                
                if text and self.callback_function:
                    logger.info(f"识别到语音：{text}")
                    self.callback_function(text)
                    
            except sr.UnknownValueError:
                logger.debug("语音识别：无法理解音频内容")
                if self.callback_function:
                    self.callback_function(None, "无法理解，请重试")
            except sr.RequestError as e:
                logger.error(f"语音识别服务错误：{e}")
                if self.callback_function:
                    self.callback_function(None, f"语音识别服务错误：{e}")
            except Exception as e:
                logger.error(f"语音处理异常：{e}")
        
        try:
            self.stop_listening = self.recognizer.listen_in_background(
                self.microphone, audio_callback, phrase_time_limit=10
            )
            logger.info("开始监听语音输入")
            return True
        except Exception as e:
            logger.error(f"启动语音监听失败：{e}")
            return False
    
    def stop_listening_input(self):
        """停止监听语音输入"""
        self.is_listening = False
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)
            logger.info("停止监听语音输入")
    
    def recognize_audio_file(self, audio_file_path):
        """识别音频文件中的语音"""
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
            
            text = self.recognizer.recognize_azure(
                audio,
                key=AZURE_SPEECH_KEY,
                location=AZURE_SPEECH_REGION,
                language='zh-CN'
            )
            return text
        except Exception as e:
            logger.error(f"音频文件识别失败：{e}")
            return None
    
    def test_microphone(self):
        """测试麦克风是否正常工作"""
        try:
            with self.microphone as source:
                print("正在测试麦克风，请说话...")
                audio = self.recognizer.listen(source, timeout=5)
                
            text = self.recognizer.recognize_azure(
                audio,
                key=AZURE_SPEECH_KEY,
                location=AZURE_SPEECH_REGION,
                language='zh-CN'
            )
            print(f"测试成功，识别结果：{text}")
            return True
        except Exception as e:
            print(f"麦克风测试失败：{e}")
            return False
