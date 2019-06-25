#!./venv/bin/python

import click
from shell import Shell


@click.command()
@click.option('--blue', is_flag=True)
@click.option('--red', is_flag=True)
@click.option('--mapfile', default="maps/default")
def cli(blue, red, mapfile):
    app = Shell(mapfile)
    app.mainloop(blue, red)

if __name__ == '__main__':
    cli()
