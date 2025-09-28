#!/usr/bin/env python3
"""
プロジェクトルート起動ファイル

【機能仕様】
■ 目的: プロジェクトルートから簡単にアプリケーションを起動
■ アーキテクチャ: ルート起動ファイル（便利なエントリーポイント）
■ 依存関係: launchers/start_runner.py を使用
■ 機能:
  - シンプルなコマンドライン起動
  - 引数なしの場合は基本アプリを起動
  - 引数ありの場合は start_runner.py に委任
■ 使用方法: 
  - python run.py          # 基本アプリ起動
  - python run.py extended # 拡張アプリ起動
  - python run.py --help   # ヘルプ表示
■ 対象ユーザー: プロジェクトルートからの簡単起動を好むユーザー
"""
import sys
import os

# プロジェクトルートをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """メイン関数"""
    if len(sys.argv) == 1:
        # 引数なし = 基本アプリ起動
        from launchers.start_basic import main as start_basic
        start_basic()
    else:
        # 引数あり = ランナーに委任
        from launchers.start_runner import main as start_runner
        start_runner()

if __name__ == "__main__":
    main()
