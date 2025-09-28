import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# image_toolkit import動作検証用テストスクリプト

def main():
    try:
        from image_toolkit import BasicGuiApp, ExtendedGuiApp, ImageProcessorApp
        from image_toolkit.widgets.scalable_widgets import ScalableLabel, StyledButton
        from image_toolkit.core.font_manager import FontManager
        from image_toolkit.core.style_manager import StyleManager
        from image_toolkit.layouts.tab_mode import TabLayout

        print("image_toolkitのimportは成功しました。")
        print("BasicGuiApp:", BasicGuiApp)
        print("ScalableLabel:", ScalableLabel)
        print("FontManager:", FontManager)
        print("StyleManager:", StyleManager)
        print("TabLayout:", TabLayout)
    except Exception as e:
        print("importエラー:", e)

if __name__ == "__main__":
    main()
