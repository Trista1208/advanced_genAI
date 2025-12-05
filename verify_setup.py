#!/usr/bin/env python3
"""
Verification script to check if the environment is properly set up.
Run this after setup to ensure all dependencies and configurations are correct.
"""

import sys
import os
from pathlib import Path

def print_status(check_name, passed, message=""):
    """Print colored status message."""
    status = "✓" if passed else "✗"
    color = "\033[92m" if passed else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{status}{reset} {check_name}", end="")
    if message:
        print(f": {message}")
    else:
        print()
    return passed

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    passed = version.major == 3 and version.minor >= 8
    return print_status(
        "Python version",
        passed,
        f"{version.major}.{version.minor}.{version.micro}" + 
        ("" if passed else " (need 3.8+)")
    )

def check_dependencies():
    """Check if required packages are installed."""
    required = [
        "bs4", "docling", "dateparser", "yake", "lingua",
        "spacy", "openai", "pydantic", "dotenv", "pdfplumber"
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    passed = len(missing) == 0
    message = "All installed" if passed else f"Missing: {', '.join(missing)}"
    return print_status("Python packages", passed, message)

def check_spacy_models():
    """Check if spaCy language models are installed."""
    try:
        import spacy
        models = {"en_core_web_sm": False, "de_core_news_sm": False}
        
        for model in models.keys():
            try:
                spacy.load(model)
                models[model] = True
            except OSError:
                pass
        
        installed = [k for k, v in models.items() if v]
        missing = [k for k, v in models.items() if not v]
        
        passed = len(missing) == 0
        if passed:
            message = f"Installed: {', '.join(installed)}"
        else:
            message = f"Missing: {', '.join(missing)}"
        return print_status("spaCy models", passed, message)
    except ImportError:
        return print_status("spaCy models", False, "spaCy not installed")

def check_env_file():
    """Check if .env file exists and has API key."""
    env_path = Path(".env")
    if not env_path.exists():
        return print_status(".env file", False, "Not found")
    
    content = env_path.read_text()
    has_key = "OPENAI_API_KEY" in content and "your-api-key-here" not in content
    
    message = "Configured" if has_key else "Found but key not set"
    return print_status(".env file", has_key, message)

def check_directories():
    """Check if required directories exist."""
    required_dirs = [
        "data", "data_cleaned", "benchmark", "subsample"
    ]
    
    existing = []
    missing = []
    
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            existing.append(dir_name)
        else:
            missing.append(dir_name)
    
    passed = len(missing) == 0
    if passed:
        message = "All present"
    else:
        message = f"Missing: {', '.join(missing)} (run setup_directories.py)"
    return print_status("Directories", passed, message)

def check_input_data():
    """Check if input data exists."""
    data_dir = Path("data")
    if not data_dir.exists():
        return print_status("Input HTML files", False, "data/ directory not found")
    
    html_files = list(data_dir.rglob("*.html"))
    passed = len(html_files) > 0
    message = f"Found {len(html_files)} HTML files" if passed else "No HTML files found"
    return print_status("Input HTML files", passed, message)

def check_scripts():
    """Check if all pipeline scripts exist."""
    scripts = [
        "step_1_hybrid.py",
        "step_1_2_advanced_cleaning_and_metadata.py",
        "step_1_3_validation_filter.py",
        "step_1_4_benchmark_extraction.py",
        "2_1_llm_metadataextraction.py",
        "2_1_2_relevance_score.py"
    ]
    
    missing = [s for s in scripts if not Path(s).exists()]
    passed = len(missing) == 0
    message = "All present" if passed else f"Missing: {', '.join(missing)}"
    return print_status("Pipeline scripts", passed, message)

def main():
    print("=" * 60)
    print("Advanced GenAI Pipeline - Setup Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("spaCy Models", check_spacy_models),
        ("Environment Config", check_env_file),
        ("Directory Structure", check_directories),
        ("Pipeline Scripts", check_scripts),
        ("Input Data", check_input_data),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            results.append(check_func())
        except Exception as e:
            print_status(name, False, f"Error: {e}")
            results.append(False)
    
    print()
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All checks passed! ({passed}/{total})")
        print("\nYou're ready to run the pipeline!")
        print("Start with: python step_1_hybrid.py data data_cleaned/minimal_hybrid")
        return 0
    else:
        print(f"⚠️  {passed}/{total} checks passed")
        print("\nFix the issues above before running the pipeline.")
        print("\nCommon fixes:")
        print("  • Install dependencies: pip install -r requirements.txt")
        print("  • Download spaCy models: python -m spacy download en_core_web_sm")
        print("  • Create directories: python setup_directories.py")
        print("  • Configure API key: Edit .env file")
        print("  • Add input data: Place HTML files in data/ directory")
        return 1

if __name__ == "__main__":
    sys.exit(main())

