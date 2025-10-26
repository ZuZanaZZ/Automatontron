# Introduction
Automatontron is a logic game inspired by the Human Resource Machine game. In Automatontron, the player is tasked with constructing an automaton that recognises the language of the given level and thus progresses in the game.
## How to start:
- First, download the ZIP file from GitHub by clicking on the < > Code button.
- Unzip and extract the files by right-clicking on the downloaded file, choosing "Extract All...", and selecting your desired destination.
- If you do have Python and Pygame installed, you can play the game by opening the downloaded folder and going to the "main.py" file, and running it in the IDE of your choice.
- If you don't have Python, Pygame, or you don't want to install them, you can double-click on the Automatontron.exe file!

## Controls:
- ARROW keys: movement
- ENTER: select
- SPACEBAR: carry a circle
    - stand on a circle and press SPACEBAR to pick up or put down the circle
- S: rotate between variants of a circle
    - stand on a circle, press S to rotate through: base, accepting, initial, and initial-accepting variants
- A: start/stop drawing an arrow
    - straight arrow: stand on a circle and press A
    - loop arrow: press A twice on the same circle
- D: delete an arrow
    - delete the arrow you are standing on by pressing D
- Z, X, C, V: add a symbol to an arrow
    - (stand on the arrow and press any of these keys)

## Objective of the game:
- With your acquired knowledge, complete every level and become a master of automata!

# Showcase of Automatontron
## Menu
The game features a menu system.
### Main menu
After starting the game, the main menu is displayed. The player can choose from the options for the 'levels', 'resolution', and 'audio' menus. There is also an option to 'quit game'.

<img width="630" height="350.4" alt="main_menu" src="https://github.com/user-attachments/assets/b65c90eb-6d3a-4ad8-a520-bda24b0bdaa8" />

### Levels menu
- The levels are divided into two sections. The first section contains deterministic automata, and the second contains non-deterministic ones. Each level introduces a new concept in automata construction. The player is tasked with creating an automaton that recognizes the language of the given level. 
- The levels are initially locked, but after completing one level, the next one is unlocked. The state of the level menu at the beginning and end of the game can be seen in the picture below. The goal of the game is to gradually complete all levels up to the last one and become the master of automata. In the last level of each section, the player is tasked with implementing all the concepts learned so far into one larger automaton.

<img width="324" height="284.4" alt="level_menu" src="https://github.com/user-attachments/assets/a8603bd5-a459-4b0f-9c3d-001dcdd90d34" />

### Resolution menu
- This menu screen allows selection of different screen resolutions. Only the background image is scaled when the resolution is selected. The other graphic elements have a fixed size. The placement of the game elements on the screen is automatically adjusted relative to the size of the selected resolution. As can be seen in the picture below, the options are “1280 × 720”, “1920 × 1080” and “fullscreen”. If the screen is too small, some game elements may overlap in fullscreen mode and not work properly.
- There is also a bug with Pygame, that sometimes, when entering fullscreen mode, it readjusts the size of the other fullscreen windows.

<img width="105.5" height="98" alt="resolution_menu" src="https://github.com/user-attachments/assets/3fe85951-23c7-49e2-8749-19048ec884c5" />

### Audio menu
- The audio menu provides options to enable or disable music and sound effects as seen on the picture.

<img width="158.4" height="122.4" alt="audio_menu" src="https://github.com/user-attachments/assets/a6e8507d-42c2-4879-9f93-eb2a4fb6dbd8" />

## User interface
- The levels take place on a playing surface that contains user interface elements, which are depicted on the picture below. Their detailed description is as follows:
- Playing surface:
    - The background on which the game takes place.
- Helper with a text bubble:
    - A character that accompanies the player during level solving. It provides useful hints, informs the player about the correctness of his machine and warns about possible errors.
- Player character:
    - The player controls this character and interacts with the game environment. The character has animations of movement to the right, to the left, and standing still. 
- Circle generator:
    - When the player stands on the generator, one circle appears.
- Button:
    - After pressing the button, the process of checking the player's automaton is started. The helper then announces whether the player's automaton is correct or incorrect.
- Circle Remover:
    - When a player steps on the circle remover, the circle they are holding is removed.

<img width="630" height="350.4" alt="level_ui_elements" src="https://github.com/user-attachments/assets/acd5feea-2a11-461f-99c6-4a9cf1b083bf" />

## Circles, arrows, and adding symbols
- When standing on the circle and pressing the "s" key, the circle variant is changed. It cycles between "normal", "accepting", "initial" and "initial-accepting" variants. The appearance of the circles can be seen in the figure below.
- The key "a" controls the drawing of both arrow variants. To draw a straight arrow, the player must stand on the circle and press the "a" key. After moving to the target circle, it is necessary to press the "a" key twice. To create a loop, i.e., an arrow starting and ending in the same state, it is necessary to press the "a" key twice on one circle. The picture below shows the appearance of the arrow variants.
- To remove the arrow, the "d" key can be pressed. It removes the arrow the player character is standing on.
- The keys "z", "x", "c", and "v" add a symbol to the arrow the player is standing on, which can be seen on the figure below.

<img width="184" height="148" alt="arrow_variants_with_symbols" src="https://github.com/user-attachments/assets/fa39e5cf-8e30-4efc-8853-f22c8b62e9ea" />

<img width="363" height="81.95" alt="circle_variants" src="https://github.com/user-attachments/assets/673fd311-aaef-4da0-a977-7830c3e9a277" />

## Automaton responses
- During the levels, the player can receive useful tips from the assistant regarding new concepts in the level. The assistant also informs the player whether their automaton accepts the language of the level or if the automaton has a problem and needs to be fixed. For example, it lists the string that differs between the language of the player's automaton and the language of the level, as can be seen below.

<img width="472.5" height="184.5" alt="automaton_doesnt_accept" src="https://github.com/user-attachments/assets/22141ee1-a212-48a2-9120-f1b94e2aa5cf" />

<img width="492.94" height="188.65" alt="automaton_accepts" src="https://github.com/user-attachments/assets/dd8e614f-a5b0-4592-9f61-d876ed53e3f3" />

## Game completion
- Upon completing the game, the player becomes a master of automata!
<img width="630" height="350.4" alt="game_completion" src="https://github.com/user-attachments/assets/e16edf3c-73ae-49b2-816d-786229386488" />

# Technical details
- Below is a UML diagram showing the class structure of the game’s code.
## Class diagram
<img width="726.68" height="298.22" alt="class_diagram" src="https://github.com/user-attachments/assets/81d8e8b9-918a-4c71-9f01-73d763cd41a0" />

