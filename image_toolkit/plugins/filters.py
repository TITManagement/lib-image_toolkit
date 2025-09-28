# FilterProcessingPluginダミー実装
class FilterProcessingPlugin:
    def get_display_name(self):
        return "フィルター処理"

    def get_description(self):
        return "各種フィルター・画像処理"

    def create_ui(self, parent):
        import customtkinter as ctk
        label = ctk.CTkLabel(parent, text="フィルター処理プラグイン（テスト表示）", fg_color="lightgreen")
        label.pack(fill="x", padx=5, pady=5)
    def get_parameters(self):
        # TODO: 必要に応じてパラメータを返す
        return {}
    def __init__(self):
        self.parameter_change_callback = None
        self.special_filter_callback = None
        self.morphology_callback = None
        self.contour_callback = None
        self.undo_special_filter_callback = None
        self.undo_morphology_callback = None
        self.undo_contour_callback = None

    def set_parameter_change_callback(self, func):
        self.parameter_change_callback = func

    def set_special_filter_callback(self, func):
        self.special_filter_callback = func

    def set_morphology_callback(self, func):
        self.morphology_callback = func

    def set_contour_callback(self, func):
        self.contour_callback = func

    def set_undo_special_filter_callback(self, func):
        self.undo_special_filter_callback = func

    def set_undo_morphology_callback(self, func):
        self.undo_morphology_callback = func

    def set_undo_contour_callback(self, func):
        self.undo_contour_callback = func
