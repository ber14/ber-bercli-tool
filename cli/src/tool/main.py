import time
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box
import os
import sys
import winreg
import subprocess
import typer
import pyfiglet

console = Console()
colors = ["bright_red", "bright_yellow", "bright_green", "bright_cyan", "bright_blue", "bright_magenta"]


with Live("", refresh_per_second=10) as live:
    for i in range(20):  
        time.sleep(0.08)
        current_color = colors[i % len(colors)]
        live.update(f"[bold black on {current_color}] ⏳ connecting to berber [/bold black on {current_color}]")

app = typer.Typer()

def setup_windows_autorun(shortcuts_dir):
 
    try:
        registry_path = r"Software\Microsoft\Command Processor"
        autorun_cmd = f'FOR %f IN ("{shortcuts_dir}\\*.bat") DO @DOSKEY %~nf="{shortcuts_dir}\\%~nxf" $*'
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "AutoRun", 0, winreg.REG_SZ, autorun_cmd)
        winreg.CloseKey(key)
        return True
    except Exception:
        return False

def show_banner():
  
    ascii_banner = pyfiglet.figlet_format("ber :) ", font="puffy")
    console.print(ascii_banner, style="bold cyan")
    console.print("[bold magenta][dim]hello![/dim]\n")

@app.command()
def main():
    show_banner()
    
    inp_box = Panel(
        "Type [bold yellow]/e[/bold yellow] to exit the creator", 
        title="[bright_red]Commands[/]", 
        border_style="bright_red",
        box=box.ROUNDED
    )
    console.print(inp_box)
    
   
    user_home = os.environ.get("USERPROFILE") or os.path.expanduser("~")
    shortcuts_dir = os.path.join(user_home, "cmd_shortcuts")
    
    if not os.path.exists(shortcuts_dir):
        os.makedirs(shortcuts_dir)
        
    while True:
        
        create = Prompt.ask("[bold yellow]Create a new shortcut? (Press Enter to continue or /e to exit)[/bold yellow]").strip()
        if create == "/e":
            console.print("[bold magenta]Goodbye from berber! 👋[/bold magenta]")
            break
            
        alias_name = Prompt.ask("[bold cyan]Shortcut command name? (e.g., bandit)[/bold cyan]").strip()
        if not alias_name:
            console.print("[bold red]Command name cannot be empty![/bold red]")
            continue
            
        if alias_name == "/e":
            break
            
        alias_cmd = Prompt.ask(f"[bold yellow]What command should '{alias_name}' run?[/bold yellow]").strip()
        if not alias_cmd:
            console.print("[bold red]It's not valid: cause empty[/bold red]")
            continue

        
        bat_file_path = os.path.join(shortcuts_dir, f"{alias_name}.bat")
        bat_content = f"@echo off\n{alias_cmd} %*\n"
    
        try:
            with open(bat_file_path, "w", encoding="utf-8") as f:
                f.write(bat_content)
            
            
            subprocess.run(f'DOSKEY {alias_name}="{bat_file_path}" $*', shell=True)
            
           
            setup_windows_autorun(shortcuts_dir)
            
            console.print(f"\n[bold green]✔ Shortcut successfully saved permanently![/bold green]")
            console.print(Panel(
                f"The shortcut [bold cyan]'{alias_name}'[/bold cyan] is now active!\n\n"
                f"  • It works [bold green]RIGHT NOW[/bold green] in this current window.\n"
                f"  • It will load [bold green]AUTOMATICALLY[/bold green] in any future CMD windows.\n\n"
                f"[dim]No 'source' command needed for Windows![/dim]",
                title="[bold green]Success![/bold green]",
                box=box.ROUNDED
            ))
        except Exception as e:
            console.print(f"[bold red]Failed to write shortcut: {e}[/bold red]")

if __name__ == "__main__":
  
    app()
