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
