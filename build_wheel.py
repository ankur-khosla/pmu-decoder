#!/usr/bin/env python3
"""
Build script for AB Race Translator package

This script automates the build process including:
- Cleaning previous builds
- Validating package structure
- Creating required files
- Building source distribution and wheel
- Verifying the build
- Creating examples
"""

import os
import sys
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


def clean_build():
    """Clean previous build artifacts."""
    print("🧹 Cleaning previous builds...")
    
    dirs_to_clean = ['build', 'dist', 'ab_race_translator.egg-info', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")
    
    # Clean .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))
    
    print("✅ Build cleanup completed")


def validate_structure():
    """Validate package structure."""
    print("🔍 Validating package structure...")
    
    required_files = [
        'ab_race_translator/__init__.py',
        'ab_race_translator/ab_race.py',
        'ab_race_translator/ab_msg_translator.py',
        'ab_race_translator/constants.py',
        'ab_race_translator/data_structures.py',
        'ab_race_translator/utils.py',
        'ab_race_translator/example_usage.py',
        'setup.py',
        'pyproject.toml',
        'README.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ Package structure validation passed")
    return True


def create_required_files():
    """Create additional required files."""
    print("📄 Creating required files...")
    
    # Create LICENSE file
    if not os.path.exists('LICENSE'):
        with open('LICENSE', 'w') as f:
            f.write("""MIT License

Copyright (c) 2024 AB Race Translator

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")
        print("   Created LICENSE")
    
    # Create MANIFEST.in
    if not os.path.exists('MANIFEST.in'):
        with open('MANIFEST.in', 'w') as f:
            f.write("""include README.md
include LICENSE
include pyproject.toml
include requirements*.txt
recursive-include ab_race_translator *.py
recursive-exclude * __pycache__
recursive-exclude * *.py[co]
""")
        print("   Created MANIFEST.in")
    
    # Create requirements.txt
    if not os.path.exists('requirements.txt'):
        with open('requirements.txt', 'w') as f:
            f.write("""# No external dependencies required for core functionality
""")
        print("   Created requirements.txt")
    
    # Create requirements-dev.txt
    if not os.path.exists('requirements-dev.txt'):
        with open('requirements-dev.txt', 'w') as f:
            f.write("""pytest>=7.0.0
pytest-cov>=4.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
isort>=5.12.0
build>=0.10.0
twine>=4.0.0
""")
        print("   Created requirements-dev.txt")
    
    # Create py.typed file for type checking
    py_typed_path = 'ab_race_translator/py.typed'
    if not os.path.exists(py_typed_path):
        with open(py_typed_path, 'w') as f:
            f.write('')  # Empty file indicates package supports typing
        print("   Created py.typed")
    
    print("✅ Required files created")


def install_build_dependencies():
    """Install build dependencies."""
    print("📦 Installing build dependencies...")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '--upgrade',
            'build', 'setuptools', 'wheel', 'twine'
        ], check=True, capture_output=True)
        print("✅ Build dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install build dependencies: {e}")
        return False


def build_package():
    """Build the package."""
    print("🔨 Building package...")
    
    try:
        # Build using modern build tool
        result = subprocess.run([
            sys.executable, '-m', 'build'
        ], check=True, capture_output=True, text=True)
        
        print("✅ Package built successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"   stdout: {e.stdout}")
        print(f"   stderr: {e.stderr}")
        return False


def verify_build():
    """Verify the built package."""
    print("🔬 Verifying build...")
    
    # Check if dist directory exists and has files
    if not os.path.exists('dist'):
        print("❌ dist/ directory not found")
        return False
    
    dist_files = os.listdir('dist')
    if not dist_files:
        print("❌ No files in dist/ directory")
        return False
    
    # Check for wheel and source distribution
    has_wheel = any(f.endswith('.whl') for f in dist_files)
    has_sdist = any(f.endswith('.tar.gz') for f in dist_files)
    
    if not has_wheel:
        print("⚠️  Warning: No wheel (.whl) file found")
    if not has_sdist:
        print("⚠️  Warning: No source distribution (.tar.gz) file found")
    
    print(f"📁 Built files in dist/:")
    for file in dist_files:
        file_path = os.path.join('dist', file)
        file_size = os.path.getsize(file_path)
        print(f"   - {file} ({file_size:,} bytes)")
    
    # Test import in clean environment
    print("🧪 Testing package import...")
    
    # Find the wheel file
    wheel_files = [f for f in dist_files if f.endswith('.whl')]
    if wheel_files:
        wheel_path = os.path.join('dist', wheel_files[0])
        
        # Test installation and import in temporary environment
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Install in temp directory
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', '--target', temp_dir, wheel_path
                ], check=True, capture_output=True)
                
                # Test import
                old_path = sys.path.copy()
                sys.path.insert(0, temp_dir)
                
                try:
                    import ab_race_translator
                    from ab_race_translator import create_ab_race
                    
                    # Test basic functionality
                    translator = create_ab_race()
                    print("✅ Package import and basic functionality test passed")
                    
                except ImportError as e:
                    print(f"❌ Import test failed: {e}")
                    return False
                finally:
                    sys.path = old_path
                    
            except subprocess.CalledProcessError as e:
                print(f"❌ Package installation test failed: {e}")
                return False
    
    print("✅ Build verification completed")
    return True


def create_examples():
    """Create examples directory with sample files."""
    print("📚 Creating examples...")
    
    examples_dir = 'examples'
    if not os.path.exists(examples_dir):
        os.makedirs(examples_dir)
    
    # Copy example usage
    if os.path.exists('ab_race_translator/example_usage.py'):
        shutil.copy2('ab_race_translator/example_usage.py', 
                     os.path.join(examples_dir, 'basic_usage.py'))
    
    # Create test import script
    test_import_content = '''#!/usr/bin/env python3
"""
Test script to verify ab_race_translator installation and basic functionality.
"""

def test_import():
    """Test package import."""
    try:
        import ab_race_translator
        print("✅ ab_race_translator imported successfully")
        
        from ab_race_translator import create_ab_race, Msg
        print("✅ Main classes imported successfully")
        
        # Test translator creation
        translator = create_ab_race()
        print("✅ Translator created successfully")
        
        # Test with sample data
        from ab_race_translator.data_structures import create_sample_msg
        msg = create_sample_msg()
        print("✅ Sample message created successfully")
        
        # Test translation
        result = translator.translate_action(msg)
        print(f"✅ Translation successful: {len(result)} characters")
        
        print("\\n🎉 All tests passed! Package is working correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    test_import()
'''
    
    with open(os.path.join(examples_dir, 'test_import.py'), 'w') as f:
        f.write(test_import_content)
    
    # Create requirements file for examples
    with open(os.path.join(examples_dir, 'requirements.txt'), 'w') as f:
        f.write("ab-race-translator>=1.0.0\n")
    
    print("✅ Examples created")


def print_summary():
    """Print build summary."""
    print("\n" + "="*60)
    print("🎉 AB Race Translator Build Summary")
    print("="*60)
    
    if os.path.exists('dist'):
        dist_files = os.listdir('dist')
        print(f"📦 Built {len(dist_files)} package(s):")
        for file in dist_files:
            file_path = os.path.join('dist', file)
            file_size = os.path.getsize(file_path)
            print(f"   • {file} ({file_size:,} bytes)")
    
    print("\n📋 Next Steps:")
    print("   1. Test the package:")
    print("      python examples/test_import.py")
    print("   2. Install the package:")
    print("      pip install dist/ab_race_translator-1.0.0-py3-none-any.whl")
    print("   3. Run examples:")
    print("      python examples/basic_usage.py")
    print("   4. Upload to PyPI (optional):")
    print("      twine upload dist/*")
    
    print("\n✨ Build completed successfully!")


def main():
    """Main build function."""
    print("🚀 Starting AB Race Translator build process...")
    print("="*60)
    
    try:
        # Step 1: Clean previous builds
        clean_build()
        
        # Step 2: Validate package structure
        if not validate_structure():
            sys.exit(1)
        
        # Step 3: Create required files
        create_required_files()
        
        # Step 4: Install build dependencies
        if not install_build_dependencies():
            sys.exit(1)
        
        # Step 5: Build package
        if not build_package():
            sys.exit(1)
        
        # Step 6: Verify build
        if not verify_build():
            sys.exit(1)
        
        # Step 7: Create examples
        create_examples()
        
        # Step 8: Print summary
        print_summary()
        
    except KeyboardInterrupt:
        print("\n❌ Build interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Build failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()