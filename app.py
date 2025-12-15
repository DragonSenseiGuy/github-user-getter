from flask import Flask, render_template, request, redirect, url_for
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_github_user(username):
    token = os.getenv('GITHUB_TOKEN')
    headers = {'Authorization': f'token {token}'} if token else {}

    # Try GraphQL first (needs token) to get actual pinned repos
    if token:
        query = """
        query($login: String!) {
          user(login: $login) {
            login
            name
            avatarUrl
            bio
            location
            websiteUrl
            twitterUsername
            followers {
              totalCount
            }
            following {
              totalCount
            }
            repositories {
              totalCount
            }
            pinnedItems(first: 6, types: REPOSITORY) {
              nodes {
                ... on Repository {
                  name
                  description
                  stargazerCount
                  primaryLanguage {
                    name
                  }
                  url
                }
              }
            }
          }
        }
        """
        response = requests.post(
            'https://api.github.com/graphql',
            json={'query': query, 'variables': {'login': username}},
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            if 'data' in data and data['data']['user']:
                user = data['data']['user']
                pinned_repos = []
                for node in user['pinnedItems']['nodes']:
                    if node:
                        pinned_repos.append({
                            "name": node['name'],
                            "description": node['description'] or "",
                            "language": node['primaryLanguage']['name'] if node['primaryLanguage'] else "N/A",
                            "stars": node['stargazerCount'],
                            "url": node['url']
                        })
                
                return {
                    "username": user['login'],
                    "name": user['name'],
                    "avatar_url": user['avatarUrl'],
                    "bio": user['bio'],
                    "public_repos": user['repositories']['totalCount'],
                    "followers": user['followers']['totalCount'],
                    "following": user['following']['totalCount'],
                    "location": user['location'],
                    "website": user['websiteUrl'],
                    "twitter_username": user['twitterUsername'],
                    "pinned_repos": pinned_repos
                }

    # Fallback to REST API (Simulate Pinned by getting top starred)
    user_url = f"https://api.github.com/users/{username}"
    user_response = requests.get(user_url, headers=headers)
    
    if user_response.status_code != 200:
        return None
    
    user_data = user_response.json()
    
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    repos_response = requests.get(repos_url, headers=headers)
    
    pinned_repos = []
    if repos_response.status_code == 200:
        repos = repos_response.json()
        sorted_repos = sorted(repos, key=lambda r: r['stargazers_count'], reverse=True)
        top_repos = sorted_repos[:4]
        
        for repo in top_repos:
            pinned_repos.append({
                "name": repo['name'],
                "description": repo['description'] or "",
                "language": repo['language'] or "N/A",
                "stars": repo['stargazers_count'],
                "url": repo['html_url']
            })

    return {
        "username": user_data.get('login'),
        "name": user_data.get('name'),
        "avatar_url": user_data.get('avatar_url'),
        "bio": user_data.get('bio'),
        "public_repos": user_data.get('public_repos'),
        "followers": user_data.get('followers'),
        "following": user_data.get('following'),
        "location": user_data.get('location'),
        "website": user_data.get('blog'),
        "twitter_username": user_data.get('twitter_username'),
        "pinned_repos": pinned_repos
    }

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            return redirect(url_for('user', username=username))
    elif request.method == 'GET': # This block is added back
        username = request.args.get('username')
        if username:
            return redirect(url_for('user', username=username))
    return render_template('index.html')

@app.route('/user/<username>')
def user(username):
    user_data = get_github_user(username)
    if not user_data:
        return f"User {username} not found", 404
    return render_template('user.html', user=user_data)

if __name__ == '__main__':
    app.run(debug=True)