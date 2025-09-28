# Launchers Directory - ランチャーファイル使い分けガイド

## 📁 ディレクトリ構成と役割

```
launchers/
├── start_basic.py           # 基本GUIアプリ専用ランチャー
├── start_extended.py        # 拡張GUIアプリ専用ランチャー  
├── start_image_processor.py # 画像処理アプリ専用ランチャー
└── start_runner.py         # 統合ランチャー（全アプリ対応）
```

## 🎯 各ランチャーの使い分け

### 1. `start_basic.py` - 基本GUIアプリランチャー

**用途**: シンプルなGUIアプリケーションを起動
**対象アプリ**: `apps/gui_basic.py` の `BasicGuiApp`

```bash
# 直接起動
python launchers/start_basic.py

# パッケージインストール後
imagegui
```

**特徴**:
- ✅ 軽量でシンプル
- ✅ 基本的なCustomTkinter設定のみ
- ✅ 初心者向け
- ❌ プラグイン機能なし
- ❌ 高度な設定管理なし

**適用場面**:
- プロトタイプ開発
- シンプルなUIテスト
- 基本機能のデモ

---

### 2. `start_extended.py` - 拡張GUIアプリランチャー

**用途**: プラグイン対応の高機能GUIアプリケーションを起動
**対象アプリ**: `apps/gui_extended.py` の `ExtendedGuiApp`

```bash
# 直接起動
python launchers/start_extended.py

# パッケージインストール後
imagegui-extended
```

**特徴**:
- ✅ プラグインシステム搭載
- ✅ 複数レイアウト対応（タブ、ツールバー）
- ✅ 高度な設定管理
- ✅ 外部ライブラリ（gui_framework）統合
- ✅ 商用レベルの機能性

**適用場面**:
- 本格的なアプリケーション開発
- プラグイン拡張が必要なシステム
- 企業向けソフトウェア
- 複雑なワークフロー管理

---

### 3. `start_image_processor.py` - 画像処理アプリランチャー

**用途**: 高度な画像処理に特化したアプリケーションを起動
**対象アプリ**: `apps/gui_image_processor.py` の `ImageProcessorApp`

```bash
# 直接起動
python launchers/start_image_processor.py

# パッケージインストール後
image-processor
```

**特徴**:
- ✅ 8種類の高度画像処理カテゴリ
- ✅ リアルタイムプレビュー
- ✅ 原画像・処理後画像の並列表示
- ✅ OpenCV・NumPy統合
- ✅ ディレクトリ一括処理
- ✅ 専門的な画像編集機能

**適用場面**:
- 写真編集・レタッチ
- 画像解析・研究
- クリエイティブワーク
- バッチ画像処理

---

### 4. `start_runner.py` - 統合ランチャー 🎯

**用途**: 全アプリケーションを統一インターフェースで起動
**対象**: 上記3つのアプリ全て

```bash
# 基本アプリ起動
python launchers/start_runner.py basic

# 拡張アプリ起動  
python launchers/start_runner.py extended

# 画像処理アプリ起動
python launchers/start_runner.py processor

# ヘルプ表示
python launchers/start_runner.py --help
```

**特徴**:
- ✅ 単一エントリーポイント
- ✅ コマンドライン引数対応
- ✅ 詳細なヘルプメッセージ
- ✅ エラーハンドリング充実
- ✅ バージョン管理統合

**適用場面**:
- 複数アプリの切り替え使用
- スクリプト化・自動化
- CI/CD環境での起動
- デモンストレーション

## 🛠️ 開発者向け推奨事項

### 開発フェーズ別の使い分け

1. **プロトタイプ段階**: `start_basic.py`
   - 素早い機能検証
   - シンプルなUI実装

2. **機能拡張段階**: `start_extended.py`
   - プラグイン開発
   - 高度な機能実装

3. **専門用途開発**: `start_image_processor.py`
   - 画像処理機能の開発・テスト
   - OpenCV機能の検証

4. **統合テスト・運用**: `start_runner.py`
   - 全体的な動作確認
   - ユーザー向け提供

### コマンド別クイックリファレンス

```bash
# 開発中の素早いテスト
python launchers/start_basic.py

# プラグイン機能のテスト
python launchers/start_extended.py

# 画像処理機能のテスト
python launchers/start_image_processor.py

# 統合的な操作・デモ
python launchers/start_runner.py [basic|extended|processor]
```

## 📋 依存関係マトリックス

| ランチャー | GUI Framework | OpenCV/NumPy | プラグイン | 設定管理 |
|-----------|---------------|--------------|------------|----------|
| basic     | 間接利用      | ❌           | ❌         | 基本     |
| extended  | 完全統合      | ❌           | ✅         | 高度     |
| processor | ❌            | ✅           | ❌         | 基本     |
| runner    | 全て対応      | 全て対応     | 全て対応   | 全て対応 |

この構成により、用途に応じた最適なアプリケーション選択が可能になっています。
