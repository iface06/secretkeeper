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
    secret, key = ctrls.store(dto)
    click.echo('Secret stored with given name ' + secret.name)
    click.echo('Encrypted with key: ' + key)
    click.echo('Store key and name to decrypt the given secret.')
    if tag:
        click.echo('Given Tags: ' + ', '.join(tag))

@click.command(help='Decrypt and show a secret')
@click.option('--name', '-n', required=True, help='Name of secret ist used for file naming')
@click.option('--key', '-k', help='Key for fact encryption')
@click.option('--factonly', '-fo', help='show only the decrypted fact on cli', default=False, is_flag=True)
def load(name, key, factonly):
    secret = ctrls.readSecret(name, key)
    if(factonly):
        click.echo( secret.fact)
    else:
        click.echo('Secret Name: ' + secret.name)
        click.echo('Secret Fact: ' + secret.fact)
        click.echo('Secret Tags: ' + str(secret.tags))

@click.command(help='Decrypt and show a secret')
def list():
    secretFiles= ctrls.listSecrets()
    if(len(secretFiles) > 0):
        for file in secretFiles:
            click.echo(file.getSecretName())
    else:
        click.echo('No json-secret-files (jsons) found in given directory')

@click.command(help='Find Secrets by tags')
@click.option('--tag', '-t', required=True, multiple=True, help='Name of secret ist used for file naming')
def find(tag):
    secretFiles = ctrls.findSecretByTags(tag)
    for secretFile in secretFiles:
        click.echo(secretFile.getSecretName())

cli.add_command(store)
cli.add_command(load)
cli.add_command(find)
cli.add_command(list)