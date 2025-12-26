#computer choice

import random


def computer_choice():
 stp=["rock","paper","scissor"]
 choice=random.choice(stp)
 return choice

def decide_result(player,computer):
  if player==computer:
    return "tie" 
  

  winning_pairs = {
        ("rock", "scissor"),
        ("scissor", "paper"),
        ("paper", "rock")
    }

  if (player,computer) in winning_pairs:
    return "win"
  else:
    return "lose"