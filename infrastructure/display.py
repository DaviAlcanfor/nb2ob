import pyfiglet
import typer
import yaspin



def display_banner() -> None:
    ascii_art = pyfiglet.figlet_format("NB2OB", font="doom")
    typer.echo(typer.style(ascii_art, fg="bright_magenta"))
    
    
def spin(text: str, func, *args, **kwargs):
    with yaspin(text=text, color="magenta") as spinner:
        try:
            result = func(*args, **kwargs)
            spinner.ok("✔")
            return result
        except Exception:
            spinner.fail("✖")
            raise