import qrcode
import numpy as np
import os
import logging
from urllib.parse import urlparse
from pathlib import Path
import sys
import argparse
import json
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import yaml
import configparser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class QRCodeGenerator:
    """
    A class for generating QR codes from URLs.
    """

    def __init__(
        self,
        urls: List[str],
        output_directory: str = "qr_codes",
        config: Optional[Dict] = None
    ):
        """
        Initialize the QRCodeGenerator.
        
        Args:
            urls: List of URLs to process
            output_directory: Directory to save QR codes
            config: Optional configuration dictionary
        """
        self.urls = urls
        self.output_directory = output_directory
        self.config = config or {}
        
        # Set default configuration
        # Set default configuration
        self.version = self.config.get('version', 5)
        self.error_correction = self.config.get('error_correction', qrcode.constants.ERROR_CORRECT_H)
        self.box_size = self.config.get('box_size', 10)
        self.border = self.config.get('border', 4)
        self.fill_color = self.config.get('fill_color', "black")
        self.back_color = self.config.get('back_color', "white")
        
        # Batch processing settings
        self.batch_size = self.config.get('batch_size', 100)
        self.max_workers = self.config.get('max_workers', 4)
        
        # Log configuration values in debug mode
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"QR Code Configuration:")
            logger.debug(f"  Version: {self.version}")
            logger.debug(f"  Error Correction: {self.error_correction}")
            logger.debug(f"  Box Size: {self.box_size}")
            logger.debug(f"  Border: {self.border}")
            logger.debug(f"  Fill Color: {self.fill_color}")
            logger.debug(f"  Back Color: {self.back_color}")
            logger.debug(f"  Batch Size: {self.batch_size}")
            logger.debug(f"  Max Workers: {self.max_workers}")
        """
        Initialize the QRCodeGenerator.
        
        Args:
            urls: List of URLs to process
            output_directory: Directory to save QR codes
            config: Optional configuration dictionary
        """
        self.urls = urls
        self.output_directory = output_directory
        self.config = config or {}
        
        # Set default configuration
        self.version = self.config.get('version', 5)
        self.error_correction = self.config.get('error_correction', qrcode.constants.ERROR_CORRECT_H)
        self.box_size = self.config.get('box_size', 10)
        self.border = self.config.get('border', 4)
        self.fill_color = self.config.get('fill_color', "black")
        self.back_color = self.config.get('back_color', "white")

    def _generate_single_qr(self, url: str) -> bool:
        """
        Generate a single QR code for a URL.
        
        Args:
            url: URL to generate QR code for
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate URL
            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                raise ValueError(f"Invalid URL format: {url}")

            # Generate QR code
            qr = qrcode.QRCode(
                version=self.version,
                error_correction=self.error_correction,
                box_size=self.box_size,
                border=self.border,
            )
            qr.add_data(url)
            qr.make(fit=True)

            # Create an image of the QR code
            img = qr.make_image(
                fill_color=self.fill_color,
                back_color=self.back_color
            )

            # Generate safe filename
            url_slug = parsed_url.netloc.replace(".", "_")
            filename = os.path.join(self.output_directory, f"qrcode_{url_slug}.png")
            
            # Save the QR code image
            img.save(filename)
            logger.info(f"Successfully saved QR code for {url} as {filename}")
            return True

        except Exception as e:
            logger.error(f"Failed to process URL {url}: {str(e)}")
            return False

    def generate_all(self) -> int:
        """
        Generate QR codes for all URLs in batches.
        
        Returns:
            int: Number of successfully generated QR codes
        """
        try:
            # Create output directory
            Path(self.output_directory).mkdir(parents=True, exist_ok=True)
            
            total_urls = len(self.urls)
            logger.info(f"Starting QR code generation for {total_urls} URLs")
            logger.info(f"Processing in batches of {self.batch_size} URLs")
            
            successful = 0
            
            # Process URLs in batches
            for batch_idx, batch in enumerate(self._batch_urls(self.urls, self.batch_size), 1):
                logger.info(f"Processing batch {batch_idx} (size: {len(batch)})")
                
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    results = list(tqdm(
                        executor.map(self._generate_single_qr, batch),
                        total=len(batch),
                        desc=f"Batch {batch_idx} of {len(batch)}",
                        unit="QR codes"
                    ))
                
                batch_successful = sum(results)
                successful += batch_successful
                
                logger.info(f"Batch {batch_idx} completed. {batch_successful}/{len(batch)} successful")
                
            logger.info(f"QR code generation completed. Successfully generated {successful} out of {total_urls} QR codes.")
            return successful
            
        except Exception as e:
            logger.error(f"Failed to generate QR codes: {str(e)}")
            raise

    def _batch_urls(self, urls: List[str], batch_size: int) -> List[List[str]]:
        """
        Split URLs into batches.
        
        Args:
            urls: List of URLs to batch
            batch_size: Size of each batch
            
        Returns:
            List of URL batches
        """
        return [urls[i:i + batch_size] for i in range(0, len(urls), batch_size)]
        """
        Generate QR codes for all URLs.
        
        Args:
            max_workers: Maximum number of concurrent workers
            
        Returns:
            int: Number of successfully generated QR codes
        """
        try:
            # Create output directory
            Path(self.output_directory).mkdir(parents=True, exist_ok=True)
            
            # Process URLs with progress bar
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                results = list(tqdm(
                    executor.map(self._generate_single_qr, self.urls),
                    total=len(self.urls),
                    desc="Generating QR codes",
                    unit="QR codes"
                ))
            
            successful = sum(results)
            logger.info(f"QR code generation completed. Successfully generated {successful} out of {len(self.urls)} QR codes.")
            return successful
            
        except Exception as e:
            logger.error(f"Failed to generate QR codes: {str(e)}")
            raise

def load_urls_from_file(file_path: str) -> List[str]:
    """
    Load URLs from a file. Supports JSON, YAML, and INI formats.
    
    Args:
        file_path: Path to the file containing URLs
        
    Returns:
        List of URLs
    """
    try:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext == '.json':
            with open(file_path) as f:
                return json.load(f)
        elif ext in ['.yaml', '.yml']:
            with open(file_path) as f:
                return yaml.safe_load(f)
        elif ext == '.ini':
            config = configparser.ConfigParser()
            config.read(file_path)
            return config['urls']['urls'].split(',')
        else:
            with open(file_path) as f:
                return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logger.error(f"Failed to load URLs from file {file_path}: {str(e)}")
        raise

def load_config(config_path: str) -> Dict:
    """
    Load configuration from a file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Configuration dictionary
    """
    try:
        if not os.path.exists(config_path):
            return {}
            
        with open(config_path) as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load configuration from {config_path}: {str(e)}")
        return {}
    """
    Generates QR codes for a list of URLs and saves them to the specified directory.

    Parameters:
        urls (list of str): List of URLs to generate QR codes for.
        output_directory (str): Directory to save the QR code images.
        version (int): QR code version (1-40)
        error_correction (int): Error correction level
        box_size (int): Size of each box in pixels
        border (int): Width of the border in boxes
        fill_color (str): Color of the QR code
        back_color (str): Background color

    Returns:
        None

    Raises:
        ValueError: If invalid parameters are provided
        Exception: If QR code generation fails
    """
    if not urls:
        raise ValueError("URL list cannot be empty")

    # Create the output directory if it doesn't exist
    try:
        Path(output_directory).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create output directory: {e}")
        raise

    total_urls = len(urls)
    logger.info(f"Starting QR code generation for {total_urls} URLs")

    for i, url in enumerate(urls, 1):
        try:
            # Validate URL
            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                raise ValueError(f"Invalid URL format: {url}")

            logger.info(f"Processing URL {i}/{total_urls}: {url}")

            # Generate QR code
            qr = qrcode.QRCode(
                version=version,
                error_correction=error_correction,
                box_size=box_size,
                border=border,
            )
            qr.add_data(url)
            qr.make(fit=True)

            # Create an image of the QR code
            img = qr.make_image(
                fill_color=fill_color,
                back_color=back_color
            )

            # Generate safe filename
            url_slug = parsed_url.netloc.replace(".", "_")
            filename = os.path.join(output_directory, f"qrcode_{url_slug}.png")
            
            # Save the QR code image
            img.save(filename)
            logger.info(f"Successfully saved QR code for {url} as {filename}")

        except Exception as e:
            logger.error(f"Failed to process URL {url}: {str(e)}")
            continue

    logger.info("QR code generation completed")

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Generate QR codes from URLs")
    
    # Add debug option
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    # Required arguments
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--urls',
        nargs='+',
        help='List of URLs to generate QR codes for'
    )
    input_group.add_argument(
        '--url-file',
        help='Path to file containing URLs (one per line or JSON/YAML format)'
    )
    
    parser.add_argument(
        '--output-dir',
        required=True,
        help='Directory to save QR code images'
    )
    
    # Optional arguments
    parser.add_argument(
        '--config',
        help='Path to configuration file (YAML format)'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of concurrent workers to use'
    )
    parser.add_argument(
        '--version',
        type=int,
        choices=range(1, 41),
        help='QR code version (1-40)'
    )
    parser.add_argument(
        '--box-size',
        type=int,
        default=10,
        help='Size of each box in pixels'
    )
    parser.add_argument(
        '--border',
        type=int,
        default=4,
        help='Width of the border in boxes'
    )
    parser.add_argument(
        '--fill-color',
        default='black',
        help='Color of the QR code'
    )
    parser.add_argument(
        '--back-color',
        default='white',
        help='Background color'
    )
    parser.add_argument(
        '--error-correction',
        choices=['L', 'M', 'Q', 'H'],
        default='H',
        help='Error correction level (L, M, Q, H)'
    )

    # Parse arguments
    args = parser.parse_args()

    # Configure logging based on debug flag
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load base configuration from file
    base_config = load_config(args.config) if args.config else {}
    
    # Get QR settings from nested config
    qr_config = base_config.get('qr', {})
    processing_config = base_config.get('processing', {})
    
    # Create initial config with defaults from YAML
    config = {
        'version': qr_config.get('version', 5),
        'error_correction': qr_config.get('error_correction', 'H'),
        'box_size': qr_config.get('box_size', 10),
        'border': qr_config.get('border', 4),
        'fill_color': qr_config.get('fill_color', 'black'),
        'back_color': qr_config.get('back_color', 'white'),
        'batch_size': processing_config.get('batch_size', 100),
        'max_workers': processing_config.get('max_workers', 4)
    }
    
    # Override with command-line arguments
    if args.version is not None:
        config['version'] = args.version
    if args.box_size is not None:
        config['box_size'] = args.box_size
    if args.border is not None:
        config['border'] = args.border
    if args.fill_color is not None:
        config['fill_color'] = args.fill_color
    if args.back_color is not None:
        config['back_color'] = args.back_color
    if args.error_correction is not None:
        config['error_correction'] = args.error_correction
    if args.workers is not None:
        config['max_workers'] = args.workers
    
    # Convert error correction level to constant
    error_correction_map = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H
    }
    config['error_correction'] = error_correction_map.get(config['error_correction'].upper(), qrcode.constants.ERROR_CORRECT_H)

    # Create QRCodeGenerator instance with final configuration
    generator = QRCodeGenerator(
        urls=args.urls if args.urls else load_urls_from_file(args.url_file),
        output_directory=args.output_dir,
        config=config
    )

    try:
        # Generate QR codes
        success_count = generator.generate_all()
        logger.info(f"Successfully generated {success_count} QR codes")
        
        if success_count == 0:
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Failed to generate QR codes: {str(e)}")
        sys.exit(1)
