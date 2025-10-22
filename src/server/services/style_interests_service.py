"""
Style Interests File Service

Simple service to read user's style preferences from markdown file.
"""

from pathlib import Path
from typing import Dict, List
import re


class StyleInterestsService:
    """Service for managing user's style interests."""
    
    def __init__(self, interests_file: Path):
        """Initialize with path to interests file."""
        self.interests_file = interests_file
    
    def read_interests(self) -> Dict:
        """
        Read and parse the style interests markdown file.
        
        Returns:
            Dictionary with style preferences, colors, subreddits, etc.
        """
        if not self.interests_file.exists():
            return {
                "style_preferences": [],
                "favorite_colors": [],
                "subreddits": [],
                "occasions": [],
                "notes": []
            }
        
        content = self.interests_file.read_text(encoding="utf-8")
        
        # Parse sections
        interests = {
            "personal_info": self._extract_list_section(content, "Personal Info"),
            "style_preferences": self._extract_list_section(content, "Style Preferences"),
            "favorite_colors": self._extract_list_section(content, "Favorite Colors"),
            "subreddits": self._extract_list_section(content, "Favorite Subreddits"),
            "occasions": self._extract_list_section(content, "Occasion Types"),
            "body_preferences": self._extract_list_section(content, "Body Type & Fit Preferences"),
            "notes": self._extract_list_section(content, "Notes")
        }
        
        # Extract gender from personal info
        interests["gender"] = self._extract_gender(interests["personal_info"])
        
        return interests
    
    def _extract_gender(self, personal_info: List[str]) -> str:
        """Extract gender from personal info list."""
        for item in personal_info:
            if item.lower().startswith("gender:"):
                return item.split(":", 1)[1].strip()
        return "Not specified"
    
    def _extract_list_section(self, content: str, section_name: str) -> List[str]:
        """Extract list items from a markdown section."""
        # Find section header (using raw string for regex)
        pattern = rf"## {section_name}.*?(?=##|\Z)"
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            return []
        
        section_text = match.group(0)
        
        # Extract list items (lines starting with -)
        items = []
        for line in section_text.split('\n'):
            line = line.strip()
            if line.startswith('- ') and not line.startswith('<!--'):
                item = line[2:].strip()
                if item:
                    items.append(item)
        
        return items
    
    def get_subreddits(self) -> List[str]:
        """Get list of favorite subreddits (cleaned)."""
        interests = self.read_interests()
        subreddits = interests.get("subreddits", [])
        
        # Clean subreddit names (remove r/ prefix if present)
        cleaned = []
        for sub in subreddits:
            sub = sub.strip()
            if sub.startswith('r/'):
                sub = sub[2:]
            cleaned.append(sub)
        
        return cleaned

