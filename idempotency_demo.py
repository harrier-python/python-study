"""
べき等性（Idempotency）のデモンストレーション・スクリプト
このスクリプトは、設定ファイルに対する操作を通じて「べき等性がある処理」と
「ない処理」の違いを検証するものです。
"""

import os

# テスト用の設定ファイル名と、書き込みたい設定内容
CONFIG_FILE = "sample_config.txt"
SETTING_LINE = "Timeout=30\n"

def reset_file():
    """テスト用にファイルを初期化（空にする）します。"""
    open(CONFIG_FILE, 'w', encoding='utf-8').close()
    print(f"[準備] {CONFIG_FILE} を初期化しました。\n")

def non_idempotent_write():
    """
    【❌ べき等性がない処理】
    現在のファイルの状態を確認せずに、ただ指示された手順（追記）を実行します。
    自動化スクリプトでこれを行うと、再実行時にシステムを壊す危険性があります。
    """
    print("--- べき等性のない処理を実行します ---")
    with open(CONFIG_FILE, 'a', encoding='utf-8') as file:
        file.write(SETTING_LINE)
    print("=> 設定を追記しました。（※実行した回数だけ重複してしまいます）\n")

def idempotent_write():
    """
    【⭕️ べき等性がある処理】
    現在の状態を確認し、「すでに理想の状態であれば何もしない」、
    「理想の状態でなければ変更する」というアプローチをとります。
    何度実行しても安全です。
    """
    print("--- べき等性のある処理を実行します ---")
    
    # 1. まず現在のファイルの状態を確認する
    lines = []
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            lines = file.readlines()

    # 2. 状態の判定と適用
    if SETTING_LINE in lines:
        print("=> すでに正しい状態です。何も変更しません。\n")
    else:
        with open(CONFIG_FILE, 'a', encoding='utf-8') as file:
            file.write(SETTING_LINE)
        print("=> 設定が存在しなかったため、新しく追記しました。\n")

def show_file_content():
    """現在のファイルの中身を表示します。"""
    print("[現在のファイルの中身]")
    with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
        content = file.read()
        if content == "":
            print("(空)")
        else:
            print(content, end="")
    print("-" * 30 + "\n")

if __name__ == "__main__":
    # --- テスト1：べき等性がない処理の検証 ---
    reset_file()
    non_idempotent_write() # 1回目
    non_idempotent_write() # 2回目（ネットワークエラーなどで再実行した想定）
    non_idempotent_write() # 3回目
    show_file_content()    # 重複して書き込まれていることを確認

    # --- テスト2：べき等性がある処理の検証 ---
    reset_file()
    idempotent_write()     # 1回目
    idempotent_write()     # 2回目（再実行しても安全）
    idempotent_write()     # 3回目
    show_file_content()    # 1行だけ正しく書き込まれていることを確認
    
    # テスト終了後にファイルを削除（掃除）
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)










# ITオートメーションにおける「べき等性（Idempotency）」の理解

このリポジトリは、ITオートメーションや構成管理において最も重要な概念の一つである**「べき等性（Idempotency）」**を理解するためのPythonサンプルコードです。

## べき等性（べきとうせい）とは？
「ある操作を1回行っても、複数回連続で行っても、最終的なシステムの状態が全く同じになる性質」のことです。
自動化スクリプトを実行する際、途中でエラーが起きて再実行した場合でも、システムを破壊したり設定を二重に書き込んだりしない安全なプログラムを作るための大前提となります。

- **❌ べき等性がない操作（手順の指示）：** 「ファイルにテキストを追記する」 -> 実行するたびにテキストが増え続ける。
- **⭕️ べき等性がある操作（状態の定義）：** 「ファイルにテキストが無ければ追記する」 -> 何度実行しても理想の状態が維持される。

## スクリプトの概要
`idempotency_demo.py` は、設定ファイル（`sample_config.txt`）に対して、設定値（`Timeout=30`）を書き込むシミュレーションを行います。

1. **`non_idempotent_write()`**: 状態を確認せず、ただ追記するだけの危険な関数。
2. **`idempotent_write()`**: 現在の状態を確認し、必要な場合のみ書き込む安全な関数。

実行結果の違いを通じて、安全な自動化スクリプトの書き方を学ぶことができます。
