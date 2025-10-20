# Voice Control Assistant

A voice-controlled computer application based on large language models, enabling users to control their computers through natural language voice commands.

## Features

### Core Functionality
- **Voice Recognition**: High-precision voice recognition using Azure Speech Services
- **Command Parsing**: Natural language understanding and command parsing using OpenAI GPT-4
- **System Control**: Support for volume adjustment, brightness control, screen locking, and other system operations
- **Application Management**: Support for launching/closing common applications
- **Media Control**: Support for music playback/pause control
- **File Operations**: Support for folder opening, file searching, and other file operations
- **Voice Feedback**: Voice feedback using Azure TTS services

### User Interface
- **Command Line Interface**: Clean command-line operation interface
- **Graphical Interface**: User-friendly GUI interface with real-time log viewing and status monitoring

## System Requirements

### Operating System
- Windows 10/11
- macOS 10.15+
- Linux (partial functionality)

### Python Version
- Python 3.8+

### Hardware Requirements
- Microphone device
- Speakers or headphones

## Installation Guide

### 1. Clone the Project
```bash
git clone https://github.com/dingxusen/AAny.git
cd AAny
```

### 2. Install Dependencies
```bash
python install.py
```

### 3. Configure API Keys
Copy `env_example.txt` to `.env` and fill in your API keys:

```bash
cp env_example.txt .env
```

Edit the `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=eastus
```

### 4. Get API Keys

#### OpenAI API Key
1. Visit [OpenAI website](https://platform.openai.com/)
2. Register an account and get an API key
3. Ensure your account has sufficient credits

#### Azure Speech Service Key
1. Visit [Azure Portal](https://portal.azure.com/)
2. Create a Speech Service resource
3. Get subscription key and region information

## Usage

### Command Line Mode
```bash
python start.py
```

### GUI Mode
```bash
python start.py --mode gui
```

### Supported Voice Commands

#### Media Control
- "播放音乐" (Play music) - Start playing music
- "暂停音乐" (Pause music) - Pause/resume music playback
- "下一首歌" (Next song) - Switch to next song

#### System Control
- "声音大一点" (Turn up volume) - Increase volume
- "声音小一点" (Turn down volume) - Decrease volume
- "屏幕亮一点" (Brighten screen) - Increase screen brightness
- "锁屏" (Lock screen) - Lock computer screen

#### Application Operations
- "打开记事本" (Open notepad) - Launch notepad application
- "打开计算器" (Open calculator) - Launch calculator application
- "打开文件管理器" (Open file manager) - Open file browser

#### File Operations
- "打开文件夹" (Open folder) - Open file manager
- "搜索文件" (Search files) - Open file search functionality

## Project Structure

```
AAny/
├── main.py                 # Main program entry
├── config/                 # Configuration files
│   ├── settings.py         # Application settings
│   └── api_keys.py         # API key configuration
├── modules/                # Core modules
│   ├── voice_input.py      # Voice input module
│   ├── command_parser.py   # Command parsing module
│   ├── system_executor.py  # System execution module
│   └── voice_feedback.py   # Voice feedback module
├── utils/                  # Utility modules
│   ├── logger.py           # Logging utilities
│   └── system_utils.py     # System utilities
├── gui/                    # GUI interface
│   └── app.py              # GUI application
├── tests/                  # Test modules
│   └── test_command_parser.py
├── requirements.txt        # Dependencies
└── README.md              # Project documentation
```

## Development Notes

### Adding New Commands
1. Add command content in `config/settings.py`
2. Add parsing logic in `modules/command_parser.py`
3. Add execution logic in `modules/system_executor.py`
4. Update test cases

### Debug Mode
Set environment variable to enable debug mode:
```bash
export LOG_LEVEL=DEBUG
```

### Running Tests
```bash
python -m pytest tests/
```

## Troubleshooting

### Common Issues

#### 1. Microphone Cannot Be Recognized
- Check if the microphone device is working properly
- Confirm microphone permissions have been granted to the application
- Check audio device drivers

#### 2. Inaccurate Voice Recognition
- Ensure a quiet environment and reduce background noise
- Speak clearly at a moderate pace
- Check network connection (Azure Speech Service requires internet)

#### 3. Command Execution Failure
- Check system permission settings
- Confirm target applications are installed
- Check log files for detailed error information

#### 4. API Call Failures
- Verify API keys are correct
- Check API quota is sufficient
- Confirm network connection is normal

## Security Notes

1. **API Key Security**: Do not commit API keys to version control systems
2. **Permission Control**: The application requires system-level permissions, use with caution
3. **Privacy Protection**: Voice data will be sent to cloud services, please pay attention to privacy policies
4. **Network Security**: Ensure secure network connections and avoid using in insecure network environments

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Issues and Pull Requests are welcome to improve the project.

## Contact

For questions or suggestions, please contact:
- Submit GitHub Issues
- Send email to project maintainers

## Changelog

### v1.0.0
- Initial version release
- Support for basic voice control functionality
- Provide both command-line and GUI interfaces
- Integration with OpenAI GPT-4 and Azure Speech Services
