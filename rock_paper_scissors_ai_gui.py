import tkinter as tk
from tkinter import ttk, scrolledtext
import random
from collections import defaultdict, deque

class RPSLearningAI:
    """
    Rock-Paper-Scissors AI that learns player patterns over time.
    Uses pattern recognition to predict next move based on history.
    """
    
    def __init__(self, pattern_length=3):
        self.pattern_length = pattern_length
        self.player_history = deque(maxlen=100)
        self.pattern_dict = defaultdict(lambda: {'R': 0, 'P': 0, 'S': 0})
        self.moves = ['R', 'P', 'S']
        self.counter_move = {'R': 'P', 'P': 'S', 'S': 'R'}
        self.wins = 0
        self.losses = 0
        self.ties = 0
        
    def get_ai_move(self):
        """Generate AI move based on learned patterns or random if insufficient data."""
        if len(self.player_history) < self.pattern_length:
            return random.choice(self.moves)
        
        recent_pattern = ''.join(list(self.player_history)[-self.pattern_length:])
        
        if recent_pattern in self.pattern_dict:
            pattern_data = self.pattern_dict[recent_pattern]
            
            if sum(pattern_data.values()) >= 2:
                predicted_player_move = max(pattern_data, key=pattern_data.get)
                return self.counter_move[predicted_player_move]
        
        return random.choice(self.moves)
    
    def learn_pattern(self, player_move):
        """Update pattern dictionary with the player's move."""
        if len(self.player_history) >= self.pattern_length:
            pattern = ''.join(list(self.player_history)[-self.pattern_length:])
            self.pattern_dict[pattern][player_move] += 1
        
        self.player_history.append(player_move)
    
    def determine_winner(self, player_move, ai_move):
        """Determine the winner of the round."""
        if player_move == ai_move:
            self.ties += 1
            return 'tie'
        elif (player_move == 'R' and ai_move == 'S') or \
             (player_move == 'P' and ai_move == 'R') or \
             (player_move == 'S' and ai_move == 'P'):
            self.losses += 1
            return 'player'
        else:
            self.wins += 1
            return 'ai'
    
    def reset_stats(self):
        """Reset game statistics but keep learned patterns."""
        self.wins = 0
        self.losses = 0
        self.ties = 0


class RPSGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock-Paper-Scissors AI")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        self.ai = RPSLearningAI(pattern_length=3)
        self.round_number = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the GUI interface."""
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🎮 Rock-Paper-Scissors AI 🤖",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#ecf0f1")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Info label
        info_label = tk.Label(
            content_frame,
            text="The AI learns your patterns over time. Try to beat it!",
            font=("Arial", 11),
            bg="#ecf0f1",
            fg="#34495e"
        )
        info_label.pack(pady=10)
        
        # Round counter
        self.round_label = tk.Label(
            content_frame,
            text="Round: 0",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        self.round_label.pack(pady=5)
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg="#ecf0f1")
        button_frame.pack(pady=20)
        
        # Rock button
        self.rock_btn = tk.Button(
            button_frame,
            text="✊\nROCK",
            font=("Arial", 14, "bold"),
            width=10,
            height=4,
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            command=lambda: self.play_round('R')
        )
        self.rock_btn.grid(row=0, column=0, padx=10)
        
        # Paper button
        self.paper_btn = tk.Button(
            button_frame,
            text="✋\nPAPER",
            font=("Arial", 14, "bold"),
            width=10,
            height=4,
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            command=lambda: self.play_round('P')
        )
        self.paper_btn.grid(row=0, column=1, padx=10)
        
        # Scissors button
        self.scissors_btn = tk.Button(
            button_frame,
            text="✌\nSCISSORS",
            font=("Arial", 14, "bold"),
            width=10,
            height=4,
            bg="#2ecc71",
            fg="white",
            activebackground="#27ae60",
            command=lambda: self.play_round('S')
        )
        self.scissors_btn.grid(row=0, column=2, padx=10)
        
        # Result display
        self.result_text = scrolledtext.ScrolledText(
            content_frame,
            height=10,
            width=70,
            font=("Courier", 10),
            bg="#34495e",
            fg="#ecf0f1",
            state=tk.DISABLED
        )
        self.result_text.pack(pady=10)
        
        # Stats frame
        stats_frame = tk.Frame(content_frame, bg="#ecf0f1")
        stats_frame.pack(pady=10)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="AI: 0 | Player: 0 | Ties: 0 | Win Rate: 0.0%",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        self.stats_label.pack()
        
        # Control buttons
        control_frame = tk.Frame(content_frame, bg="#ecf0f1")
        control_frame.pack(pady=10)
        
        reset_btn = tk.Button(
            control_frame,
            text="Reset Stats",
            font=("Arial", 10),
            bg="#95a5a6",
            fg="white",
            command=self.reset_game
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        self.pattern_label = tk.Label(
            control_frame,
            text="Patterns Learned: 0",
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#7f8c8d"
        )
        self.pattern_label.pack(side=tk.LEFT, padx=20)
        
        # Initial message
        self.add_message("Welcome! Make your first move to start playing.\n")
        
    def add_message(self, message):
        """Add a message to the result text area."""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, message)
        self.result_text.see(tk.END)
        self.result_text.config(state=tk.DISABLED)
        
    def get_move_name(self, move):
        """Convert move letter to full name."""
        names = {'R': 'Rock', 'P': 'Paper', 'S': 'Scissors'}
        return names.get(move, move)
    
    def play_round(self, player_move):
        """Play a round of the game."""
        self.round_number += 1
        
        # Get AI move
        ai_move = self.ai.get_ai_move()
        
        # Determine winner
        result = self.ai.determine_winner(player_move, ai_move)
        
        # Display round info
        self.add_message(f"\n{'='*60}\n")
        self.add_message(f"Round {self.round_number}\n")
        self.add_message(f"{'='*60}\n")
        self.add_message(f"You chose:  {self.get_move_name(player_move)} ({player_move})\n")
        self.add_message(f"AI chose:   {self.get_move_name(ai_move)} ({ai_move})\n")
        
        # Display result
        if result == 'player':
            self.add_message(">> YOU WIN THIS ROUND! 🎉\n")
        elif result == 'ai':
            self.add_message(">> AI WINS THIS ROUND! 🤖\n")
        else:
            self.add_message(">> IT'S A TIE! 🤝\n")
        
        # Learn from player's move
        self.ai.learn_pattern(player_move)
        
        # Update displays
        self.update_stats()
        self.round_label.config(text=f"Round: {self.round_number}")
        self.pattern_label.config(text=f"Patterns Learned: {len(self.ai.pattern_dict)}")
        
        # Show learning progress
        if self.round_number > 0 and self.round_number % 10 == 0:
            self.add_message(f"\n[INFO] AI has learned {len(self.ai.pattern_dict)} patterns!\n")
    
    def update_stats(self):
        """Update the statistics display."""
        total = self.ai.wins + self.ai.losses + self.ai.ties
        win_rate = (self.ai.wins / total * 100) if total > 0 else 0
        
        self.stats_label.config(
            text=f"AI: {self.ai.wins} | Player: {self.ai.losses} | Ties: {self.ai.ties} | AI Win Rate: {win_rate:.1f}%"
        )
    
    def reset_game(self):
        """Reset the game statistics."""
        self.ai.reset_stats()
        self.round_number = 0
        self.round_label.config(text="Round: 0")
        self.update_stats()
        self.add_message("\n[RESET] Statistics reset! (Learned patterns retained)\n")


def main():
    root = tk.Tk()
    app = RPSGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
