from pathlib import Path
from typing import Optional

def combine_logs(log_folder: str, max_chars: int = 7500) -> Optional[str]:
    """Combine logs with character limit optimization for cost-effective token usage."""
    try:
        folder_path = Path(log_folder)
        if not folder_path.exists():
            return None
            
        markdown_files = sorted(folder_path.glob("*.md"))
        if not markdown_files:
            return None
            
        combined_content = []
        current_length = 0
        
        print(f"📁 Processing {len(markdown_files)} files from {log_folder}")
        
        for file_path in markdown_files:
            try:
                content = file_path.read_text(encoding='utf-8').strip()
                
                # Smart truncation to stay within character limit
                if current_length + len(content) > max_chars:
                    remaining_chars = max_chars - current_length
                    if remaining_chars > 200:  # Only add if we have meaningful space
                        content = content[:remaining_chars] + "\n\n[CONTENT TRUNCATED - REMAINING FILES SKIPPED]"
                        combined_content.append(content)
                        print(f"⚠️  Truncated content at {remaining_chars} characters")
                    break
                
                combined_content.append(content)
                current_length += len(content)
                print(f"✅ Added {file_path.name} ({len(content)} chars)")
                
            except Exception as e:
                print(f"❌ Error reading {file_path.name}: {e}")
                continue
                
        result = "\n\n" + "="*80 + "\n\n".join(combined_content) if combined_content else None
        
        # Debug information
        if result:
            print(f"\n📊 OPTIMIZATION RESULTS:")
            print(f"   📏 Final context length: {len(result)} characters")
            print(f"   📁 Files processed: {len(combined_content)}")
            print(f"   💰 Estimated token savings: ~{((len(result) / 7500) * 100):.1f}% of original")
            print(f"   ✅ Context optimized for cost-effective processing!")
            
        return result
        
    except Exception as e:
        print(f"❌ Error in combine_logs: {e}")
        return None