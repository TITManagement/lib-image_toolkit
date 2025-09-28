#!/usr/bin/env python3
"""
カーブエディタウィジェット - Curve Editor Widget

0-255範囲のガンマ補正カーブを2次元グラフで編集するためのUIコンポーネント
"""

import tkinter as tk
import customtkinter as ctk
import numpy as np
from typing import List, Tuple, Callable, Optional
from scipy.interpolate import interp1d


class CurveEditor(ctk.CTkFrame):
    """
    ガンマ補正用カーブエディタ
    ...（advanced-image-editor/src/ui/curve_editor.pyの内容を全て展開）...
    """
    def __init__(self, parent, width: int = 255, height: int = 255, 
                 on_curve_change: Optional[Callable] = None):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.on_curve_change = on_curve_change
        self.control_points = [(0, 0), (255, 255)]
        self.selected_point = None
        self.point_radius = 8
        self.grid_color = "black"
        self.curve_color = "black"
        self.point_color = "#ff0000"
        self.selected_point_color = "#ffff00"
        self.is_dragging = False
        self.drag_start_pos = None
        self.drag_start_point = None
        self.click_threshold = 5
        self.update_timer = None
        self.debounce_delay = 100
        self.is_dragging = False
        self._setup_ui()
        self._update_curve()

    def _setup_ui(self):
        self.label = ctk.CTkLabel(self, text="ガンマ補正カーブ")
        self.label.pack(pady=(0, 5))
        self.canvas = tk.Canvas(
            self, 
            width=self.width, 
            height=self.height,
            bg="lightgray",
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(pady=5)
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<Double-Button-1>", self._on_double_click)
        self.canvas.bind("<Button-3>", self._on_right_click)
        self.reset_button = ctk.CTkButton(
            self, 
            text="リセット", 
            width=80,
            command=self._reset_curve
        )
        self.reset_button.pack(pady=5)
        self.info_label = ctk.CTkLabel(self, text="制御点: 2個")
        self.info_label.pack()

    def _canvas_to_curve(self, canvas_x: int, canvas_y: int) -> Tuple[int, int]:
        actual_width = self.canvas.winfo_width()
        actual_height = self.canvas.winfo_height()
        if actual_width <= 1 or actual_height <= 1:
            actual_width = self.width
            actual_height = self.height
        curve_x = max(0, min(255, int(canvas_x)))
        curve_y = max(0, min(255, int(255 - canvas_y)))
        return curve_x, curve_y

    def _curve_to_canvas(self, curve_x: int, curve_y: int) -> Tuple[int, int]:
        canvas_x = max(0, min(255, int(curve_x)))
        canvas_y = max(0, min(255, int(255 - curve_y)))
        return canvas_x, canvas_y

    def _draw_grid(self):
        self.canvas.delete("grid")
        for i in range(1, 4):
            x = int((i * 64 / 255) * self.width)
            self.canvas.create_line(
                x, 0, x, self.height, 
                fill=self.grid_color, 
                width=1, 
                tags="grid"
            )
        for i in range(1, 4):
            y = int(self.height - (i * 64 / 255) * self.height)
            self.canvas.create_line(
                0, y, self.width, y, 
                fill=self.grid_color, 
                width=1, 
                tags="grid"
            )
        self.canvas.create_rectangle(
            0, 0, self.width, self.height, 
            outline=self.grid_color, 
            width=2, 
            tags="grid"
        )

    def _draw_curve(self):
        self.canvas.delete("curve")
        if len(self.control_points) < 2:
            return
        sorted_points = sorted(self.control_points, key=lambda p: p[0])
        x_points = [p[0] for p in sorted_points]
        y_points = [p[1] for p in sorted_points]
        x_interp = np.linspace(0, 255, 256)
        try:
            if len(sorted_points) == 2:
                y_interp = np.interp(x_interp, x_points, y_points)
            else:
                try:
                    f = interp1d(x_points, y_points, kind='cubic', bounds_error=False)
                    y_interp = f(x_interp)
                except ValueError:
                    f = interp1d(x_points, y_points, kind='linear', bounds_error=False)
                    y_interp = f(x_interp)
                y_interp = np.clip(y_interp, 0, 255)
            canvas_points = []
            for i in range(len(x_interp)):
                canvas_x, canvas_y = self._curve_to_canvas(int(x_interp[i]), int(y_interp[i]))
                canvas_points.extend([canvas_x, canvas_y])
            if len(canvas_points) >= 4:
                self.canvas.create_line(
                    canvas_points,
                    fill=self.curve_color,
                    width=1,
                    smooth=True,
                    tags="curve"
                )
        except Exception as e:
            print(f"⚠️ カーブ描画エラー: {e}")
            canvas_points = []
            for point in sorted_points:
                canvas_x, canvas_y = self._curve_to_canvas(point[0], point[1])
                canvas_points.extend([canvas_x, canvas_y])
            if len(canvas_points) >= 4:
                self.canvas.create_line(
                    canvas_points,
                    fill=self.curve_color,
                    width=1,
                    tags="curve"
                )

    def _draw_control_points(self):
        self.canvas.delete("control_points")
        for i, (x, y) in enumerate(self.control_points):
            canvas_x, canvas_y = self._curve_to_canvas(x, y)
            color = self.selected_point_color if i == self.selected_point else self.point_color
            self.canvas.create_oval(
                canvas_x - self.point_radius, canvas_y - self.point_radius,
                canvas_x + self.point_radius, canvas_y + self.point_radius,
                fill=color,
                outline="white",
                width=2,
                tags="control_points"
            )
            self.canvas.create_text(
                canvas_x, canvas_y - self.point_radius - 15,
                text=f"({x},{y})",
                fill="white",
                font=("Arial", 8),
                tags="control_points"
            )

    def _update_curve(self):
        self._draw_grid()
        self._draw_curve()
        self._draw_control_points()
        self.info_label.configure(text=f"制御点: {len(self.control_points)}個")

    def _schedule_callback_update(self):
        if self.update_timer:
            self.after_cancel(self.update_timer)
        self.update_timer = self.after(self.debounce_delay, self._execute_callback)

    def _execute_callback(self):
        self.update_timer = None
        if self.on_curve_change:
            self.on_curve_change(self.get_lut())

    def _find_point_at(self, canvas_x: int, canvas_y: int) -> Optional[int]:
        for i, (x, y) in enumerate(self.control_points):
            point_canvas_x, point_canvas_y = self._curve_to_canvas(x, y)
            distance = ((canvas_x - point_canvas_x) ** 2 + (canvas_y - point_canvas_y) ** 2) ** 0.5
            if distance <= self.point_radius:
                return i
        return None

    def _on_click(self, event):
        self.drag_start_pos = (event.x, event.y)
        clicked_point = self._find_point_at(event.x, event.y)
        if clicked_point is None:
            curve_x, curve_y = self._canvas_to_curve(event.x, event.y)
            self.control_points.append((curve_x, curve_y))
            self._update_curve()
            self.selected_point = None
            self.is_dragging = False
        else:
            self.selected_point = clicked_point
            self.drag_start_point = self.control_points[self.selected_point]
            self.is_dragging = False
        self._schedule_callback_update()

    def _on_drag(self, event):
        if (self.selected_point is not None and self.drag_start_pos is not None and 
            self.drag_start_point is not None):
            dx = event.x - self.drag_start_pos[0]
            dy = event.y - self.drag_start_pos[1]
            move_distance = (dx * dx + dy * dy) ** 0.5
            if move_distance > self.click_threshold:
                if not self.is_dragging:
                    self.is_dragging = True
                curve_x, curve_y = self._canvas_to_curve(event.x, event.y)
                final_point = (curve_x, curve_y)
                self.control_points[self.selected_point] = final_point
                self._update_curve()
                self._schedule_callback_update()

    def _on_release(self, event):
        if self.is_dragging:
            self.is_dragging = False
            self.selected_point = None
            self.drag_start_pos = None
            self.drag_start_point = None
            self._update_curve()
            if self.update_timer:
                self.after_cancel(self.update_timer)
                self.update_timer = None
            self._execute_callback()

    def _on_double_click(self, event):
        curve_x, curve_y = self._canvas_to_curve(event.x, event.y)
        for x, y in self.control_points:
            if abs(x - curve_x) < 10 and abs(y - curve_y) < 10:
                return
        self.control_points.append((curve_x, curve_y))
        self._update_curve()

    def _on_right_click(self, event):
        point_index = self._find_point_at(event.x, event.y)
        if point_index is not None and len(self.control_points) > 2:
            if point_index != 0 and point_index != len(self.control_points) - 1:
                self.control_points.pop(point_index)
                self._update_curve()
                self._execute_callback()

    def _reset_curve(self):
        self.control_points = [(0, 0), (255, 255)]
        self.selected_point = None
        self.is_dragging = False
        self.drag_start_pos = None
        self.drag_start_point = None
        self._update_curve()
        self._execute_callback()

    def get_lut(self) -> np.ndarray:
        try:
            sorted_points = sorted(self.control_points, key=lambda p: p[0])
            x_points = [p[0] for p in sorted_points]
            y_points = [p[1] for p in sorted_points]
            x_values = np.arange(256)
            if len(sorted_points) == 2:
                lut = np.interp(x_values, x_points, y_points)
            else:
                try:
                    f = interp1d(x_points, y_points, kind='cubic', bounds_error=False)
                    lut = f(x_values)
                except ValueError:
                    f = interp1d(x_points, y_points, kind='linear', bounds_error=False)
                    lut = f(x_values)
            lut = np.clip(lut, 0, 255).astype(np.uint8)
            return lut
        except Exception as e:
            return np.arange(256, dtype=np.uint8)

    def set_curve(self, control_points: List[Tuple[int, int]]):
        if len(control_points) >= 2:
            self.control_points = control_points.copy()
            self.selected_point = None
            self.is_dragging = False
            self.drag_start_pos = None
            self.drag_start_point = None
            self._update_curve()

    def get_curve(self) -> List[Tuple[int, int]]:
        return self.control_points.copy()
