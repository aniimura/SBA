# アーキテクチャ詳細

## パイプライン概要

```
┌─────────────────┐
│  CT/MRI画像     │
│  (DICOM/NIfTI)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ TotalSegmentator│  3D医療画像セグメンテーション
│  (骨格抽出)     │  104クラス対応
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 矢状断RaySum    │  3D→2D投影
│  生成           │  ★課題: 軸判定・向き判定
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ ConvNeXtV2      │  26チャンネル入力
│  (特徴抽出)     │  SOTA CNNアーキテクチャ
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ ヒートマップ    │  各脊椎位置を回帰
│  回帰モデル     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 脊椎番号出力    │  C1非表示/C1除外評価
└─────────────────┘
```

## コンポーネント詳細

### 1. TotalSegmentator

医療画像用3Dセグメンテーションツール。

- **リポジトリ**: wasserth/TotalSegmentator
- **機能**: 104の解剖学的構造をセグメント
- **入力**: CT/MRI画像（NIfTI形式推奨）
- **出力**: セグメンテーションマスク

脊椎関連のセグメントクラス:
- vertebrae_C1〜C7（頸椎）
- vertebrae_T1〜T12（胸椎）
- vertebrae_L1〜L5（腰椎）
- sacrum（仙骨）

### 2. RaySum生成

3Dボリュームから2D矢状断画像を生成。

```python
# 概念的な処理フロー
def generate_raysum(volume_3d, axis='sagittal'):
    # 指定軸方向に投影
    raysum_2d = volume_3d.sum(axis=projection_axis)
    return normalize(raysum_2d)
```

**課題**:
- 軸判定の自動化が必要
- 元データの向きによって結果が不安定

**解決案**:
1. DICOM ImageOrientationPatient活用（推奨）
2. 2D分類モデルで事後補正（フォールバック）

### 3. ConvNeXtV2

Meta AI開発のCNNアーキテクチャ。

- **バージョン**: ConvNeXtV2-Base
- **入力チャンネル**: 26（カスタム）
- **事前学習**: ImageNet
- **出力**: 特徴ベクトル

### 4. ヒートマップ回帰

各脊椎位置をガウシアンヒートマップとして表現。

- **入力**: ConvNeXtV2特徴
- **出力**: 脊椎数分のヒートマップ
- **後処理**: ピーク検出で位置特定

### 5. C1非表示/C1除外評価

C1（環椎）の特殊処理。

- **C1非表示**: 出力からC1を除外
- **C1除外評価**: 評価時にC1を含めない

## DICOM方向情報

### ImageOrientationPatient

DICOMタグ (0020,0037) に格納される方向情報。

```
[Xx, Xy, Xz, Yx, Yy, Yz]

Xx, Xy, Xz: 行方向の単位ベクトル
Yx, Yy, Yz: 列方向の単位ベクトル
```

### 軸判定ロジック（案）

```python
def determine_sagittal_axis(orientation):
    row_vec = orientation[:3]
    col_vec = orientation[3:]
    
    # 外積で法線ベクトル計算
    normal = np.cross(row_vec, col_vec)
    
    # 最大成分の軸が垂直方向
    # 矢状断は左右軸(X)が法線
    if abs(normal[0]) > 0.5:
        return 'sagittal'
    elif abs(normal[1]) > 0.5:
        return 'coronal'
    else:
        return 'axial'
```

## DICOM Locator出力（未実装）

目標: 2D生成画像をスカウト同様の形式で出力。

必要な要素:
- Secondary Capture (SC) SOPクラス
- Locator情報の埋め込み
- PACSとの連携

実装手段:
- pydicomライブラリ使用

## 探索ブランチ: Skellytour

骨格検出ライブラリ。

- **状態**: 評価中
- **mediumモデル**: テスト済み、分離不十分
- **highモデル**: 未テスト
- **課題**: 正常変異での挙動が不安定

**結論**: RaySum出して番号振り直すのが妥当
