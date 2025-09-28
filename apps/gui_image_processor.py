"""
画像処理アプリケーション

機能:
- ディレクトリ選択による画像読み込み
- 原画像と処理後画像の並列表示
- リアルタイム画像処理プレビュー
- 複数の画像処理フィルター
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageOps
import cv2
import numpy as np
from pathlib import Path


class ImageProcessorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # ウィンドウ設定
        self.title("Image Processor - 画像処理アプリ")
        self.geometry("1400x800")
        
        # 変数初期化
        self.current_directory = None
        self.image_files = []
        self.current_image_index = 0
        self.original_image = None
        self.processed_image = None
        
        # GUI作成
        self.create_widgets()
        
    def create_widgets(self):
        """GUI要素を作成"""
        
        # メインフレーム
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # コントロールパネル
        self.create_control_panel()
        
        # 画像表示エリア
        self.create_image_display_area()
        
        # 処理パラメータパネル
        self.create_parameter_panel()
        
    def create_control_panel(self):
        """コントロールパネルを作成"""
        control_frame = ctk.CTkFrame(self.main_frame, height=80)
        control_frame.pack(fill="x", padx=5, pady=5)
        control_frame.pack_propagate(False)
        
        # ディレクトリ選択
        self.dir_button = ctk.CTkButton(
            control_frame, 
            text="📁 ディレクトリ選択",
            command=self.select_directory,
            width=150
        )
        self.dir_button.pack(side="left", padx=10, pady=20)
        
        # 画像ナビゲーション
        nav_frame = ctk.CTkFrame(control_frame)
        nav_frame.pack(side="left", padx=20, pady=10)
        
        self.prev_button = ctk.CTkButton(
            nav_frame, 
            text="◀ 前の画像",
            command=self.previous_image,
            width=100
        )
        self.prev_button.pack(side="left", padx=5)
        
        self.image_label = ctk.CTkLabel(nav_frame, text="画像: 0/0")
        self.image_label.pack(side="left", padx=10)
        
        self.next_button = ctk.CTkButton(
            nav_frame, 
            text="次の画像 ▶",
            command=self.next_image,
            width=100
        )
        self.next_button.pack(side="left", padx=5)
        
        # 保存ボタン
        self.save_button = ctk.CTkButton(
            control_frame,
            text="💾 保存",
            command=self.save_processed_image,
            width=100
        )
        self.save_button.pack(side="right", padx=10, pady=20)
        
    def create_image_display_area(self):
        """画像表示エリアを作成"""
        display_frame = ctk.CTkFrame(self.main_frame)
        display_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 原画像表示
        original_frame = ctk.CTkFrame(display_frame)
        original_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(original_frame, text="原画像", font=("Arial", 16, "bold")).pack(pady=5)
        self.original_canvas = ctk.CTkCanvas(original_frame, bg="white")
        self.original_canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 処理後画像表示
        processed_frame = ctk.CTkFrame(display_frame)
        processed_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(processed_frame, text="処理後画像", font=("Arial", 16, "bold")).pack(pady=5)
        self.processed_canvas = ctk.CTkCanvas(processed_frame, bg="white")
        self.processed_canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
    def create_parameter_panel(self):
        """処理パラメータパネルを作成"""
        param_frame = ctk.CTkFrame(self.main_frame, height=200)
        param_frame.pack(fill="x", padx=5, pady=5)
        param_frame.pack_propagate(False)
        
        # 処理タイプ選択
        type_frame = ctk.CTkFrame(param_frame)
        type_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(type_frame, text="画像処理タイプ:", font=("Arial", 14, "bold")).pack(side="left", padx=10)
        
        self.process_type = ctk.CTkOptionMenu(
            type_frame,
            values=[
                "基本調整",
                "芸術的効果",
                "プロ補正",
                "フィルター効果",
                "エッジ・輪郭",
                "ノイズ処理",
                "色彩変換",
                "ヴィンテージ"
            ],
            command=self.on_process_type_change
        )
        self.process_type.pack(side="left", padx=10)
        
        # パラメータスライダー
        self.create_parameter_sliders(param_frame)
        
    def create_parameter_sliders(self, parent):
        """パラメータスライダーを作成"""
        slider_frame = ctk.CTkFrame(parent)
        slider_frame.pack(fill="x", padx=10, pady=10)
        
        # 明度
        brightness_frame = ctk.CTkFrame(slider_frame)
        brightness_frame.pack(fill="x", pady=2)
        
        ctk.CTkLabel(brightness_frame, text="明度:", width=80).pack(side="left", padx=5)
        self.brightness_slider = ctk.CTkSlider(
            brightness_frame, 
            from_=1, 
            to=300, 
            number_of_steps=299,
            command=self.update_image
        )
        self.brightness_slider.set(100)  # 100 = 1.0倍
        self.brightness_slider.pack(side="left", fill="x", expand=True, padx=5)
        
        self.brightness_value = ctk.CTkLabel(brightness_frame, text="1.0", width=40)
        self.brightness_value.pack(side="left", padx=5)
        
        # コントラスト
        contrast_frame = ctk.CTkFrame(slider_frame)
        contrast_frame.pack(fill="x", pady=2)
        
        ctk.CTkLabel(contrast_frame, text="コントラスト:", width=80).pack(side="left", padx=5)
        self.contrast_slider = ctk.CTkSlider(
            contrast_frame, 
            from_=1, 
            to=300, 
            number_of_steps=299,
            command=self.update_image
        )
        self.contrast_slider.set(100)  # 100 = 1.0倍
        self.contrast_slider.pack(side="left", fill="x", expand=True, padx=5)
        
        self.contrast_value = ctk.CTkLabel(contrast_frame, text="1.0", width=40)
        self.contrast_value.pack(side="left", padx=5)
        
        # 彩度
        saturation_frame = ctk.CTkFrame(slider_frame)
        saturation_frame.pack(fill="x", pady=2)
        
        ctk.CTkLabel(saturation_frame, text="彩度:", width=80).pack(side="left", padx=5)
        self.saturation_slider = ctk.CTkSlider(
            saturation_frame, 
            from_=0, 
            to=300, 
            number_of_steps=300,
            command=self.update_image
        )
        self.saturation_slider.set(100)  # 100 = 1.0倍
        self.saturation_slider.pack(side="left", fill="x", expand=True, padx=5)
        
        self.saturation_value = ctk.CTkLabel(saturation_frame, text="1.0", width=40)
        self.saturation_value.pack(side="left", padx=5)
        
    def select_directory(self):
        """ディレクトリを選択"""
        directory = filedialog.askdirectory(title="画像ディレクトリを選択")
        if directory:
            self.current_directory = directory
            self.load_images()
            
    def load_images(self):
        """ディレクトリから画像ファイルを読み込み"""
        if not self.current_directory:
            return
            
        # サポートする画像形式
        supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif'}
        
        self.image_files = []
        for file_path in Path(self.current_directory).iterdir():
            if file_path.suffix.lower() in supported_formats:
                self.image_files.append(str(file_path))
                
        if self.image_files:
            self.current_image_index = 0
            self.load_current_image()
        else:
            messagebox.showwarning("警告", "指定されたディレクトリに画像ファイルが見つかりませんでした。")
            
    def load_current_image(self):
        """現在の画像を読み込み"""
        if not self.image_files:
            return
            
        image_path = self.image_files[self.current_image_index]
        try:
            self.original_image = Image.open(image_path)
            self.display_original_image()
            self.update_image()
            self.update_navigation_label()
        except Exception as e:
            messagebox.showerror("エラー", f"画像の読み込みに失敗しました: {str(e)}")
            
    def display_original_image(self):
        """原画像を表示"""
        if not self.original_image:
            return
            
        # キャンバスサイズに合わせてリサイズ
        canvas_width = self.original_canvas.winfo_width()
        canvas_height = self.original_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.after(100, self.display_original_image)
            return
            
        display_image = self.resize_image_for_display(self.original_image, canvas_width, canvas_height)
        
        # Canvas に表示
        self.original_photo = ImageTk.PhotoImage(display_image)
        self.original_canvas.delete("all")
        self.original_canvas.create_image(
            canvas_width//2, 
            canvas_height//2, 
            image=self.original_photo
        )
        
    def resize_image_for_display(self, image, canvas_width, canvas_height):
        """表示用に画像をリサイズ"""
        # アスペクト比を保持してリサイズ
        img_width, img_height = image.size
        
        # キャンバスに余裕を持たせる
        max_width = canvas_width - 20
        max_height = canvas_height - 20
        
        # アスペクト比計算
        ratio = min(max_width / img_width, max_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
    def update_image(self, value=None):
        """画像処理を適用して表示更新"""
        if not self.original_image:
            return
            
        # パラメータ値取得（スライダー値を0.01倍して実際の値に変換）
        brightness = self.brightness_slider.get() / 100.0
        contrast = self.contrast_slider.get() / 100.0
        saturation = self.saturation_slider.get() / 100.0
        
        # 値表示更新
        self.brightness_value.configure(text=f"{brightness:.1f}")
        self.contrast_value.configure(text=f"{contrast:.1f}")
        self.saturation_value.configure(text=f"{saturation:.1f}")
        
        # 選択された処理タイプに応じて処理を実行
        process_type = self.process_type.get()
        processed = self.apply_image_processing(self.original_image, process_type, brightness, contrast, saturation)
        
        self.processed_image = processed
        self.display_processed_image()
        
    def apply_image_processing(self, image, process_type, brightness, contrast, saturation):
        """画像処理を適用"""
        processed = image.copy()
        
        if process_type == "基本調整":
            # 明度調整
            enhancer = ImageEnhance.Brightness(processed)
            processed = enhancer.enhance(brightness)
            
            # コントラスト調整
            enhancer = ImageEnhance.Contrast(processed)
            processed = enhancer.enhance(contrast)
            
            # 彩度調整
            enhancer = ImageEnhance.Color(processed)
            processed = enhancer.enhance(saturation)
            
        elif process_type == "芸術的効果":
            processed = self.apply_artistic_effects(processed, brightness, contrast, saturation)
            
        elif process_type == "プロ補正":
            processed = self.apply_professional_correction(processed, brightness, contrast, saturation)
            
        elif process_type == "フィルター効果":
            processed = self.apply_filter_effects(processed, brightness, contrast, saturation)
            
        elif process_type == "エッジ・輪郭":
            processed = self.apply_edge_detection(processed, brightness, contrast, saturation)
            
        elif process_type == "ノイズ処理":
            processed = self.apply_noise_processing(processed, brightness, contrast, saturation)
            
        elif process_type == "色彩変換":
            processed = self.apply_color_transformation(processed, brightness, contrast, saturation)
            
        elif process_type == "ヴィンテージ":
            processed = self.apply_vintage_effects(processed, brightness, contrast, saturation)
            
        return processed
        
    def display_processed_image(self):
        """処理後画像を表示"""
        if not self.processed_image:
            return
            
        # キャンバスサイズに合わせてリサイズ
        canvas_width = self.processed_canvas.winfo_width()
        canvas_height = self.processed_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.after(100, self.display_processed_image)
            return
            
        display_image = self.resize_image_for_display(self.processed_image, canvas_width, canvas_height)
        
        # Canvas に表示
        self.processed_photo = ImageTk.PhotoImage(display_image)
        self.processed_canvas.delete("all")
        self.processed_canvas.create_image(
            canvas_width//2, 
            canvas_height//2, 
            image=self.processed_photo
        )
        
    def previous_image(self):
        """前の画像に移動"""
        if self.image_files and self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_current_image()
            
    def next_image(self):
        """次の画像に移動"""
        if self.image_files and self.current_image_index < len(self.image_files) - 1:
            self.current_image_index += 1
            self.load_current_image()
            
    def update_navigation_label(self):
        """ナビゲーションラベル更新"""
        if self.image_files:
            current = self.current_image_index + 1
            total = len(self.image_files)
            filename = Path(self.image_files[self.current_image_index]).name
            self.image_label.configure(text=f"{current}/{total}: {filename}")
        else:
            self.image_label.configure(text="画像: 0/0")
            
    def on_process_type_change(self, choice):
        """処理タイプ変更時の処理"""
        # TODO: 選択された処理タイプに応じてパラメータパネルを変更
        print(f"処理タイプ変更: {choice}")
        
    def save_processed_image(self):
        """処理後画像を保存"""
        if not self.processed_image:
            messagebox.showwarning("警告", "保存する画像がありません。")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.processed_image.save(file_path)
                messagebox.showinfo("成功", f"画像を保存しました: {file_path}")
            except Exception as e:
                messagebox.showerror("エラー", f"画像の保存に失敗しました: {str(e)}")
                
    # ========== 高度な画像処理メソッド ==========
    
    def apply_artistic_effects(self, image, brightness, contrast, saturation):
        """芸術的効果を適用"""
        processed = image.copy()
        
        # セピア効果（brightness値で強度調整）
        if brightness > 1.0:
            # RGB画像をセピア調に変換
            sepia_matrix = (
                0.393 + 0.607 * (2 - brightness), 0.769 - 0.769 * (brightness - 1), 0.189 - 0.189 * (brightness - 1), 0,
                0.349 - 0.349 * (brightness - 1), 0.686 + 0.314 * (2 - brightness), 0.168 - 0.168 * (brightness - 1), 0,
                0.272 - 0.272 * (brightness - 1), 0.534 - 0.534 * (brightness - 1), 0.131 + 0.869 * (2 - brightness), 0
            )
            processed = processed.convert('RGB')
            processed = processed.convert('RGB', sepia_matrix)
        
        # 油絵風効果（contrast値で強度調整）
        if contrast > 1.0:
            # OpenCVを使用してより高度な処理
            cv_image = cv2.cvtColor(np.array(processed), cv2.COLOR_RGB2BGR)
            # 平滑化フィルタを適用
            kernel_size = int(contrast * 5)
            if kernel_size % 2 == 0:
                kernel_size += 1
            cv_image = cv2.bilateralFilter(cv_image, kernel_size, 80, 80)
            processed = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        
        # ポスタライゼーション（saturation値で色数調整）
        if saturation != 1.0:
            # 色数を制限してポスター風に
            color_levels = max(2, int(8 * saturation))
            cv_image = cv2.cvtColor(np.array(processed), cv2.COLOR_RGB2BGR)
            factor = 255.0 / (color_levels - 1)
            cv_image = (cv_image / factor).astype(np.uint8) * factor
            processed = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        
        return processed
    
    def apply_professional_correction(self, image, brightness, contrast, saturation):
        """プロフェッショナル補正を適用"""
        processed = image.copy()
        
        # ヒストグラム均等化
        if brightness > 1.2:
            cv_image = cv2.cvtColor(np.array(processed), cv2.COLOR_RGB2BGR)
            # 各チャンネルに対してヒストグラム均等化
            cv_image[:,:,0] = cv2.equalizeHist(cv_image[:,:,0])
            cv_image[:,:,1] = cv2.equalizeHist(cv_image[:,:,1])
            cv_image[:,:,2] = cv2.equalizeHist(cv_image[:,:,2])
            processed = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        
        # ガンマ補正
        if contrast != 1.0:
            gamma = 1.0 / contrast
            cv_image = np.array(processed, dtype=np.float32) / 255.0
            cv_image = np.power(cv_image, gamma)
            cv_image = (cv_image * 255).astype(np.uint8)
            processed = Image.fromarray(cv_image)
        
        # アンシャープマスク（シャープネス強化）
        if saturation > 1.0:
            cv_image = cv2.cvtColor(np.array(processed), cv2.COLOR_RGB2BGR)
            blurred = cv2.GaussianBlur(cv_image, (0, 0), 2.0)
            sharpened = cv2.addWeighted(cv_image, 1.0 + saturation, blurred, -saturation, 0)
            processed = Image.fromarray(cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB))
        
        return processed
    
    def apply_filter_effects(self, image, brightness, contrast, saturation):
        """フィルター効果を適用"""
        processed = image.copy()
        
        # ぼかし効果
        if brightness < 1.0:
            blur_radius = (1.0 - brightness) * 5
            processed = processed.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        
        # シャープネス
        elif brightness > 1.0:
            sharpness_factor = brightness
            enhancer = ImageEnhance.Sharpness(processed)
            processed = enhancer.enhance(sharpness_factor)
        
        # エンボス効果
        if contrast > 1.5:
            processed = processed.filter(ImageFilter.EMBOSS)
        
        # 輪郭強調
        if saturation > 1.5:
            processed = processed.filter(ImageFilter.EDGE_ENHANCE_MORE)
        
        return processed
    
    def apply_edge_detection(self, image, brightness, contrast, saturation):
        """エッジ検出を適用"""
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        
        # Cannyエッジ検出
        low_threshold = int(50 * brightness)
        high_threshold = int(150 * contrast)
        edges = cv2.Canny(cv_image, low_threshold, high_threshold)
        
        # エッジを3チャンネルに変換
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        
        # 元画像とエッジを合成
        if saturation > 0.5:
            alpha = min(saturation, 1.0)
            cv_original = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv_original = cv2.cvtColor(cv_original, cv2.COLOR_BGR2RGB)
            blended = cv2.addWeighted(cv_original, 1-alpha, edges_colored, alpha, 0)
            return Image.fromarray(blended)
        else:
            return Image.fromarray(edges_colored)
    
    def apply_noise_processing(self, image, brightness, contrast, saturation):
        """ノイズ処理を適用"""
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # ノイズ除去
        if brightness > 1.0:
            # Non-local Means Denoising
            denoised = cv2.fastNlMeansDenoisingColored(cv_image, None, 10, 10, 7, 21)
            processed = Image.fromarray(cv2.cvtColor(denoised, cv2.COLOR_BGR2RGB))
        else:
            processed = image.copy()
        
        # モルフォロジー演算
        if contrast > 1.0:
            kernel = np.ones((3,3), np.uint8)
            cv_image = cv2.cvtColor(np.array(processed), cv2.COLOR_RGB2BGR)
            cv_image = cv2.morphologyEx(cv_image, cv2.MORPH_CLOSE, kernel)
            processed = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        
        return processed
    
    def apply_color_transformation(self, image, brightness, contrast, saturation):
        """色彩変換を適用"""
        processed = image.copy()
        
        # HSV色空間での操作
        cv_image = cv2.cvtColor(np.array(processed), cv2.COLOR_RGB2HSV)
        
        # 色相シフト
        cv_image[:,:,0] = (cv_image[:,:,0] + int(brightness * 30)) % 180
        
        # 明度調整
        cv_image[:,:,2] = np.clip(cv_image[:,:,2] * contrast, 0, 255)
        
        # 彩度調整
        cv_image[:,:,1] = np.clip(cv_image[:,:,1] * saturation, 0, 255)
        
        processed = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_HSV2RGB))
        return processed
    
    def apply_vintage_effects(self, image, brightness, contrast, saturation):
        """ヴィンテージ効果を適用"""
        processed = image.copy()
        
        # 古い写真風の色調整
        cv_image = cv2.cvtColor(np.array(processed), cv2.COLOR_RGB2BGR)
        
        # 黄色っぽいヴィンテージ感
        cv_image[:,:,0] = np.clip(cv_image[:,:,0] * (0.8 + brightness * 0.2), 0, 255)  # Blue減少
        cv_image[:,:,1] = np.clip(cv_image[:,:,1] * (0.9 + contrast * 0.1), 0, 255)   # Green
        cv_image[:,:,2] = np.clip(cv_image[:,:,2] * (1.0 + saturation * 0.2), 0, 255) # Red増加
        
        # ビネット効果（周辺減光）
        h, w = cv_image.shape[:2]
        center_x, center_y = w // 2, h // 2
        
        # 距離マップ作成
        Y, X = np.ogrid[:h, :w]
        dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
        max_dist = np.sqrt(center_x**2 + center_y**2)
        
        # ビネット強度
        vignette_strength = 0.3 + (saturation - 1.0) * 0.2
        vignette_mask = 1 - (dist_from_center / max_dist) * vignette_strength
        vignette_mask = np.clip(vignette_mask, 0.3, 1.0)
        
        # 各チャンネルに適用
        for i in range(3):
            cv_image[:,:,i] = cv_image[:,:,i] * vignette_mask
        
        processed = Image.fromarray(cv2.cvtColor(cv_image.astype(np.uint8), cv2.COLOR_BGR2RGB))
        return processed


def main():
    """メイン関数"""
    app = ImageProcessorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
