# Chess Game AI

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Screenshots](#screenshots)
* [TODO](#todo)
* [Instructions](#instructions)
* [Further development ideas](#further-development-ideas)

## General info 
A tutorial by Eddie Sharick: [Eddie's YouTube channel](https://www.youtube.com/channel/UCaEohRz5bPHywGBwmR18Qww)

## Technologies
* Python 3.7.8
* pygame 2.3.0

## Screenshots
![Menu Screen](https://user-images.githubusercontent.com/80916844/238141284-3694d30a-e724-4212-9441-a88d03761b55.png)

![Options Screen](https://user-images.githubusercontent.com/80916844/238141619-7dd206b2-d676-42aa-9107-3bb313aeeef9.png)

![Start screen](https://user-images.githubusercontent.com/80916844/240957535-4e884d64-3e1a-43c9-acdb-583373a076ab.png)

## TODO
- [ ] Cleaning up the code - right now it is really messy.
- [ ] Using numpy arrays instead of 2d lists.
- [ ] Stalemate on 3 repeated moves or 50 moves without capture/pawn advancement.
- [x] Menu to select player vs player/computer.
- [ ] Allow dragging pieces.
- [ ] Resolve ambiguating moves (notation).

## Instructions
1. Clone this repository.
```
git clone https://github.com/TNuan/Chess-Game-AI.git
```
2. Install packages from requirements.txt
```
cd Chess-Game-AI
python -m pip install -r requirements.txt
```
3. Run `main.py`

#### Sic:
* Press `z` to undo a move.
* Press `r` to reset the game.

## Further development ideas
1. Ordering the moves (ex. looking at checks and/or captures) should make the engine much quicker (because of the alpha-beta pruning).
2. Keeping track of all the possible moves in a given position, so that after a move is made the engine doesn't have to recalculate all the moves.
3. Evaluating kings placement on the board (separate in middle game and in the late game).
4. Book of openings.