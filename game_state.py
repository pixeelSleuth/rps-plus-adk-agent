from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class GameState:
    """
    Persistent state model for Rock-Paper-Scissors-Plus.
    Stores the absolute truth of the game, independent of the Agent's context.
    """
    round_count: int = 0
    max_rounds: int = 3
    user_score: int = 0
    bot_score: int = 0
    user_used_bomb: bool = False
    bot_used_bomb: bool = False
    game_over: bool = False
    # History tracks the details of every round for debugging/explanation
    history: List[Dict] = field(default_factory=list)

    def get_scores(self) -> Dict[str, int]:
        """Returns current score summary."""
        return {
            "user": self.user_score,
            "bot": self.bot_score
        }

    def get_final_winner(self) -> str:
        """Determines the final winner based on current scores."""
        if self.user_score > self.bot_score:
            return "User wins the game!"
        elif self.bot_score > self.user_score:
            return "Bot wins the game!"
        else:
            return "The game ends in a Draw!"