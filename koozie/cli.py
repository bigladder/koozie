"""koozie command line interface"""
import sys
import click
import koozie


def list_callback(context: click.Context, _: click.Parameter, value: str) -> None:
    """Callback function for the list command."""
    if not value or context.resilient_parsing:
        return

    unit_list = koozie.koozie.get_unit_list()

    for dim in unit_list:
        dim_aliases = ""
        if len(unit_list[dim]["aliases"]) > 0:
            dim_aliases = f" ({', '.join(unit_list[dim]['aliases'])})"
        if value in dim or value == "*" or value in dim_aliases:
            heading = f"{dim}{dim_aliases}"
            click.echo(heading)
            click.echo("-" * len(heading))
            for unit in unit_list[dim]["units"]:
                aliases = ""
                if len(unit_list[dim]["units"][unit]) > 0:
                    aliases = f" ({', '.join(unit_list[dim]['units'][unit])})"
                try:
                    click.echo(f"  - {unit}{aliases}")
                except UnicodeEncodeError:
                    click.echo(f"  - {unit}")
            click.echo("\n")

    context.exit()


@click.command(
    context_settings={"help_option_names": ["-h", "--help"], "ignore_unknown_options": True}
)
@click.version_option(None, "-v", "--version")
@click.option(
    "-l",
    "--list",
    help='Print a list of available units by dimension (e.g., "power"). Default: list all units.',
    type=click.STRING,
    is_flag=False,
    flag_value="*",
    callback=list_callback,
)
@click.argument("value", type=click.FLOAT)
@click.argument("from_units", type=click.STRING)
@click.argument("to_units", type=click.STRING, required=False)
def koozie_cli(
    value: float,
    from_units: str,
    to_units: str,
    list: str,  # pylint: disable=unused-argument,redefined-builtin
) -> None:
    """koozie: Convert VALUE from FROM_UNITS to TO_UNITS.

    If TO_UNITS is not specified, VALUE will be converted from FROM_UNITS into base SI units.
    """
    try:
        if to_units is None:
            click.echo(f"{koozie.koozie.fr_q(value,from_units)}")
        else:
            click.echo(f"{koozie.koozie.convert_q(value,from_units,to_units)}")
    except (koozie.koozie.pint.UndefinedUnitError, koozie.koozie.pint.DimensionalityError) as e:
        sys.exit(str(e))
