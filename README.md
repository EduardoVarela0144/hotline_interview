# Recipe Assistant - AI-Powered Cooking Assistant

An intelligent recipe suggestion app that uses AI to analyze images of ingredients and generate personalized recipe recommendations in English.

## 🚀 Features

- **Image Analysis**: Upload an image of ingredients and let AI detect what you have
- **Smart Recipe Generation**: Get 2-3 personalized recipe suggestions based on your ingredients
- **Chat Interface**: Clean, modern chat interface for natural interaction
- **AI-Powered**: Uses OpenAI GPT-4 Vision API and LangChain for intelligent responses
- **Responsive Design**: Works beautifully on desktop, tablet, and mobile devices

## 🛠️ Technologies

- **Backend**: Python, Flask
- **AI/ML**: OpenAI GPT-4 Vision API, LangChain
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Image Processing**: Pillow

## 📋 Requirements

- Python 3.8+
- pip
- OpenAI API Key

## 🔧 Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd hotline
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**:
Copy the example env file and customize:
```bash
cp env.example .env
```

Edit `.env` with your configuration (minimal required: `OPENAI_API_KEY`):
```bash
# Required
OPENAI_API_KEY=your-openai-api-key-here

# Optional - Customize as needed
HOST=0.0.0.0
PORT=5000
OPENAI_MODEL=gpt-4o
LANGCHAIN_TEMPERATURE=0.7
MAX_CONTENT_LENGTH=16
IMAGE_MAX_SIZE=1024
IMAGE_QUALITY=85
```

## 🚀 Running the Application

```bash
python app.py
```

The application will be available at:
- **Web Interface**: http://localhost:5000

## 📱 How to Use

1. **Upload an Image**: Click on the camera button or the input area to upload an image of your ingredients
2. **Wait for Analysis**: The AI will automatically detect all ingredients in your image
3. **Get Recipes**: Receive 2-3 recipe suggestions with descriptions, prep time, and difficulty level
4. **Try Another Image**: Upload more images to discover new recipes

## 🔌 API Endpoint

### Analyze Ingredients
```http
POST /api/analyze-ingredients
Content-Type: multipart/form-data

{
  "image": <image file>
}
```

**Response**:
```json
{
  "success": true,
  "timestamp": "2024-01-01T12:00:00",
  "ingredients_detected": "tomatoes, onions, garlic, olive oil, basil...",
  "recipes": "### Pasta with Fresh Tomato Sauce\n\n..."
}
```

### Health Check
```http
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "server": {
    "host": "0.0.0.0",
    "port": 5000
  },
  "configuration": {
    "langchain_available": true,
    "openai_configured": true,
    "openai_model": "gpt-4o",
    "langchain_temperature": 0.7,
    "langchain_max_tokens": 2000,
    "max_content_length_mb": 16,
    "image_max_size": 1024,
    "image_quality": 85
  }
}
```

## ⚙️ Advanced Configuration

All settings can be configured via environment variables in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | - | **Required** OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o` | OpenAI model to use |
| `LANGCHAIN_TEMPERATURE` | `0.7` | AI response creativity (0-1) |
| `LANGCHAIN_MAX_TOKENS` | `2000` | Max tokens for recipe generation |
| `IMAGE_MAX_TOKENS` | `500` | Max tokens for image analysis |
| `HOST` | `0.0.0.0` | Server host address |
| `PORT` | `5000` | Server port |
| `MAX_CONTENT_LENGTH` | `16` | Max file size in MB |
| `IMAGE_MAX_SIZE` | `1024` | Max image dimension in pixels |
| `IMAGE_QUALITY` | `85` | JPEG quality (1-100) |

## 📊 Project Structure

```
hotline/
├── app.py                 # Flask application
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
├── env.example            # Environment variables example
├── .env                   # Environment variables (create from env.example)
├── api.log                # Application logs
├── templates/             # HTML templates
│   ├── base.html          # Base template (legacy)
│   └── index.html         # Main chat interface
└── static/                # Static files
    └── css/
        └── custom.css     # Custom styles
```

## 🎨 Design Features

- **Modern Chat Interface**: Clean, intuitive chat UI
- **Gradient Design**: Beautiful green gradient theme
- **Smooth Animations**: Elegant transitions and effects
- **Responsive**: Fully responsive design for all devices
- **Accessibility**: Accessible and inclusive design

## 🔒 Security

- **CORS**: Configured for local development
- **Environment Variables**: Secure API key storage
- **File Validation**: Image type and size validation
- **Logging**: Activity logging for debugging

## 🧪 Testing

To test the application:

1. **Upload Test Images**: Use images with clearly visible ingredients
2. **Verify Results**: Check that ingredients are detected and recipes are generated
3. **Check Health**: Visit http://localhost:5000/health

## 📈 Monitoring

- **Logs**: Check `api.log` for system information
- **Health Check**: Visit `/health` endpoint for system status
- **Console**: Browser console for frontend debugging

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 📞 Support

For technical support or questions:
- Create an issue in the repository
- Contact the development team

---

**Recipe Assistant** - Transforming cooking with artificial intelligence.
