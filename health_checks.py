#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
import psutil
import sys

def check_disk_usage(disk):
    """
    指定されたディスクの空き容量をチェックする関数
    空き容量が20%以上あればTrue、20%未満ならFalseを返す
    """
    du = shutil.disk_usage(disk)
    # 空き容量の割合（%）を計算
    free_percentage = (du.free / du.total) * 100
    return free_percentage > 20

def check_cpu_usage():
    """
    CPUの使用率をチェックする関数
    1秒間の平均使用率が75%未満ならTrue、75%以上ならFalseを返す
    """
    # 1秒間サンプリングしてCPU使用率を取得
    usage_percentage = psutil.cpu_percent(1)
    return usage_percentage < 75

def main():
    """
    メインの実行処理
    すべてのチェックを通過した場合は 'Everything ok' を出力。
    異常を検知した場合は、対応するエラーメッセージを出力して異常終了する。
    """
    # フラグの初期化
    has_error = False

    # 1. ディスク容量のチェック（ルートディレクトリ '/' を対象）
    if not check_disk_usage("/"):
        print("[ERROR] ディスクの空き容量が20%未満です！", file=sys.stderr)
        has_error = True

    # 2. CPU使用率のチェック
    if not check_cpu_usage():
        print("[ERROR] CPU使用率が75%を超えています！", file=sys.stderr)
        has_error = True

    # 判定結果の出力制御
    if has_error:
        # 異常がある場合はステータスコード1で終了
        sys.exit(1)
    else:
        # すべて正常な場合
        print("Everything ok")
        sys.exit(0)

if __name__ == "__main__":
    main()


# Health Checks System

このプロジェクトは、サーバーやローカルPCのシステム健全性（ディスク空き容量、CPU使用率）を自動的に監視するためのPythonスクリプトです。

## 機能概要
- **ディスク監視**: ルートディレクトリの空き容量が20%以上あるか確認します。
- **CPU監視**: CPUの負荷が75%未満であるか確認します。
- 全てのチェックを通過した場合は `Everything ok` と出力され、異常を検知した場合は標準エラー出力にエラーメッセージが表示されます。

## 必要要件
システム情報を取得するため、サードパーティ製ライブラリの `psutil` を使用しています。
```bash
pip install psutil




python3 health_checks.py

Update README to use the new name of the script

Also add more information about how this works.
Closes #1

