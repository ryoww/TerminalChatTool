from rich.console import Console
from rich.text import Text

console = Console()

# チャットメッセージのデータ
messages = [
    {"sender": "A", "message": "Hello, how are you?"},
    {"sender": "B", "message": "I'm good! How about you?"},
    {"sender": "A", "message": "I'm doing well, thanks!"},
    {"sender": "B", "message": "What are you up to?"},
]

# メッセージを表示
for msg in messages:
    sender = Text(f"{msg['sender']}: ", style="magenta" if msg['sender'] == "A" else "cyan")
    message = Text(msg["message"], style="white")
    console.print(sender.append(message))
