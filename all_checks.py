#!/usr/bin/env python3
# このスクリプトはPython3で実行することを指定するシバン（Shebang）です

import os
import sys

def check_reboot():
    """コンピューターの再起動が保留されているかどうかを確認する関数"""
    # Linux（Ubuntuなど）で再起動が必要な時に作られるファイルの存在をチェックします
    return os.path.exists("/run/reboot-required")

def main():
    # check_reboot関数を呼び出し、True（再起動が必要）であればif文の中を実行します
    if check_reboot():
        print("Pending Reboot.")  # 再起動保留中であることを表示
        sys.exit(1)               # 異常終了（ステータスコード1）としてプログラムを終了

    # 再起動が不要な場合の処理
    print("Everything ok.")       # 全て正常であることを表示
    sys.exit(0)                   # 正常終了（ステータスコード0）としてプログラムを終了

# スクリプトが実行されたときに main() 関数を呼び出します
main()
