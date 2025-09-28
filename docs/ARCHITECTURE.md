# アーキテクチャ設計ガイド

## 概要
このドキュメントでは、image_toolkitプロジェクトのアーキテクチャ設計思想と、フォルダ構成の詳細な設計理念を説明します。

## アーキテクチャ原則

### 1. 関心の分離（Separation of Concerns）
各ディレクトリは明確な責任を持ち、他の関心事と混合しない設計。

```
launchers/  → 起動の責任
apps/       → アプリケーション実装の責任
core/       → 基本機能（設定・フォント・スタイル・画像処理）の責任
widgets/    → カスタムウィジェットの責任
layouts/    → レイアウトシステムの責任
plugins/    → 機能拡張の責任
docs/       → ドキュメンテーションの責任
```

### 2. 単一責任原則（Single Responsibility Principle）
各ファイルは単一の明確な責任を持つ。

```python
# 良い例
apps/gui_basic.py      # 基本GUIアプリのみ
core/font_manager.py   # フォント管理のみ

# 悪い例
main_and_config.py     # 複数の責任が混在
```

### 3. 依存性の逆転（Dependency Inversion）
上位レベルのモジュールが下位レベルのモジュールに依存する設計。

```
launchers/（高レベル）
    ↓ import
apps/（中レベル）
    ↓ import
core/widgets/layouts（低レベル・外部依存）
```

## ディレクトリ設計詳細

### launchers/ - 起動層
**役割**: アプリケーションのエントリーポイント
**設計原則**:
- 軽量性: 最小限のロジックのみ
- 単純性: 複雑な処理は含まない
- 明確性: どのアプリを起動するか明示

**ファイル構成例**:
```python
launchers/
├── start_basic.py     # 基本アプリ起動
├── start_extended.py  # 拡張アプリ起動
└── start_runner.py    # 選択型ランナー
```

**典型的な内容例**:
```python
# start_basic.py の例
from apps.gui_basic import BasicGuiApp

def main():
    """基本アプリケーションを起動"""
    app = BasicGuiApp()
    app.mainloop()

if __name__ == "__main__":
    main()
```

### apps/ - アプリケーション層

**役割**: ビジネスロジックとUI実装

**設計原則**:
- 凝集性: 関連する機能をまとめる
- 再利用性: 他の起動方法でも使用可能
- テスト可能性: 単体テストが容易

**ファイル構成**:
```python
apps/
├── gui_basic.py       # BasicGuiApp クラス
└── gui_extended.py    # ExtendedGuiApp クラス
```

**典型的な内容**:
```python
# gui_basic.py の例
import customtkinter as ctk
from gui_framework.core import FontManager, StyleManager

class BasicGuiApp(ctk.CTk):
    """基本的なGUIアプリケーション"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """UI構築ロジック"""
        pass
```

### core/ - 基本機能層

**役割**: 設定・フォント・スタイル・画像処理などの基本機能

**設計原則**:
- 再利用性: 他のモジュールから再利用可能
- 抽象化: 具体的な実装に依存しない
- テスト容易性: 単体テストが容易

**ファイル構成**:
```python
core/
├── __init__.py
├── config.py          # 設定管理
├── font_manager.py    # フォント管理
├── style_manager.py   # スタイル管理
└── image_processor.py # 画像処理
```

**典型的な内容**:
```python
# config.py の例
class Config:
    """アプリケーション設定"""
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700
    THEME = "dark"
```

### widgets/ - ウィジェット層

**役割**: カスタムウィジェットの定義

**設計原則**:
- 再利用性: 他のアプリケーションでも再利用可能
- 一貫性: アプリ全体で一貫した外観・動作
- 拡張性: 新しいウィジェットの追加が容易

**ファイル構成**:
```python
widgets/
├── __init__.py
├── custom_button.py    # カスタムボタン
└── custom_entry.py     # カスタムエントリー
```

**典型的な内容**:
```python
# custom_button.py の例
import customtkinter as ctk

class CustomButton(ctk.CTkButton):
    """カスタムデザインのボタン"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(fg_color="blue", text_color="white")
```

### layouts/ - レイアウト層

**役割**: アプリケーションのレイアウト管理

**設計原則**:
- 柔軟性: 異なる画面サイズや解像度に対応
- 再利用性: 他のアプリケーションでも再利用可能
- 明確性: レイアウトの意図が明確

**ファイル構成**:
```python
layouts/
├── __init__.py
├── grid_layout.py      # グリッドレイアウト
└── form_layout.py      # フォームレイアウト
```

**典型的な内容**:
```python
# grid_layout.py の例
from tkinter import Grid

class GridLayout:
    """グリッドレイアウト管理"""
    def __init__(self, parent):
        self.parent = parent
        self.grid = Grid()
```

### plugins/ - 拡張層

**役割**: 機能の動的拡張

**設計原則**:
- プラグアビリティ: 動的な機能追加
- 独立性: 他のプラグインに依存しない
- 標準化: 共通インターフェース

**ファイル構成**:
```python
plugins/
├── __init__.py
├── plugin_image_analysis.py   # 画像分析機能
└── plugin_sample_filter.py    # フィルター機能
```

