import os
import requests
import pandas as pd

TOKEN = os.getenv("GITHUB_TOKEN", "")

def fetch_repos(page: int = 1):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": "language:python",
        "sort": "stars",
        "order": "desc",
        "per_page": 100,
        "page": page
    }
    headers = {}
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"

    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()

def main():
    repos = []
    for page in [1, 2]:
        data = fetch_repos(page)
        items = data.get("items", [])
        for r in items:
            repos.append({
                "name": r["full_name"],
                "html_url": r["html_url"],
                "stargazers_count": r["stargazers_count"],
                "created_at": r["created_at"],
                "description": r.get("description") or ""
            })

    df = pd.DataFrame(repos)
    df.to_excel("github_python_repos.xlsx", index=False)
    print(f"Saved {len(df)} repos to github_python_repos.xlsx")

if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
