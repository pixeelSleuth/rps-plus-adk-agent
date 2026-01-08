import os
from dotenv import load_dotenv
from google import genai
from google.genai import types  
from tools import GameRefTools
from game_state import GameState

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

class GameRefereeAgent:
    def __init__(self):
        self.state = GameState()
        self.tools = GameRefTools(self.state)
        
       
        self.client = genai.Client(api_key=API_KEY)

        sys_instruction = (
            "You are the Referee for a Rock-Paper-Scissors-Plus game. "
            "You must use the `submit_player_move` tool to process every move. "
            "Do not track scores yourself; trust the tool output. "
            "If the tool returns 'game_over': True, declare the final winner explicitly. "
            "Keep responses concise and round-by-round."
        )

      
        self.chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction,
                tools=[self.tools.submit_player_move], # Pass function directly
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=False
                )
            )
        )

    def explain_rules(self) -> str:
      
        return (
            "Welcome to Rock–Paper–Scissors–Plus!\n"
            "• Best of 3 rounds. Moves: rock, paper, scissors, bomb.\n"
            "• Bomb beats all (usable once per player).\n"
            "• Invalid input wastes the round.\n"
            "• Game ends automatically after 3 rounds."
        )

    def handle_user_input(self, user_input: str) -> str:
        try:
           
            response = self.chat.send_message(user_input)
            return response.text
        except Exception as e:
            return f"System Error: {str(e)}"