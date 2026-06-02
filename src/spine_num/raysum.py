"""
RaySum生成モジュール

3Dボリュームから2D矢状断画像を生成する
"""

import numpy as np
from typing import Optional, Tuple


def generate_raysum(
    volume: np.ndarray,
    projection_axis: int = 0,
    normalize: bool = True,
) -> np.ndarray:
    """
    3Dボリュームから2D RaySum画像を生成する

    Args:
        volume: 3D numpy配列 (D, H, W) or (H, W, D)
        projection_axis: 投影軸 (0, 1, or 2)
        normalize: 正規化するかどうか

    Returns:
        2D numpy配列 (RaySum画像)
    """
    # 指定軸方向に総和を取る
    raysum = np.sum(volume, axis=projection_axis)

    if normalize:
        raysum = normalize_image(raysum)

    return raysum


def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    画像を0-1の範囲に正規化する

    Args:
        image: 入力画像

    Returns:
        正規化された画像
    """
    min_val = image.min()
    max_val = image.max()

    if max_val - min_val < 1e-8:
        return np.zeros_like(image, dtype=np.float32)

    normalized = (image - min_val) / (max_val - min_val)
    return normalized.astype(np.float32)


def apply_orientation_correction(
    raysum: np.ndarray,
    flip_horizontal: bool = False,
    flip_vertical: bool = False,
    rotate_90: int = 0,
) -> np.ndarray:
    """
    RaySum画像の向きを補正する

    Args:
        raysum: 2D RaySum画像
        flip_horizontal: 水平反転
        flip_vertical: 垂直反転
        rotate_90: 90度回転の回数 (0-3)

    Returns:
        補正された画像
    """
    result = raysum.copy()

    if flip_horizontal:
        result = np.flip(result, axis=1)

    if flip_vertical:
        result = np.flip(result, axis=0)

    if rotate_90 > 0:
        result = np.rot90(result, k=rotate_90)

    return result


def generate_multichannel_raysum(
    segmentation_masks: dict[str, np.ndarray],
    projection_axis: int = 0,
) -> np.ndarray:
    """
    セグメンテーションマスクから26チャンネルRaySumを生成する

    Args:
        segmentation_masks: 構造名をキーとするマスク辞書
        projection_axis: 投影軸

    Returns:
        (26, H, W) の多チャンネル画像
    """
    # TotalSegmentatorの脊椎関連クラス
    vertebrae_classes = [
        "vertebrae_C1", "vertebrae_C2", "vertebrae_C3", "vertebrae_C4",
        "vertebrae_C5", "vertebrae_C6", "vertebrae_C7",
        "vertebrae_T1", "vertebrae_T2", "vertebrae_T3", "vertebrae_T4",
        "vertebrae_T5", "vertebrae_T6", "vertebrae_T7", "vertebrae_T8",
        "vertebrae_T9", "vertebrae_T10", "vertebrae_T11", "vertebrae_T12",
        "vertebrae_L1", "vertebrae_L2", "vertebrae_L3", "vertebrae_L4",
        "vertebrae_L5",
        "sacrum",
    ]

    channels = []
    for class_name in vertebrae_classes:
        if class_name in segmentation_masks:
            mask = segmentation_masks[class_name]
            raysum = generate_raysum(mask, projection_axis, normalize=True)
        else:
            # マスクがない場合はゼロ画像
            # 形状は他のマスクから推定（実装時に要調整）
            raysum = None
        channels.append(raysum)

    # 形状を揃えてスタック
    # 実装時: 全てのraySumがNoneでないことを確認し、形状を統一
    valid_channels = [c for c in channels if c is not None]
    if not valid_channels:
        raise ValueError("No valid segmentation masks provided")

    target_shape = valid_channels[0].shape
    result_channels = []

    for ch in channels:
        if ch is None:
            result_channels.append(np.zeros(target_shape, dtype=np.float32))
        else:
            result_channels.append(ch)

    return np.stack(result_channels, axis=0)
