"""
パッケージセットアップ・インストール設定ファイル

【機能仕様】
    install_requires=[
        "customtkinter>=5.0.0",
        "Pillow>=9.0.0",
        "opencv-python>=4.7.0",
        "numpy>=1.21.0",
        "gui-framework @ git+https://github.com/TITManagement/lib.git"
    ],
    entry_points={
        "console_scripts": [
            "imagegui=launchers.start_basic:main",
            "imagegui-extended=launchers.start_extended:main",
            "image-processor=launchers.start_image_processor:main"
        ]
    },_gui_app パッケージのインストール・配布設定
■ アーキテクチャ: 設定・補助ファイル（パッケージ管理）
■ 機能:
  - パッケージメタデータ定義（名前、バージョン、作者等）
  - 依存関係管理（CustomTkinter, Pillow, gui_framework）
  - パッケージ検出（find_packages()による自動検出）
  - パッケージデータ含有（*.json, *.md, プラグイン等）
  - コンソールエントリーポイント定義:
    * imagegui: launchers.start_basic の main() 関数を呼び出し
    * imagegui-extended: launchers.start_extended の main() 関数を呼び出し
  - Python バージョン互換性（3.7以上）
  - PyPI 分類子（開発ステータス、対象ユーザー、ライセンス等）
■ 使用方法:
  - pip install . (ローカルインストール)
  - pip install -e . (開発モードインストール)
  - python setup.py sdist bdist_wheel (配布パッケージ作成)
■ インストール後の利用:
  - imagegui コマンドで基本アプリ起動
  - imagegui-extended コマンドで拡張アプリ起動
■ 対象ユーザー: 開発者、システム管理者、パッケージ管理者
"""
from setuptools import setup, find_packages

setup(
    name="image_toolkit",
    version="1.0.0",
    packages=find_packages(),
    package_data={
        "": ["*.json", "*.md"],
        "plugins": ["*.py"],
        "layouts": ["*.py"],
        "widgets": ["*.py"],
    },
    include_package_data=True,
    install_requires=[
        "customtkinter>=5.2.0",
        "Pillow>=9.0.0",
        "opencv-python>=4.7.0",
        "numpy>=1.21.0",
        "pyzbar>=0.1.8",
        "pandas>=2.0.0",
        "setuptools>=60.0.0"
    ],
    entry_points={
        "console_scripts": [
            "imagegui=image_toolkit.apps.gui_basic:main",
            "imagegui-extended=image_toolkit.apps.gui_extended:main",
            "image-processor=image_toolkit.apps.gui_image_processor:main"
        ]
    },
    python_requires=">=3.7",
    author="TITManagement",
    description="画像処理アプリケーション用の汎用GUIライブラリ（CustomTkinterベース）",
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)