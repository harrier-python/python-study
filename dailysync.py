#!/usr/bin/env python3
import os
import subprocess
import multiprocessing

def sync_data(folder):
    """
    rsyncコマンドを使用して、指定されたディレクトリをバックアップ先に同期する関数
    
    Parameters:
    folder (str): バックアップ元となる個別のディレクトリの絶対パス
    """
    src = folder
    dest = "/data/prod_backup/"
    
    # subprocess.callを使用してOSのrsyncコマンドを実行
    # オプションの説明:
    # -a (archive): パーミッションやタイムスタンプを保持したまま同期
    # -r (recursive): ディレクトリ内を再帰的に（深い階層まで）同期
    # -q (quiet): 実行中の標準出力を抑制（バックグラウンド処理に適している）
    subprocess.call(["rsync", "-arq", src, dest])

if __name__ == "__main__":
    # 1. バックアップ元の親ディレクトリを指定
    src_dir = "/data/prod/"

    # 2. 同期対象となるディレクトリのリストを作成
    folders = []
    
    # os.walk()を使用してディレクトリツリーを探索
    # root: 現在のディレクトリパス, dirs: サブディレクトリのリスト, files: ファイルのリスト
    for root, dirs, files in os.walk(src_dir):
        for directory in dirs:
            # os.path.joinで絶対パスを生成し、リストに追加
            folders.append(os.path.join(root, directory))
        # トップレベルのディレクトリ（プロジェクトごとのフォルダ）のみを取得するため、
        # 深い階層へ進む前にbreakでループを抜ける
        break 

    # 3. サーバーのCPUコア数を取得
    # ハードウェアの性能に合わせて最適な並列数を決定する
    core_count = multiprocessing.cpu_count()

    # 4. マルチプロセスのプールを作成
    # 取得したCPUコアの数だけ、タスクを処理できるワーカーを準備
    pool = multiprocessing.Pool(core_count)

    # 5. 並列処理の実行
    # pool.map()により、foldersリスト内の各ディレクトリパスを、
    # 順番にsync_data関数の引数として渡し、複数のCPUコアで同時に実行する
    pool.map(sync_data, folders)

    # 6. リソースの解放
    # プールへの新しいタスクの追加を終了し、すべての処理が完了するのを待機
    pool.close()
    pool.join()

# Daily Backup Sync Optimizer (Python Multiprocessing)

## 概要
大容量のメディアデータを効率的にバックアップするため、Pythonの `multiprocessing` モジュールと `rsync` を組み合わせて開発した自動化スクリプトです。

## 解決した課題
従来、サーバーの1つのCPUコアのみを使用して直列で行っていたバックアップ処理は、データ量の増加に伴い完了までに20時間以上を要し、ボトルネック（CPUバウンド）となっていました。
本スクリプトでは、独立した各プロジェクトフォルダの同期タスクを、アイドル状態の複数CPUコアへ並列に割り当てることで、バックアップの実行時間を大幅に短縮しています。

## 使用技術とモジュール
* **Python 3**
* `multiprocessing`: CPUコア数を取得し、Poolクラスの `map` メソッドを用いて並列処理を実装。
* `subprocess`: Pythonスクリプト内からOSコマンドである `rsync` を呼び出し。
* `os`: `os.walk` メソッドによるディレクトリツリーのトラバースとパス操作。
* `rsync` (Linux Command): 差分転送アルゴリズムを使用し、ネットワークとディスクI/Oの負荷を最小限に抑えた高速なデータ同期。

## スクリプトの動作フロー
1.  `os.walk()` を使用して、バックアップ元 (`/data/prod/`) 直下のプロジェクトディレクトリ一覧を取得。
2.  `multiprocessing.cpu_count()` でシステムの利用可能なCPUコア数を算出。
3.  `Pool` クラスを使用してワーカープロセスを生成。
4.  各プロジェクトディレクトリをバックアップ先 (`/data/prod_backup/`) へ同期する `rsync -arq` コマンドを並列で実行。
