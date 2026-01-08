import random
from typing import Dict, Any
from game_state import GameState


VALID_MOVES = {"rock", "paper", "scissors", "bomb"}

class GameRefTools:
    def __init__(self, state: GameState):
        self.state = state

    def submit_player_move(self, move: str) -> Dict[str, Any]:
        """
        Process a single player move and update game state.
        """
        
        move = move.lower().strip()

        # Reject moves after game ends
        if self.state.game_over:
            return {
                "error": "Game is already over.",
                "game_over": True,
                "final_result": self.state.get_final_winner()
            }

        # Invalid input = wastes 
        if move not in VALID_MOVES:
            return self._waste_round(f"Invalid move '{move}'.")

        # single bomb usage
        if move == "bomb":
            if self.state.user_used_bomb:
                 return self._waste_round("Bomb already used.")
            # Mark bomb as used for future checks
            self.state.user_used_bomb = True

        
        bot_move = self._generate_bot_move()

       
        round_winner = self._determine_winner(move, bot_move)

       
        self.state.round_count += 1
        
        if round_winner == "user":
            self.state.user_score += 1
        elif round_winner == "bot":
            self.state.bot_score += 1
        
        self.state.history.append({
            "round": self.state.round_count,
            "user": move,
            "bot": bot_move,
            "winner": round_winner
        })

        
        self._check_game_end()

        return {
            "status": "success",
            "round": self.state.round_count,
            "user_move": move,
            "bot_move": bot_move,
            "round_winner": round_winner,
            "scores": self.state.get_scores(),
            "game_over": self.state.game_over,
            "final_result": self.state.get_final_winner() if self.state.game_over else None
        }

    def _waste_round(self, reason: str) -> Dict[str, Any]:
        """Helper to handle wasted rounds due to invalid input/rules."""
        self.state.round_count += 1
        self._check_game_end()
        return {
            "status": "round_wasted",
            "round": self.state.round_count,
            "message": f"{reason} Round wasted.",
            "game_over": self.state.game_over,
            "scores": self.state.get_scores(),
            "final_result": self.state.get_final_winner() if self.state.game_over else None
        }

    def _generate_bot_move(self) -> str:
        """Generates a valid bot move, respecting the bot's own bomb limit."""
        options = ["rock", "paper", "scissors"]
        # Bot can use bomb if it hasn't used it yet
        if not self.state.bot_used_bomb:
            options.append("bomb")
        
        choice = random.choice(options)
        
        if choice == "bomb":
            self.state.bot_used_bomb = True
        return choice

    def _determine_winner(self, u: str, b: str) -> str:
        """Core Game Logic: Rock-Paper-Scissors-Plus rules."""
        if u == b:
            return "draw"  
        
       
        if u == "bomb": return "user"
        if b == "bomb": return "bot"
        
       
        wins = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
        if wins.get(u) == b:
            return "user"
        return "bot"

    def _check_game_end(self):
        """Enforces the 3-round limit automatically."""
        if self.state.round_count >= self.state.max_rounds:
            self.state.game_over = True