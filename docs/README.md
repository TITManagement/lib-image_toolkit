# Image GUI Template

画像処理アプリケーション用の汎用GUIテンプレートです。CustomTkinterを使用してモダンなUIを提供し、拡張可能なアーキテクチャを実装しています。

## 特徴

- **モダンなUI**: CustomTkinterを使用したスタイリッシュなインターフェース
- **スケーラブルなレイアウト**: ウィンドウサイズに応じて自動調整される要素
- **プラグインシステム**: 機能を動的に追加できる拡張可能な設計
- **複数レイアウトモード**: タブモード、ツールバーモードなど
- **設定管理**: JSON形式での設定保存・読み込み
- **進捗管理**: 長時間処理用の進捗ダイアログ
- **ロギングシステム**: デバッグとトレーサビリティ
- **カスタマイズ可能**: フォントやスタイルを簡単に変更可能
- **クロスプラットフォーム**: Windows、macOS、Linuxで動作
- **外部ライブラリ統合**: 再利用可能なGUIフレームワークとの連携

## アーキテクチャ

### 外部ライブラリ統合

このプロジェクトは外部の `gui_framework` ライブラリ（https://github.com/TITManagement/lib）を使用してモジュール化されています：

```python
# 外部ライブラリからのインポート
from gui_framework.core import ConfigManager, FontManager, StyleManager, ImageUtils
from gui_framework.plugins import PluginManager
from gui_framework.widgets import ScalableLabel, StyledButton, MessageDialog, TaskRunner
from gui_framework.layouts import TabLayout, ToolbarLayout
from gui_framework.utils import LoggingUtils
```

#### ライブラリ構造:
- **core**: 基本機能（設定、フォント、スタイル、画像処理）
- **widgets**: カスタムウィジェット（ボタン、ラベル、ダイアログ）
- **layouts**: レイアウトシステム（タブ、ツールバー）
- **plugins**: プラグインシステム
- **utils**: ユーティリティ関数（ログ、検証、データ処理）

## インストール

### 必要要件

- Python 3.8以上

### ライブラリのインストール

外部GUIフレームワークライブラリをインストール：

```bash
# GitHubから直接インストール
pip install git+https://github.com/TITManagement/lib.git

# または、ローカルにクローンしてからインストール
git clone https://github.com/TITManagement/lib.git
pip install -e ./lib
```

### 依存関係のインストール

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本アプリケーションの起動

```bash
# 方法1: 直接実行
python launchers/start_basic.py

# 方法2: 統合ランナー使用
python run.py

# 方法3: ランナースクリプト使用
python launchers/start_runner.py basic

# 方法4: インストール後のコマンド
imagegui
```

### 拡張アプリケーションの起動

```bash
# 方法1: 直接実行
python launchers/start_extended.py

# 方法2: ランナースクリプト使用
python launchers/start_runner.py extended

# 方法3: インストール後のコマンド
imagegui-extended
```

### 実行可能ファイルの作成

PyInstallerを使用して実行可能ファイルを作成できます：

```bash
pyinstaller launchers/start_basic.py --noconfirm --onefile --windowed --name imagegui
```

詳細は `docs/BUILD_PYINSTALLER.md` をご覧ください。

## プロジェクト構造

```
image_gui_template/
├── run.py                      # 統合起動スクリプト
├── launchers/                  # アプリケーション起動スクリプト
│   ├── start_basic.py         # 基本アプリケーション起動
│   ├── start_extended.py      # 拡張アプリケーション起動
│   └── start_runner.py        # 選択型ランナー
├── apps/                       # アプリケーションクラス
│   ├── gui_basic.py           # 基本GUIアプリケーションクラス
│   └── gui_extended.py        # 拡張GUIアプリケーションクラス
├── config/                     # 設定・パッケージ管理
│   ├── config_app.json        # アプリケーション設定
│   └── config_package.py      # パッケージセットアップ設定
├── docs/                       # ドキュメント
│   ├── README.md              # プロジェクト説明書
│   └── BUILD_PYINSTALLER.md   # ビルド手順
├── plugins/                    # アプリケーション固有のプラグイン
│   ├── plugin_sample_filter.py    # サンプルフィルタープラグイン
│   └── plugin_image_analysis.py   # 画像分析プラグイン
└── requirements.txt            # Python依存関係
```

### ライブラリの依存関係

