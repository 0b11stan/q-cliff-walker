#!./venv/bin/python

import click
from shell import Shell


@click.command()
@click.option('--blue', is_flag=True)
@click.option('--red', is_flag=True)
def cli(blue, red):
    app = Shell()
    app.mainloop(blue, red)

if __name__ == '__main__':
    cli()
