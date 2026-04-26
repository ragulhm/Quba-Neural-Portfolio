import os
import requests
import json
import django
import sys
from datetime import datetime

# Setup Django environment
# Add the project root to sys.path so it can find the 'core' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings

def extract():
    username = 'ragulhm'
    token = getattr(settings, 'GITHUB_TOKEN', os.environ.get('GITHUB_TOKEN'))
    
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    # Use per_page=100 to get as many repos as possible in one call
    url = f'https://api.github.com/users/{username}/repos?per_page=100&sort=updated'
    
    print(f"Initializing Knowledge Matrix Extraction for user: {username}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repos = response.json()
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    knowledge_base = []
    print(f"Found {len(repos)} repositories. Filtering non-forks...")

    for repo in repos:
        # We only want Ragul's original creations, not forks
        if repo['fork']:
            continue
            
        print(f"Analyzing: {repo['name']}...")
        
        # Get detailed languages for a more accurate tech stack
        tech_stack = []
        try:
            lang_resp = requests.get(repo['languages_url'], headers=headers, timeout=5)
            if lang_resp.status_code == 200:
                tech_stack = list(lang_resp.json().keys())
        except:
            pass
            
        # Fallback to primary language if API fails
        if not tech_stack and repo['language']:
            tech_stack = [repo['language']]
            
        # Add topics
        if repo['topics']:
            tech_stack.extend(repo['topics'])
            
        # Deduplicate
        tech_stack = list(set(tech_stack))

        knowledge_base.append({
            "name": repo['name'],
            "description": repo['description'] or "A specialized software solution developed by Ragul.",
            "tech_stack": tech_stack,
            "category": "Innovative Development",
            "url": repo['html_url'],
            "impact": f"High-performance repository with {repo['stargazers_count']} stars and {repo['forks_count']} forks.",
            "stars": repo['stargazers_count'],
            "forks": repo['forks_count'],
            "last_updated": repo['updated_at']
        })

    # Save to the data directory
    output_path = os.path.join(settings.BASE_DIR, 'portfolio', 'data', 'github_knowledge.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(knowledge_base, f, indent=2)
        
    print(f"Success! Knowledge matrix updated with {len(knowledge_base)} repositories.")
    print(f"📍 Location: {output_path}")

if __name__ == "__main__":
    extract()
