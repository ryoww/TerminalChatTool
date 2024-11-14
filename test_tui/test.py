from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align

console = Console()

# チャットメッセージのデータ
messages = [
    {"sender": "Alice", "message": "Hello, how are you?"},
    {"sender": "You", "message": "I'm good! How about you?"},
    {"sender": "Alexander", "message": "I'm doing well, thanks!"},
    {"sender": "You", "message": "What are you up to?"},
]

def display_chat():
    """チャット全体を表示する関数"""
    # 送信者名の最大長を計算
    max_sender_width = max(len(msg['sender']) for msg in messages) + 1
    
    content = Text()
    for msg in messages:
        # 送信者名の表示幅を揃える
        sender = Text(f"{msg['sender']:<{max_sender_width}}", style="magenta" if msg['sender'] == "You" else "cyan")
        separator = Text("| ", style="dim")
        message = Text(msg["message"], style="white")

        # 各部分を連結して内容に追加
        content.append(sender)
        content.append(separator)
        content.append(message)
        content.append("\n")

    # 全体を枠で囲んで表示
    console.clear()
    console.print(Panel(Align.left(content), title="Chat Room", border_style="blue", padding=(0, 1)))

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
