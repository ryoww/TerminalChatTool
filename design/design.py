from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

# Consoleの設定
console = Console()

# Instagram風のカラフルなバナー表示
def instagram_banner():
    gradient_text = Text("Welcome to InstaChat!")
    colors = ["#FF5733", "#C70039", "#900C3F", "#581845", "#DAF7A6", "#FFC300"]
    for i, char in enumerate(gradient_text.plain):
        gradient_text.stylize(f"bold {colors[i % len(colors)]}", i, i + 1)
    banner = Panel(
        Align.center(gradient_text),
        border_style="bold magenta",
        title="InstaChat",
        title_align="left",
    )
    console.print(banner)

# メッセージ表示
def display_message(user, message, is_sender=False):
    if is_sender:
        color = "bold green"
        align = "right"
    else:
        color = "bold cyan"
        align = "left"

    msg = Text(f"{user}: {message}", style=color)
    aligned_msg = Align(msg, align=align)
    console.print(aligned_msg)

# チャット機能
def chat():
    console.clear()
    instagram_banner()
    console.print("\n[bold yellow]Type 'exit' to leave the chat.[/bold yellow]\n")
    
    user_name = console.input("[bold magenta]Enter your username: [/bold magenta]").strip()
    console.print(f"\n[bold green]Welcome, {user_name}! Start chatting below.[/bold green]\n")
    
    while True:
        message = console.input(f"[bold magenta]{user_name}[/bold magenta]: ").strip()
        if message.lower() == 'exit':
            console.print("[bold red]Goodbye! See you soon![/bold red]")
            break
        display_message(user_name, message, is_sender=True)
        # ダミーレスポンス（相手のメッセージ）
        display_message("Friend", "That's awesome! Tell me more!")

if __name__ == "__main__":
    chat()
