#!./venv/bin/python

import click
from gui import Gui
from shell import Shell


@click.group()
def cli():
    pass


@cli.command()
#@cli.option('--blue', is_flag=True)
#@cli.option('--red', is_flag=True)
def shell():
    app = Shell()
    # blue
    app.mainloop(True, False)
    # red
    #app.mainloop(False, True)


@cli.command()
def gui():
    app = Gui()
    app.mainloop()


if __name__ == '__main__':
    cli()
