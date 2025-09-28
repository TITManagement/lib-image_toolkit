"""
拡張されたGUIアプリケーションクラス

【機能仕様】
■ 目的: 高機能な画像処理GUIアプリケーションの実装
■ アーキテクチャ: クラス側（アプリケーション実装）
■ 継承関係: customtkinter.CTk を継承
■ 外部依存: gui_framework ライブラリを全面的に使用
  - ConfigManager: JSON設定管理
  - PluginManager: プラグインシステム
  - FontManager: フォント管理
  - StyleManager: スタイル管理
  - ImageUtils: 画像ファイル操作
  - ScalableLabel, StyledButton: UIコンポーネント
  - TabLayout, ToolbarLayout: レイアウトシステム
  - MessageDialog, TaskRunner: ダイアログシステム
  - LoggingUtils: ログ管理
■ 主要機能:
  - 設定ファイル（config.json）ベースの初期化
  - 動的プラグインシステム（plugins/ディレクトリから自動読み込み）
  - 複数レイアウトモード（タブモード/ツールバーモード）の切り替え
  - メニューシステム（ファイル、編集、表示、ツール、ヘルプ）
  - 進捗ダイアログ付き長時間処理実行
  - 包括的なログ記録
  - 設定の永続化
■ UI構成:
  - メニューバー: 5つの主要メニュー
  - レイアウト選択: ドロップダウンでモード切り替え
  - 動的コンテンツエリア: 選択されたレイアウトに応じて変化
  - プラグインUI統合: 各プラグインの専用タブ
■ 対象ユーザー: 
  - 高度な画像処理機能が必要な専門ユーザー
  - プラグイン開発者
  - カスタマイズ性を重視するユーザー
■ 拡張性: 完全なプラグインアーキテクチャ
"""
import customtkinter as ctk
from image_toolkit.core.font_manager import FontManager
from image_toolkit.core.style_manager import StyleManager
from image_toolkit.core.image_utils import ImageUtils
from image_toolkit.widgets.scalable_widgets import ScalableLabel, StyledButton
from image_toolkit.layouts.tab_mode import TabLayout
# 以下はダミークラス（本来はplugins, layouts, widgets, utils等で拡張）
class ConfigManager:
    def get(self, key, default=None):
        return default
    def save_config(self):
        pass
class PluginManager:
    def load_all_plugins(self, app):
        pass
    def get_loaded_plugins(self):
        return []
class MessageDialog:
    @staticmethod
    def show_info(*args, **kwargs):
        pass
    @staticmethod
    def show_confirm(*args, **kwargs):
        return True
    @staticmethod
    def show_error(*args, **kwargs):
        pass
class TaskRunner:
    @staticmethod
    def run_with_progress(*args, **kwargs):
        pass
