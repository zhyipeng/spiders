from typer import Typer

from spiders.tieba import tieba


app = Typer()

app.command('tieba')(tieba)

if __name__ == '__main__':
    app()
