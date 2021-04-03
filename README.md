# Chess Game

Chess game developed using PyGame library.

This project is meant to be an exercise of SOLID and Design Patterns. It is important to highlight that as interfaces are not strictly enforced on Python, due to its dynamic nature, the language encourages the application of [duck-typing](https://docs.python.org/3.8/glossary.html#term-duck-typing) and [EAFP](https://docs.python.org/3.8/glossary.html#term-eafp).

- **Single Responsability Principle**: Obtained through separation of concerns and the Command Pattern abstraction applied to the movement logic. The presentation layer, built with PyGame, is also decoupled from the bussiness logic. 
- **Open Closed Principle**: The architecture aims to be extensible, requiring only to subclass `Piece` or `Movement` to add new funcionality to the game.
- **Liskov Substitution Principle**: The two class families (pieces and movements) follow consistent interfaces, allowing its subtypes to be interchangeable.
- **Interface Segregation**: Every class implements and relies on the bare minimum interface requirements, namely the interfaces defined by `Piece` or `Movement` classes.
- **Dependency Inversion**: All messages exchanges relies on common interfaces of object families, allowing implementations and interfaces to evolve independently. 

## Running the code
- You will need to have `python3` and `pip` installed
- Install the requirements with `pip install -r requirements.txt`
- Run the code with `python3 game.py`
- There are two keyboard shortcuts:
    - `u`: Undo the last movement
    - `n`: Start a new game

## Project Structure
- `pieces/`: Implementations for each chess piece
- `board.py`: Implementation of the chess board data structure
- `moves.py`: Implementation of movements logic
- `game.py`: Presentation logic, using pygame library.
- `images/`: Contains image assets for the game (i.e. pieces and chess board)
