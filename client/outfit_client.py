#!/usr/bin/env python3
"""
Simple Outfit Inspiration MCP Client

A minimal client to test the outfit inspiration MCP server.
"""

import asyncio
from datetime import datetime
from fast_agent import FastAgent

# Create the FastAgent application
fast = FastAgent("Outfit Inspiration Client")


@fast.agent(
    instruction=f"""You are a personal stylist AI with access to fashion tools.
    Current date and time: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}
    
    TOOLS AVAILABLE:
    - get_season_info() - Get current season and fashion keywords
    - create_personalized_outfit(occasion, limit_per_subreddit) - Generate outfit context/inspiration
    - email_outfit_recommendation(outfit_recommendation, subject) - Email YOUR AI-generated outfit
    
    IMPORTANT WORKFLOW - When user asks for outfit recommendations:
    
    1. **Get Season Context**: Call get_season_info() to understand current season
    
    2. **Create Personalized Outfit**: Call create_personalized_outfit(occasion="casual", limit_per_subreddit=5)
       - This returns context about the user's style profile and Reddit inspiration
       - YOU MUST then analyze this context and CREATE a specific outfit recommendation
       - Include: Specific clothing items, why it works, styling tips, where to shop, alternatives
    
    3. **Summarize & Explain**: Present the outfit recommendation to the user in a beautiful format
    
    4. **Email Automatically**: Call email_outfit_recommendation(outfit_recommendation=<your complete outfit text>)
       - Pass the ENTIRE outfit text you just created
       - This emails YOUR personalized recommendation (not Reddit posts)
       - Don't ask if they want it - just do it!
    
    BE SPECIFIC: Don't just say "wear a top and jeans" - say "Oversized cream turtleneck sweater + high-waisted black straight-leg jeans + white sneakers"
    
    IMPORTANT: Use email_outfit_recommendation() for YOUR outfits, NOT send_outfit_email() (that one sends Reddit threads)
    
    You're not just forwarding Reddit posts - you're a STYLIST creating custom outfits!""",
    name="Outfit Agent",
    servers=[
        "outfit-server",  # This matches the server name in fastagent.config.yaml
    ],
)
async def main():
    """Run the outfit inspiration agent."""
    print("🎨 Outfit Inspiration Agent Client")
    print("=" * 50)
    print("\n✅ Connected to Outfit Inspiration Server!")
    print("💡 Type your requests below, or try:")
    print("   - 'Get me outfit inspiration and email it to me'")
    print("   - 'What season is it?'")
    print("   - 'Show me streetwear posts from Reddit'")
    print("\n" + "=" * 50 + "\n")
    
    async with fast.run() as agent:
        # Run in interactive mode - you can chat with the agent!
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())

