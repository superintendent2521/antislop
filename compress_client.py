#!/usr/bin/env python3
"""
Compress the client directory into an XPI file using deflate compression.
This is the format expected by Firefox for WebExtensions.
"""

import os
import zipfile
import argparse
from pathlib import Path

def compress_client_to_xpi(source_dir="client", output_file="client/antislop-youtube-blocker.xpi"):
    """
    Compress the client directory into an XPI file using deflate compression.
    
    Args:
        source_dir (str): Path to the client directory to compress
        output_file (str): Path for the output XPI file
    """
    source_path = Path(source_dir)
    output_path = Path(output_file)
    
    if not source_path.exists():
        raise FileNotFoundError(f"Source directory '{source_dir}' does not exist")
    
    if not source_path.is_dir():
        raise ValueError(f"Source path '{source_dir}' is not a directory")
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create XPI file with deflate compression
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as xpi:
        # Walk through the source directory
        for root, dirs, files in os.walk(source_path):
            for file in files:
                # Skip the existing XPI file if it exists
                if file.endswith('.xpi'):
                    continue
                    
                file_path = Path(root) / file
                # Calculate the relative path within the XPI
                arc_path = file_path.relative_to(source_path)
                
                # Add file to XPI with deflate compression
                xpi.write(file_path, arc_path)
                print(f"Added: {arc_path}")
    
    print(f"\nSuccessfully created XPI file: {output_path}")
    print(f"File size: {output_path.stat().st_size:,} bytes")

def main():
    parser = argparse.ArgumentParser(description="Compress client directory to XPI file")
    parser.add_argument("-s", "--source", default="client", 
                       help="Source directory to compress (default: client)")
    parser.add_argument("-o", "--output", default="client/antislop-youtube-blocker.xpi",
                       help="Output XPI file path (default: client/antislop-youtube-blocker.xpi)")
    
    args = parser.parse_args()
    
    try:
        compress_client_to_xpi(args.source, args.output)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
