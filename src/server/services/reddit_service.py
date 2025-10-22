"""
Reddit Service for Outfit Inspiration

Simple service to fetch outfit posts from Reddit fashion subreddits.
"""

import asyncio
from typing import Dict, List
import httpx
from datetime import datetime


class RedditService:
    """Service for fetching outfit inspiration from Reddit."""
    
    def __init__(self):
        self.base_url = "https://www.reddit.com"
        self.headers = {
            "User-Agent": "OutfitInspirationBot/1.0"
        }
    
    async def fetch_outfit_posts(
        self, 
        subreddit: str, 
        limit: int = 10,
        time_filter: str = "week"
    ) -> List[Dict]:
        """
        Fetch outfit posts from a subreddit.
        
        Args:
            subreddit: Subreddit name (e.g., 'malefashionadvice')
            limit: Number of posts to fetch (1-25)
            time_filter: Time filter (day, week, month, year, all)
            
        Returns:
            List of outfit posts with title, url, score, author
        """
        try:
            # Use Reddit's JSON API (no auth needed for public posts)
            url = f"{self.base_url}/r/{subreddit}/top.json"
            params = {
                "limit": min(limit, 25),
                "t": time_filter
            }
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    url, 
                    headers=self.headers,
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                
                posts = []
                for post in data.get("data", {}).get("children", []):
                    post_data = post.get("data", {})
                    
                    # Filter for posts with images or that look like outfit posts
                    title_lower = post_data.get("title", "").lower()
                    has_image = post_data.get("post_hint") == "image" or post_data.get("url", "").endswith(('.jpg', '.png', '.jpeg'))
                    
                    posts.append({
                        "title": post_data.get("title", ""),
                        "url": f"https://www.reddit.com{post_data.get('permalink', '')}",
                        "image_url": post_data.get("url", ""),
                        "score": post_data.get("score", 0),
                        "author": post_data.get("author", "unknown"),
                        "created_utc": post_data.get("created_utc", 0),
                        "has_image": has_image,
                        "subreddit": subreddit
                    })
                
                return posts
                
        except Exception as e:
            print(f"Error fetching from r/{subreddit}: {e}")
            return []
    
    async def fetch_multiple_subreddits(
        self,
        subreddits: List[str],
        limit_per_sub: int = 5
    ) -> Dict[str, List[Dict]]:
        """
        Fetch posts from multiple subreddits concurrently.
        
        Args:
            subreddits: List of subreddit names
            limit_per_sub: Number of posts per subreddit
            
        Returns:
            Dictionary mapping subreddit to list of posts
        """
        tasks = [
            self.fetch_outfit_posts(sub, limit_per_sub)
            for sub in subreddits
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            sub: posts if not isinstance(posts, Exception) else []
            for sub, posts in zip(subreddits, results)
        }