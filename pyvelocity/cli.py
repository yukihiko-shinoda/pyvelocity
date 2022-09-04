"""Console script for pyvelocity."""

import click
from click import ClickException

from pyvelocity.checks.aggregation import Checks, Results
from pyvelocity.configurations.aggregation import Configurations
from pyvelocity.configurations.files.aggregation import ConfigurationFiles


@click.command()
def main() -> None:
    """Console script for pyvelocity."""
    configuration_files = ConfigurationFiles()
    configurations = Configurations(configuration_files)
    results = Results(list(Checks(configuration_files, configurations).execute()))
    if results.message:
        click.echo(results.message)
    if not results.is_ok:
        exception = ClickException("Looks there are some of improvements.")
        exception.exit_code = 3
        raise exception
    click.echo("Looks high velocity! ⚡️ 🚄 ✨")
