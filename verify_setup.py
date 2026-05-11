"""
Simple test script to verify the web app setup
Run this to make sure everything is configured correctly
"""

import sys
import importlib

def check_dependency(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name}")
        return True
    except ImportError:
        print(f"❌ {package_name} - Install with: pip install {package_name}")
        return False

def check_data_files():
    """Check if data files exist"""
    import os
    from pathlib import Path
    
    data_dir = Path("./albany-data")
    required_files = ["calendar.csv", "listings.csv", "reviews.csv"]
    
    all_exist = True
    for file in required_files:
        file_path = data_dir / file
        if file_path.exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - Missing!")
            all_exist = False
    
    return all_exist

def check_models():
    """Check if trained models exist"""
    from pathlib import Path
    
    model_dir = Path("./models")
    required_models = [
        "occupancy_model.pkl",
        "occupancy_features.pkl",
        "price_model.pkl",
        "price_features.pkl"
    ]
    
    all_exist = True
    for model in required_models:
        model_path = model_dir / model
        if model_path.exists():
            print(f"✅ {model}")
        else:
            print(f"⚠️  {model} - Not found (run: python model_trainer.py)")
            all_exist = False
    
    return all_exist

def main():
    print("\n" + "="*50)
    print("🔍 Albany Airbnb App - Setup Verification")
    print("="*50 + "\n")
    
    # Check dependencies
    print("📦 Checking Dependencies...")
    dependencies = [
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("streamlit", "streamlit"),
        ("scikit-learn", "sklearn"),
        ("lightgbm", "lightgbm"),
        ("plotly", "plotly"),
        ("joblib", "joblib"),
    ]
    
    deps_ok = all(check_dependency(pkg, imp) for pkg, imp in dependencies)
    
    # Check data files
    print("\n📊 Checking Data Files...")
    data_ok = check_data_files()
    
    # Check models
    print("\n🤖 Checking Models...")
    models_ok = check_models()
    
    # Summary
    print("\n" + "="*50)
    print("📋 Setup Summary")
    print("="*50)
    
    if deps_ok:
        print("✅ All dependencies installed")
    else:
        print("❌ Missing dependencies - run: pip install -r requirements.txt")
    
    if data_ok:
        print("✅ All data files found")
    else:
        print("❌ Missing data files in ./albany-data/")
    
    if models_ok:
        print("✅ All models trained")
    else:
        print("⚠️  Models not trained yet")
        print("   Run: python model_trainer.py")
    
    print("\n" + "="*50)
    
    if deps_ok and data_ok and models_ok:
        print("✅ Setup Complete! Ready to go!")
        print("\n🚀 Start the app with:")
        print("   streamlit run app.py")
        return 0
    elif deps_ok and data_ok:
        print("⚠️  Almost ready!")
        print("\n🚀 Train models with:")
        print("   python model_trainer.py")
        print("\nThen start the app with:")
        print("   streamlit run app.py")
        return 1
    else:
        print("❌ Setup incomplete")
        print("\n📚 Follow the setup guide:")
        print("   cat QUICKSTART.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
