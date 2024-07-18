# this is a lexer implementaion it takes a string and converts it into list of tokens which parser can parse

import tokenTypes
from typing import Any

# this token calss is there to specify the types of possible returned tokens
# each token will have a type and value associated with it so as the constructor of this calss runs the types will be passed

class Token:
    def __init__(self,tokenType:tokenTypes.TokenType,value : Any) -> None:
        self.tokenType = tokenType
        self.value = value

class Lexer:

    tokens : list[Token]       # this is list of output tokens

    def __init__(self,text:str) -> None:
        self.text = text    # the input text
        self.start = 0      # start pointer
        self.current = 0    # current pointer
        self.lines = 1      # number of lines
        self.tokens = []    # the token list initializing it to be an empty list

    def move_to_next_and_return_current(self) -> str:
        char = self.text[self.current]
        self.current += 1
        return char
    
    def advance(self):
        self.current += 1

    def peek_next(self):
        try:
            self.current +=1
            return self.text[self.current]
        finally:
            self.current -= 1

    def scan(self) -> list[Token]:
        while not self.is_end(): # is end will return ture or false specifying that we have reached end of file or not
            self.start = self.current
            self.scan_current()

        self.tokens.append(Token(tokenTypes.TokenType.EOF,None)) # after we have completed scanning we add an end of file token
        return self.tokens    
    
    def is_end(self) -> bool:        # if current pointer exceeds total length
        return self.current >= len(self.text)

    def peek(self) -> str:
        if self.is_end():
            return ""
        else:
            return self.text[self.current]

    def scan_current(self): 
        character = self.move_to_next_and_return_current()
        match character:
            case "{": # starting of an object
                self.tokens.append(Token(tokenTypes.TokenType.LEFT_BRACE,character))
            case "}": # ending of an object
                self.tokens.append(Token(tokenTypes.TokenType.RIGHT_BRACE,character))
            case '"': # starting of an string
                self.add_string()   # parse and add the whole string as once
            case '[':
                self.tokens.append(Token(tokenTypes.TokenType.LEFT_SQUARE_BRACKET,character))
            case ']':
                self.tokens.append(Token(tokenTypes.TokenType.RIGHT_SQUARE_BRACKET,character))                    
            case ':':
                self.tokens.append(Token(tokenTypes.TokenType.COLON,character))
            case ',':
                self.tokens.append(Token(tokenTypes.TokenType.COMMA,character))
            case '-':
                if self.peek().isdigit():
                    self.add_number()
                else:
                    raise ValueError('- sign must be followed by a digit')        
            case "\n":
                self.lines += 1
            case " ":
                pass    
            case _:
                if character.isdigit():
                    self.add_number()
                elif character.isalpha():
                    self.add_none_or_boolean()
                else:
                    raise ValueError(f'unknown character at index {self.current}')        

    def add_string(self) -> None:
        while self.peek() != '"' or self.is_end():
            self.move_to_next_and_return_current()

        if  self.is_end():
            raise ValueError('string must end with " ')
        
        self.move_to_next_and_return_current() # if all above is not true means the string is terminated and we move past the end double quote

        self.tokens.append(Token(tokenTypes.TokenType.STRING,
                                 self.text[self.start+1:self.current-1]))  

    def add_number(self) -> None:
        while self.peek().isdigit():
            self.move_to_next_and_return_current() # this will break when the loop is at a non digit character

            if self.peek() == '.': # means the digit should be float
                if not self.peek_next().isdigit():
                    raise ValueError('. should be followed by a digit')
                self.advance() # move past .
                
                while self.peek().isdigit(): # this will break at a non digit number and current will be at that thing
                    self.advance()
                # if this condition has run means the digit is a float

                self.tokens.append(Token(tokenTypes.TokenType.FLOAT,
                                         float(self.text[self.start:self.current])))    
                return
          
        self.tokens.append(Token(tokenTypes.TokenType.NUMBER,
                                         int(self.text[self.start:self.current])))
        return    
        
    def add_none_or_boolean(self):
         
        while self.peek().isalpha():
            self.advance()

        token = self.text[self.start:self.current].lower()
        if len(token) < 3: # means not either null none true or false
            raise ValueError('unknown token')
        match token:
            case 'null':
                self.tokens.append(Token(tokenTypes.TokenType.NONE,None))
            case 'none':
                self.tokens.append(Token(tokenTypes.TokenType.NONE,None))
            case 'true':
                self.tokens.append(Token(tokenTypes.TokenType.BOOLEAN,True))
            case 'false':
                self.tokens.append(Token(tokenTypes.TokenType.BOOLEAN,False))   
            case _ :
                raise ValueError('unknown string')            
            