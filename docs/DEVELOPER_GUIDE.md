# 開発者クイックリファレンス（image_toolkit）

## 新しいファイル追加時のチェックリスト

### 1. ファイル種別と配置場所
| 作りたいもの | 配置場所 | 命名規則 | 例 |
|---|---|---|---|
| 🚀 起動スクリプト | `launchers/` | `start_*.py` | `start_basic.py` |
| 🖥️ GUIアプリ | `apps/` | `gui_*.py` | `gui_minimal.py` |
| ⚙️ 設定ファイル | `core/` | `config_*.*` | `config_themes.json` |
| 🔌 プラグイン | `plugins/` | `plugin_*.py` | `plugin_export.py` |
| 📚 ドキュメント | `docs/` | `*.md` | `API_GUIDE.md` |

### 2. テンプレート例

#### 起動スクリプト (launchers/start_*.py)
```python
"""
新しい起動スクリプトの説明
【機能仕様】
■ 目的: [具体的な目的]
■ アーキテクチャ: 起動側（main呼び出し）
■ 外部ライブラリ: image_toolkit
■ 主機能: [主機能の説明]
■ 対象ユーザー: [対象ユーザー]
"""

from apps.gui_[target] import [TargetApp]

def main():
    """[アプリ名]を起動"""
    app = [TargetApp]()
    app.mainloop()

if __name__ == "__main__":
    main()
```

#### GUIアプリ (apps/gui_*.py)
```python
"""
新しいGUIアプリケーションクラス
【機能仕様】
■ 目的: [アプリの目的]
■ アーキテクチャ: クラス側（アプリケーション実装）
■ 継承関係: customtkinter.CTk を継承
■ 外部依存: image_toolkit
■ 主機能: [主機能のリスト]
■ UI構成: [UI要素の説明]
■ 対象ユーザー: [対象ユーザー]
"""

import customtkinter as ctk
from image_toolkit.core import FontManager, StyleManager
from image_toolkit.widgets import ScalableLabel, StyledButton

class [Name]GuiApp(ctk.CTk):
    """[アプリ名]GUIアプリケーション"""
    
    def __init__(self):
        super().__init__()
        self.geometry("1000x700")
        self.title("[アプリタイトル]")
        
        self.font_mgr = FontManager()
        self.style_mgr = StyleManager()
        
        self.setup_ui()
    
    def setup_ui(self):
        """UIの設定"""
        # UI構築ロジック
        pass
```

#### プラグイン (plugins/plugin_*.py)
```python
"""
新しいプラグイン

【機能仕様】
■ 目的: [プラグインの目的]
■ アーキテクチャ: プラグイン（拡張機能）
■ 継承関係: PluginBase を継承
■ 外部依存: gui_framework ライブラリを使用
■ 主要機能: [主要機能のリスト]
■ 対象ユーザー: [対象ユーザー]
"""

import customtkinter as ctk
from gui_framework.plugins import PluginBase
from gui_framework.widgets import ScalableLabel, StyledButton

class [Name]Plugin(PluginBase):
    """[プラグイン名]プラグイン"""
    
    @property
    def name(self):
        return "[プラグイン表示名]"
    
    @property
    def version(self):
        return "1.0.0"
    
    @property
    def description(self):
        return "[プラグインの説明]"
    
    def initialize(self, app):
        """プラグインの初期化"""
        self.app = app
        print(f"{self.name} プラグインが初期化されました")
    
    def create_ui(self, parent):
        """UIコンポーネントを作成"""
        frame = ctk.CTkFrame(parent)
        
        # UI構築
        
        return frame
```

## よく使うコマンド

### 開発・テスト
```bash
# 基本版アプリ起動
python launchers/start_basic.py

# 拡張版アプリ起動  
python launchers/start_extended.py

# 選択型ランナー
python launchers/start_runner.py

# 統合起動（推奨）
python run.py

# 外部ライブラリのテスト
python -c "import gui_framework; print('OK')"
```

### パッケージング
```bash
# 開発モードインストール
pip install -e .

# パッケージ作成
python config/config_package.py sdist bdist_wheel

# PyInstallerビルド
pyinstaller launchers/start_basic.py --noconfirm --onefile --windowed --name imagegui-basic
```

