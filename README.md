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

### VS Code Setup

To run and develop this project in Visual Studio Code:

1. **Open the project**:
   - Open VS Code
   - Use `File > Open Folder` and select the `AITest` directory
   - Or use the command line: `code .` from the project directory

2. **Recommended VS Code extensions**:
   - **Python** (Microsoft) - Essential for Python development
   - **Python Debugger** (Microsoft) - For debugging Python code
   - **Pylance** (Microsoft) - Enhanced Python language support
   - **Jupyter** (Microsoft) - If you want to work with notebooks
   - **GitLens** (GitKraken) - Enhanced Git integration

3. **Configure Python interpreter**:
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) to open Command Palette
   - Type "Python: Select Interpreter"
   - Choose the interpreter from your virtual environment: `./venv/bin/python`

4. **VS Code workspace settings** (included):
   This project includes pre-configured VS Code settings in the `.vscode/` folder:
   - `settings.json` - Python interpreter, linting, and formatting settings
   - `tasks.json` - Common tasks like starting the web app and running tests
   - `launch.json` - Debug configurations for different components
   - `extensions.json` - Recommended extensions for the best development experience
   
   VS Code will automatically suggest installing the recommended extensions when you open the project.

5. **Running the application in VS Code**:
   - **Web Interface**: Open terminal in VS Code (`Terminal > New Terminal`) and run:
     ```bash
     python web_app.py
     ```
   - **CLI Interface**: Use the integrated terminal for CLI commands:
     ```bash
     python cli.py text-to-image "Your prompt here"
     ```
   - **Debug Mode**: Set breakpoints in the code and use F5 to start debugging
   - **Using Tasks**: Press `Ctrl+Shift+P` and type "Tasks: Run Task" to access pre-configured tasks

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
