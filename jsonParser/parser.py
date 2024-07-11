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
    #     print(tokens[i].tokenType)
    parser = Parser(tokens)
    return parser.parse()

class Parser: # this contains all the parser features

    def __init__(self,tokens : list[Token]) -> None: # takes the token list as input
        self.tokens = tokens 
        self.current = 0 # pointer to move


    def giveToken(self) -> Token: # returns the token currently the pointer is at
        currentToken = self.tokens[self.current]
        self.current += 1
        return currentToken
    
    def getCurrentToken(self) -> Token:
        return self.tokens[self.current]


    def parse(self) -> JSON_OBJECT: # the parse method which give the final json object as output
        token = self.giveToken() # this will be passed to parse_from_given_token
        return self.parse_from_given_token(token)


    def parse_from_given_token(self,token : Token) -> JSON_OBJECT: # parse on basis of the token type and returns the appropriate python representaion
        match token.tokenType:
            case TokenType.LEFT_BRACE: # if we encounter a left brace means we are at start of python object so calling the parse object
                return self.parseObject()
            case TokenType.STRING | TokenType.EOF:
                return self.getCurrentToken().value

    def parseColon(self):
        if self.tokens[self.current].tokenType != TokenType.COLON:
            #print(self.current)
           # print(self.getCurrentToken().value)
            raise ValueError("string must be followed by colon")
        
        # means it is colon and we shift the current pointer by 1
        self.current += 1        

    def parseObject(self) -> JSON_OBJECT:
        
        json_object : JSON_OBJECT = {}

        key_token = self.giveToken() # this provides the next token after left brace
       
        while key_token.tokenType != TokenType.RIGHT_BRACE:
            if key_token.tokenType == TokenType.EOF: # means only { was provided
                raise ValueError("Incorrect JSON type")
            
            if key_token.tokenType != TokenType.STRING:
                raise ValueError('objects must begin with a valid "key" ')

            if key_token.tokenType == TokenType.RIGHT_BRACE: # means an empty {} was passed
                return json_object
            
            # if all the cases above not executed then it is correct json format so next thing must be colon
            # print(self.getCurrentToken().value)
            
            self.parseColon()
            #print(self.current)
            # now after parsing of colon the pointer is at next token so calling the parse_from_given_token on it for value
            json_object[key_token.value] = self.parse_from_given_token(self.getCurrentToken())
            self.giveToken()
            key_token = self.getCurrentToken()

        return json_object   
    
print(parse())
