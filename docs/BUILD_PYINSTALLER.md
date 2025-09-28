# PyInstaller Build Instructions (image_toolkit)

## 基本アプリケーション:
    pyinstaller launchers/start_basic.py --noconfirm --onefile --windowed --name image-toolkit-basic

## 拡張アプリケーション:
    pyinstaller launchers/start_extended.py --noconfirm --onefile --windowed --name image-toolkit-extended

## 画像処理アプリケーション:
    pyinstaller launchers/start_image_processor.py --noconfirm --onefile --windowed --name image-toolkit-processor

- --onefile: 単一ファイル実行形式
- --windowed: GUI用（コンソール非表示）
- --icon=icon.ico: アイコン指定（任意）

出力は /dist/ 以下に生成されます。

## 注意
- 必要な依存パッケージは requirements.txt で事前にインストールしてください。
- 実行環境に合わせてPythonバージョン・パスを調整してください。