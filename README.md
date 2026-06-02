# Spine_Num D2

医療画像（CT/MRI）から脊椎番号を自動で付与するシステム

## 概要

このリポジトリは、脊椎番号自動付与システム（Spine_Num D2）の実装候補の仕様・参照コード・DICOM localizer化に向けたAI側入出力を整理したものです。

現時点では production-ready package ではなく、reference implementation + documentation の段階です。

## アーキテクチャ

```
CT/MRI画像 → TotalSegmentator → 矢状断RaySum生成 → ConvNeXtV2(26ch) → ヒートマップ回帰 → 脊椎番号出力
(DICOM/NIfTI)    (骨格抽出)       (3D→2D投影)      (特徴抽出)        (位置推定)
```

### 主要コンポーネント

| コンポーネント | 役割 | 状態 |
|---------------|------|------|
| TotalSegmentator | 3D医療画像セグメンテーション | 採用 |
| ConvNeXtV2 (26ch) | 特徴抽出 | 採用 |
| ヒートマップ回帰 | 脊椎位置推定 | 採用 |
| Skellytour | 骨格検出（探索中） | 評価中 |

## ディレクトリ構成

```
.
├── README.md                 # 本ファイル
├── docs/
│   ├── model_registry.md     # モデルcheckpoint管理
│   └── architecture.md       # 詳細アーキテクチャ
├── src/
│   └── spine_num/            # メインパッケージ
│       ├── __init__.py
│       ├── inference.py      # 推論エントリーポイント
│       ├── raysum.py         # RaySum生成
│       └── dicom_utils.py    # DICOM処理ユーティリティ
├── scripts/
│   └── run_inference.py      # CLIスクリプト
└── tests/
    └── test_inference.py     # テスト
```

## 未解決課題

1. **軸判定・向き判定の自動化** - TotalSegmentatorからRaySum生成時の課題
2. **RaySum投影方向の不整合** - 元データにより結果が不安定
3. **DICOM locator形式出力** - 完全未着手

## 開発方針

- 現行本線（TotalSegmentator + ConvNeXtV2）を優先
- Skellytourは並行評価（highモデルで追加検証）
- 軸判定問題はDICOM方向情報活用を第一候補

## データ・モデル管理

- 実データ（DICOM/NIfTI、PNG）は含めない
- checkpointは別途共有ストレージで管理し、`docs/model_registry.md`に記録

## ライセンス

TBD
