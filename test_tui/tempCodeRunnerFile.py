from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from rich.rule import Rule

# Consoleのインスタンスを作成
console = Console()

# 部屋の選択肢（初期部屋）
rooms = ["General", "Sports", "Technology"]

# ロビー画面の表示関数
def display_lobby():
    layout = Layout()

    # タイトルを中央揃えで表示（装飾追加）
    title_panel = Panel(
        Align.center("[bold magenta]✨ Chat Lobby ✨[/bold magenta]"),
        style="bright_black",
        border_style="magenta",
    )
    layout.split_column(
        Layout(title_panel, name="title", size=5),
        Layout(name="main"),
    )

    # チャットルーム選択のテーブル
    table = Table(style="cyan", border_style="bright_blue")
    table.add_column("番号", justify="center", style="bold yellow")
    table.add_column("部屋の名前", style="bold green")
    for index, room in enumerate(rooms, start=1):
        table.add_row(f"🏷 {index}", room)
    table.add_row(f"➕ {len(rooms) + 1}", "[italic cyan]部屋の追加[/italic cyan]")

    # テーブルをパネルに追加
    panel = Panel(
        table,
        title="[bold yellow]Choose a room[/bold yellow]",
        border_style="bright_blue",
        padding=(0, 2),
    )

    # メインレイアウトにパネルを設定
    layout["main"].update(panel)

    # ロビー画面全体を描画
    console.print(layout)
    console.print(Rule("[bold cyan]番号を入力してください[/bold cyan]"))

# 部屋の追加または選択の処理
def main():
    while True:
        display_lobby()

        # ユーザーの入力を取得
        choice = Prompt.ask(
            "[bold cyan]番号を選択してください[/bold cyan]",
            choices=[str(i) for i in range(1, len(rooms) + 2)],
            default=str(len(rooms) + 1),  # デフォルトを部屋の追加に設定
        )

        # 選択した部屋に基づいて処理を行う
        if int(choice) == len(rooms) + 1:  # 部屋の追加が選択された場合
            room_name = Prompt.ask("[bold green]新しい部屋の名前を入力してください[/bold green]")
            rooms.append(room_name)
            console.print(f"\n[bold green]🎉 {room_name} が追加されました！[/bold green]\n")
        else:
            selected_room = rooms[int(choice) - 1]
            console.print(f"\n[bold yellow]🛋️ {selected_room} に入りました！[/bold yellow]\n")
            # 部屋に入った場合の処理をここに追加可能

# 実行
if __name__ == "__main__":
    main()
