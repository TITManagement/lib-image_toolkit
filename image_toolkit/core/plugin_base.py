# PluginManagerダミー実装
class PluginManager:
    def __init__(self):
        self.plugins = {}

    def register_plugin(self, plugin):
        # プラグインID（name属性）で登録（全プラグインで統一）
        plugin_id = getattr(plugin, 'name', plugin.__class__.__name__)
        self.plugins[plugin_id] = plugin

    def get_plugin(self, name):
        return self.plugins.get(name)

    def get_all_plugins(self):
        return list(self.plugins.values())

    def get_enabled_plugins(self):
        # 必要に応じて有効なプラグインのみ返す（ここでは全て返す）
        return list(self.plugins.values())

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable, List, Tuple, Union
from PIL import Image
import customtkinter as ctk

class ImageProcessorPlugin(ABC):
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.enabled = True
        self._sliders = {}
        self._labels = {}
        self._buttons = {}
    @abstractmethod
    def get_display_name(self) -> str:
        pass
    @abstractmethod
    def get_description(self) -> str:
        pass
    @abstractmethod
    def create_ui(self, parent: ctk.CTkFrame) -> None:
        pass
    @abstractmethod
    def process_image(self, image: Image.Image, **params) -> Image.Image:
        pass
    def apply_special_filter(self, image: Image.Image, filter_type: str) -> Image.Image:
        return image
    def get_parameters(self) -> Dict[str, Any]:
        params = {}
        for name, slider in self._sliders.items():
            params[name] = slider.get()
        return params
    def reset_parameters(self) -> None:
        for slider in self._sliders.values():
            default_value = slider.default_value if hasattr(slider, 'default_value') else 0
            slider.set(default_value)
            if hasattr(slider, 'command') and slider.command:
                try:
                    slider.command(default_value)
                except Exception as e:
                    print(f"⚠️ スライダーコールバックエラー: {e}")
    def set_parameter_change_callback(self, callback: Callable) -> None:
        self.parameter_change_callback = callback
    def _on_parameter_change(self, value: Any = None) -> None:
        if hasattr(self, 'parameter_change_callback'):
            self.parameter_change_callback()
    def enable(self) -> None:
        self.enabled = True
    def disable(self) -> None:
        self.enabled = False
    def is_enabled(self) -> bool:
        return self.enabled

class PluginUIHelper:
    @staticmethod
    def create_slider_with_label(
        parent: ctk.CTkFrame,
        text: str,
        from_: float,
        to: float,
        default_value: float,
        command: Optional[Callable] = None,
        value_format: str = "{:.1f}"
    ) -> Tuple[ctk.CTkSlider, ctk.CTkLabel]:
        label = ctk.CTkLabel(parent, text=text, font=("Arial", 11))
        label.pack(anchor="w", padx=3, pady=(5, 0))
        value_label = ctk.CTkLabel(parent, text=value_format.format(default_value), font=("Arial", 9))
        value_label.pack(anchor="w", padx=3)
        def handle_slider_change(value):
            clamped_value = max(from_, min(to, value))
            value_label.configure(text=value_format.format(clamped_value))
            if abs(value - clamped_value) > 0.001:
                print(f"⚠️ スライダー値修正: {value:.3f} → {clamped_value:.3f} (範囲: {from_}〜{to})")
            if command:
                command(clamped_value)
        slider = ctk.CTkSlider(
            parent,
            from_=from_,
            to=to,
            command=handle_slider_change
        )
        slider.set(default_value)
        def on_mouse_release(event):
            if command:
                current_value = slider.get()
                clamped_value = max(from_, min(to, current_value))
                print(f"🖱️ マウスリリース: 値={current_value:.3f}, 修正後={clamped_value:.3f}")
                if abs(current_value - clamped_value) > 0.001:
                    slider.set(clamped_value)
                command(clamped_value)
        slider.bind("<ButtonRelease-1>", on_mouse_release)
        setattr(slider, 'default_value', default_value)
        slider.pack(fill="x", padx=5, pady=3)
        return slider, value_label
    @staticmethod
    def create_button(
        parent: ctk.CTkFrame,
        text: str,
        command: Optional[Callable] = None,
        width: int = 120
    ) -> ctk.CTkButton:
        button = ctk.CTkButton(parent, text=text, command=command, width=width)
        button.pack(padx=5, pady=5)
        return button
