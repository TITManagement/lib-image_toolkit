# 新規ImageEditorプロジェクト作成ガイド

## 🚀 新規プロジェクト作成手順

このガイドでは、現在のimage_gui_templateライブラリを使用して、新しいImageEditorプロジェクトを作成する手順を説明します。

## 📁 ディレクトリ構造

### 1. ライブラリディレクトリの準備

```bash
# ライブラリディレクトリの作成
mkdir -p /Users/tinoue/Development.local/lib

# 現在のプロジェクトをライブラリとしてコピー
cp -r /Users/tinoue/Development.local/image_gui_template /Users/tinoue/Development.local/lib/

# ライブラリとしてインストール
cd /Users/tinoue/Development.local/lib/image_gui_template
pip install -e .
```

### 2. 新規プロジェクトディレクトリの作成

```bash
# プロジェクトディレクトリの作成
mkdir -p /Users/tinoue/Development.local/ImageEditor

# プロジェクト内構造の作成
cd /Users/tinoue/Development.local/ImageEditor
mkdir -p src/editor src/ui src/utils assets config tests
```

## 📝 必要ファイルのテンプレート

### 1. requirements.txt

```
# ベースライブラリ（ローカルインストール推奨）
-e /Users/tinoue/Development.local/lib/image_gui_template

# 追加依存関係
customtkinter>=5.0.0
opencv-python>=4.7.0
Pillow>=9.0.0
numpy>=1.21.0
```

### 2. src/main.py（メインアプリケーション）

```python
#!/usr/bin/env python3
"""
ImageEditor - 高度な画像編集アプリケーション

image_gui_templateライブラリを使用した新規プロジェクト
"""

import sys
from pathlib import Path

# ライブラリからインポート
try:
    from apps.gui_image_processor import ImageProcessorApp
    import customtkinter as ctk
except ImportError as e:
    print(f"❌ ライブラリのインポートエラー: {e}")
    print("💡 image_gui_templateライブラリがインストールされていることを確認してください")
    print("📦 インストール方法: pip install -e /Users/tinoue/Development.local/lib/image_gui_template")
    sys.exit(1)

class ImageEditor(ImageProcessorApp):
    \"\"\"
    ImageProcessorAppを継承した独自の画像編集アプリケーション
    \"\"\"
    
    def __init__(self):
        super().__init__()
        self.title("ImageEditor - Professional Image Editor")
        self.setup_custom_features()
    
    def setup_custom_features(self):
        \"\"\"独自機能の追加\"\"\"
        # ここに独自の機能を追加
        pass

def main():
    \"\"\"メイン実行関数\"\"\"
    print("🎨 ImageEditor を起動中...")
    
    try:
        # CustomTkinter設定
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        # アプリケーション起動
        app = ImageEditor()
        print("✅ ImageEditor が起動しました")
        app.mainloop()
        
    except Exception as e:
        print(f"❌ アプリケーションの起動に失敗しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 3. setup.py（パッケージ設定）

```python
from setuptools import setup, find_packages

setup(
    name="imageeditor",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "customtkinter>=5.0.0",
        "opencv-python>=4.7.0",
        "Pillow>=9.0.0",
        "numpy>=1.21.0",
    ],
    dependency_links=[
        "file:///Users/tinoue/Development.local/lib/image_gui_template#egg=image_gui_app"
    ],
    entry_points={
        "console_scripts": [
            "imageeditor=src.main:main",
        ]
    },
    author="Your Name",
    description="Professional Image Editor using image_gui_template library",
    python_requires=">=3.8",
)
```

## 🔧 実装手順

### Step 1: 基本セットアップ

```bash
# 1. ディレクトリ移動
cd /Users/tinoue/Development.local/ImageEditor

# 2. Python仮想環境作成
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# 3. ライブラリインストール
pip install -e /Users/tinoue/Development.local/lib/image_gui_template

# 4. 依存関係インストール
pip install -r requirements.txt
```

### Step 2: 基本アプリケーション作成

上記のテンプレートを使用して基本ファイルを作成

### Step 3: アプリケーション起動テスト

```bash
python src/main.py
```

### Step 4: 独自機能の追加

`src/editor/`ディレクトリに独自の画像編集機能を追加

## 📚 ライブラリ活用例

### 基本的な使用方法

```python
# ライブラリからコンポーネントをインポート
from apps.gui_image_processor import ImageProcessorApp
from apps.gui_basic import BasicGuiApp
from apps.gui_extended import ExtendedGuiApp

# 継承して独自アプリケーションを作成
class MyImageEditor(ImageProcessorApp):
    def __init__(self):
        super().__init__()
        # 独自の初期化処理
        
    def setup_custom_ui(self):
        # 独自UIの追加
        pass
```

### 高度な使用方法

```python
# 特定の機能のみを利用
from launchers.start_image_processor import main as start_image_processor

# カスタムランチャーの作成
def custom_launcher():
    start_image_processor()
```

## 🎯 開発のメリット

1. **既存ライブラリの活用**: 画像処理機能をすぐに利用可能
2. **モジュラー設計**: 必要な機能のみを選択的に使用
3. **拡張性**: 独自機能を簡単に追加可能
4. **保守性**: ライブラリの更新を簡単に取り込み可能

## 🔄 ライブラリ更新時の対応

```bash
# ライブラリ更新
cd /Users/tinoue/Development.local/lib/image_gui_template
git pull origin main
pip install -e . --upgrade

# プロジェクトでの確認
cd /Users/tinoue/Development.local/ImageEditor
python src/main.py
```

このガイドに従って、新規プロジェクトを作成してください。
