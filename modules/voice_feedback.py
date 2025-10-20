"""
语音反馈模块
负责语音合成和播放反馈信息
"""
import logging
import threading
import time
import tempfile
import os
from config.api_keys import AZURE_SPEECH_KEY, AZURE_SPEECH_REGION

logger = logging.getLogger(__name__)

class VoiceFeedback:
    def __init__(self):
        self.tts_enabled = bool(AZURE_SPEECH_KEY)
        self.is_speaking = False
        self.speech_queue = []
        self.speech_thread = None
        
        if self.tts_enabled:
            try:
                import azure.cognitiveservices.speech as speechsdk
                self.speech_config = speechsdk.SpeechConfig(
                    subscription=AZURE_SPEECH_KEY,
                    region=AZURE_SPEECH_REGION
                )
                self.speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"
                self.synthesizer = speechsdk.SpeechSynthesizer(
                    speech_config=self.speech_config
                )
                logger.info("语音合成服务初始化成功")
            except ImportError:
                logger.warning("Azure语音服务库未安装，将使用文本反馈")
                self.tts_enabled = False
            except Exception as e:
                logger.error(f"语音合成服务初始化失败：{e}")
                self.tts_enabled = False
        else:
            logger.warning("语音合成服务未配置，将使用文本反馈")
    
    def speak(self, text, priority=1):
        """
        语音反馈
        priority: 1=高优先级（立即播放），2=普通优先级（排队播放）
        """
        if not text:
            return
        
        logger.info(f"语音反馈：{text}")
        
        if priority == 1:
            # 高优先级，立即播放
            self._speak_immediately(text)
        else:
            # 普通优先级，加入队列
            self._add_to_queue(text)
    
    def _speak_immediately(self, text):
        """立即播放语音"""
        if self.tts_enabled:
            try:
                # 停止当前播放
                if self.is_speaking:
                    self._stop_current_speech()
                
                # 启动新的语音合成
                self.speech_thread = threading.Thread(
                    target=self._synthesize_and_play,
                    args=(text,)
                )
                self.speech_thread.daemon = True
                self.speech_thread.start()
                
            except Exception as e:
                logger.error(f"语音播放失败：{e}")
                self._fallback_feedback(text)
        else:
            self._fallback_feedback(text)
    
    def _add_to_queue(self, text):
        """添加语音到播放队列"""
        self.speech_queue.append(text)
        
        # 如果没有正在播放，开始播放队列
        if not self.is_speaking:
            self._process_speech_queue()
    
    def _process_speech_queue(self):
        """处理语音播放队列"""
        if not self.speech_queue:
            return
        
        if self.speech_thread and self.speech_thread.is_alive():
            return
        
        text = self.speech_queue.pop(0)
        self.speech_thread = threading.Thread(
            target=self._synthesize_and_play,
            args=(text,)
        )
        self.speech_thread.daemon = True
        self.speech_thread.start()
    
    def _synthesize_and_play(self, text):
        """合成并播放语音"""
        try:
            self.is_speaking = True
            
            if self.tts_enabled:
                # 使用Azure TTS服务
                result = self.synthesizer.speak_text_async(text).get()
                
                import azure.cognitiveservices.speech as speechsdk
                if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                    logger.debug("语音合成完成")
                else:
                    logger.error(f"语音合成失败：{result.reason}")
                    self._fallback_feedback(text)
            else:
                # 使用系统TTS
                self._system_tts(text)
            
            # 播放完成后处理队列中的下一个
            time.sleep(0.5)  # 短暂延迟
            self.is_speaking = False
            
            if self.speech_queue:
                self._process_speech_queue()
                
        except Exception as e:
            logger.error(f"语音合成播放失败：{e}")
            self.is_speaking = False
            self._fallback_feedback(text)
    
    def _stop_current_speech(self):
        """停止当前语音播放"""
        try:
            if hasattr(self, 'synthesizer') and self.synthesizer:
                self.synthesizer.stop_speaking_async()
            self.is_speaking = False
        except Exception as e:
            logger.error(f"停止语音播放失败：{e}")
    
    def _system_tts(self, text):
        """使用系统TTS"""
        try:
            import platform
            system = platform.system()
            
            if system == "Windows":
                # Windows系统TTS
                import pyttsx3
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
                
            elif system == "Darwin":  # macOS
                # macOS系统TTS
                os.system(f"say '{text}'")
                
            elif system == "Linux":
                # Linux系统TTS
                os.system(f"espeak '{text}'")
                
            else:
                logger.warning(f"不支持的系统TTS：{system}")
                self._fallback_feedback(text)
                
        except ImportError:
            logger.warning("系统TTS库未安装")
            self._fallback_feedback(text)
        except Exception as e:
            logger.error(f"系统TTS失败：{e}")
            self._fallback_feedback(text)
    
    def _fallback_feedback(self, text):
        """备用反馈方式（文本输出）"""
        print(f"[语音反馈] {text}")
    
    def speak_command_result(self, result):
        """播报命令执行结果"""
        if not result:
            self.speak("命令执行失败")
            return
        
        if result.get("success"):
            message = result.get("message", "命令执行成功")
            self.speak(message, priority=1)
        else:
            error_msg = result.get("message", "命令执行失败")
            self.speak(f"抱歉，{error_msg}", priority=1)
    
    def speak_error(self, error_message):
        """播报错误信息"""
        self.speak(f"出现错误：{error_message}", priority=1)
    
    def speak_welcome(self):
        """播报欢迎信息"""
        welcome_text = "语音控制助手已启动，请说出您的指令"
        self.speak(welcome_text, priority=1)
    
    def speak_goodbye(self):
        """播报告别信息"""
        goodbye_text = "语音控制助手已关闭，再见"
        self.speak(goodbye_text, priority=1)
    
    def clear_queue(self):
        """清空语音播放队列"""
        self.speech_queue.clear()
        self._stop_current_speech()
    
    def test_speech(self):
        """测试语音功能"""
        test_text = "语音反馈功能测试，如果您能听到这段话，说明语音合成工作正常"
        self.speak(test_text, priority=1)
    
    def get_status(self):
        """获取语音反馈状态"""
        return {
            "tts_enabled": self.tts_enabled,
            "is_speaking": self.is_speaking,
            "queue_length": len(self.speech_queue)
        }
