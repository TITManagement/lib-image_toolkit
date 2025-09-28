# ImageAnalysisPluginダミー実装
class ImageAnalysisPlugin:
    def __init__(self):
        self.name = "image_analysis"
        self.histogram_callback = None
        self.feature_callback = None
        self.frequency_callback = None
        self.blur_callback = None
        self.noise_callback = None
        self.undo_features_callback = None
        self.undo_frequency_callback = None
        self.undo_blur_callback = None
        self.undo_noise_callback = None
        self.undo_histogram_callback = None

    def get_parameters(self):
        # TODO: 必要に応じてパラメータを返す
        return {}

    def get_display_name(self):
        return "画像解析"

    def get_description(self):
        return "画像特徴量・周波数・ノイズ等の解析"

    def create_ui(self, parent):
        import customtkinter as ctk
        label = ctk.CTkLabel(parent, text="画像解析プラグイン（テスト表示）", fg_color="orange")
        label.pack(fill="x", padx=5, pady=5)

    def set_histogram_callback(self, func):
        self.histogram_callback = func

    def set_feature_callback(self, func):
        self.feature_callback = func

    def set_frequency_callback(self, func):
        self.frequency_callback = func

    def set_blur_callback(self, func):
        self.blur_callback = func

    def set_noise_callback(self, func):
        self.noise_callback = func

    def set_undo_features_callback(self, func):
        self.undo_features_callback = func

    def set_undo_frequency_callback(self, func):
        self.undo_frequency_callback = func

    def set_undo_blur_callback(self, func):
        self.undo_blur_callback = func

    def set_undo_noise_callback(self, func):
        self.undo_noise_callback = func

    def set_undo_histogram_callback(self, func):
        self.undo_histogram_callback = func
