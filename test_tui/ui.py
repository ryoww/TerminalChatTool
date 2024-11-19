from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align

console = Console()

# チャットメッセージのデータ
messages = [
    {"sender": "A", "message": "Hello, how are you?"},
    {"sender": "B", "message": "I'm good! How about you?"},
    {"sender": "A", "message": "I'm doing well, thanks!"},
    {"sender": "B", "message": "What are you up to?"},
]

# メッセージをまとめたテキストオブジェクトを作成
content = Text()

for msg in messages:
    sender = Text(f"{msg['sender']}: ", style="magenta" if msg['sender'] == "A" else "cyan")
    message = Text(msg["message"], style="white")
    content.append(sender)
    content.append(message)
    content.append("\n")  # 各メッセージごとに改行を追加

# 全体を枠で囲んで表示
console.print(Panel(Align.left(content), title="Chat Room", border_style="blue", padding=(1, 2)))
