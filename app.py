from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import json
import os
import base64
from io import BytesIO
from PIL import Image
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Server Configuration
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '5000'))
MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', '16')) * 1024 * 1024  # Default 16MB

app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Configure CORS - Allow all origins
CORS(app, resources={r"/*": {"origins": "*"}})

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o')
LANGCHAIN_TEMPERATURE = float(os.getenv('LANGCHAIN_TEMPERATURE', '0.7'))
LANGCHAIN_MAX_TOKENS = int(os.getenv('LANGCHAIN_MAX_TOKENS', '2000'))
IMAGE_MAX_TOKENS = int(os.getenv('IMAGE_MAX_TOKENS', '500'))

# Image Processing Configuration
IMAGE_MAX_SIZE = int(os.getenv('IMAGE_MAX_SIZE', '1024'))  # Max width/height for resizing
IMAGE_QUALITY = int(os.getenv('IMAGE_QUALITY', '85'))  # JPEG quality (1-100)

# Initialize LangChain
if OPENAI_API_KEY:
    llm = ChatOpenAI(
        temperature=LANGCHAIN_TEMPERATURE,
        openai_api_key=OPENAI_API_KEY,
        max_tokens=LANGCHAIN_MAX_TOKENS,
        model_name=OPENAI_MODEL
    )
    logger.info(f"LangChain initialized successfully with model: {OPENAI_MODEL}")
else:
    llm = None
    logger.warning("OPENAI_API_KEY not configured")

def analyze_image_with_openai(image_base64):
    """Analyze image using OpenAI Vision API to detect ingredients"""
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Identify all the ingredients you can see in this image. List them in a clear format, one ingredient per line. Be specific with types and quantities if visible. Only list what you can clearly see."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=IMAGE_MAX_TOKENS
        )
        
        ingredients_text = response.choices[0].message.content.strip()
        logger.info(f"Detected ingredients: {ingredients_text}")
        return ingredients_text
        
    except Exception as e:
        logger.error(f"Error analyzing image: {e}")
        return None

def generate_recipes_with_langchain(ingredients_text):
    """Generate recipe suggestions using LangChain"""
    if not llm:
        return "LangChain not available - please configure OPENAI_API_KEY"
    
    try:
        messages = [
            SystemMessage(content="""
You are a professional chef and recipe expert. Your task is to suggest delicious and practical recipes based on the ingredients provided.
Always respond in English.
"""),
            HumanMessage(content=f"""
Based on these ingredients:
{ingredients_text}

Please suggest 2-3 recipes that can be prepared using these ingredients. For each recipe, provide:
1. Recipe name
2. Brief description (1-2 sentences)
3. Key ingredients used (from the list provided)
4. Estimated preparation time
5. Difficulty level (Easy/Medium/Hard)

Format your response clearly with recipe names as headings.
Be creative and practical in your suggestions.
""")
        ]
        
        response = llm.invoke(messages)
        recipes = response.content.strip()
        
        return recipes
    
    except Exception as e:
        logger.error(f"Error generating recipes: {e}")
        return f"Error generating recipes: {str(e)}"

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "server": {
            "host": HOST,
            "port": PORT
        },
        "configuration": {
            "langchain_available": llm is not None,
            "openai_configured": bool(OPENAI_API_KEY),
            "openai_model": OPENAI_MODEL if OPENAI_API_KEY else None,
            "langchain_temperature": LANGCHAIN_TEMPERATURE,
            "langchain_max_tokens": LANGCHAIN_MAX_TOKENS,
            "max_content_length_mb": MAX_CONTENT_LENGTH / (1024 * 1024),
            "image_max_size": IMAGE_MAX_SIZE,
            "image_quality": IMAGE_QUALITY,
            "cors_enabled": True
        }
    }
    return jsonify(health_data)

@app.route('/api/analyze-ingredients', methods=['POST'])
def analyze_ingredients():
    """Analyze image and generate recipe suggestions"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Validate image
        try:
            img = Image.open(file.stream)
            img.verify()
        except Exception as e:
            logger.error(f"Invalid image file: {e}")
            return jsonify({"error": "Invalid image file"}), 400
        
        # Reset file stream and convert to base64
        file.stream.seek(0)
        img_bytes = BytesIO(file.read())
        img = Image.open(img_bytes)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large
        max_size = (IMAGE_MAX_SIZE, IMAGE_MAX_SIZE)
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=IMAGE_QUALITY)
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Analyze image for ingredients
        logger.info("Analyzing image for ingredients...")
        ingredients = analyze_image_with_openai(img_base64)
        
        if not ingredients:
            return jsonify({"error": "Failed to detect ingredients from image"}), 500
        
        # Generate recipes using LangChain
        logger.info("Generating recipe suggestions...")
        recipes = generate_recipes_with_langchain(ingredients)
        
        return jsonify({
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "ingredients_detected": ingredients,
            "recipes": recipes
        })
    
    except Exception as e:
        logger.error(f"Error in analyze-ingredients endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    """Main page with chat interface"""
    return render_template('index.html')

if __name__ == '__main__':
    logger.info("Starting Recipe Chat Application")
    logger.info(f"Server: {HOST}:{PORT}")
    logger.info(f"LangChain available: {llm is not None}")
    if llm:
        logger.info(f"Using model: {OPENAI_MODEL}")
    
    print(f"Starting server on {HOST}:{PORT}")
    print(f"Access the web interface at: http://localhost:{PORT}")
    
    app.run(
        host=HOST,
        port=PORT,
        debug=False,
        use_reloader=False
    )
