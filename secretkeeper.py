#import secret
import click

@click.command()
@click.argument('name')
def cli(name):
    click.echo('Store was called for ' + name)
