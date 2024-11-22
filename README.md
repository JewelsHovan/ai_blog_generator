# Data Science Blog Generator

## Overview
An AI-powered blog post generator for data science and analysis projects, leveraging advanced language models through OpenRouter's API. This tool automatically generates engaging, narrative-driven blog posts from your data analysis context and visualizations.

## Features
- 🤖 Multiple AI model support through OpenRouter
- 📊 Automatic image analysis and integration
- 📝 Multiple narrative generation
- 🎨 Interactive narrative selection
- 📁 Directory-based image processing
- 📑 Markdown output format

## Prerequisites
- Python 3.7+
- OpenRouter API Key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenRouter API key:
Create a `.env` file in the project root:
```bash
OPEN_ROUTER_API_KEY=your_api_key_here
```

## Usage

### Basic Usage
```bash
python main.py -c context.txt -i image1.png image2.png
```

### Using a Directory of Images
```bash
python main.py -c context.txt -d path/to/images/directory
```

### Selecting a Different Model
```bash
python main.py -c context.txt -i images/*.png --model meta-llama/llama-2-70b-chat
```

### Command Line Arguments
- `-c, --context`: Path to context file (required)
- `-i, --images`: List of image paths
- `-d, --image-dir`: Directory containing images
- `-o, --output-dir`: Output directory (default: blog_posts)
- `--model`: AI model to use (default: openai/gpt-4o-mini)
- `--api-key`: OpenRouter API key (optional if set in .env)

## Supported Models
- openai/gpt-4o-mini (default)
- google/palm-2-chat-bison
- meta-llama/llama-2-70b-chat

## Project Structure
```
.
├── data_blog_generator.py  # Main generator class
├── main.py                # CLI interface
├── prompts.py            # Prompt templates
├── requirements.txt      # Dependencies
└── .env                 # API key configuration
```

## Implementation Details

### Modern LangChain Expression Language (LCEL)
The project uses LCEL's pipe operator for efficient chain composition:
```python
narrative_chain = (
    prompt 
    | llm 
    | output_parser 
    | custom_function
)
```

### Image Processing
- Supports multiple image formats: PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP
- Automatic image analysis and context integration
- Directory-based batch processing

### Blog Generation Process
1. Context Analysis: Process the provided data analysis context
2. Image Analysis: Analyze and extract insights from visualizations
3. Narrative Generation: Create multiple potential narrative approaches
4. Interactive Selection: User selects preferred narrative
5. Content Generation: Generate structured blog post
6. Output: Save as formatted markdown file

## Development

### Adding New Features
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

### Adding New Models
Update the `AVAILABLE_MODELS` list in `main.py`:
```python
AVAILABLE_MODELS = [
    "openai/gpt-4o-mini",
    "your-new-model-here",
]
```

## Limitations
- Requires OpenRouter API key
- API usage costs apply
- Output quality depends on chosen model
- Image analysis is currently text-based

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
[Your License Here]
