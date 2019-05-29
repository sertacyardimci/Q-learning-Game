# Q-learning-Game
Q-learning is a values-based learning algorithm in reinforcement learning.

## Q-Learning — a simplistic overview (Game)
Let’s say that a robot has to cross a maze and reach the end point. There are mines, and the robot can only move one tile at a time. If the robot steps onto a mine, the robot is dead. The robot has to reach the end point in the shortest time possible.
<p align="center">
  <img src="https://github.com/sertacyardimci/Q-learning-Game/blob/master/readme/game.jpg" title="Game">
  <img src="https://github.com/sertacyardimci/Q-learning-Game/blob/master/readme/example_route.jpg" title="Example Route">
</p>

## Requirements
* Python 3 and later
* Pygame

## Installation
* `pip install pygame`

## AI train
* `python q.py`
* "Do you want train ? y => Yes, n => No:  "
*  Answer "y"

<p align="center">
  <img src="https://github.com/sertacyardimci/Q-learning-Game/blob/master/readme/trainingAI.gif" title="Training AI">
</p>

 
## AI Run
* `python q.py`
* "Do you want train ? y => Yes, n => No:  "
*  **Answer "n"**
* "Do you use train data ? y => Yes, n => No:  "
*  **Answer "y"**
*  "Which Data ? => 1 = System Data, 2 = User Data:  "
*  **Answer "2"**
*  Play with **space bar** (Space key on keyboard)

<p align="center">
  <img src="https://github.com/sertacyardimci/Q-learning-Game/blob/master/readme/playingAI.gif" title="Playing AI">
</p>

