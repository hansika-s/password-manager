import typer

from passwordmanager import auth, vault

app = typer.Typer(help="Password Manager CLI - manage your passwords securely")

_state: dict[str, bytes] = {}


@app.callback()
def _main() -> None:
    _state["key"] = auth.unlock_or_setup()


@app.command("add", help="Add credentials for a service.")
def add_cmd(service: str, username: str, password: str) -> None:
    vault.add_credential(service, username, password, _state["key"])
    typer.echo(f"Added credentials for {service}.")


@app.command("get", help="Retrieve credentials for a service.")
def get_cmd(service: str) -> None:
    result = vault.get_credential(service, _state["key"])
    if result is None:
        typer.echo(f"Service '{service}' not found.")
        raise typer.Exit(code=1)
    username, password = result
    typer.echo(f"Service:  {service}")
    typer.echo(f"Username: {username}")
    typer.echo(f"Password: {password}")


@app.command("delete", help="Delete credentials for a service.")
def delete_cmd(service: str) -> None:
    if vault.delete_credential(service):
        typer.echo(f"Deleted credentials for {service}.")
    else:
        typer.echo(f"Service '{service}' not found.")
        raise typer.Exit(code=1)


@app.command("edit", help="Edit credentials for a service.")
def edit_cmd(
    service: str,
    username: str = typer.Option(None, "--username", "-u"),
    password: str = typer.Option(None, "--password", "-p"),
) -> None:
    if vault.edit_credential(service, username, password, _state["key"]):
        typer.echo(f"Updated credentials for {service}.")
    else:
        typer.echo(f"Service '{service}' not found.")
        raise typer.Exit(code=1)


@app.command("services", help="List all stored services.")
def services_cmd() -> None:
    services = vault.list_services()
    if not services:
        typer.echo("No services stored yet.")
        return
    typer.echo("Stored services:")
    for s in services:
        typer.echo(f"- {s}")