class ToolbarLayout(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def get_content_frame(self):
        return self
class LoggingUtils:
    def info(self, msg):
        print(msg)
    def error(self, msg):
        print(msg)
def sample_long_task(*args, **kwargs):
    import time
    time.sleep(1)
    return "完了"

class ExtendedGuiApp(ctk.CTk):
    """拡張されたGUIアプリケーション"""
    
    def __init__(self):
        super().__init__()
        
        # 設定とマネージャーの初期化
        self.config = ConfigManager()
        self.plugin_manager = PluginManager()
        self.logger = LoggingUtils()
        
        # ウィンドウ設定
        self.setup_window()
        
        # UI要素の初期化
        base_size = self.config.get("fonts.base_size", 14)
        if isinstance(base_size, (int, float)):
            self.font_mgr = FontManager(int(base_size))
        else:
            self.font_mgr = FontManager(14)
        self.style_mgr = StyleManager()
        
        # UI構築
        self.setup_ui()
        
        # プラグイン読み込み
        self.load_plugins()
        
        self.logger.info("拡張GUIアプリケーションが起動しました")
    
    def setup_window(self):
        """ウィンドウの設定"""
        width = self.config.get("window.width", 1000)
        height = self.config.get("window.height", 700)
        if isinstance(width, (int, float)) and isinstance(height, (int, float)):
            self.geometry(f"{int(width)}x{int(height)}")
        else:
            self.geometry("1000x700")
        self.title("拡張GUI テンプレート - サンプル")
        
        # テーマ設定
        theme = self.config.get("window.theme", "blue")
        appearance = self.config.get("window.appearance_mode", "System")
        if isinstance(theme, str):
            ctk.set_default_color_theme(theme)
        if isinstance(appearance, str):
            ctk.set_appearance_mode(appearance)
    
    def setup_ui(self):
        """UIの設定"""
        # メニューバー（簡易版）
        self.menu_frame = ctk.CTkFrame(self, height=40)
        self.menu_frame.pack(fill="x", padx=5, pady=5)
        self.menu_frame.pack_propagate(False)
        
        # メニューボタン
        menu_buttons = [
            ("ファイル", self.show_file_menu),
            ("編集", self.show_edit_menu),
            ("表示", self.show_view_menu),
            ("ツール", self.show_tools_menu),
            ("ヘルプ", self.show_help_menu),
        ]
        
        for text, command in menu_buttons:
            btn = StyledButton(
                self.menu_frame,
                text=text,
                command=command,
                font_mgr=self.font_mgr,
                style_mgr=self.style_mgr,
                width=80
            )
            btn.pack(side="left", padx=2, pady=5)
        
        # レイアウト選択
        layout_frame = ctk.CTkFrame(self.menu_frame, fg_color="transparent")
        layout_frame.pack(side="right", padx=10)
        
        layout_label = ScalableLabel(
            layout_frame,
            text="レイアウト:",
            font_mgr=self.font_mgr,
            style_mgr=self.style_mgr
        )
        layout_label.pack(side="left", padx=5)
        
        self.layout_selector = ctk.CTkOptionMenu(
            layout_frame,
            values=["タブモード", "ツールバーモード"],
            command=self.change_layout
        )
        self.layout_selector.pack(side="left")
        
        # メインコンテンツエリア
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        # デフォルトレイアウトを設定
        self.current_layout = None
        self.change_layout("タブモード")
    
    def change_layout(self, layout_name):
        """レイアウトを変更"""
        if self.current_layout:
            self.current_layout.destroy()
        
        if layout_name == "タブモード":
            self.current_layout = TabLayout(
                self.main_frame,
                font_mgr=self.font_mgr,
                style_mgr=self.style_mgr
            )
            self.setup_tab_content()
        elif layout_name == "ツールバーモード":
            self.current_layout = ToolbarLayout(
                self.main_frame,
                font_mgr=self.font_mgr,
                style_mgr=self.style_mgr
            )
            self.setup_toolbar_content()
        
        if self.current_layout:
            self.current_layout.pack(expand=True, fill="both")
            self.logger.info(f"レイアウトを{layout_name}に変更しました")
    
    def setup_tab_content(self):
        """タブレイアウトのコンテンツを設定"""
        if not isinstance(self.current_layout, TabLayout):
            return
            
        # プラグインのUIを各タブに追加
        for plugin in self.plugin_manager.get_loaded_plugins():
            if hasattr(plugin, 'create_ui'):
                tab_parent = None
                if plugin.name == "サンプルフィルター":
                    tab_parent = self.current_layout.tabview.tab("フィルタ")
                elif plugin.name == "画像分析":
                    tab_parent = self.current_layout.tabview.tab("解析")
                
                if tab_parent:
                    plugin_ui = plugin.create_ui(tab_parent)
                    if plugin_ui:
                        plugin_ui.pack(expand=True, fill="both", padx=10, pady=10)
    
    def setup_toolbar_content(self):
        """ツールバーレイアウトのコンテンツを設定"""
        if not isinstance(self.current_layout, ToolbarLayout):
            return
            
        content_frame = self.current_layout.get_content_frame()
        
        # サンプルコンテンツ
        welcome_label = ScalableLabel(
            content_frame,
            text="ツールバーモードのサンプルコンテンツ",
            font_mgr=self.font_mgr,
            style_mgr=self.style_mgr
        )
        welcome_label.pack(pady=20)
        
        # 機能ボタン
        demo_btn = StyledButton(
            content_frame,
            text="デモ機能実行",
            command=self.run_demo_task,
            font_mgr=self.font_mgr,
            style_mgr=self.style_mgr
        )
        demo_btn.pack(pady=10)
    
    def load_plugins(self):
        """プラグインを読み込み"""
        try:
            self.plugin_manager.load_all_plugins(self)
            loaded_count = len(self.plugin_manager.get_loaded_plugins())
            self.logger.info(f"{loaded_count}個のプラグインを読み込みました")
        except Exception as e:
            self.logger.error(f"プラグイン読み込みエラー: {e}")
    
    # メニューハンドラー
    def show_file_menu(self):
        self.logger.info("ファイルメニューが選択されました")
        MessageDialog.show_info(
            self,
            "ファイルメニュー",
            "ファイル操作メニューです。\n\n"
            "・新規作成\n"
            "・開く\n"
            "・保存\n"
            "・名前を付けて保存\n"
            "・最近使用したファイル"
        )
    
    def show_edit_menu(self):
        self.logger.info("編集メニューが選択されました")
        MessageDialog.show_info(
            self,
            "編集メニュー",
            "編集機能メニューです。\n\n"
            "・元に戻す\n"
            "・やり直し\n"
            "・切り取り\n"
            "・コピー\n"
            "・貼り付け"
        )
    
    def show_view_menu(self):
        self.logger.info("表示メニューが選択されました")
        MessageDialog.show_info(
            self,
            "表示メニュー",
            "表示設定メニューです。\n\n"
            "・ズーム\n"
            "・フルスクリーン\n"
            "・テーマ変更\n"
            "・レイアウト設定"
        )
    
    def show_tools_menu(self):
        result = MessageDialog.show_confirm(
            self,
            "ツール",
            "長時間処理のデモを実行しますか？"
        )
        if result:
            self.run_demo_task()
    
    def show_help_menu(self):
        MessageDialog.show_info(
            self,
            "ヘルプ",
            "これは拡張GUIテンプレートのサンプルアプリケーションです。\n\n"
            "機能:\n"
            "・設定管理システム\n"
            "・プラグインシステム\n"
            "・複数レイアウトモード\n"
            "・進捗ダイアログ\n"
            "・ロギング機能\n\n"
            "開発者: TITManagement\n"
            "バージョン: 1.0.0"
        )
    
    def run_demo_task(self):
        """デモタスクを実行"""
        def task_completed(result):
            MessageDialog.show_info(self, "完了", f"タスクが完了しました: {result}")
        
        try:
            TaskRunner.run_with_progress(
                self,
                sample_long_task,
                title="デモ処理実行中",
                message="サンプル処理を実行しています...",
                callback=task_completed
            )
        except Exception as e:
            MessageDialog.show_error(self, "エラー", f"処理中にエラーが発生しました: {e}")
    
    def on_closing(self):
        """アプリケーション終了時の処理"""
        # 設定を保存
        self.config.save_config()
        self.logger.info("拡張GUIアプリケーションが終了しました")
        self.destroy()
