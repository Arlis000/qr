# QR Code Generator

A Python-based tool for generating QR codes from URLs with support for command-line arguments, configuration files, and batch processing.

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Features

- Generate QR codes from URLs
- Support for command-line arguments and configuration files
- Batch processing with configurable worker count
- Configurable QR code settings (version, error correction, box size, colors)
- Support for multiple color formats (names, hex, RGB, RGBA)
- Debug mode for detailed logging

## Usage

### Basic Usage

Generate QR codes for a single URL:
```bash
python qr_code.py --urls "https://example.com" --output-dir qr_codes
```

### Using URL File

Create a file with URLs (one per line, JSON, or YAML format):
```bash
# urls.txt
https://example.com
https://google.com
```

Then run:
```bash
python qr_code.py --url-file urls.txt --output-dir qr_codes
```

### Using Configuration File

Create a `config.yaml` file with nested structure:
```bash
python qr_code.py --url-file urls.txt --output-dir qr_codes --config config.yaml
```

### Debug Mode

Enable debug logging to see detailed configuration and processing information:
```bash
python qr_code.py --debug --urls "https://example.com" --output-dir qr_codes
```

## Command-Line Arguments

### Required Arguments

```bash
--urls URLS             List of URLs to generate QR codes for
--url-file URL_FILE     Path to file containing URLs (one per line, JSON, or YAML format)
--output-dir OUTPUT_DIR Directory to save QR code images
```

### Optional Arguments

```bash
--config CONFIG         Path to configuration file (YAML format)
--workers WORKERS       Number of concurrent workers to use (default: 4)
--version VERSION       QR code version (1-40) (default: 5)
--box-size BOX_SIZE     Size of each box in pixels (default: 10)
--border BORDER         Width of the border in boxes (default: 4)
--fill-color FILL_COLOR Color of the QR code (default: black)
--back-color BACK_COLOR Background color (default: white)
--error-correction ERR_CORR Error correction level (L, M, Q, H) (default: H)
--debug                Enable debug logging
--version-info         Show program's version number and exit
```

## Configuration File

The configuration file (`config.yaml`) supports a nested structure with the following options:

### Basic Settings
```yaml
output_directory: qr_codes       # Directory for QR code output
batch_size: 100                  # Number of URLs to process in each batch
```

### QR Code Settings
```yaml
qr:
  version: 5                     # QR code version (1-40)
  error_correction: H            # Error correction level (L, M, Q, H)
  box_size: 10                   # Size of each box in pixels
  border: 4                      # Width of the border in boxes
  fill_color: black              # Color of the QR code
  back_color: white              # Background color
```

### Processing Settings
```yaml
processing:
  max_workers: 4                 # Maximum number of concurrent workers
  timeout: 30                    # Timeout for URL processing
  retry_attempts: 3              # Number of retry attempts
  retry_delay: 5                 # Delay between retries
```

### Color Formats

The `fill_color` and `back_color` settings support multiple formats:
- Color names (e.g., "red", "blue", "black", "white")
- Hex values (e.g., "#FF0000", "#F00")
- RGB tuples (e.g., (255, 0, 0))
- RGBA tuples (e.g., (255, 0, 0, 255))

### URL Validation
```yaml
url_validation:
  enabled: true                  # Enable URL validation
  timeout: 5                     # Validation timeout
  max_retries: 2                 # Maximum validation retries
  retry_delay: 2                 # Delay between validation retries
```

### Logging
```yaml
logging:
  level: INFO                    # Logging level (DEBUG, INFO, WARNING, ERROR)
  format: '%(asctime)s - %(levelname)s - %(message)s'
  file: qr_generator.log         # Log file name
  max_size: 10485760            # Maximum log file size (10MB)
  backup_count: 5                # Number of backup log files
```

### Error Handling
```yaml
error_handling:
  continue_on_error: true        # Continue processing after errors
  max_errors: 10                 # Maximum number of errors before stopping
  error_threshold: 0.1           # Error rate threshold (10%)
```

### File Handling
```yaml
file_handling:
  max_file_size: 1048576         # Maximum file size (1MB)
  max_files_per_batch: 1000      # Maximum files per batch
  compress_output: false         # Compress output files
```

### Advanced Settings
```yaml
advanced:
  cache_enabled: true            # Enable caching
  cache_timeout: 3600            # Cache timeout in seconds
  cache_size: 100                # Maximum cache size
  use_proxy: false               # Use proxy for URL validation
  proxy_url: ""                  # Proxy URL
  proxy_timeout: 10              # Proxy timeout
```

### Notifications (Optional)
```yaml
notifications:
  enabled: false                 # Enable email notifications
  smtp_server: ""                # SMTP server
  smtp_port: 587                 # SMTP port
  sender_email: ""               # Sender email
  recipient_email: ""            # Recipient email
  use_tls: true                  # Use TLS for email
```

## Examples

### Generate QR codes from command line
```bash
python qr_code.py \
    --urls "https://example.com" "https://google.com" \
    --output-dir output \
    --version 5 \
    --box-size 12 \
    --border 5
```

### Generate QR codes from file with configuration
```bash
python qr_code.py \
    --url-file urls.txt \
    --output-dir output \
    --config config.yaml \
    --workers 8
```

### Generate QR codes with custom colors
```bash
python qr_code.py \
    --urls "https://example.com" \
    --output-dir output \
    --fill-color "#FF0000" \
    --back-color "#FFFFFF"
```

## Notes

- URLs can be provided either through command-line arguments or from a file
- The output directory will be created if it doesn't exist
- Configuration file values can be overridden by command-line arguments
- Progress is shown using a progress bar during generation
- Logs are saved to `qr_generator.log` by default

## Requirements

- Python 3.7+
- pip
- virtualenv (recommended)

## License

MIT License