**プラグインインターフェース**:
```python
from gui_framework.plugins import PluginBase

class MyPlugin(PluginBase):
    @property
    def name(self): return "プラグイン名"
    
    def initialize(self, app): pass
    def create_ui(self, parent): pass
```

### docs/ - ドキュメント層

**役割**: プロジェクト情報とガイド

**設計原則**:
- 完全性: 必要な情報を網羅
- 最新性: コードと同期した内容
- アクセス容易性: 必要な時に簡単に参照可能

**ファイル構成**:
```
docs/
├── README.md                 # プロジェクト概要
├── BUILD_PYINSTALLER.md      # ビルド手順
├── NAMING_CONVENTIONS.md     # 命名規則
└── ARCHITECTURE.md           # このファイル
```

## 外部依存関係の設計

### gui_framework ライブラリとの連携

**設計原則**:
- 抽象化: 具体的な実装に依存しない
- 安定性: ライブラリ更新に耐える設計
- テスト容易性: モック化が可能

**依存関係図**:
```
image_gui_template
├── launchers/    → apps/ に依存
├── apps/         → gui_framework/ に依存
├── plugins/      → gui_framework/ に依存
└── config/       → 依存なし（設定のみ）
```

## スケーラビリティ設計

### 水平拡張（新機能追加）

**起動方式の追加**:
```python
# 新しい起動方式
launchers/start_debug.py      # デバッグモード
launchers/start_kiosk.py      # キオスクモード
```

**アプリケーション種類の追加**:
```python
# 新しいアプリケーション
apps/gui_minimal.py          # 最小限版
apps/gui_enterprise.py      # エンタープライズ版
```

**プラグインの追加**:
```python
# 新しいプラグイン
plugins/plugin_export.py     # エクスポート機能
plugins/plugin_batch.py      # バッチ処理機能
```

### 垂直拡張（機能深化）

**設定の階層化**:
```python
config/
├── config_app.json          # 基本設定
├── config_advanced.json     # 高度な設定
└── config_user.json         # ユーザー固有設定
```

## パフォーマンス設計

### 遅延読み込み（Lazy Loading）

```python
# apps/gui_extended.py
class ExtendedGuiApp:
    def __init__(self):
        # 初期化時は軽量に
        self.plugins = None
        
    def load_plugins(self):
        # 必要時に読み込み
        if self.plugins is None:
            self.plugins = self._discover_plugins()
```

### メモリ効率

```python
# プラグインの動的読み込み
def load_plugin_on_demand(plugin_name):
    """必要時にプラグインを読み込み"""
    module = importlib.import_module(f"plugins.{plugin_name}")
    return module
```

## エラー処理設計

### 階層的エラー処理

```python
launchers/     # エラー表示・ログ出力
    ↓
apps/          # ビジネスロジックエラー処理
    ↓  
gui_framework/ # 低レベルエラー処理
```

### 回復可能性

```python
# 起動時の回復処理
def safe_start():
    try:
        return start_extended()
    except ImportError:
        # 拡張版が使えない場合は基本版で起動
        return start_basic()
```

## テスト設計

### テスタビリティ

```python
# apps/ - 単体テスト容易
def test_basic_gui_creation():
    app = BasicGuiApp()
    assert app.title == "Expected Title"

# launchers/ - 統合テスト
def test_application_startup():
    # アプリケーション全体の起動テスト
    pass
```

### モック化対応

```python
# 外部依存のモック化
@patch('gui_framework.core.FontManager')
def test_with_mock_font_manager(mock_font):
    app = BasicGuiApp()
    # テスト実行
```

## セキュリティ設計

### 設定ファイルの保護

```python
config/
├── config_app.json      # 公開可能な設定
└── config_secret.json   # 機密情報（.gitignore対象）
```

### プラグインの検証

```python
def load_plugin_safely(plugin_path):
    """プラグインの安全な読み込み"""
    # デジタル署名検証
    # サンドボックス実行
    pass
```

## 運用・保守設計

### ログ設計

```python
# 階層的ログ
launchers/     # 起動・終了ログ
apps/          # アプリケーションログ  
plugins/       # プラグインログ
```

### 設定の段階的移行

```python
def migrate_config(old_config, new_version):
    """設定ファイルのバージョン移行"""
    # 後方互換性を保ちながら移行
    pass
```

## 将来の拡張可能性

### マイクロサービス化対応

```python
# 将来のマイクロサービス分割点
launchers/     # API Gateway
apps/          # Application Service  
plugins/       # Plugin Service
```

### クラウド対応

```python
config/
├── config_local.json    # ローカル環境
├── config_cloud.json   # クラウド環境
└── config_hybrid.json  # ハイブリッド環境
```

## まとめ

この アーキテクチャ設計は以下の目標を達成します：

1. **保守性**: 明確な責任分離により変更が容易
2. **拡張性**: 新機能追加が既存コードに影響しない  
3. **テスト容易性**: 各層が独立してテスト可能
4. **理解容易性**: 新しい開発者が迅速に理解可能
5. **再利用性**: コンポーネントの再利用が容易

---

**更新日**: 2025年8月18日  
**バージョン**: 1.0.0
