---
layout: post
title:  "Snake"
date:   2017-03-15 18:37:02 +0530
category: projects
---

# The Snake Game
The notorious **Snake** Game. Celebrating the "relaunch" of Nokia 3310!

## How to play?
Clone the game first:
```{r, engine='bash', count_lines}
git clone https://github.com/pranavgokhale95/Snake_Game.git
```

Run the game as below:
```{r, engine='bash', count_lines}
cd Snake_Game
g++ -o snake snake_linux.cpp
./snake
```

Use the following keys:<br>
<kbd>w</kbd> -- for going up <br>
<kbd>s</kbd> -- for going down <br>
<kbd>a</kbd> -- for going left <br>
<kbd>d</kbd> -- for going right <br>
and eat the food represented by "**$**" to increase your score ie. the length of the snake.

PS: Press the key and wait for a second. 

The game is over when: The head of the snake hits any part of the snake. 

Want to stop the game in between? Use <kbd>Ctrl</kbd>+<kbd>z</kbd> just in case.


## Known Issues?
* Render food everytime. Disappears when food appears on snake 
* Solve the length=2 snake length problem (Turns back on its head, then the game isn't over!. Logical problem)

Apart from these issues please report any other issues in the issue section. Thanks!

## Possible Improvements or Addition of Features
* Possible optimization in code.
* Make the game fast (The sleep is annoying but helpful for debugging. Reduce it if you want)
* Add a more random rand() function. The seed can specified and srand can be used.
* Add obstacles ie. add different game modes.
* The simple do-while for play again :P
* Add a section for high scores and corresponding names.
