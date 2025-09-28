# Image Toolkit

画像処理アプリケーション用の汎用GUIライブラリ。CustomTkinterベースでモダンUI・拡張性・クロスプラットフォーム対応。

## 特徴
- モダンUI（CustomTkinter）
- スケーラブルなレイアウト
- プラグインシステム
- タブ/ツールバー等の複数レイアウト
- 設定管理（JSON）
- 進捗・ロギング
- フォント/スタイルカスタマイズ
- Windows/macOS/Linux対応
- 主要外部ライブラリ統合

## インストール
```sh
pip install -r requirements.txt
```

## 依存関係
- customtkinter>=5.2.0
- opencv-python>=4.7.0
- pyzbar>=0.1.8
- pandas>=2.0.0
- Pillow>=9.0.0
- numpy>=1.21.0
- setuptools>=60.0.0

## 使い方
```python
from image_toolkit import BasicGuiApp, ExtendedGuiApp, ImageProcessorApp
from image_toolkit.widgets.scalable_widgets import ScalableLabel, StyledButton
from image_toolkit.core.font_manager import FontManager
from image_toolkit.core.style_manager import StyleManager
from image_toolkit.layouts.tab_mode import TabLayout
```

## プロジェクト構成
```
image_toolkit/
├── main.py
├── apps/
├── core/
├── widgets/
├── layouts/
├── requirements.txt
├── setup.py
└── README.md
```

## ライセンス
MIT License

## 詳細ドキュメント

本ライブラリの設計・開発・運用・拡張方法については、以下のドキュメントをご参照ください。

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) — ライブラリ全体の設計思想・構造・設計方針
- [BUILD_PYINSTALLER.md](docs/BUILD_PYINSTALLER.md) — PyInstallerによる配布・ビルド手順
- [DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) — 開発者向けガイド・拡張方法・コーディング規約
- [LAUNCHER_GUIDE.md](docs/LAUNCHER_GUIDE.md) — ランチャー・起動方法・コマンド解説
- [NAMING_CONVENTIONS.md](docs/NAMING_CONVENTIONS.md) — ファイル・クラス・関数の命名規則
- [NEW_PROJECT_GUIDE.md](docs/NEW_PROJECT_GUIDE.md) — 新規プロジェクト作成・導入手順

各ドキュメントは、image_toolkitの利用・拡張・運用・開発に役立つ情報を体系的にまとめています。目的に応じてご活用ください。
