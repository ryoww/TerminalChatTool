from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.align import Align

# Consoleのインスタンスを作成
console = Console()

# 部屋の選択肢（初期部屋）
rooms = ["General", "Sports", "Technology"]

# ロビー画面の表示関数
def display_lobby():
    layout = Layout()

    # タイトルパネルを中央揃えで表示
    title_panel = Panel(
        Align.center("[bold magenta]Chat Lobby[/bold magenta]"),
        style="purple",
    )
    layout.split_column(
        Layout(title_panel, name="title", size=3),
        Layout(name="main"),
    )

    # チャットルーム選択のテーブル
    table = Table(title="Available Chat Rooms", style="cyan")
    table.add_column("番号", justify="center", style="bold")
    table.add_column("部屋の名前", style="green")

    # 部屋のリストをテーブルに追加
    for index, room in enumerate(rooms, start=1):
        table.add_row(str(index), room)

    # 最後に部屋の追加オプションを追加
    table.add_row(str(len(rooms) + 1), "部屋の追加")

    # テーブルを固定サイズのパネルに追加
    panel = Panel(
        table, 
        title="Choose a room", 
        border_style="blue", 
        height=15   # 高さを固定
    )

    # メインレイアウトにパネルを設定
    layout["main"].update(panel)

    # ロビー画面を表示
    console.print(layout)

# 部屋の追加または選択の処理
def main():
    while True:
        # ロビー画面の表示
        display_lobby()

        # ユーザーの入力を取得
        choice = Prompt.ask("番号を入力してください", choices=[str(i) for i in range(1, len(rooms) + 2)])

        # 選択した部屋に基づいて処理を行う
        if int(choice) == len(rooms) + 1:  # 部屋の追加が選択された場合
            room_name = Prompt.ask("部屋の名前を入力してください")
            # 新しい部屋を追加し、部屋リストを更新
            rooms.append(room_name)
            console.print(f"[bold green]{room_name} が追加されました。[/bold green]\n")
        else:
            selected_room = rooms[int(choice) - 1]
            console.print(f"\n[bold green]{selected_room} に入りました。[/bold green]\n")
            # 部屋に入った場合の処理をここに追加可能

# 実行
main()
