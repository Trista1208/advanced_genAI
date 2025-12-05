#!/usr/bin/env python3
"""
Setup script to create necessary directory structure for the pipeline.
Run this before processing any data.
"""

import os
from pathlib import Path

def create_directory_structure():
    """Create all necessary directories for the pipeline."""
    
    directories = [
        # Input data
        "data",
        
        # Stage 1 outputs
        "data_cleaned/minimal_hybrid",
        "data_cleaned/advanced",
        "data_cleaned/advanced_validated",
        
        # Benchmark data
        "benchmark",
        "benchmark/metadata",
        "benchmark/score",
        
        # Chunked data
        "subsample",
        "subsample/semantic_chunk",
        
        # Logs
        "logs",
    ]
    
    print("Creating directory structure...")
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {dir_path}")
    
    print("\n✅ Directory structure created successfully!")
    print("\nNext steps:")
    print("1. Place your HTML files in the 'data/' directory")
    print("2. Place your benchmark PDF in the 'benchmark/' directory")
    print("3. Run the pipeline scripts in order (see README.md)")

if __name__ == "__main__":
    create_directory_structure()

