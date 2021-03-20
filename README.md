# Chess Game

Chess game developed using PyGame library.

Project created to test the Command Design Pattern, applied on the movement logic.
The architecture aims to be extensible. To add new pieces, create a class inheriting from `Piece` and implement the required methods. Custom movement logic can be also added by inheriting from `Movement` or `ComposedMovement`.

## Running the code
- You will need to have `python3` and `pip` installed
- Install the requirements with `pip install -r requirements.txt`
- Run the code with `python3 game.py`


## Project Structure
- `pieces/`: Implementations for each chess piece
- `board.py`: Implementation of the chess board data structure
- `moves.py`: Movements logic
- `game.py`: Presentation logic, using pygame library.
- `images/`: Contains image assets for the game (i.e. pieces and chess board)
