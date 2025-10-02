# 🚀 Professor - AI Research Assistant

A futuristic, AI-powered research assistant that combines web scraping, content analysis, and advanced language models to provide comprehensive research on any topic.

## ✨ Features

### 🎨 Modern Futuristic UI
- **Animated Neural Network Background**: Dynamic particle system with interconnected nodes
- **Holographic Display**: 3D-style result presentation with glowing effects
- **Intellectual Loading Animations**: Engaging brain-inspired processing animations
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Voice Input**: Speak your research topics using voice recognition
- **Real-time Progress**: Live updates during research process

### 🧠 Advanced AI Research
- **Multi-Source Web Scraping**: Automatically finds and extracts content from relevant sources
- **Intelligent Content Processing**: Cleans and organizes scraped data
- **AI-Powered Analysis**: Uses Google Gemini AI for comprehensive research generation
- **Customizable Output**: Choose from different response styles (Comprehensive, Concise, Technical, Beginner-friendly)
- **Source Attribution**: Optional inclusion of source references

### 🔧 Technical Features
- **Asynchronous Processing**: Non-blocking research operations
- **Real-time Status Updates**: Live progress tracking via WebSocket-like polling
- **Error Handling**: Robust error management with user-friendly messages
- **Export Options**: Copy, download, or share research results
- **API-First Design**: RESTful API for easy integration

## 📁 Project Structure

```
professor-ai-researcher/
├── 🚀 Entry Points
│   ├── app.py              # Main Flask web application
│   ├── start.py            # Cross-platform startup script
│   └── start.bat           # Windows batch startup script
│
├── 🧠 Core AI Modules
│   ├── get_links.py        # Web search and link discovery
│   ├── scrape.py           # Content extraction and scraping
│   ├── cleaning.py         # Data processing and optimization
│   └── llm.py              # AI model integration (Gemini)
│
├── 🎨 Frontend
│   ├── templates/
│   │   └── index.html      # Main web interface
│   ├── style.css           # Futuristic UI styling
│   └── script.js           # Interactive functionality
│
├── 🛠️ Development & Testing
│   ├── main.py             # CLI research pipeline
│   ├── demo.py             # Interactive demonstration
│   ├── test_optimization.py # Performance testing
│   └── list_models.py      # Available AI models
│
├── 📋 Configuration
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # API keys (create this)
│   └── README.md          # This file
│
└── 📊 Generated Data
    └── logs/              # Research logs and cache
```

### 📝 File Descriptions

#### 🚀 **Entry Points**
- **`app.py`** - Main Flask web application with REST API endpoints, real-time progress tracking, and web interface
- **`start.py`** - Cross-platform Python startup script with environment validation and automatic browser opening  
- **`start.bat`** - Windows batch file with ASCII art, virtual environment setup, and dependency checking

#### 🧠 **Core AI Modules**
- **`get_links.py`** - Searches web using Serper API, filters relevant sources, returns prioritized URLs
- **`scrape.py`** - Extracts content from web pages, handles different content types, manages rate limiting
- **`cleaning.py`** - Processes scraped content, removes noise, optimizes for AI context windows
- **`llm.py`** - Integrates Google Gemini AI, manages prompts, handles different response styles

#### 🛠️ **Development & Testing**  
- **`main.py`** - Simple CLI script for testing the research pipeline without web interface
- **`demo.py`** - Interactive demonstration with progress display and result saving options
- **`test_optimization.py`** - Tests context optimization with different character limits for performance tuning
- **`list_models.py`** - Lists available Google AI models and their capabilities for setup verification

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Google API Key (for Gemini AI)
- Serper API Key (for web search)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd professor-ai-researcher
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_google_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

#### Getting API Keys:

**Google API Key (Gemini AI):**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