アプリケーションは以下の外部ライブラリに依存しています：

1. **gui-framework**: 再利用可能なGUIコンポーネント
   - リポジトリ: https://github.com/TITManagement/lib
   - バージョン: 1.0.0
   - 機能: コア機能、ウィジェット、レイアウト、プラグインシステム

2. **CustomTkinter**: モダンGUIフレームワーク
3. **Pillow**: 画像処理ライブラリ

## 開発ガイド

### 📚 ドキュメント

- **[命名規則・フォルダ構成ガイド](NAMING_CONVENTIONS.md)** - プロジェクトの命名規則とフォルダ構成の詳細
- **[アーキテクチャ設計ガイド](ARCHITECTURE.md)** - システム設計思想とアーキテクチャの詳細
- **[開発者クイックリファレンス](DEVELOPER_GUIDE.md)** - 開発時の実践的なガイド

### 新しいアプリケーションの作成

外部ライブラリを使用して新しいアプリケーションを作成：

```python
import customtkinter as ctk
from gui_framework.core import FontManager, StyleManager
from gui_framework.widgets import ScalableLabel, StyledButton
from gui_framework.layouts import TabLayout

class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("マイアプリ")
        self.geometry("800x600")
        
        # フレームワークコンポーネントの初期化
        self.font_mgr = FontManager()
        self.style_mgr = StyleManager()
        
        # UIの構築
        self.setup_ui()
    
    def setup_ui(self):
        # フレームワークのウィジェットを使用
        label = ScalableLabel(
            self,
            text="Hello Framework!",
            font_mgr=self.font_mgr,
            style_mgr=self.style_mgr
        )
        label.pack(pady=20)
        
        layout = TabLayout(self, font_mgr=self.font_mgr, style_mgr=self.style_mgr)
        layout.pack(expand=True, fill="both")

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
```

### プラグイン開発

プラグインの作成：

1. `PluginBase`クラスを継承
2. 必要なメソッドを実装
3. `plugins/` フォルダに配置

```python
from gui_framework.plugins import PluginBase
import customtkinter as ctk

class MyPlugin(PluginBase):
    @property
    def name(self):
        return "マイプラグイン"
    
    @property
    def version(self):
        return "1.0.0"
    
    @property
    def description(self):
        return "カスタムプラグインの説明"
    
    def initialize(self, app):
        self.app = app
    
    def create_ui(self, parent):
        frame = ctk.CTkFrame(parent)
        # UIコンポーネントを追加
        return frame
```

## カスタマイズ

### 設定の変更

外部ライブラリの `ConfigManager` を使用して設定をカスタマイズできます：

```python
from gui_framework.core import ConfigManager

config = ConfigManager()
config.set("window.width", 1200)
config.set("fonts.base_size", 16)
config.save_config()
```

### フォントの変更

`FontManager` でフォントサイズやスタイルを調整：

```python
from gui_framework.core import FontManager

font_mgr = FontManager(base_size=16)
title_font = font_mgr.get_title_font()
```

### スタイルの変更

`StyleManager` で色やテーマを変更：

```python
from gui_framework.core import StyleManager

style_mgr = StyleManager()
button_style = style_mgr.get_button_style()
```

## 外部ライブラリの開発

このプロジェクトは外部の `gui_framework` ライブラリを直接pipインストールして使用しています。ライブラリの開発や拡張は、https://github.com/TITManagement/lib リポジトリで行われます。

ライブラリの更新がある場合は、以下のコマンドで最新版をインストールできます：

```bash
pip install --upgrade git+https://github.com/TITManagement/lib.git
```

## ライセンス

MIT License

## 貢献

プルリクエストやイシューの報告を歓迎します。

## 関連リポジトリ

- **GUI Framework Library**: https://github.com/TITManagement/lib
- **Image GUI Template**: https://github.com/TITManagement/image_gui_template

## 技術的な詳細

### 使用ライブラリ
- **gui-framework**: カスタムGUIフレームワーク
- **CustomTkinter**: モダンなGUIフレームワーク
- **Pillow**: 画像処理
- **JSON**: 設定管理
- **Threading**: バックグラウンド処理

### 拡張ポイント
1. **プラグインインターフェース**: 新機能の追加
2. **レイアウトシステム**: 新しいレイアウトモード
3. **スタイルシステム**: カスタムテーマ
4. **設定システム**: アプリケーション固有の設定
