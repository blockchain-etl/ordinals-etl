import click

from ordinalsetl.cli.stream import stream


@click.group()
@click.version_option(version='1.0.0')
@click.pass_context
def cli(ctx):
    pass

# streaming
cli.add_command(stream, "stream")