**Serper API Key (Web Search):**
1. Visit [Serper.dev](https://serper.dev/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Copy the key to your `.env` file

### 4. Run the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## 🚀 Quick Start

### Option 1: Web Interface (Recommended)
```bash
# Easy startup with validation
python start.py

# Or direct Flask app
python app.py
```

### Option 2: Command Line Demo
```bash
# Interactive demonstration
python demo.py

# Direct pipeline test
python main.py
```

### Option 3: Windows Users
```batch
# Double-click or run in Command Prompt
start.bat
```

## 🎯 Usage

### Web Interface
1. **Open your browser** and navigate to `http://localhost:5000`
2. **Enter your research topic** in the search field
3. **Configure options**:
   - Choose response style (Comprehensive, Concise, Technical, Beginner-friendly)
   - Toggle source inclusion
4. **Click "Generate Research"** or press Ctrl+Enter
5. **Watch the AI work** with real-time progress updates
6. **View results** in the futuristic holographic display
7. **Export or share** your research using the action buttons

### Voice Input
- Click the microphone button next to the search field
- Speak your research topic clearly
- The system will automatically transcribe your speech

### Keyboard Shortcuts
- `Ctrl/Cmd + Enter`: Start research
- `Escape`: Return to search (start new research)

## 🔌 API Endpoints

### Start Research
```http
POST /api/research
Content-Type: application/json

{
    "topic": "artificial intelligence",
    "response_style": "Comprehensive",
    "include_sources": true
}
```

### Check Status
```http
GET /api/research/{task_id}/status
```

### Get Results
```http
GET /api/research/{task_id}/result
```

### Health Check
```http
GET /api/health
```

## 🏗️ Architecture

### Frontend
- **HTML5**: Semantic structure with accessibility features
- **CSS3**: Advanced animations, gradients, and responsive design
- **Vanilla JavaScript**: Modern ES6+ with async/await patterns
- **No Framework Dependencies**: Pure web technologies for maximum performance

### Backend
- **Flask**: Lightweight Python web framework
- **Threading**: Asynchronous task processing
- **RESTful API**: Clean, predictable endpoints
- **CORS Support**: Cross-origin resource sharing enabled

### AI & Data Processing
- **Google Gemini AI**: Advanced language model for research generation
- **BeautifulSoup**: HTML parsing and content extraction
- **Custom Scraping**: Intelligent content selection and cleaning
- **Token Optimization**: Efficient prompt engineering for cost control

## 🎨 UI Components

### Loading Animations
- **AI Brain**: Rotating rings with pulsing core
- **Neural Waves**: Expanding wave animations
- **Progress Bar**: Smooth progress with shine effects
- **Step Indicators**: Visual feedback for each processing stage

### Results Display
- **Holographic Frame**: 3D-style container with corner accents
- **Typewriter Effect**: Character-by-character text animation
- **Syntax Highlighting**: Formatted code and technical content
- **Action Buttons**: Copy, download, share, and new search options

### Background Effects
- **Particle System**: Floating particles with physics simulation
- **Neural Network**: Animated nodes and connections
- **Gradient Overlays**: Dynamic color transitions
- **Responsive Animations**: Adapts to screen size and device capabilities

## 🔧 Configuration

### Environment Variables
```env
# Required
GOOGLE_API_KEY=your_google_api_key
SERPER_API_KEY=your_serper_api_key

# Optional
FLASK_ENV=development
FLASK_DEBUG=true
MAX_SOURCES=10
CONTEXT_LIMIT=7500
```

### Customization Options
- **Color Themes**: Modify CSS variables in `style.css`
- **Animation Speed**: Adjust timing in JavaScript
- **API Timeouts**: Configure in `app.py`
- **Content Limits**: Modify scraping parameters

## 📱 Mobile Support

The interface is fully responsive and includes:
- **Touch-friendly controls**: Large buttons and touch targets
- **Optimized layouts**: Stacked components on smaller screens
- **Reduced animations**: Performance optimizations for mobile devices
- **Voice input**: Enhanced mobile voice recognition support

## 🚀 Performance

### Optimization Features
- **Lazy Loading**: Components load as needed
- **Caching**: Intelligent caching of API responses
- **Compression**: Optimized asset delivery
- **Async Operations**: Non-blocking user interface
- **Memory Management**: Automatic cleanup of old tasks

### Benchmarks
- **Average Response Time**: 15-45 seconds (depending on topic complexity)
- **Memory Usage**: ~50-100MB during processing
- **Concurrent Users**: Supports multiple simultaneous research tasks
- **Token Efficiency**: Optimized prompts for cost-effective AI usage

## 🛡️ Security

- **API Key Protection**: Environment variables for sensitive data
- **Input Validation**: Sanitized user inputs
- **CORS Configuration**: Controlled cross-origin access
- **Error Handling**: No sensitive information in error messages
- **Rate Limiting**: Built-in protection against abuse

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI**: Advanced language model capabilities
- **Serper.dev**: Reliable web search API
- **Font Awesome**: Beautiful icons
- **Google Fonts**: Orbitron and Rajdhani typefaces

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed information
3. Include your environment details and error messages

---

**Built with ❤️ and futuristic vision**

*Transform your research experience with AI-powered intelligence and stunning visual design.*
