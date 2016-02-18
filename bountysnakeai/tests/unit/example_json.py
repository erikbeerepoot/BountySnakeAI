dummy_snake_1 = """{
    "id": "1234-567890-123456-7890",
    "name": "The first snaaaake",
    "status": "alive",
    "message": "Moved north",
    "taunt": "Let's rock!",
    "age": 56,
    "health": 83,
    "coords": [ [1, 1], [1, 2], [2, 2] ],
    "kills": 4,
    "food": 12,
    "gold": 2
}"""
dummy_snake_2 = """{
    "id": "9876-543210-123456-7890",
    "name": "Another snaaaaake",
    "status": "alive",
    "message": "Moved south",
    "taunt": "Let's rock!",
    "age": 56,
    "health": 70,
    "coords": [ [4, 4], [4, 3], [4, 2], [4, 1] ],
    "kills": 4,
    "food": 20,
    "gold": 2
}"""
dummy_game = """{
    "game": "hairy-cheese",
    "mode": "advanced",
    "turn": 4,
    "board": {
        "height": 20,
        "width": 30
    },
    "snakes": [
        %s, %s
    ],
    "food": [
        [1, 5], [9, 3]
    ]
}""" % (dummy_snake_1, dummy_snake_2)

