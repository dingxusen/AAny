# 语音控制电脑应用

一个基于大模型的语音控制电脑应用，支持通过语音指令控制电脑的各种功能。

## 功能特性

### 核心功能
- **语音识别**：使用Azure语音服务进行高精度语音识别
- **指令解析**：使用OpenAI GPT-4进行自然语言理解和指令解析
- **系统控制**：支持音量调节、亮度调节、锁屏等系统操作
- **应用管理**：支持启动/关闭常用应用程序
- **媒体控制**：支持音乐播放/暂停控制
- **文件操作**：支持文件夹打开、文件搜索等操作
- **语音反馈**：使用Azure TTS服务提供语音反馈

### 用户界面
- **命令行界面**：简洁的命令行操作界面
- **图形界面**：友好的GUI界面，支持实时日志查看和状态监控

## 系统要求

### 操作系统
- Windows 10/11
- macOS 10.15+
- Linux (部分功能)

### Python版本
- Python 3.8+

### 硬件要求
- 麦克风设备
- 扬声器或耳机

## 安装指南

### 1. 克隆项目
```bash
git clone <repository-url>
cd voice_control_assistant
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置API密钥
复制 `env_example.txt` 为 `.env` 文件，并填入您的API密钥：

```bash
cp env_example.txt .env
```

编辑 `.env` 文件：
```
OPENAI_API_KEY=your_openai_api_key_here
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=eastus
```

### 4. 获取API密钥

#### OpenAI API密钥
1. 访问 [OpenAI官网](https://platform.openai.com/)
2. 注册账户并获取API密钥
3. 确保账户有足够的额度

#### Azure语音服务密钥
1. 访问 [Azure门户](https://portal.azure.com/)
2. 创建语音服务资源
3. 获取订阅密钥和区域信息

## 使用方法

### 命令行模式
```bash
python main.py
```

### GUI模式
```bash
python gui/app.py
```

### 可用命令示例

#### 媒体控制
- "播放音乐" - 开始播放音乐
- "暂停音乐" - 暂停/恢复音乐播放
- "下一首歌" - 切换到下一首歌曲

#### 系统控制
- "声音大一点" - 增加音量
- "声音小一点" - 减少音量
- "屏幕亮一点" - 增加屏幕亮度
- "锁屏" - 锁定电脑屏幕

#### 应用操作
- "打开记事本" - 启动记事本应用
- "打开计算器" - 启动计算器应用
- "打开文件管理器" - 打开文件浏览器

#### 文件操作
- "打开文件夹" - 打开文件管理器
- "搜索文件" - 打开文件搜索功能

## 项目结构

```
voice_control_assistant/
├── main.py                 # 主程序入口
├── config/                 # 配置文件
│   ├── settings.py         # 应用设置
│   └── api_keys.py         # API密钥配置
├── modules/                # 核心模块
│   ├── voice_input.py      # 语音输入模块
│   ├── command_parser.py   # 指令解析模块
│   ├── system_executor.py  # 系统执行模块
│   └── voice_feedback.py   # 语音反馈模块
├── utils/                  # 工具模块
│   ├── logger.py           # 日志工具
│   └── system_utils.py     # 系统工具
├── gui/                    # GUI界面
│   └── app.py              # GUI应用
├── tests/                  # 测试模块
│   └── test_command_parser.py
├── requirements.txt        # 依赖包
└── README.md              # 项目说明
```

## 开发说明

### 添加新命令
1. 在 `config/settings.py` 中添加命令内容
2. 在 `modules/command_parser.py` 中添加解析逻辑
3. 在 `modules/system_executor.py` 中添加执行逻辑
4. 更新测试用例

### 调试模式
设置环境变量启用调试模式：
```bash
export LOG_LEVEL=DEBUG
```

### 运行测试
```bash
python -m pytest tests/
```

## 故障排除

### 常见问题

#### 1. 麦克风无法识别
- 检查麦克风设备是否正常工作
- 确认麦克风权限已授予应用
- 检查音频设备驱动

#### 2. 语音识别不准确
- 确保环境安静，减少背景噪音
- 说话清晰，语速适中
- 检查网络连接（Azure语音服务需要网络）

#### 3. 命令执行失败
- 检查系统权限设置
- 确认目标应用程序已安装
- 查看日志文件获取详细错误信息

#### 4. API调用失败
- 验证API密钥是否正确
- 检查API配额是否充足
- 确认网络连接正常

## 安全注意事项

1. **API密钥安全**：不要将API密钥提交到版本控制系统
2. **权限控制**：应用需要系统级权限，请谨慎使用
3. **隐私保护**：语音数据会发送到云端服务，请注意隐私政策
4. **网络安全**：确保网络连接安全，避免在不安全的网络环境下使用

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 贡献指南

欢迎提交Issue和Pull Request来改进项目。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至项目维护者

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基础语音控制功能
- 提供命令行和GUI两种界面
- 集成OpenAI GPT-4和Azure语音服务
