import feedparser
import re
from bs4 import BeautifulSoup
from datetime import datetime

class MediumAPI:
    def __init__(self, username):
        # Medium RSS URL format
        self.rss_url = f'https://medium.com/feed/@{username}'

    def get_recent_articles(self, limit=3):
        """Fetch the most recent articles from Medium RSS feed."""
        try:
            feed = feedparser.parse(self.rss_url)
            
            if feed.bozo:
                print(f"Error parsing Medium feed for {self.rss_url}")
                return []
                
            entries = feed.entries[:limit]
            articles = []
            
            for entry in entries:
                # Extract image thumbnail using BeautifulSoup
                # Medium usually puts the first image inside the content:encoded tag
                thumbnail_url = None
                if hasattr(entry, 'content'):
                    html_content = entry.content[0].value
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    # Find all images but skip the 1x1 tracking pixels Medium injects
                    for img in soup.find_all('img'):
                        src = img.get('src', '')
                        if src and 'stat.medium.com' not in src:
                            thumbnail_url = src
                            break
                
                # Parse date
                # Medium format is usually like: 'Thu, 28 Dec 2023 15:43:08 GMT'
                try:
                    published_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
                except Exception:
                    published_date = None
                    
                articles.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published_date': published_date,
                    'thumbnail': thumbnail_url,
                    # We can add categories as well
                    'categories': getattr(entry, 'tags', [])
                })
                
            return articles
        except Exception as e:
            print(f"Medium API Exception: {e}")
            return []
