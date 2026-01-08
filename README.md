# Rock-Paper-Scissors-Plus (AI Referee)

A minimal AI referee for **Rock–Paper–Scissors–Plus**, focused on clean architecture, correct rule enforcement, and explicit state management.

---

## Overview

This project implements a conversational agent that runs a best-of-3 Rock–Paper–Scissors–Plus game between a user and a bot in a CLI environment.

The goal is to demonstrate:
- Clear separation between agent reasoning and game logic.
- Safe, persistent state handling (not relying on LLM context).
- Correct use of Google ADK-style agent and tool primitives.


The agent interprets user intent and narrates outcomes, while deterministic tools handle validation, rule enforcement, and state updates.

---

## Game Rules (Brief)

- **Best of 3 rounds**
- Valid moves: `rock`, `paper`, `scissors`, `bomb`
- `bomb` beats all other moves
- `bomb` vs `bomb` results in a draw
- Each player may use `bomb` only once per game
- Invalid input wastes the round (no points awarded)
- Game ends automatically after 3 rounds

---

## Architecture

The solution is separated into three distinct components:

### 1. State Model (`game_state.py`)
- Acts as the **single source of truth**.
- Tracks scores, round count, bomb usage, and game-over status in a persistent Python object.
- **Why:** Ensures game state is deterministic and strictly enforces limits (like max rounds) regardless of the conversation history.

### 2. Game Logic & Tools (`tools.py`)
- Implements the **Atomic Tool Pattern**.
- A single explicit tool, `submit_player_move`, handles the entire turn lifecycle:
  1. Validates input.
  2. Enforces constraints (e.g., bomb usage).
  3. Generates the bot's move.
  4. Updates the state and determines the winner.
- **Why:** This prevents "partial updates" (e.g., the agent moving the bot but forgetting to check if the user's move was valid).

### 3. Agent Layer (`agent.py`)
- Uses the **Google GenAI Client** to handle:
  - Intent understanding (translating natural language to tool calls).
  - Tool invocation.
  - Response narration.
- The agent trusts the tool's output implicitly and does not manage scores itself.


---

## Design Decisions & Tradeoffs

- **Single Atomic Tool:**
  I chose a single `submit_player_move` tool rather than separate `validate` and `update` tools. This guarantees that invalid inputs (like reusing a bomb) always result in a Wasted Round instantly, preventing the LLM from bypassing penalties.

- **ADK Implementation Choice:**
  I implemented the agent using Google’s current GenAI client to explicitly configure agents, tools, and automatic tool calling. This provides clear control over agent behavior while keeping state mutation fully within tools.

- **Bot Strategy:**
  The bot plays randomly (respecting its own bomb usage limit). I prioritized fairness and strict rule compliance over strategic complexity for this iteration.

---

## Sample Output

```text
Referee: Round 1: You both chose bomb. It's a draw.

Referee: Round 2: You tried to use bomb again, but it's already been used. Round wasted.

Referee: Round 3: You played paper, and the bot played rock. You win the round!
The game is over, and you are the final winner!

## 🚀 How to Run

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure API Key:**
    Create a `.env` file in the root directory:
    ```text
    GOOGLE_API_KEY=your_actual_key_here
    ```

3.  **Start the Game:**
    ```bash
    python main.py
    ```

## 🔮 Future Improvements

If I had more time, I would focus on:
* **Smarter Bot Strategy:** Currently, the bot plays randomly (while respecting its bomb limit). A smarter version could analyze the user's history to predict moves.
* **Persistent Storage:** Replacing the in-memory `GameState` with SQLite to allow pausing and resuming games later.