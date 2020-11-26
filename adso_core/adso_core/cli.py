#
# Created on Wed Nov 25 2020
# Author : Trung Le
# Email : trung.le@cast2cloud.com
# Copyright (c) 2020 cast2cloud.com , all rights reserved.
#
"""Console script for adso_core."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for adso_core."""
    click.echo("Replace this message by putting your code into "
               "adso_core.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
