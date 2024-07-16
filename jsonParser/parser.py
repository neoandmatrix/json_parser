# this is scanner class that scans the token list from lexer and converts it to correct output

from lexer import Lexer,Token
from tokenTypes import TokenType


JSON_OBJECT = dict[str,str]

def parse() -> JSON_OBJECT:
    test_string = input()
    lexer = Lexer(test_string)
    tokens = lexer.scan()
    #print(tokens)
    # print(len(tokens))
    # for i in range(len(tokens)):
    #     print(tokens[i].value)
    parser = Parser(tokens)
    return parser.parse()

class Parser: # this contains all the parser features

    def __init__(self,tokens : list[Token]) -> None: # takes the token list as input
        self.tokens = tokens 
        self.current = 0 # pointer to move


    def give_token_and_advance(self) -> Token: # returns the token currently the pointer is at and increases pointer by 1
        if self.current >= len(self.tokens):
            return self.tokens[len(self.tokens)-1]
        currentToken = self.tokens[self.current]
        self.current += 1
        return currentToken
    
    def get_current_token(self) -> Token:
        return self.tokens[self.current]


    def parse(self) -> JSON_OBJECT: # the parse method which give the final json object as output
        token = self.get_current_token() # this will be passed to parse_from_given_token
        return self.parse_from_given_token(token)


    def parse_from_given_token(self,token : Token) -> JSON_OBJECT: # parse on basis of the token type and returns the appropriate python representaion
        match token.tokenType:
            case TokenType.LEFT_BRACE: # if we encounter a left brace means we are at start of python object so calling the parse object
                return self.parseObject()
            case TokenType.STRING :
                return self.get_current_token().value
    
    def advance_current(self)->None:
        self.current += 1        

    def parse_colon(self) -> None:
        if self.tokens[self.current].tokenType != TokenType.COLON:
            #print(self.current)
           # print(self.getCurrentToken().value)
            raise ValueError("string must be followed by colon")
        
        # means it is colon and we shift the current pointer by 1
        self.current += 1        

    def parseObject(self) -> JSON_OBJECT:
        
        json_object : JSON_OBJECT = {}
        
        self.advance_current()
        key_token = self.give_token_and_advance() # this will be the key or a right brace in which case we return an empty json object and current will be on colon

        while key_token.tokenType != TokenType.RIGHT_BRACE:
            print(key_token.value,key_token.tokenType)

            if key_token.tokenType == TokenType.EOF: # means only { was provided
                break
            
            if key_token.tokenType != TokenType.STRING:
                raise ValueError('objects must begin with a valid "key"')
            
            # if all the cases above not executed then it is correct json format so next thing must be colon
            
            self.parse_colon()

            # now after parsing of colon the pointer is at next token so calling the parse_from_given_token on it for value
            json_object[key_token.value] = self.parse_from_given_token(self.get_current_token())
            
            self.advance_current()
            
            key_token = self.give_token_and_advance() # here key token will be right brace or comma and current will be on either { or another key string

            if key_token.tokenType == TokenType.COMMA:
                key_token = self.give_token_and_advance() # here key token will be string and current will be on colon
            
        return json_object   
    
print(parse())
