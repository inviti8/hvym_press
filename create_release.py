#!/usr/bin/env python3
"""
Helper script to create and push version tags for GitHub Actions releases
"""

import subprocess
import sys
import re
from pathlib import Path

def run_command(cmd, check=True, capture_output=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=capture_output, text=True)
        return result
    except subprocess.CalledProcessError as e:
        if capture_output:
            print(f"Command failed: {cmd}")
            print(f"Error: {e}")
            if e.stdout:
                print(f"Output: {e.stdout}")
            if e.stderr:
                print(f"Error: {e.stderr}")
        return e

def get_current_version():
    """Get the current version from git tags"""
    result = run_command("git tag --sort=-version:refname | head -n 1")
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    return "v0.00"  # Default if no tags exist

def validate_version_format(version):
    """Validate version format (vX.XX)"""
    pattern = r'^v\d+\.\d{2}$'
    if not re.match(pattern, version):
        print(f"❌ Invalid version format: {version}")
        print("Version must be in format: vX.XX (e.g., v0.01, v1.00, v2.15)")
        return False
    return True

def suggest_next_version(current_version):
    """Suggest the next version number"""
    if current_version == "v0.00":
        return "v0.01"
    
    # Extract major and minor parts
    match = re.match(r'^v(\d+)\.(\d{2})$', current_version)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2))
        
        if minor < 99:
            return f"v{major}.{minor + 1:02d}"
        else:
            return f"v{major + 1}.00"
    
    return "v0.01"

def create_and_push_tag(version, message=None):
    """Create and push a git tag"""
    if not message:
        message = f"Release {version}"
    
    print(f"🚀 Creating release tag: {version}")
    
    # Check if we have uncommitted changes
    status_result = run_command("git status --porcelain")
    if status_result.returncode == 0 and status_result.stdout.strip():
        print("⚠️  Warning: You have uncommitted changes!")
        print("Current git status:")
        print(status_result.stdout)
        
        response = input("Do you want to continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("❌ Aborted. Please commit or stash your changes first.")
            return False
    
    # Check if tag already exists
    tag_exists = run_command(f"git tag -l {version}")
    if tag_exists.returncode == 0 and tag_exists.stdout.strip():
        print(f"❌ Tag {version} already exists!")
        return False
    
    # Create the tag
    print(f"📝 Creating tag: {version}")
    tag_result = run_command(f'git tag -a {version} -m "{message}"')
    if tag_result.returncode != 0:
        print("❌ Failed to create tag")
        return False
    
    # Push the tag
    print(f"📤 Pushing tag: {version}")
    push_result = run_command(f"git push origin {version}")
    if push_result.returncode != 0:
        print("❌ Failed to push tag")
        print("You can manually push with: git push origin {version}")
        return False
    
    print(f"✅ Successfully created and pushed tag: {version}")
    print(f"🌐 GitHub Actions will now build and release version {version}")
    print(f"📋 Monitor progress at: https://github.com/YOUR_USERNAME/hvym_press/actions")
    
    return True

def main():
    """Main function"""
    print("🔧 HVYM Press Release Tag Creator")
    print("=" * 40)
    
    # Check if we're in a git repository
    if not Path(".git").exists():
        print("❌ Not in a git repository!")
        print("Please run this script from the root of your git repository.")
        sys.exit(1)
    
    # Check if we have a remote origin
    remote_result = run_command("git remote get-url origin")
    if remote_result.returncode != 0:
        print("❌ No remote origin found!")
        print("Please add a remote origin: git remote add origin <your-repo-url>")
        sys.exit(1)
    
    # Get current version
    current_version = get_current_version()
    print(f"📋 Current version: {current_version}")
    
    # Suggest next version
    suggested_version = suggest_next_version(current_version)
    print(f"💡 Suggested next version: {suggested_version}")
    
    # Get user input
    print("\nOptions:")
    print("1. Use suggested version")
    print("2. Enter custom version")
    print("3. Show current git status")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        version = suggested_version
        message = input(f"Enter release message for {version} (or press Enter for default): ").strip()
        if not message:
            message = f"Release {version}"
        
        if validate_version_format(version):
            create_and_push_tag(version, message)
        else:
            sys.exit(1)
            
    elif choice == "2":
        version = input("Enter version (format: vX.XX): ").strip()
        if validate_version_format(version):
            message = input(f"Enter release message for {version}: ").strip()
            if not message:
                message = f"Release {version}"
            
            create_and_push_tag(version, message)
        else:
            sys.exit(1)
            
    elif choice == "3":
        print("\n📊 Current git status:")
        status_result = run_command("git status")
        if status_result.returncode == 0:
            print(status_result.stdout)
        else:
            print("Failed to get git status")
            
    elif choice == "4":
        print("👋 Goodbye!")
        sys.exit(0)
        
    else:
        print("❌ Invalid choice!")
        sys.exit(1)

if __name__ == "__main__":
    main()
