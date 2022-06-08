# Chess Game

Chess game developed using PyGame library.

This project is meant to be an exercise of SOLID and Design Patterns. It is important to highlight that as interfaces are not strictly enforced on Python, due to its dynamic nature, the language encourages the application of [duck-typing](https://docs.python.org/3.8/glossary.html#term-duck-typing) and [EAFP](https://docs.python.org/3.8/glossary.html#term-eafp).

- **Single Responsability Principle**: Obtained through separation of concerns and the Command Pattern abstraction applied to the movement logic. The presentation layer, built with PyGame, is also decoupled from the bussiness logic. 
- **Open Closed Principle**: The architecture aims to be extensible, requiring only to subclass `Piece` or `Movement` to add new funcionality to the game.
- **Liskov Substitution Principle**: The two class families (pieces and movements) follow consistent interfaces, allowing its subtypes to be interchangeable.
- **Interface Segregation**: Every class implements and relies on the bare minimum interface requirements, namely the interfaces defined by `Piece` and `Movement` classes.
- **Dependency Inversion**: All messages exchanges relies on common interfaces of object families, allowing implementations and interfaces to evolve independently. 

## Running the code
- You will need to have `python3` and `pip` installed
- Install the requirements with `pip install -r requirements.txt`
- Run the code with `python3 game.py`
- During the game, there are two keyboard shortcuts:
    - `u`: Undo the last movement
    - `n`: Start a new game

## Project Structure
- `game/`: Core game files and logic
    - `pieces.py`: Implementation of the basic movement of each chess piece
    - `game.py`: Core game interactions
    - `moves.py`: Movement logic, abstracted using the Command and Factory patterns
- `screens/`: Presentation layer
    - `base.py`: Basic screen classes and functionality
    - `main.py`: Main presentation component
    - `menu.py`: Main Menu screen
    - `board.py`: Chess board screen, draws the game state
    - `about.py`: About screen
    - `game_over.py`: Game over
- `assets/`: All the game assets, like image files and themes
