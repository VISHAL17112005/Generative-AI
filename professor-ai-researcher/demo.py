#!/usr/bin/env python3
"""
Professor AI Research Assistant - Demo Script
Demonstrates the research capabilities without the web interface
"""

import os
import sys
import time
from datetime import datetime

# Import your existing modules
try:
    from get_links import get_links
    from scrape import scrape_links, initialize_logs
    from cleaning import combine_logs
    from llm import call_gemini, context_combine_prompt
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("💡 Make sure all required files are in the current directory")
    sys.exit(1)

def print_header():
    """Print the demo header"""
    print("🧠 Professor AI Research Assistant - Demo")
    print("=" * 50)
    print("This demo shows how the research process works")
    print("without the web interface.")
    print()

def print_step(step_num, title, description=""):
    """Print a processing step"""
    print(f"📍 Step {step_num}: {title}")
    if description:
        print(f"   {description}")
    print()

def demo_research(topic="Artificial Intelligence"):
    """Demonstrate the research process"""
    print_header()
    
    print(f"🔍 Research Topic: {topic}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    start_time = time.time()
    
    try:
        # Step 1: Get links
        print_step(1, "Searching Web Sources", "Finding relevant information across the internet")
        links = get_links(topic)
        print(f"✅ Found {len(links)} sources")
        for i, link in enumerate(links[:5], 1):  # Show first 5 links
            print(f"   {i}. {link}")
        if len(links) > 5:
            print(f"   ... and {len(links) - 5} more")
        print()
        
        # Step 2: Scrape content
        print_step(2, "Scraping Content", "Extracting valuable data from discovered sources")
        log_folder = initialize_logs(topic)
        scrape_links(links, save_logs=True, log_folder=log_folder)
        print(f"✅ Content saved to: {log_folder}")
        print()
        
        # Step 3: Process data
        print_step(3, "Processing Data", "Cleaning and organizing the collected information")
        context_from_logs = combine_logs(log_folder)
        
        if context_from_logs:
            context_length = len(context_from_logs)
            print(f"✅ Processed {context_length} characters of content")
            print(f"📊 Estimated tokens: ~{context_length // 4}")
        else:
            print("❌ No content could be processed")
            return
        print()
        
        # Step 4: Generate insights
        print_step(4, "Generating Insights", "Creating comprehensive research using AI")
        final_prompt = context_combine_prompt(context_from_logs, topic, "Comprehensive", True)
        
        print("🤖 Calling AI model...")
        answer = call_gemini(final_prompt)
        
        processing_time = time.time() - start_time
        
        # Display results
        print("=" * 50)
        print("🎉 RESEARCH COMPLETE!")
        print("=" * 50)
        print(f"⏱️  Processing time: {processing_time:.1f} seconds")
        print(f"📄 Sources processed: {len(links)}")
        print(f"📝 Content length: {len(context_from_logs)} characters")
        print()
        print("📋 RESEARCH RESULTS:")
        print("-" * 30)
        print(answer)
        print()
        print("=" * 50)
        
        # Ask if user wants to save results
        try:
            save_results = input("💾 Save results to file? (y/n): ").lower().strip()
            if save_results in ['y', 'yes']:
                filename = f"research_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"Research Topic: {topic}\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Processing Time: {processing_time:.1f} seconds\n")
                    f.write(f"Sources: {len(links)}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(answer)
                print(f"✅ Results saved to: {filename}")
        except KeyboardInterrupt:
            print("\n👋 Demo completed")
        
    except Exception as e:
        print(f"❌ Error during research: {e}")
        print("💡 Check your API keys and internet connection")

def interactive_demo():
    """Run an interactive demo"""
    print_header()
    
    try:
        # Get topic from user
        topic = input("🔍 Enter research topic (or press Enter for 'Artificial Intelligence'): ").strip()
        if not topic:
            topic = "Artificial Intelligence"
        
        print()
        confirm = input(f"🚀 Start research on '{topic}'? (y/n): ").lower().strip()
        if confirm not in ['y', 'yes', '']:
            print("👋 Demo cancelled")
            return
        
        print()
        demo_research(topic)
        
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main demo function"""
    if len(sys.argv) > 1:
        # Use command line argument as topic
        topic = " ".join(sys.argv[1:])
        demo_research(topic)
    else:
        # Interactive mode
        interactive_demo()

if __name__ == "__main__":
    main()
