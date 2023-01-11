# gomoku-ai

a simple gomoku AI Use **Minimax algorithm**

![](https://github.com/Hotshot824/gomoku-ai/blob/main/image/document_image.png?raw=true)

## Requirement

Install python environement `python -m pip install requirements.txt`

## How to play?

1. Start gomoku-ai server, run command `python start_server.py`
2. Choose interface, run `python Cli_gomoku.py` or `python Gui_gomoku.py`
3. Play Gomoku Game.

## Features

- [x] Simple gomoku AI, using search algorithm.
- [x] Have a clear inheritance relationship.
    * Server: base -> gomokuAI -> server
    * Client: base -> client -> CLI/GUI
- [x] Support player online battle
- [x] Support multiple player at the same time.

## Future plans

- [ ] Deeper recursion depth.
- [ ] Wider search range.
- [ ] Improved heuristic function.