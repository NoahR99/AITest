# AI Generator

An AI-powered application that generates stunning images and videos from text prompts, and can transform existing images using advanced machine learning models.

## Features

- **Text to Image**: Generate high-quality images from text descriptions
- **Image to Image**: Transform existing images with AI guidance
- **Text to Video**: Create short video clips from text prompts
- **Web Interface**: Easy-to-use web application with intuitive controls
- **CLI Interface**: Command-line tool for batch processing and automation
- **Multiple Models**: Support for various Stable Diffusion and video generation models

## Quick Start

### Prerequisites
- Python 3.8 or higher
- CUDA-compatible GPU (recommended, but CPU mode is also supported)
- At least 10GB of free disk space (for model downloads)
- Stable internet connection for initial model downloads

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/NoahR99/AITest.git
cd AITest
```

2. **Run the setup script**:
```bash
chmod +x setup.sh
./setup.sh
```

3. **Activate the virtual environment**:
```bash
source venv/bin/activate
```

### Usage

#### Web Interface (Recommended)
Start the web application:
```bash
python web_app.py
```
Then open your browser to `http://localhost:5000`

#### Command Line Interface
Generate an image from text:
```bash
python cli.py text-to-image "A beautiful sunset over mountains"
```

Transform an image:
```bash
python cli.py image-to-image "Turn this into a painting" path/to/image.jpg
```

Generate a video:
```bash
python cli.py text-to-video "A bird flying through clouds"
```

View all CLI options:
```bash
python cli.py --help
```

## Running in VS Code

### Prerequisites for VS Code
- [Visual Studio Code](https://code.visualstudio.com/) installed
- [Python extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python) installed

### Setup in VS Code

1. **Open the project in VS Code**:
```bash
code AITest
```
Or use `File > Open Folder` in VS Code to open the project directory.

2. **Configure the Python interpreter**:
   - Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
   - Type "Python: Select Interpreter"
   - Choose the interpreter from your virtual environment: `./venv/bin/python` (Linux/Mac) or `.\venv\Scripts\python.exe` (Windows)

3. **Install recommended extensions** (when prompted by VS Code):
   - Python (ms-python.python)
   - Pylance (ms-python.vscode-pylance)
   - Python Debugger (ms-python.debugpy)

### Running the Application in VS Code

#### Method 1: Using the Integrated Terminal
1. Open a new terminal in VS Code (`Terminal > New Terminal`)
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```
3. Run the application:
   ```bash
   # Web interface
   python web_app.py
   
   # CLI commands
   python cli.py --help
   python cli.py text-to-image "A beautiful landscape"
   ```

#### Method 2: Using VS Code's Run Button
1. Open `web_app.py` in the editor
2. Click the "Run Python File" button (▶️) in the top-right corner
3. The web application will start and you can access it at `http://localhost:5000`

#### Method 3: Creating Launch Configurations
Create a `.vscode/launch.json` file for debugging:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Web App",
            "type": "python",
            "request": "launch",
            "program": "web_app.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "CLI Help",
            "type": "python",
            "request": "launch",
            "program": "cli.py",
            "args": ["--help"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "Text to Image",
            "type": "python",
            "request": "launch",
            "program": "cli.py",
            "args": ["text-to-image", "A beautiful sunset"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

### VS Code Workspace Settings
Create a `.vscode/settings.json` file for optimal development experience:

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "files.exclude": {
        "**/__pycache__": true,
        "**/venv": true,
        "**/.git": true
    }
}
```

### Debugging in VS Code
1. Set breakpoints by clicking in the left margin of your code
2. Use the Debug panel (`Run and Debug` in the sidebar)
3. Select your launch configuration and press F5 to start debugging
4. Use F10 (step over), F11 (step into), and F5 (continue) to navigate through your code

### Tips for VS Code Development
- Use `Ctrl+`` ` to quickly open/close the integrated terminal
- Install the "Python Docstring Generator" extension for better documentation
- Use `Ctrl+Shift+P` and type "Python: Create Terminal" to get a terminal with the virtual environment already activated
- The Python extension will automatically detect your `requirements.txt` and suggest installing packages

## Examples

### Text to Image
```bash
# Basic usage
python cli.py text-to-image "A robot in a cyberpunk city"

# With custom parameters
python cli.py text-to-image "A serene lake" --width 768 --height 768 --steps 30 --seed 42
```

### Image to Image
```bash
# Transform a photo into artwork
python cli.py image-to-image "oil painting style" photo.jpg --strength 0.7

# Subtle style changes
python cli.py image-to-image "add dramatic lighting" image.png --strength 0.3
```

### Text to Video
```bash
# Generate a short video
python cli.py text-to-video "Ocean waves at sunset" --frames 24 --fps 12
```

## Configuration

The application uses sensible defaults, but you can customize settings in `config.py`:

- **Model selection**: Choose different AI models
- **Default parameters**: Adjust image/video generation settings
- **Output directories**: Change where files are saved
- **Device settings**: Configure GPU/CPU usage

## File Management

- **Generated files**: Saved to the `outputs/` directory
- **Temporary files**: Stored in `temp/` (automatically cleaned)
- **View outputs**: Use the web gallery or `python cli.py list-outputs`
- **Clear outputs**: `python cli.py clear-outputs`

## System Requirements

### Minimum
- 8GB RAM
- 4GB free disk space
- CPU-only mode (slow)

### Recommended
- 16GB+ RAM
- NVIDIA GPU with 8GB+ VRAM
- 20GB+ free disk space
- CUDA 11.8 or higher

## Supported Formats

### Input Images
- PNG, JPEG, JPG, GIF, BMP, WebP

### Output Formats
- Images: PNG (high quality)
- Videos: MP4 (H.264 codec)

## Troubleshooting

### Common Issues

1. **Out of memory errors**:
   - Reduce image resolution (use 512x512 instead of 1024x1024)
   - Use fewer inference steps
   - Enable CPU mode by setting `CUDA_VISIBLE_DEVICES=""`

2. **Slow generation**:
   - Ensure CUDA is properly installed
   - Use a GPU with more VRAM
   - Reduce number of inference steps

3. **Model download issues**:
   - Check internet connection
   - Ensure sufficient disk space
   - Try restarting the application

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Ensure all requirements are properly installed
3. Verify your system meets the minimum requirements
4. Try using smaller image sizes or fewer inference steps

## Advanced Usage

### Custom Models
You can use different AI models by modifying the `MODELS` configuration in `config.py`.

### Batch Processing
Use the CLI for batch operations:
```bash
# Generate multiple variations
for i in {1..5}; do
    python cli.py text-to-image "A fantasy castle" --seed $i
done
```

### API Integration
The core `AIGenerator` class can be imported and used in your own Python scripts:
```python
from ai_generator import AIGenerator

generator = AIGenerator()
images = generator.generate_image_from_text("Your prompt here")
generator.save_images(images, "my_prefix")
```

## License

This project is open source. Please check the repository for license details.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Acknowledgments

This project uses several open-source AI models and libraries:
- Stable Diffusion models from Stability AI and RunwayML
- Hugging Face Transformers and Diffusers libraries
- PyTorch deep learning framework
