"""
推論エントリーポイント

単一ケースの脊椎番号付け推論を実行する
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import json


@dataclass
class SpineLabel:
    """脊椎ラベル"""

    name: str  # e.g., "C1", "T5", "L3"
    y_position: float  # 画像内のY座標（上端が0）
    confidence: float  # 信頼度スコア (0-1)


@dataclass
class InferenceResult:
    """推論結果"""

    labels: list[SpineLabel]
    image_path: str
    model_version: str
    exclude_c1: bool

    def to_dict(self) -> dict:
        """辞書形式に変換"""
        return {
            "labels": [
                {
                    "name": label.name,
                    "y_position": label.y_position,
                    "confidence": label.confidence,
                }
                for label in self.labels
            ],
            "image_path": self.image_path,
            "model_version": self.model_version,
            "exclude_c1": self.exclude_c1,
        }

    def to_json(self) -> str:
        """JSON文字列に変換"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


def run_inference(
    input_path: str | Path,
    checkpoint_dir: Optional[str | Path] = None,
    exclude_c1: bool = True,
) -> InferenceResult:
    """
    単一ケースの脊椎番号付け推論を実行する

    Args:
        input_path: 入力ファイルパス（DICOM/NIfTI）
        checkpoint_dir: モデルcheckpointのディレクトリ
        exclude_c1: C1（環椎）を出力から除外するか

    Returns:
        InferenceResult: 推論結果

    Raises:
        FileNotFoundError: 入力ファイルが存在しない
        ValueError: サポートされていないファイル形式
    """
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # ファイル形式の判定
    suffix = input_path.suffix.lower()
    if suffix == ".dcm":
        file_type = "dicom"
    elif suffix in [".nii", ".gz"]:
        file_type = "nifti"
    else:
        raise ValueError(f"Unsupported file format: {suffix}")

    # TODO: 実際の推論パイプラインを実装
    # 1. ファイル読み込み
    # 2. TotalSegmentatorでセグメンテーション
    # 3. DICOM方向情報の取得・軸判定
    # 4. RaySum生成
    # 5. ConvNeXtV2で特徴抽出
    # 6. ヒートマップ回帰で位置推定
    # 7. ラベル生成

    # プレースホルダー結果
    labels = _generate_placeholder_labels(exclude_c1)

    return InferenceResult(
        labels=labels,
        image_path=str(input_path),
        model_version="0.1.0-placeholder",
        exclude_c1=exclude_c1,
    )


def _generate_placeholder_labels(exclude_c1: bool) -> list[SpineLabel]:
    """プレースホルダーのラベルを生成（開発用）"""
    all_vertebrae = [
        "C1", "C2", "C3", "C4", "C5", "C6", "C7",
        "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12",
        "L1", "L2", "L3", "L4", "L5",
    ]

    if exclude_c1:
        all_vertebrae = all_vertebrae[1:]  # C1を除外

    labels = []
    for i, name in enumerate(all_vertebrae):
        labels.append(
            SpineLabel(
                name=name,
                y_position=float(i * 20),  # プレースホルダー座標
                confidence=0.0,  # プレースホルダー
            )
        )

    return labels


# パイプラインコンポーネント（未実装）


def _load_volume(path: Path, file_type: str):
    """ボリュームデータを読み込む"""
    raise NotImplementedError("Volume loading not implemented")


def _run_total_segmentator(volume):
    """TotalSegmentatorを実行する"""
    raise NotImplementedError("TotalSegmentator integration not implemented")


def _get_dicom_orientation(path: Path):
    """DICOM方向情報を取得する"""
    raise NotImplementedError("DICOM orientation extraction not implemented")


def _generate_raysum_from_segmentation(segmentation, orientation):
    """セグメンテーションからRaySumを生成する"""
    raise NotImplementedError("RaySum generation not implemented")


def _run_convnext_feature_extraction(raysum):
    """ConvNeXtV2で特徴抽出する"""
    raise NotImplementedError("ConvNeXtV2 feature extraction not implemented")


def _run_heatmap_regression(features):
    """ヒートマップ回帰を実行する"""
    raise NotImplementedError("Heatmap regression not implemented")


def _extract_labels_from_heatmap(heatmap, exclude_c1: bool):
    """ヒートマップからラベルを抽出する"""
    raise NotImplementedError("Label extraction not implemented")
