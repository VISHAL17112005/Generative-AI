import requests
from get_links import get_links
import os
from datetime import datetime
from bs4 import BeautifulSoup
import re
from typing import List, Optional


def initialize_logs(topic):
    """Create a folder named as the topic with timestamp
    Returns the path of the created folder"""
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    topic_folder = os.path.join(logs_dir, f"{topic}_{timestamp}")
    os.makedirs(topic_folder, exist_ok=True)

    return topic_folder

def scrape_links(links: List[str], save_logs: bool = True, log_folder: Optional[str] = None) -> Optional[str]:
    """Scrape content from a list of links.
    Args:
        links (List[str]): List of URLs to scrape.
        save_logs (bool): Whether to save each page as a markdown file.
        log_folder (Optional[str]): Folder to save logs. If None, logs won't be saved.
    Returns:
    if save_logs is False, returns combined content as a string.
    if save_logs is True, returns None.
    """
    combined_content = ""


    # ✅ enumerate gives us both index and URL
    for i, link in enumerate(links, 1):
        try:
            response = requests.get(link, timeout=10)
            if response.status_code == 200:
                print(f"Successfully scraped {link}")

                soup = BeautifulSoup(response.content, "html.parser")

                # ----- Title -----
                title_tag = soup.find("title")
                title_text = title_tag.get_text(strip=True) if title_tag else f"Article_{i}"

                # Clean title for filename
                safe_title = re.sub(r"[^\w\s-]", "", title_text)
                safe_title = re.sub(r"\s+", "_", safe_title).strip("_")

                # ----- Content -----
                content_selectors = [
                    "article", "main", "content",
                    ".post-content", ".entry-content", ".article-content", "body"
                ]
                content_text = ""
                for selector in content_selectors:
                    content = soup.select_one(selector)
                    if content:
                        for script in content(["script", "style"]):
                            script.decompose()
                        content_text = content.get_text(separator="\n", strip=True)
                        break
                if not content_text:
                    content_text = soup.get_text(separator="\n", strip=True)

                # ----- Markdown -----
                markdown_content=f"# {title_text}\n\n"
                markdown_content += f"**Source**: {link}\n\n"
                markdown_content += f"**Scraped on**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                markdown_content += f"---\n\n"
                markdown_content += f"{content_text}"
                


                # Save to file if requested
                if save_logs and log_folder:
                    filename = f"{i:03d}_{safe_title}.md"
                    filepath = os.path.join(log_folder, filename)
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(markdown_content)
                    print(f"Saved → {filepath}")
                else:
                    combined_content += markdown_content + "\n\n---\n\n"
                    
        except Exception as e:
            print(f"failed to scrape {link}: {str(e)}")
    if save_logs and log_folder:
        print(f"All pages saved in folder: {log_folder}")
        return None
    else:
        return combined_content


