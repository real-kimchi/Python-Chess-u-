# `oo-chess`
This is a two-player interactive chess game that enforces the rules of Chess.


# Start the container
We'll do everything inside the container:

```
docker-compose run shell
```

# Play
From within a running container, execute:

```
python -m chess
```

### Caveat
The display of the chess board is quite rudimentary: It just prints the
Unicode symbols for chess-pieces. One potential source of confusion can 
occur if you're running this in a terminal with a dark background and 
light characters: Black pieces will look white and white pieces will 
look black.


# Run Tests
From within a running container, execute:

```
pytest tests
```
