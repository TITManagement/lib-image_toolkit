# BasicAdjustmentPluginダミー実装
class BasicAdjustmentPlugin:
    def get_display_name(self):
        return "基本調整"

    def get_description(self):
        return "明るさ・コントラスト等の基本調整"

    def create_ui(self, parent):
        import customtkinter as ctk
        label = ctk.CTkLabel(parent, text="基本調整プラグイン（テスト表示）", fg_color="lightblue")
        label.pack(fill="x", padx=5, pady=5)
    def get_parameters(self):
        # TODO: 必要に応じてパラメータを返す
        return {}
    def __init__(self):
        self.parameter_change_callback = None

    def set_parameter_change_callback(self, func):
        self.parameter_change_callback = func
