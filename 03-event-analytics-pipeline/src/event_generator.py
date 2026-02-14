"""
Generate synthetic mobile game event data.

Events include: sessions, level completions, purchases, ads, achievements
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
import uuid

import numpy as np
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)


class GameEventGenerator:
    """Generate realistic mobile game telemetry events."""
    
    EVENT_TYPES = [
        "session_start",
        "session_end",
        "level_start",
        "level_complete",
        "level_fail",
        "purchase",
        "ad_watched",
        "achievement_unlocked"
    ]
    
    DEVICE_TYPES = ["iOS", "Android"]
    COUNTRIES = ["US", "UK", "DE", "TR", "FR", "JP", "BR"]
    
    def __init__(self, num_players: int = 5000, num_days: int = 30):
        self.num_players = num_players
        self.num_days = num_days
        self.start_date = datetime.now() - timedelta(days=num_days)
        self.players = self._generate_players()
        
    def _generate_players(self) -> List[Dict]:
        """Generate player profiles."""
        players = []
        for _ in range(self.num_players):
            install_date = self.start_date + timedelta(
                days=random.randint(0, self.num_days - 7)
            )
            
            player = {
                "player_id": str(uuid.uuid4()),
                "install_date": install_date,
                "device_type": random.choice(self.DEVICE_TYPES),
                "country": random.choice(self.COUNTRIES),
                "is_payer": random.random() < 0.08,  # 8% paying users
                "engagement_level": random.choice(["low", "medium", "high"]),
                "current_level": 1
            }
            players.append(player)
        return players
    
    def _generate_session(self, player: Dict, day: datetime) -> List[Dict]:
        """Generate events for a single session."""
        events = []
        session_id = str(uuid.uuid4())
        
        # Session start
        session_start_time = day + timedelta(
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        events.append({
            "event_id": str(uuid.uuid4()),
            "player_id": player["player_id"],
            "session_id": session_id,
            "event_type": "session_start",
            "timestamp": session_start_time.isoformat(),
            "properties": {
                "device_type": player["device_type"],
                "country": player["country"]
            }
        })
        
        # Session duration based on engagement level
        if player["engagement_level"] == "low":
            session_duration = random.randint(60, 300)  # 1-5 min
            levels_played = random.randint(0, 2)
        elif player["engagement_level"] == "medium":
            session_duration = random.randint(300, 900)  # 5-15 min
            levels_played = random.randint(1, 5)
        else:  # high
            session_duration = random.randint(900, 3600)  # 15-60 min
            levels_played = random.randint(3, 10)
        
        current_time = session_start_time
        
        # Generate level events
        for _ in range(levels_played):
            level = player["current_level"]
            level_duration = random.randint(30, 180)
            
            # Level start
            events.append({
                "event_id": str(uuid.uuid4()),
                "player_id": player["player_id"],
                "session_id": session_id,
                "event_type": "level_start",
                "timestamp": current_time.isoformat(),
                "properties": {
                    "level": level
                }
            })
            
            current_time += timedelta(seconds=level_duration)
            
            # Level complete or fail
            success = random.random() > 0.2  # 80% success rate
            events.append({
                "event_id": str(uuid.uuid4()),
                "player_id": player["player_id"],
                "session_id": session_id,
                "event_type": "level_complete" if success else "level_fail",
                "timestamp": current_time.isoformat(),
                "properties": {
                    "level": level,
                    "success": success,
                    "duration": level_duration,
                    "score": random.randint(1000, 10000) if success else 0
                }
            })
            
            if success:
                player["current_level"] += 1
                
                # Achievement unlock chance
                if random.random() < 0.1:  # 10% chance
                    events.append({
                        "event_id": str(uuid.uuid4()),
                        "player_id": player["player_id"],
                        "session_id": session_id,
                        "event_type": "achievement_unlocked",
                        "timestamp": current_time.isoformat(),
                        "properties": {
                            "achievement_id": f"achievement_{random.randint(1, 20)}",
                            "achievement_name": fake.catch_phrase()
                        }
                    })
        
        # Ad watched (non-payers more likely)
        ad_probability = 0.3 if not player["is_payer"] else 0.1
        if random.random() < ad_probability:
            events.append({
                "event_id": str(uuid.uuid4()),
                "player_id": player["player_id"],
                "session_id": session_id,
                "event_type": "ad_watched",
                "timestamp": current_time.isoformat(),
                "properties": {
                    "ad_type": random.choice(["rewarded", "interstitial", "banner"]),
                    "reward": random.choice([None, "coins", "lives"])
                }
            })
            current_time += timedelta(seconds=30)
        
        # Purchase (payers only)
        if player["is_payer"] and random.random() < 0.25:  # 25% chance per session
            events.append({
                "event_id": str(uuid.uuid4()),
                "player_id": player["player_id"],
                "session_id": session_id,
                "event_type": "purchase",
                "timestamp": current_time.isoformat(),
                "properties": {
                    "product_id": random.choice(["coins_100", "coins_500", "coins_1000", "remove_ads"]),
                    "price_usd": random.choice([0.99, 2.99, 4.99, 9.99]),
                    "currency": "USD"
                }
            })
        
        # Session end
        session_end_time = session_start_time + timedelta(seconds=session_duration)
        events.append({
            "event_id": str(uuid.uuid4()),
            "player_id": player["player_id"],
            "session_id": session_id,
            "event_type": "session_end",
            "timestamp": session_end_time.isoformat(),
            "properties": {
                "session_duration": session_duration,
                "levels_played": levels_played
            }
        })
        
        return events
    
    def generate_events(self) -> List[Dict]:
        """Generate all events for all players."""
        all_events = []
        
        for day_offset in range(self.num_days):
            current_day = self.start_date + timedelta(days=day_offset)
            
            for player in self.players:
                # Skip if player hasn't installed yet
                if current_day < player["install_date"]:
                    continue
                
                # Determine if player plays today based on engagement and days since install
                days_since_install = (current_day - player["install_date"]).days
                
                # Churn model: retention decreases over time
                if player["engagement_level"] == "low":
                    play_probability = max(0.1, 0.8 - days_since_install * 0.05)
                elif player["engagement_level"] == "medium":
                    play_probability = max(0.3, 0.9 - days_since_install * 0.03)
                else:  # high
                    play_probability = max(0.5, 0.95 - days_since_install * 0.01)
                
                if random.random() > play_probability:
                    continue  # Player doesn't play today
                
                # Generate 1-3 sessions per day for active players
                num_sessions = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
                
                for _ in range(num_sessions):
                    session_events = self._generate_session(player, current_day)
                    all_events.extend(session_events)
        
        # Sort events by timestamp
        all_events.sort(key=lambda x: x["timestamp"])
        
        return all_events
    
    def save_events(self, output_dir: str = "data/raw_events"):
        """Generate and save events to JSON lines file."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"Generating events for {self.num_players} players over {self.num_days} days...")
        events = self.generate_events()
        
        output_file = output_path / f"events_{self.start_date.strftime('%Y%m%d')}.jsonl"
        
        with open(output_file, 'w') as f:
            for event in events:
                f.write(json.dumps(event) + '\n')
        
        print(f"Generated {len(events):,} events")
        print(f"Saved to: {output_file}")
        
        # Print summary statistics
        event_type_counts = {}
        for event in events:
            event_type = event["event_type"]
            event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1
        
        print("\nEvent breakdown:")
        for event_type, count in sorted(event_type_counts.items()):
            print(f"  {event_type}: {count:,}")
        
        return output_file


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate synthetic game events")
    parser.add_argument("--players", type=int, default=5000, help="Number of players")
    parser.add_argument("--days", type=int, default=30, help="Number of days")
    parser.add_argument("--output", type=str, default="data/raw_events", help="Output directory")
    
    args = parser.parse_args()
    
    generator = GameEventGenerator(num_players=args.players, num_days=args.days)
    generator.save_events(output_dir=args.output)
