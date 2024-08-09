# Welcome to my practice page!
My name is Pavan Chaudhari, a data scientist at Enact Mortgage Insurance. I'm using this repo to practice programming small games in pygame to try and start learning game dev. There is a requirements.txt file that is intended to be installed before you start the games, and they run nicely in a venv.

# Pygame
[Pygame] is a game dev module in Python built on the SDL library. This gives it some nice capabilities with the familiarity of Python (i.e., simple clean code) while having the power of great rendering tools. I was recommended to start here, before my journey into Godot.

# My games
So far I have developed the following games:

1. **Fruit Collector**: a simple game where you just move around and collect fruit. I was learning how to take in keystrokes and check image collision/hit detection here. Additionally, I learned how to wait some time before re-rendering the fruit. And finally, I uploaded a sprite sheet and read that into pygame (just made a simple one with a pixel art tool).

2. **Snake**: I wanted to try to program snake to practice game logic and making a class, and this classic just made sense to me. There was some cool challenges here, like figuring out how to mke the blocks follow each other properly (i.e., only change direction when you're in line with the previous block). Also, I essentially implemented the snake as a linked list, which was a cool concept using data structures I learned back in school. Then, after getting the game logic working, I did more practice with sprite sheets which was cool. Finally, I made a main menu screen which allows you to select your game difficulty and creates the size of the sprites based on your selection.

3. **Horse Race**: A visualiztion of a horse race. It's not flushed out yet, but the idea is the horses run at different speed and I coded some momentum in there, but the horses are somewhat random.

4. **Blackjack**: From the horse races, I got inspired to do more gambling stuff, since it's fun and the rules are very specific. I ended up diving pretty deep into this project, and I drew some cards and cardbacks to match. Run the card_maker.py first, then the blackjack_runner.py in the blackjack subfolder and it works great! I am happy with the product and could flush it out later. Also, it would integrate pretty well into a suite of casino games--maybe my next project :D

# Thanks for visiting!

[Pygame]: https://www.pygame.org/news
