# Oops-Bot
An SC2 ai to showcase OOPs principles

This project is an AI Bot that uses the python framework, BurnySC2, to play StarCraft2. The framework loads the BotAI class with most of the features I used, so I applied OOP principles to separate and encapsulate the methods based on the roles and responsibilities I needed as well as inherit shared functionality and create polymorphic functions. 

StarCraft 2 is a 1v1 real-time strategy game with fog of war (incomplete information) and an infinite amount of possibilities. A bot must gather resources, advance through the tech tree, build an army, and destroy all of the opponents buildings to win.

The 3 main abstract classes used in my bot are GamePlayer, Strategy, and Command.
GamePlayers contain the location data for my bot and the opponent.
Strategies contain the logic for charting through the infinite options. My bot starts with a rigidly programmed build order or plan to follow but quickly announces when it’s finished and transitions into being reactive with a decision tree.
The role of Commands is to provide lower level implementation logic (tactics compared to strategies). They share methods which put commands to the front of the queue or back.

I can use terminal commands to start a version of StarCraft 2 and will have access to the program data including the built-in AIs Blizzard includes in SC2. I have tested OOPs Bot against the highest level built-in AI and my bot has a high (~70%) winrate. 

https://github.com/BurnySc2/python-sc2