### Git操作
```bash
# 全体の状態確認
git status

# 新しいファイルを追加
git add [新しいファイル]
git commit -m "feat: [機能の説明]"

# GitHubにプッシュ
git push origin main
```

## インポートパターン

### プロジェクト内
```python
# アプリケーションクラス
from apps.gui_basic import BasicGuiApp
from apps.gui_extended import ExtendedGuiApp

# プラグイン
from plugins.plugin_image_analysis import ImageAnalysisPlugin
from plugins.plugin_sample_filter import SampleFilterPlugin

# 設定（JSON読み込み例）
import json
with open('config/config_app.json') as f:
    config = json.load(f)
```

### 外部ライブラリ
```python
# コア機能
from gui_framework.core import FontManager, StyleManager, ImageUtils, ConfigManager

# ウィジェット  
from gui_framework.widgets import ScalableLabel, StyledButton, MessageDialog

# レイアウト
from gui_framework.layouts import TabLayout, ToolbarLayout

# プラグインシステム
from gui_framework.plugins import PluginBase, PluginManager
```

## トラブルシューティング

### よくあるエラー

#### ModuleNotFoundError: No module named 'gui_framework'
```bash
# 解決方法: 外部ライブラリをインストール
pip install git+https://github.com/TITManagement/lib.git
```

#### ImportError: cannot import name 'BasicGuiApp'
```python
# 問題: インポートパスが間違っている
from basic_gui_app import BasicGuiApp  # ❌ 古いパス

# 解決: 新しいディレクトリ構造を使用
from apps.gui_basic import BasicGuiApp  # ✅ 正しいパス
```

#### ファイルが見つからない
```bash
# 確認: 現在のディレクトリ構造
find . -name "*.py" | grep -v .venv | sort

# 確認: 特定のファイル
ls -la launchers/
ls -la apps/
ls -la plugins/
```

### デバッグのヒント

#### 1. インポートエラーの場合
```python
# デバッグ用コード
import sys
print("Python path:", sys.path)
print("Current working directory:", os.getcwd())

# gui_frameworkが見つかるかテスト
try:
    import gui_framework
    print("gui_framework: OK")
except ImportError as e:
    print("gui_framework: NG -", e)
```

#### 2. GUI起動エラーの場合
```python
# 段階的なテスト
import customtkinter as ctk

# 1. 基本的なウィンドウ作成
app = ctk.CTk()
app.geometry("400x300")
app.mainloop()

# 2. フレームワーク機能のテスト
from gui_framework.core import FontManager
font_mgr = FontManager()
print("FontManager created successfully")
```

## パフォーマンス最適化

### 起動速度の改善
```python
# 遅延インポート
def load_heavy_modules():
    """重いモジュールは必要時に読み込み"""
    global heavy_module
    if 'heavy_module' not in globals():
        import heavy_module
    return heavy_module

# プラグインの遅延読み込み
def load_plugins_on_demand():
    """プラグインは使用時に読み込み"""
    # implementation
```

### メモリ使用量の最適化
```python
# 不要なオブジェクトの削除
def cleanup_resources(self):
    """リソースのクリーンアップ"""
    if hasattr(self, 'large_data'):
        del self.large_data
    gc.collect()
```

## ベストプラクティス

### 1. ファイル作成時
- [ ] 適切なディレクトリに配置
- [ ] 命名規則に従った名前  
- [ ] 詳細な機能仕様コメント
- [ ] 適切なインポート文

### 2. コード品質
- [ ] 単一責任原則の遵守
- [ ] 明確な関数・メソッド名
- [ ] エラーハンドリングの実装
- [ ] ドキュメント文字列の記述

### 3. テスト
- [ ] 基本的な動作確認
- [ ] エラーケースの確認  
- [ ] 他の機能との連携確認
- [ ] パフォーマンステスト

### 4. コミット前
- [ ] コードレビュー
- [ ] 不要ファイルの削除
- [ ] Git追跡対象の確認
- [ ] 適切なコミットメッセージ

---

**更新日**: 2025年8月18日  
**バージョン**: 1.0.0  
**対象**: image_gui_template 開発者
