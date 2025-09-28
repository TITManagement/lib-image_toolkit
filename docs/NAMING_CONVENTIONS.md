# 命名規則・フォルダ構成ガイド

## 概要

このドキュメントでは、image_gui_templateプロジェクトで採用している命名規則とフォルダ構成のコンセプトを説明します。

## 基本コンセプト

### プロジェクトの性質による命名規則の使い分け

| プロジェクト種別 | 命名方式 | 目的 | 例 |
|---|---|---|---|
| **アプリケーション** | プレフィックス方式 | 開発者体験向上 | `start_basic.py`, `gui_extended.py` |
| **ライブラリ** | 機能的命名 | 互換性・安定性重視 | `config_manager.py`, `font_manager.py` |

## image_gui_template プロジェクト（アプリケーション）

### フォルダ構成

```
image_gui_template/
├── run.py                      # 統合起動スクリプト
├── launchers/                  # 起動スクリプト集約
│   ├── start_basic.py         # 基本アプリ起動
│   ├── start_extended.py      # 拡張アプリ起動
│   └── start_runner.py        # 選択型ランナー
├── apps/                       # アプリケーションクラス集約
│   ├── gui_basic.py           # 基本GUIクラス
│   └── gui_extended.py        # 拡張GUIクラス
├── config/                     # 設定・パッケージ管理
│   ├── config_app.json        # アプリケーション設定
│   └── config_package.py      # パッケージセットアップ
├── docs/                       # ドキュメント集約
│   ├── README.md              # プロジェクト説明
│   ├── BUILD_PYINSTALLER.md   # ビルド手順
│   └── NAMING_CONVENTIONS.md  # このファイル
└── plugins/                    # プラグイン集約
    ├── plugin_image_analysis.py # 画像分析プラグイン
    └── plugin_sample_filter.py  # サンプルフィルター
```

### 命名規則（プレフィックス方式）

#### A. launchers/ ディレクトリ
- **プレフィックス**: `start_`
- **目的**: 起動スクリプトであることを即座に識別
- **例**: 
  - `start_basic.py` - 基本アプリケーション起動
  - `start_extended.py` - 拡張アプリケーション起動
  - `start_runner.py` - 選択型ランナー

#### B. apps/ ディレクトリ
- **プレフィックス**: `gui_`
- **目的**: GUIアプリケーションクラスであることを明示
- **例**:
  - `gui_basic.py` - BasicGuiAppクラス
  - `gui_extended.py` - ExtendedGuiAppクラス

#### C. config/ ディレクトリ
- **プレフィックス**: `config_`
- **目的**: 設定関連ファイルであることを明示
- **例**:
  - `config_app.json` - アプリケーション設定
  - `config_package.py` - パッケージセットアップ設定

#### D. plugins/ ディレクトリ
- **プレフィックス**: `plugin_`
- **目的**: プラグインモジュールであることを明示
- **例**:
  - `plugin_image_analysis.py` - ImageAnalysisPluginクラス
  - `plugin_sample_filter.py` - SampleFilterPluginクラス

#### E. docs/ ディレクトリ
- **命名**: 機能的命名（標準的なドキュメント名）
- **例**:
  - `README.md` - プロジェクト概要
  - `BUILD_PYINSTALLER.md` - ビルド手順
  - `NAMING_CONVENTIONS.md` - 命名規則

### プレフィックス方式の利点

1. **即座の識別**: ファイル名から役割が瞬時に理解できる
2. **効率的な開発**: IDEでのファイル検索・補完が効率的
3. **保守性向上**: 新しい開発者でも迷わずファイルを見つけられる
4. **一貫性**: プロジェクト全体で統一された命名

## gui_framework ライブラリ（外部依存）

### フォルダ構成

```
gui_framework/
├── core/                       # コア機能
│   ├── config_manager.py      # 設定管理
│   ├── font_manager.py        # フォント管理
│   ├── image_utils.py         # 画像ユーティリティ
│   └── style_manager.py       # スタイル管理
├── layouts/                    # レイアウトシステム
│   ├── tab_mode.py            # タブレイアウト
│   └── toolbar_mode.py        # ツールバーレイアウト
├── plugins/                    # プラグインシステム
│   └── plugin_manager.py      # プラグイン管理
├── utils/                      # ユーティリティ
└── widgets/                    # ウィジェット
    ├── dialogs.py             # ダイアログ関連
    └── scalable_widgets.py    # スケーラブルウィジェット
```

### 命名規則（機能的命名）

#### 特徴
- **標準的なPythonライブラリ命名規則**
- **機能を直接表現する名前**
- **他のライブラリとの一貫性**

#### 理由
1. **外部API**: 他のプロジェクトからimportされる
2. **互換性**: ファイル名変更は破壊的変更となる
3. **標準準拠**: Python生態系の慣習に従う
4. **安定性**: ライブラリとして安定したインターフェース提供

## 導入プロセス

### 1. 初期状態（従来の命名）
```
# 従来のファイル名
main.py
extended_app.py
basic_gui_app.py
setup.py
```

### 2. プレフィックス化
```
# プレフィックス追加
start_basic.py      # main.py から
start_extended.py   # extended_app.py から
gui_basic.py        # basic_gui_app.py から
config_package.py   # setup.py から
```

### 3. ディレクトリ整理
```
# ディレクトリ別配置
launchers/start_basic.py
apps/gui_basic.py
config/config_package.py
docs/README.md
```

## 運用ガイドライン

### 新しいファイルを追加する場合

#### A. ファイル種別の判定
1. **起動スクリプト** → `launchers/start_*.py`
2. **GUIクラス** → `apps/gui_*.py`
3. **設定ファイル** → `config/config_*.*`
4. **プラグイン** → `plugins/plugin_*.py`
5. **ドキュメント** → `docs/*.md`

#### B. 命名例
```python
# 新しい起動スクリプト
launchers/start_debug.py       # デバッグモード起動
launchers/start_production.py  # 本番モード起動

# 新しいGUIクラス
apps/gui_minimal.py           # 最小限GUI
apps/gui_enterprise.py       # エンタープライズ版

# 新しい設定ファイル
config/config_database.py    # データベース設定
config/config_themes.json    # テーマ設定

# 新しいプラグイン
plugins/plugin_export.py     # エクスポート機能
plugins/plugin_import.py     # インポート機能
```

### インポート時の注意点

#### プロジェクト内インポート
```python
# ディレクトリ構造を反映
from apps.gui_basic import BasicGuiApp
from launchers.start_runner import main
from plugins.plugin_image_analysis import ImageAnalysisPlugin
```

#### 外部ライブラリインポート
```python
# 標準的なライブラリインポート
from gui_framework.core import FontManager, StyleManager
from gui_framework.widgets import ScalableLabel, StyledButton
```

## 利点とトレードオフ

### 利点
1. **開発効率向上**: ファイルの役割が明確
2. **新人対応**: 直感的な理解が可能
3. **保守性**: 長期的なメンテナンスが容易
4. **拡張性**: 新機能追加時の命名が明確

### トレードオフ
1. **ファイル名の長さ**: プレフィックス分だけ長くなる
2. **学習コスト**: 新しい命名規則の習得が必要
3. **移行コスト**: 既存プロジェクトの変更が必要

## まとめ

この命名規則とフォルダ構成は、**開発者体験の向上**と**長期的な保守性**を目的として設計されています。

- **アプリケーション**: プレフィックス方式で開発効率重視
- **ライブラリ**: 機能的命名で互換性重視

それぞれの性質に適した命名規則を採用することで、最適な開発環境を実現しています。

---

**更新日**: 2025年8月18日  
**バージョン**: 1.0.0
