import pyfiglet
import typer


def display_banner() -> None:
    ascii_art = pyfiglet.figlet_format("NB2OB", font="doom")
    typer.echo(typer.style(ascii_art, fg="bright_magenta"))