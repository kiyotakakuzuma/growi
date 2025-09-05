import growi_api
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json

# --- 設定ファイルの読み込み ---
CONFIG_FILE = 'config.json'
try:
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    URL = config.get('url')
    ACCESS_TOKEN = config.get('access_token')
except (FileNotFoundError, json.JSONDecodeError) as e:
    messagebox.showerror("設定エラー", f"{CONFIG_FILE} が見つからないか、形式が正しくありません。\n{e}")
    URL, ACCESS_TOKEN = "", "" # エラーの場合は空文字をセット


def update_growi_page():
    """GUIから入力された情報を使ってGrowiページを更新する"""
    # GUIから情報を取得
    page_id = page_id_entry.get()
    body = body_text.get("1.0", tk.END)

    if not all([URL, ACCESS_TOKEN, page_id, body.strip()]):
        messagebox.showerror("エラー", "Page IDと更新内容を入力してください。")
        return

    try:
        # 1. 記事の現在のリビジョンIDを取得
        status_var.set("リビジョンIDを取得中...")
        app.update_idletasks()
        res = growi_api.get_page_info(URL, ACCESS_TOKEN, page_id)
        if 'page' not in res:
            raise Exception(f"ページの取得に失敗しました: {res}")

        revisionId = res['page']['revision']['_id']
        status_var.set(f"リビジョンID: {revisionId} を取得しました。ページを更新します...")
        app.update_idletasks()

        # 2. 記事の更新
        update_res = growi_api.update_page(URL, ACCESS_TOKEN, page_id, revisionId, body)
        
        status_var.set("ページの更新が完了しました。")
        messagebox.showinfo("成功", "ページの更新が正常に完了しました。")

    except Exception as e:
        status_var.set("エラーが発生しました。")
        messagebox.showerror("エラー", f"処理中にエラーが発生しました:\n{e}")

def fetch_current_page_content():
    """GUIの入力情報を使ってGrowiから現在のページ内容を取得し、テキストエリアに表示する"""
    # GUIから情報を取得
    page_id = page_id_entry.get()

    if not all([URL, ACCESS_TOKEN, page_id]):
        messagebox.showerror("エラー", "Page ID を入力してください。")
        return

    try:
        status_var.set("現在のページ内容を取得中...")
        app.update_idletasks()

        res = growi_api.get_page_info(URL, ACCESS_TOKEN, page_id)
        if 'page' not in res or 'revision' not in res['page'] or 'body' not in res['page']['revision']:
             raise Exception(f"ページの取得に失敗したか、内容が空です: {res}")

        current_body = res['page']['revision']['body']
        
        # テキストエリアをクリアしてから新しい内容を挿入
        body_text.delete("1.0", tk.END)
        body_text.insert("1.0", current_body)
        
        status_var.set("現在のページ内容を取得しました。")

    except Exception as e:
        status_var.set("エラーが発生しました。")
        messagebox.showerror("エラー", f"処理中にエラーが発生しました:\n{e}")


# --- GUIのセットアップ ---
app = tk.Tk()
app.title("Growi ページ更新ツール")
app.geometry("550x500")

# --- スタイル ---
style = ttk.Style()
style.configure("TLabel", font=("Meiryo UI", 10))
style.configure("TButton", font=("Meiryo UI", 10))
style.configure("TEntry", font=("Meiryo UI", 10))

main_frame = ttk.Frame(app, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# --- 入力フィールド ---
# Page ID
ttk.Label(main_frame, text="Page ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
page_id_var = tk.StringVar(value='685671a868e660b807288181')
page_id_entry = ttk.Entry(main_frame, textvariable=page_id_var)
page_id_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

# --- 本文入力エリア ---
ttk.Label(main_frame, text="更新内容:").grid(row=1, column=0, sticky=tk.W, pady=5)
body_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=("Meiryo UI", 10), height=15)
body_text.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

# --- ボタンエリア ---
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=3, column=0, columnspan=2, pady=10)

fetch_button = ttk.Button(button_frame, text="現在の値を取得", command=fetch_current_page_content)
fetch_button.pack(side=tk.LEFT, padx=5)

update_button = ttk.Button(button_frame, text="ページを更新", command=update_growi_page)
update_button.pack(side=tk.LEFT, padx=5)


# --- ステータスバー ---
status_var = tk.StringVar()
status_bar = ttk.Label(main_frame, textvariable=status_var, relief=tk.SUNKEN, anchor=tk.W)
status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
status_var.set("準備完了")

main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(2, weight=1)

# --- メインループ ---
if URL and ACCESS_TOKEN:
    app.mainloop()
