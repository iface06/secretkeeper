import app.controllers as ctrls
import click

@click.group(help='''Secretkeeper helps you managing your secrets like credentials a. 
                  The CLI provide all commands to manage your secrets.
                  
                  More information see: http://github.com/...
                  ''')
def cli():
    pass

@click.command(help='Encrypt and store given secret with key and name')
@click.option('--name', '-n', required=True, help='Name of secret ist used for file naming')
@click.option('--fact', '-f', required=True, help="Fact is stored encrypted to file")
@click.option('--key', '-k', help='Key for fact encryption')
@click.option('--tag', '-t', multiple=True, help="Tags stored to header of secret file")
#@click.option('--factfile', '-ff', help='Text file containing the fact')
#@click.option('--keyfile', '-kf', help='Text file containing the key for fact encryption')
def store(name, fact, key, tag):
    dto = ctrls.SecretDto(name, fact, key, tag)
    result = ctrls.store(dto)
    click.echo('Secret stored with given name ' + result.name)
    if tag:
        click.echo('Given Tags: ' + ', '.join(tag))

@click.command(help='Decrypt and show a secret')
@click.option('--name', '-n', required=True, help='Name of secret ist used for file naming')
@click.option('--key', '-k', help='Key for fact encryption')
def load(name, key):
    result = ctrls.readSecret(name, key)
    print('Secret File Content: ' + result.name)

@click.command(help='Decrypt and show a secret')
def list():
    secretFileNames = ctrls.listSecrets()
    print(secretFileNames)

@click.command(help='Find Secrets by given name or tags')
def find(name, tag):
    pass

cli.add_command(store)
cli.add_command(load)
cli.add_command(find)
cli.add_command(list)