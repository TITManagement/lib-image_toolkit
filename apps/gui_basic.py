"""
基本的なGUIアプリケーションクラス

【機能仕様】
■ 目的: シンプルな画像処理GUIアプリケーションの実装
■ アーキテクチャ: クラス側（アプリケーション実装）
■ 継承関係: customtkinter.CTk を継承
■ 外部依存: gui_framework ライブラリを使用
  - FontManager: フォント管理
  - StyleManager: スタイル管理  
  - ImageUtils: 画像ファイル操作
  - ScalableLabel: スケーラブルラベル
  - StyledButton: スタイル付きボタン
  - TabLayout: タブレイアウト
■ 主要機能:
  - 基本的なGUIレイアウト構築（タイトル、ボタン、タブ）
  - 画像ファイル読み込み機能
  - シンプルな処理実行機能（拡張可能）
  - ウィンドウサイズ: 1000x700px
■ UI構成:
  - タイトルラベル: "画像処理アプリ"
  - タブレイアウト: 機能拡張用
  - 画像読み込みボタン: ファイルダイアログ表示
  - 処理開始ボタン: サンプル処理実行
■ 対象ユーザー: シンプルな操作のみ必要なエンドユーザー
■ 拡張性: プラグインシステムなし（軽量設計）
"""
import customtkinter as ctk
from image_toolkit.core.font_manager import FontManager
from image_toolkit.core.style_manager import StyleManager
from image_toolkit.core.image_utils import ImageUtils
from image_toolkit.widgets.scalable_widgets import ScalableLabel, StyledButton
from image_toolkit.layouts.tab_mode import TabLayout

class BasicGuiApp(ctk.CTk):
    """基本的なGUIアプリケーション"""
    
    def __init__(self):
        super().__init__()
        self.geometry("1000x700")
        self.title("画像処理 GUI テンプレート")

        self.font_mgr = FontManager()
        self.style_mgr = StyleManager()

        self.setup_ui()
    
    def setup_ui(self):
        """UIの設定"""
        # タイトルラベル
        self.label = ScalableLabel(
            self, 
            text="画像処理アプリ", 
            font_mgr=self.font_mgr, 
            style_mgr=self.style_mgr
        )
        self.label.pack(pady=10)

        # タブレイアウト
        self.layout = TabLayout(self, font_mgr=self.font_mgr, style_mgr=self.style_mgr)
        self.layout.pack(expand=True, fill="both")

        # 画像読み込みボタン
        self.btn_load = StyledButton(
            self, 
            text="画像を読み込む", 
            command=self.load_image,
            font_mgr=self.font_mgr, 
            style_mgr=self.style_mgr
        )
        self.btn_load.pack(pady=5)

        # 処理開始ボタン
        self.btn_process = StyledButton(
            self, 
            text="処理開始", 
            command=lambda: print("実行！"),
            font_mgr=self.font_mgr, 
            style_mgr=self.style_mgr
        )
        self.btn_process.pack(pady=5)

    def load_image(self):
        """画像を読み込む"""
        path = ImageUtils.open_image_file()
        if path:
            print(f"画像読み込み: {path}")
        else:
            print("画像読み込みキャンセル")
