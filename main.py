import sys
import os
from agent import GameRefereeAgent

def main():
    if not os.getenv("GOOGLE_API_KEY"):
        print("CRITICAL ERROR: GOOGLE_API_KEY not found.")
        print("Please create a .env file with GOOGLE_API_KEY=your_key_here")
        return

    print("Initializing Game Referee...")
    try:
       
        referee = GameRefereeAgent()
    except Exception as e:
        print(f"Error initializing agent: {e}")
        return

    
    print("\n--- NEW GAME ---")
    print(referee.explain_rules())
    print("----------------\n")

    
    while not referee.state.game_over:
        try:
            user_input = input("Your Move (rock/paper/scissors/bomb): ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit"]:
                print("Game aborted by user.")
                break

            print("\nReferee is thinking...")
            response = referee.handle_user_input(user_input)
            
            print(f"Referee: {response}\n")
            
        except KeyboardInterrupt:
            print("\nGame aborted.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    
    print("--- GAME ENDED ---")

if __name__ == "__main__":
    main()