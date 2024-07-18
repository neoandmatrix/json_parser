import typer
from typing_extensions import Annotated
from typing import Optional
from jsonParser import __appName__,__version__
from pathlib import Path
from jsonParser import parser

app = typer.Typer()

def _version_callback(value : bool):
    if value:
        print(f'{__appName__} v{__version__}')
        raise typer.Exit()

@app.callback()
def main(version : Optional[bool] = typer.Option(
    None,
    "--version",
    "-v",
    help="Show application version and exit",
    callback=_version_callback,
    is_eager="true"
))-> None:
    return

@app.command()
def parse_file(filename : Annotated[str,typer.Argument()]):
    try:
        with open(filename,'r') as f:
            content = f.read()
            print(parser.parse(content))
    except FileNotFoundError: 
        print(f'file {filename} not found')   

@app.command()
def parse_string(text : Annotated[str,typer.Argument()]):
    print(parser.parse(text))
