
# CS3050 Final Project – Tile Based Game (Okey)

## Project Description

This project is an implementation of a tile-based strategy game developed in Python. The game supports both human and computer players and includes a graphical user interface (GUI) built using the Arcade library.

Players can:
- Draw tiles from the middle pile or discard pile (once opened)
- Form valid groups (runs and sets)
- Open their hand when meeting the required score
- Add tiles to other player's existing open groups
- Play through multiple rounds with scoring

The game enforces core gameplay rules such as turn order, discard restrictions, opening requirements, and tile validation.

### Packages required to run
Arcade

### How to Run the Program
Run the main game file: main.py

### Notes
Print statements appear in the console during gameplay to show player turn details and actions, such as drawing from the middle pile or the previous player’s discard pile, and to indicate when a player has opened. 

However, key game information is also clearly displayed in the GUI: each player’s most recent discarded tile and their open tiles are fully visible, with visual highlights to make these states easy to identify during play. Additionally, the minimum open score and player hand scores are calculated and updated dynamically throughout the game.