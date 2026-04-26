import requests
from django.conf import settings
from datetime import datetime

class GitHubAPI:
    def __init__(self):
        self.username = 'ragulhm'
        self.base_url = 'https://api.github.com'
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        
        # Add GitHub token from settings for higher rate limits
        if hasattr(settings, 'GITHUB_TOKEN') and settings.GITHUB_TOKEN:
            self.headers['Authorization'] = f'token {settings.GITHUB_TOKEN}'

    def get_recent_activity(self):
        """Fetch the most recent public events for the user."""
        try:
            response = requests.get(
                f'{self.base_url}/users/{self.username}/events/public',
                headers=self.headers,
                timeout=5
            )
            response.raise_for_status()
            events = response.json()
            
            # Filter for meaningful commits/pushes
            push_events = [e for e in events if e['type'] == 'PushEvent'][:3] # Get top 3
            
            activities = []
            for event in push_events:
                repo_name = event['repo']['name']
                # Try to get the latest commit message
                commits = event['payload'].get('commits', [])
                message = commits[0]['message'] if commits else "Made changes"
                
                # Format date nicely
                created_at = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                
                activities.append({
                    'repo': repo_name.split('/')[-1] if '/' in repo_name else repo_name,
                    'message': message.split('\n')[0], # Just the first line of commit message
                    'date': created_at,
                    'url': f"https://github.com/{repo_name}"
                })
                
            return activities
        except Exception as e:
            # Silently fail for frontend so portfolio doesn't break if GitHub is down
            print(f"GitHub API Error: {e}")
            return []

    def get_repo_stats(self):
        """Fetch general repository statistics."""
        try:
            response = requests.get(
                f'{self.base_url}/users/{self.username}/repos?sort=updated',
                headers=self.headers,
                timeout=5
            )
            response.raise_for_status()
            repos = response.json()
            
            total_stars = sum(repo['stargazers_count'] for repo in repos)
            total_forks = sum(repo['forks_count'] for repo in repos)
            
            return {
                'total_public_repos': len(repos),
                'total_stars': total_stars,
                'total_forks': total_forks
            }
        except Exception as e:
            return {'total_public_repos': 0, 'total_stars': 0, 'total_forks': 0}
