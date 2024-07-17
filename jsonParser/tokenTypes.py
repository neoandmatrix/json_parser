from enum import auto

class TokenType:
  
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    NONE = auto()
    LEFT_SQUARE_BRACKET = auto()
    RIGHT_SQUARE_BRACKET = auto()

    COLON = auto()
    COMMA = auto()
    EOF = auto()