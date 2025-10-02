#!/usr/bin/env python3
"""
Test script to demonstrate context optimization
Run this to see the before/after comparison
"""

from cleaning import combine_logs
import os
from pathlib import Path

def test_optimization():
    """Test the context optimization with different character limits."""
    
    print("🧪 TESTING CONTEXT OPTIMIZATION")
    print("=" * 50)
    
    # Find the most recent log folder
    logs_dir = Path('logs')
    if not logs_dir.exists():
        print("❌ No logs directory found. Run main.py first to create some logs.")
        return
    
    # Get the most recent folder
    folders = [f for f in logs_dir.iterdir() if f.is_dir()]
    if not folders:
        print("❌ No log folders found. Run main.py first to create some logs.")
        return
    
    latest_folder = max(folders, key=lambda x: x.stat().st_mtime)
    print(f"📁 Testing with folder: {latest_folder}")
    
    # Test different character limits
    limits = [5000, 7500, 10000, 15000]
    
    for limit in limits:
        print(f"\n🔬 Testing with {limit} character limit:")
        print("-" * 30)
        
        result = combine_logs(str(latest_folder), max_chars=limit)
        
        if result:
            print(f"✅ Success! Final length: {len(result)} characters")
            print(f"📊 Files processed: {result.count('='*80) + 1}")
        else:
            print("❌ No content found")
    
    print(f"\n🎯 RECOMMENDATION:")
    print(f"   Use 7500 characters for optimal cost/quality balance")
    print(f"   This matches GPT's efficient context size!")

if __name__ == "__main__":
    test_optimization()
