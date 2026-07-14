#!/usr/bin/env python3
"""
Extension validation script for M2.2
Validates extension structure and manifest configuration
"""

import json
import os
import re
import sys

def validate_manifest():
    """Validate manifest.json structure and references"""
    print("=" * 60)
    print("VALIDATING EXTENSION STRUCTURE")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    # Check manifest.json exists
    manifest_path = 'extension/manifest.json'
    if not os.path.exists(manifest_path):
        print("ERROR: manifest.json not found")
        return False
    
    # Parse manifest
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        print("[OK] manifest.json is valid JSON")
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in manifest.json: {e}")
        return False
    
    # Check manifest version
    if manifest.get('manifest_version') != 3:
        errors.append("Manifest version must be 3")
    else:
        print("[OK] Manifest version 3")
    
    # Check required fields
    required_fields = ['name', 'version', 'description']
    for field in required_fields:
        if field not in manifest:
            errors.append(f"Missing required field: {field}")
        else:
            print(f"[OK] {field}: {manifest[field]}")
    
    # Check permissions
    if 'permissions' in manifest:
        print(f"[OK] Permissions: {', '.join(manifest['permissions'])}")
    
    # Check action/popup
    if 'action' in manifest:
        if 'default_popup' in manifest['action']:
            popup_file = manifest['action']['default_popup']
            popup_path = f"extension/{popup_file}"
            if os.path.exists(popup_path):
                print(f"[OK] Popup file exists: {popup_file}")
                
                # Check popup HTML for CSS and JS references
                with open(popup_path, 'r') as f:
                    html_content = f.read()
                
                # Extract CSS (resolve relative to HTML file location)
                css_match = re.search(r'href=["\']([^"\']+\.css)["\']', html_content)
                if css_match:
                    css_file = css_match.group(1)
                    # Resolve relative path from HTML file directory
                    css_dir = os.path.dirname(popup_path)
                    css_path = os.path.join(css_dir, css_file)
                    if os.path.exists(css_path):
                        print(f"  [OK] CSS file exists: {css_file}")
                    else:
                        errors.append(f"CSS file missing: {css_file}")
                
                # Extract JS (resolve relative to HTML file location)
                js_match = re.search(r'src=["\']([^"\']+\.js)["\']', html_content)
                if js_match:
                    js_file = js_match.group(1)
                    # Resolve relative path from HTML file directory
                    js_dir = os.path.dirname(popup_path)
                    js_path = os.path.join(js_dir, js_file)
                    if os.path.exists(js_path):
                        print(f"  [OK] JS file exists: {js_file}")
                    else:
                        errors.append(f"JS file missing: {js_file}")
            else:
                errors.append(f"Popup file missing: {popup_file}")
    
    # Check background service worker
    if 'background' in manifest:
        if 'service_worker' in manifest['background']:
            sw_file = manifest['background']['service_worker']
            sw_path = f"extension/{sw_file}"
            if os.path.exists(sw_path):
                print(f"[OK] Service worker exists: {sw_file}")
            else:
                errors.append(f"Service worker missing: {sw_file}")
    
    # Check content scripts
    if 'content_scripts' in manifest:
        for idx, script_config in enumerate(manifest['content_scripts']):
            for js_file in script_config.get('js', []):
                js_path = f"extension/{js_file}"
                if os.path.exists(js_path):
                    print(f"[OK] Content script exists: {js_file}")
                else:
                    errors.append(f"Content script missing: {js_file}")
    
    # Check icons (optional but warn if missing)
    if 'icons' in manifest:
        for size, icon_file in manifest['icons'].items():
            icon_path = f"extension/{icon_file}"
            if os.path.exists(icon_path):
                print(f"[OK] Icon {size}x{size} exists: {icon_file}")
            else:
                warnings.append(f"Icon missing: {icon_file}")
    
    # Print summary
    print("\n" + "=" * 60)
    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"  [FAIL] {error}")
    
    if warnings:
        print("\nWARNINGS:")
        for warning in warnings:
            print(f"  [WARN] {warning}")
    
    if not errors and not warnings:
        print("[SUCCESS] ALL CHECKS PASSED - Extension is ready to load!")
    elif not errors:
        print("\n[SUCCESS] VALID - Extension can load (with warnings)")
    else:
        print("\n[FAILED] INVALID - Fix errors before loading")
    
    print("=" * 60)
    return len(errors) == 0

if __name__ == '__main__':
    success = validate_manifest()
    sys.exit(0 if success else 1)