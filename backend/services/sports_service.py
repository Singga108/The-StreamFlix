from typing import List
import asyncio
from datetime import datetime, timedelta
import random
from ..models import Sports

class SportsService:
    def __init__(self):
        # Mock sports data for now - can be replaced with real sports API later
        self.mock_sports_data = [
            {
                "title": "India vs Australia Live Cricket",
                "sport": "Cricket",
                "status": "Live",
                "teams": ["India", "Australia"],
                "venue": "Melbourne Cricket Ground",
                "start_time": datetime.now(),
                "image": "https://images.unsplash.com/photo-1512719994953-eabf50895df7?w=400&h=300&fit=crop",
                "description": "Live cricket match - Border-Gavaskar Trophy. Watch the thrilling encounter between India and Australia."
            },
            {
                "title": "Premier League Highlights: Man City vs Liverpool",
                "sport": "Football", 
                "status": "Highlights",
                "teams": ["Manchester City", "Liverpool"],
                "venue": "Etihad Stadium",
                "start_time": datetime.now() - timedelta(hours=2),
                "image": "https://images.unsplash.com/photo-1700319021396-95aec8e168ac?w=400&h=300&fit=crop",
                "description": "Best moments from Manchester City vs Liverpool - Premier League clash with goals and key highlights."
            },
            {
                "title": "NBA Finals: Lakers vs Celtics Game 7",
                "sport": "Basketball",
                "status": "Upcoming",
                "teams": ["Los Angeles Lakers", "Boston Celtics"],
                "venue": "Crypto.com Arena",
                "start_time": datetime.now() + timedelta(hours=8),
                "image": "https://images.unsplash.com/photo-1745163112810-ab65646732ba?w=400&h=300&fit=crop",
                "description": "The ultimate showdown in basketball's biggest stage. Don't miss this epic Game 7."
            },
            {
                "title": "Cricket World Cup Final",
                "sport": "Cricket",
                "status": "Upcoming",
                "teams": ["England", "New Zealand"],
                "venue": "Lords Cricket Ground",
                "start_time": datetime.now() + timedelta(days=2),
                "image": "https://images.unsplash.com/photo-1593341646782-e0b495cff86d?w=400&h=300&fit=crop",
                "description": "The biggest cricket match of the year. Don't miss the thrilling finale of the Cricket World Cup."
            },
            {
                "title": "Champions League Final Highlights",
                "sport": "Football",
                "status": "Highlights", 
                "teams": ["Real Madrid", "Barcelona"],
                "venue": "Santiago Bernabéu",
                "start_time": datetime.now() - timedelta(days=1),
                "image": "https://images.pexels.com/photos/33944536/pexels-photo-33944536.jpeg?auto=compress&cs=tinysrgb&w=400&h=300&fit=crop",
                "description": "El Clasico in the Champions League final - relive the best moments from this historic match."
            },
            {
                "title": "Tennis Wimbledon Live",
                "sport": "Tennis",
                "status": "Live",
                "teams": ["Novak Djokovic", "Carlos Alcaraz"],
                "venue": "All England Club",
                "start_time": datetime.now() - timedelta(minutes=30),
                "image": "https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=400&h=300&fit=crop",
                "description": "Live from Wimbledon - the epic final match between two tennis legends."
            }
        ]
    
    async def get_live_sports(self) -> List[Sports]:
        """Get live sports events"""
        live_events = []
        
        for event_data in self.mock_sports_data:
            if event_data["status"] == "Live":
                sports_event = Sports(
                    title=event_data["title"],
                    sport=event_data["sport"],
                    status=event_data["status"],
                    teams=event_data["teams"],
                    venue=event_data["venue"],
                    start_time=event_data["start_time"],
                    image=event_data["image"],
                    description=event_data["description"]
                )
                live_events.append(sports_event)
        
        return live_events
    
    async def get_highlights(self) -> List[Sports]:
        """Get sports highlights"""
        highlight_events = []
        
        for event_data in self.mock_sports_data:
            if event_data["status"] == "Highlights":
                sports_event = Sports(
                    title=event_data["title"],
                    sport=event_data["sport"],
                    status=event_data["status"],
                    teams=event_data["teams"],
                    venue=event_data["venue"],
                    start_time=event_data["start_time"],
                    image=event_data["image"],
                    description=event_data["description"]
                )
                highlight_events.append(sports_event)
        
        return highlight_events
    
    async def get_upcoming_events(self) -> List[Sports]:
        """Get upcoming sports events"""
        upcoming_events = []
        
        for event_data in self.mock_sports_data:
            if event_data["status"] == "Upcoming":
                sports_event = Sports(
                    title=event_data["title"],
                    sport=event_data["sport"],
                    status=event_data["status"],
                    teams=event_data["teams"],
                    venue=event_data["venue"],
                    start_time=event_data["start_time"],
                    image=event_data["image"],
                    description=event_data["description"]
                )
                upcoming_events.append(sports_event)
        
        return upcoming_events
    
    async def get_all_sports_content(self) -> List[Sports]:
        """Get all sports content (live + highlights + upcoming)"""
        all_events = []
        
        # Get all categories
        live_events = await self.get_live_sports()
        highlights = await self.get_highlights()
        upcoming = await self.get_upcoming_events()
        
        # Combine and shuffle for variety
        all_events.extend(live_events)
        all_events.extend(highlights)
        all_events.extend(upcoming)
        
        # Sort by status priority (Live first, then Upcoming, then Highlights)
        status_priority = {"Live": 1, "Upcoming": 2, "Highlights": 3}
        all_events.sort(key=lambda x: status_priority.get(x.status, 4))
        
        return all_events