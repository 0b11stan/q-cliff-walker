#!./venv/bin/python

import click
from gui import Gui
from shell import Shell


@click.group()
def cli():
    pass


@cli.command()
def shell():
    app = Shell()
    app.mainloop()


@cli.command()
def gui():
    app = Gui()
    app.mainloop()


if __name__ == '__main__':
    cli()
