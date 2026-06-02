"""
DICOM処理ユーティリティ

DICOMファイルの読み込み、方向情報の解析、出力生成を行う
"""

from typing import Tuple, Literal
import numpy as np


def parse_image_orientation(orientation: list[float]) -> dict:
    """
    ImageOrientationPatient (0020,0037) を解析する

    Args:
        orientation: [Xx, Xy, Xz, Yx, Yy, Yz] の6要素リスト

    Returns:
        dict: row_vector, col_vector, normal_vector を含む辞書
    """
    row_vec = np.array(orientation[:3])
    col_vec = np.array(orientation[3:])
    normal_vec = np.cross(row_vec, col_vec)

    return {
        "row_vector": row_vec,
        "col_vector": col_vec,
        "normal_vector": normal_vec,
    }


def determine_plane_type(
    orientation: list[float],
) -> Literal["sagittal", "coronal", "axial", "oblique"]:
    """
    DICOM方向情報から画像の断面タイプを判定する

    Args:
        orientation: ImageOrientationPatient値

    Returns:
        断面タイプ ("sagittal", "coronal", "axial", "oblique")
    """
    parsed = parse_image_orientation(orientation)
    normal = parsed["normal_vector"]

    # 法線ベクトルの最大成分で判定
    abs_normal = np.abs(normal)
    max_idx = np.argmax(abs_normal)
    max_val = abs_normal[max_idx]

    # 閾値: 0.8以上で主要軸と判定
    if max_val < 0.8:
        return "oblique"

    # X軸(左右): 矢状断、Y軸(前後): 冠状断、Z軸(上下): 軸位断
    if max_idx == 0:
        return "sagittal"
    elif max_idx == 1:
        return "coronal"
    else:
        return "axial"


def get_sagittal_projection_axis(orientation: list[float]) -> int:
    """
    矢状断RaySum生成のための投影軸を決定する

    Args:
        orientation: ImageOrientationPatient値

    Returns:
        投影軸のインデックス (0, 1, or 2)
    """
    parsed = parse_image_orientation(orientation)
    normal = parsed["normal_vector"]

    # 矢状断を得るにはX軸方向に投影
    # 法線がX軸に近い場合はそのまま、そうでなければ最もX軸に近い軸を選択
    abs_normal = np.abs(normal)

    # X成分が最大なら法線方向に投影
    if np.argmax(abs_normal) == 0:
        return 0

    # それ以外はX軸(左右)方向を投影軸とする
    return 0


def estimate_orientation_from_volume(volume: np.ndarray) -> Tuple[int, bool]:
    """
    ボリュームデータから矢状断の向きを推定する（フォールバック用）

    DICOM方向情報が利用できない場合に使用。
    形状ヒューリスティクスで推定を試みる。

    Args:
        volume: 3D numpy配列

    Returns:
        (projection_axis, needs_flip): 投影軸と反転が必要かのタプル
    """
    shape = volume.shape

    # 一般的なCT/MRIでは最も小さい次元が左右方向
    min_axis = np.argmin(shape)

    # 反転判定は実データでの検証が必要
    needs_flip = False

    return min_axis, needs_flip
