#!/usr/bin/env python3
"""
濃度調整プラグイン - Density Adjustment Plugin

ガンマ補正、シャドウ/ハイライト調整、色温度調整を提供
"""

import numpy as np
import cv2
from PIL import Image
import customtkinter as ctk
from typing import Dict, Any, Union

from image_toolkit.core.plugin_base import ImageProcessorPlugin, PluginUIHelper

# カーブエディタのインポート
try:
    from image_toolkit.ui.curve_editor import CurveEditor
    CURVE_EDITOR_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ カーブエディタインポート警告: {e}")
    CURVE_EDITOR_AVAILABLE = False


class DensityAdjustmentPlugin(ImageProcessorPlugin):
    def reset_parameters(self) -> None:
        """濃度調整の全パラメータ・UIを初期値にリセット"""
        self.gamma_value = 1.0
        self.shadow_value = 0
        self.highlight_value = 0
        self.temperature_value = 0
        self.threshold_value = 127
        self.use_curve_gamma = False
        self.gamma_lut = None
        self.applied_binary = False
        self.applied_histogram = False
        # UIスライダー・カーブ・ラベルを初期値に戻す
        if hasattr(self, 'gamma_mode_var'):
            self.gamma_mode_var.set("slider")
            self._on_gamma_mode_change()
        if CURVE_EDITOR_AVAILABLE and hasattr(self, 'curve_editor'):
            self.curve_editor._reset_curve()
        if 'gamma' in self._sliders:
            self._sliders['gamma'].set(1.0)
            if 'gamma' in self._labels:
                self._labels['gamma'].configure(text="1.00")
        if 'shadow' in self._sliders:
            self._sliders['shadow'].set(0)
            if 'shadow' in self._labels:
                self._labels['shadow'].configure(text="0")
        if 'highlight' in self._sliders:
            self._sliders['highlight'].set(0)
            if 'highlight' in self._labels:
                self._labels['highlight'].configure(text="0")
        if 'temperature' in self._sliders:
            self._sliders['temperature'].set(0)
            if 'temperature' in self._labels:
                self._labels['temperature'].configure(text="0")
        if 'threshold' in self._sliders:
            self._sliders['threshold'].set(127)
            if 'threshold' in self._labels:
                self._labels['threshold'].configure(text="127")
        print("🔄 濃度調整パラメータリセット（UIも初期化）")
    def apply_binary_threshold(self, image: Image.Image) -> Image.Image:
        """2値化を適用"""
        try:
            print(f"📐 2値化開始: 閾値={self.threshold_value}")
            print(f"[DEBUG] threshold_value type: {type(self.threshold_value)}, value: {self.threshold_value}")
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            _, binary_image = cv2.threshold(gray_image, int(self.threshold_value), 255, cv2.THRESH_BINARY)
            binary_rgb = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2RGB)
            result_image = Image.fromarray(binary_rgb)
            print(f"✅ 2値化完了")
            return result_image
        except Exception as e:
            print(f"❌ 2値化エラー: {e}")
            return image
    def _on_threshold_change(self, value: float) -> None:
        self.threshold_value = int(value)
        print(f"[DEBUG] threshold_value changed: {self.threshold_value}")
        self._on_parameter_change()

    def _apply_binary_threshold(self) -> None:
        self.applied_binary = True
        if hasattr(self, 'threshold_callback'):
            self.threshold_callback()

    def _on_histogram_equalization(self) -> None:
        self.applied_histogram = True
        if hasattr(self, 'histogram_callback'):
            self.histogram_callback()
    def _on_gamma_mode_change(self) -> None:
        mode = self.gamma_mode_var.get()
        if mode == "slider":
            self.use_curve_gamma = False
            self.gamma_lut = None
            self.gamma_slider_frame.pack(fill="x", padx=5, pady=5)
            if hasattr(self, 'gamma_curve_frame'):
                self.gamma_curve_frame.pack_forget()
        elif mode == "curve" and hasattr(self, 'gamma_curve_frame'):
            self.use_curve_gamma = True
            self.gamma_slider_frame.pack_forget()
            self.gamma_curve_frame.pack(fill="x", padx=5, pady=5)
        self._on_parameter_change()

    def _on_gamma_change(self, value: float) -> None:
        self.gamma_value = float(value)
        print(f"[DEBUG] gamma_value changed: {self.gamma_value}")
        self._on_parameter_change()

    def _on_curve_change(self, lut):
        self.gamma_lut = lut
        self._on_parameter_change()

    def _on_shadow_change(self, value: float) -> None:
        self.shadow_value = int(value)
        print(f"[DEBUG] shadow_value changed: {self.shadow_value}")
        self._on_parameter_change()

    def _on_highlight_change(self, value: float) -> None:
        self.highlight_value = int(value)
        print(f"[DEBUG] highlight_value changed: {self.highlight_value}")
        self._on_parameter_change()

    def _on_temperature_change(self, value: float) -> None:
        self.temperature_value = int(value)
        print(f"[DEBUG] temperature_value changed: {self.temperature_value}")
        self._on_parameter_change()
    def set_histogram_callback(self, func):
        self.histogram_callback = func

    def set_threshold_callback(self, func):
        self.threshold_callback = func
    """濃度調整プラグイン"""
    def __init__(self):
        super().__init__("density_adjustment", "1.0.0")
        self.gamma_value = 1.0
        self.shadow_value = 0
        self.highlight_value = 0
        self.temperature_value = 0
        self.threshold_value = 127
        self.use_curve_gamma = False
        self.gamma_lut = None
        self.applied_binary = False
        print("[DEBUG] CurveEditor生成済み")
        self.applied_histogram = False

    def get_display_name(self) -> str:
        return "濃度調整"

    def get_description(self) -> str:
        return "ガンマ補正、シャドウ/ハイライト調整、色温度調整を提供します"

    def create_ui(self, parent: ctk.CTkFrame) -> None:
        """濃度調整UIを作成（完全移植）"""
        from image_toolkit.core.plugin_base import PluginUIHelper
        try:
            from image_toolkit.ui.curve_editor import CurveEditor
            CURVE_EDITOR_AVAILABLE = True
        except ImportError:
            CURVE_EDITOR_AVAILABLE = False

        # テスト用ラベル（最低限のUI表示確認）
        test_label = ctk.CTkLabel(parent, text="濃度調整UI（テスト表示）", fg_color="yellow")
        test_label.pack(fill="x", padx=5, pady=5)

        self.gamma_mode_frame = ctk.CTkFrame(parent)
        self.gamma_mode_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(self.gamma_mode_frame, text="ガンマ補正方式").pack(pady=(5, 0))
        self.gamma_mode_var = ctk.StringVar(value="slider")
        self.gamma_mode_radio1 = ctk.CTkRadioButton(
            self.gamma_mode_frame, 
            text="スライダー", 
            variable=self.gamma_mode_var, 
            value="slider",
            command=self._on_gamma_mode_change
        )
        self.gamma_mode_radio1.pack(side="left", padx=10, pady=5)
        if CURVE_EDITOR_AVAILABLE:
            self.gamma_mode_radio2 = ctk.CTkRadioButton(
                self.gamma_mode_frame, 
                text="カーブ", 
                variable=self.gamma_mode_var, 
                value="curve",
                command=self._on_gamma_mode_change
            )
            self.gamma_mode_radio2.pack(side="left", padx=10, pady=5)

        self.gamma_control_frame = ctk.CTkFrame(parent)
        self.gamma_control_frame.pack(fill="x", padx=5, pady=5)
        self.gamma_slider_frame = ctk.CTkFrame(self.gamma_control_frame)
        self.gamma_slider_frame.pack(fill="x", padx=5, pady=5)
        self._sliders['gamma'], self._labels['gamma'] = PluginUIHelper.create_slider_with_label(
            parent=self.gamma_slider_frame,
            text="ガンマ補正",
            from_=0.1,
            to=3.0,
            default_value=1.0,
            command=self._on_gamma_change,
            value_format="{:.2f}"
        )
        if CURVE_EDITOR_AVAILABLE:
            self.gamma_curve_frame = ctk.CTkFrame(self.gamma_control_frame)
            self.curve_editor = CurveEditor(
                self.gamma_curve_frame, 
                width=250, 
                height=250,
                on_curve_change=self._on_curve_change
            )
            self.curve_editor.pack(padx=5, pady=5)
            print("[DEBUG] CurveEditor生成済み")

        self._sliders['shadow'], self._labels['shadow'] = PluginUIHelper.create_slider_with_label(
            parent=parent,
            text="シャドウ",
            from_=-100,
            to=100,
            default_value=0,
            command=self._on_shadow_change,
            value_format="{:.0f}"
        )
        self._sliders['highlight'], self._labels['highlight'] = PluginUIHelper.create_slider_with_label(
            parent=parent,
            text="ハイライト",
            from_=-100,
            to=100,
            default_value=0,
            command=self._on_highlight_change,
            value_format="{:.0f}"
        )
        self._sliders['temperature'], self._labels['temperature'] = PluginUIHelper.create_slider_with_label(
            parent=parent,
            text="色温度",
            from_=-100,
            to=100,
            default_value=0,
            command=self._on_temperature_change,
            value_format="{:.0f}"
        )

        threshold_frame = ctk.CTkFrame(parent)
        threshold_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(threshold_frame, text="2値化", font=("Arial", 11)).pack(anchor="w", padx=3, pady=(5, 0))
        self._sliders['threshold'], self._labels['threshold'] = PluginUIHelper.create_slider_with_label(
            parent=threshold_frame,
            text="閾値",
            from_=0,
            to=255,
            default_value=127,
            command=self._on_threshold_change,
            value_format="{:.0f}"
        )
        self._buttons['binary'] = PluginUIHelper.create_button(
            threshold_frame,
            text="2値化実行",
            command=self._apply_binary_threshold
        )
        self._buttons['histogram'] = PluginUIHelper.create_button(
            parent=parent,
            text="ヒストグラム均等化",
            command=self._on_histogram_equalization
        )
        self._buttons['reset'] = PluginUIHelper.create_button(
            parent=parent,
            text="リセット",
            command=self.reset_parameters
        )

    def process_image(self, image: Image.Image, **params) -> Image.Image:
        """濃度調整を適用"""
        try:
            if not image:
                return image

            print(f"🔄 濃度調整開始...")
            result_image = image.copy()

            # NumPy配列に変換
            img_array = np.array(result_image, dtype=np.float32)

            # ガンマ補正
            if self.use_curve_gamma and self.gamma_lut is not None:
                print(f"🎯 カーブベースガンマ補正適用")
                img_array_int = img_array.astype(np.uint8)
                img_array = self.gamma_lut[img_array_int].astype(np.float32)
            elif self.gamma_value != 1.0:
                print(f"🎯 スライダーベースガンマ補正適用: {self.gamma_value}")
                img_array = img_array / 255.0
                img_array = np.power(img_array, 1.0 / self.gamma_value)
                img_array = img_array * 255.0

            # シャドウ/ハイライト調整
            if self.shadow_value != 0 or self.highlight_value != 0:
                print(f"🌗 シャドウ/ハイライト調整: シャドウ={self.shadow_value}, ハイライト={self.highlight_value}")
                img_array = self._apply_shadow_highlight(img_array)

            # 色温度調整
            if self.temperature_value != 0:
                print(f"🌡️ 色温度調整: {self.temperature_value}")
                img_array = self._apply_temperature(img_array)

            # 0-255の範囲にクリップ
            img_array = np.clip(img_array, 0, 255).astype(np.uint8)
            result_image = Image.fromarray(img_array)

            print(f"✅ 濃度調整完了")
            return result_image

        except Exception as e:
            print(f"❌ 濃度調整エラー: {e}")
            return image

    def _apply_shadow_highlight(self, img_array: np.ndarray) -> np.ndarray:
        """シャドウ/ハイライト調整を適用"""
        img_normalized = img_array / 255.0
        if self.shadow_value != 0:
            shadow_factor = self.shadow_value / 100.0
            mask = img_normalized < 0.5
            img_normalized = np.where(mask,
                                    img_normalized + shadow_factor * (0.5 - img_normalized),
                                    img_normalized)
        if self.highlight_value != 0:
            highlight_factor = self.highlight_value / 100.0
            mask = img_normalized > 0.5
            img_normalized = np.where(mask,
                                    img_normalized - highlight_factor * (img_normalized - 0.5),
                                    img_normalized)
        return img_normalized * 255.0

    def _apply_temperature(self, img_array: np.ndarray) -> np.ndarray:
        """色温度調整を適用"""
        if self.temperature_value > 0:
            factor = self.temperature_value / 100.0
            img_array[:, :, 0] = np.clip(img_array[:, :, 0] * (1.0 + factor * 0.3), 0, 255)
            img_array[:, :, 2] = np.clip(img_array[:, :, 2] * (1.0 - factor * 0.2), 0, 255)
        else:
            factor = abs(self.temperature_value) / 100.0
            img_array[:, :, 0] = np.clip(img_array[:, :, 0] * (1.0 - factor * 0.2), 0, 255)
            img_array[:, :, 2] = np.clip(img_array[:, :, 2] * (1.0 + factor * 0.3), 0, 255)
        return img_array

    # その他必要なメソッド（_on_gamma_change, _on_shadow_change, ...）も同様に展開
