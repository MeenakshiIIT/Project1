import requests
from requests.auth import HTTPBasicAuth
import csv
import time

# Replace with your GitHub token and username for authenticated requests
GITHUB_TOKEN = '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'
AUTH = HTTPBasicAuth('MeenakshiIIT', GITHUB_TOKEN)

# URLs for the GitHub API
USER_SEARCH_URL = "https://api.github.com/search/users"
USER_DATA_URL = "https://api.github.com/users/"
REPO_DATA_URL = "https://api.github.com/users/{username}/repos"

# CSV filenames
USERS_CSV = 'users.csv'
REPOS_CSV = 'repositories.csv'

def fetch_users_in_city(city="Bangalore", min_followers=100):
    users = []
    page = 1
    params = {"q": f"location:{city} followers:>{min_followers}", "per_page": 30}

    while True:
        params["page"] = page
        response = requests.get(USER_SEARCH_URL, params=params, auth=AUTH)
        if response.status_code != 200:
            print(f"Error fetching users: {response.json().get('message')}")
            break
        data = response.json()
        if "items" not in data or len(data["items"]) == 0:
            break
        users.extend(data["items"])
        print(f"Fetched {len(data['items'])} users from page {page}")
        page += 1
        time.sleep(1)  # Avoid rate limits
    return users

def clean_company_name(company):
    if company:
        company = company.strip().lstrip('@').upper()
    return company or ""

def fetch_user_details(username):
    response = requests.get(USER_DATA_URL + username, auth=AUTH)
    if response.status_code != 200:
        print(f"Error fetching user {username}: {response.json().get('message')}")
        return None
    data = response.json()
    return {
        "login": data.get("login"),
        "name": data.get("name") or "",
        "company": clean_company_name(data.get("company")),
        "location": data.get("location") or "",
        "email": data.get("email") or "",
        "hireable": data.get("hireable") or False,
        "bio": data.get("bio") or "",
        "public_repos": data.get("public_repos") or 0,
        "followers": data.get("followers") or 0,
        "following": data.get("following") or 0,
        "created_at": data.get("created_at") or ""
    }

def fetch_user_repositories(username):
    repos = []
    page = 1
    while True:
        response = requests.get(REPO_DATA_URL.format(username=username), params={"page": page, "per_page": 100}, auth=AUTH)
        if response.status_code != 200:
            print(f"Error fetching repos for {username}: {response.json().get('message')}")
            break
        data = response.json()
        if len(data) == 0:
            break
        for repo in data:
            repos.append({
                "login": username,
                "full_name": repo.get("full_name") or "",
                "created_at": repo.get("created_at") or "",
                "stargazers_count": repo.get("stargazers_count") or 0,
                "watchers_count": repo.get("watchers_count") or 0,
                "language": repo.get("language") or "",
                "has_projects": repo.get("has_projects") or False,
                "has_wiki": repo.get("has_wiki") or False,
                "license_name": repo.get("license", {}).get("key", "")
            })
        page += 1
        if len(repos) >= 500:  # Limit to 500 repositories
            break
        time.sleep(1)  # Avoid rate limits
    return repos[:500]
def fetch_user_repositories(username):
    repos = []
    page = 1
    while True:
        response = requests.get(REPO_DATA_URL.format(username=username), params={"page": page, "per_page": 100}, auth=AUTH)
        if response.status_code != 200:
            print(f"Error fetching repos for {username}: {response.json().get('message')}")
            break
        data = response.json()
        if len(data) == 0:
            break
        for repo in data:
            license_name = repo["license"]["key"] if repo.get("license") else ""
            repos.append({
                "login": username,
                "full_name": repo.get("full_name") or "",
                "created_at": repo.get("created_at") or "",
                "stargazers_count": repo.get("stargazers_count") or 0,
                "watchers_count": repo.get("watchers_count") or 0,
                "language": repo.get("language") or "",
                "has_projects": repo.get("has_projects") or False,
                "has_wiki": repo.get("has_wiki") or False,
                "license_name": license_name
            })
        page += 1
        if len(repos) >= 500:  # Limit to 500 repositories
            break
        time.sleep(1)  # Avoid rate limits
    return repos[:500]

def save_users_to_csv(users):
    with open(USERS_CSV, mode='w', newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["login", "name", "company", "location", "email", "hireable", "bio", "public_repos", "followers", "following", "created_at"])
        writer.writeheader()
        writer.writerows(users)
    print(f"Saved user data to {USERS_CSV}")

def save_repos_to_csv(repos):
    with open(REPOS_CSV, mode='w', newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["login", "full_name", "created_at", "stargazers_count", "watchers_count", "language", "has_projects", "has_wiki", "license_name"])
        writer.writeheader()
        writer.writerows(repos)
    print(f"Saved repository data to {REPOS_CSV}")

def main():
    users_data = fetch_users_in_city()
    user_details = []
    all_repos = []

    for user in users_data:
        details = fetch_user_details(user['login'])
        if details:
            user_details.append(details)
            repos = fetch_user_repositories(user['login'])
            all_repos.extend(repos)
            print(f"Fetched {len(repos)} repositories for user {user['login']}")
        time.sleep(1)  # Avoid rate limits

    save_users_to_csv(user_details)
    save_repos_to_csv(all_repos)

if __name__ == "__main__":
    main()

