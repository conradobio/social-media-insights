import json
from typing import Optional
from urllib.parse import quote

from scrapfly import ScrapeConfig, ScrapflyClient, ScrapeApiResponse

def scrape_user(username: str, session: ScrapflyClient):
    """scrape user's data"""
    result = session.scrape(
        ScrapeConfig(
            url=f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
            headers={"x-ig-app-id": "936619743392459"},
            asp=True,
        )
    )
    # https://www.instagram.com/p/CqtCK6fODVK/
    data = json.loads(result.content)
    return data["data"]["user"]

def scrape_user_posts(user_id: str, session: ScrapflyClient, page_size=12, page_limit: Optional[int] = None):
    """scrape user's post data"""
    base_url = "https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables="
    variables = {
        "id": user_id,
        "first": page_size,
        "after": None,
    }
    page = 1
    while True:
        result = session.scrape(ScrapeConfig(base_url + quote(json.dumps(variables)), asp=True))
        posts = json.loads(result.content)["data"]["user"]["edge_owner_to_timeline_media"]
        for post in posts["edges"]:
            yield post["node"]
        page_info = posts["page_info"]
        if not page_info["has_next_page"]:
            break
        variables["after"] = page_info["end_cursor"]
        page += 1
        if page > page_limit:
            break

if __name__ == "__main__":
    with ScrapflyClient(key="scp-live-0947e6fe7b8f44ae9936652aa83638ca", max_concurrency=2) as session:
        #result_location = find_location_id("London, United Kingdom", session)
        #result_location_users = list(scrape_users_by_location(result_location, session, page_limit=3))
        #result_hashtag_users = list(scrape_hashtag("webscraping", session, page_limit=3))
        result_user = scrape_user("google", session)
        result_user_posts = list(scrape_user_posts(result_user["id"], session, page_limit=3))
        print("done")