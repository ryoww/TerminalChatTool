from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align

console = Console()

# チャットメッセージのデータ
messages = [
    {"sender": "A", "message": "Hello, how are you?"},
    {"sender": "B", "message": "I'm good! How about you?"},
    {"sender": "A", "message": "I'm doing well, thanks!"},
    {"sender": "B", "message": "What are you up to?"},
]

def display_chat():
    """チャット全体を表示する関数"""
    content = Text()
    for msg in messages:
        sender = Text(f"{msg['sender']}: ", style="magenta" if msg['sender'] == "A" else "cyan")
        message = Text(msg["message"], style="white")
        content.append(sender)
        content.append(message)
        content.append("\n")

    # 全体を枠で囲んで表示
    console.clear()
    console.print(Panel(Align.left(content), title="Chat Room", border_style="blue", padding=(1, 2)))

def send_message():
    """メッセージを入力して送信する関数"""
    while True:
        display_chat()  # チャット全体を表示
        user_input = Prompt.ask("あなたのメッセージを入力 ('exit'で終了)")
        if user_input.lower() == 'exit':
            console.print("\nチャットを終了します。", style="bold red")
            break
        # メッセージを追加して表示を更新
        messages.append({"sender": "You", "message": user_input})

# メイン実行
send_message()
