"""
推論モジュールのテスト
"""

import pytest
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from spine_num.inference import (
    run_inference,
    InferenceResult,
    SpineLabel,
    _generate_placeholder_labels,
)


class TestSpineLabel:
    def test_creation(self):
        label = SpineLabel(name="T5", y_position=100.0, confidence=0.95)
        assert label.name == "T5"
        assert label.y_position == 100.0
        assert label.confidence == 0.95


class TestInferenceResult:
    def test_to_dict(self):
        labels = [
            SpineLabel(name="C2", y_position=10.0, confidence=0.9),
            SpineLabel(name="C3", y_position=30.0, confidence=0.85),
        ]
        result = InferenceResult(
            labels=labels,
            image_path="/path/to/image.dcm",
            model_version="1.0.0",
            exclude_c1=True,
        )

        d = result.to_dict()
        assert len(d["labels"]) == 2
        assert d["labels"][0]["name"] == "C2"
        assert d["image_path"] == "/path/to/image.dcm"
        assert d["model_version"] == "1.0.0"
        assert d["exclude_c1"] is True

    def test_to_json(self):
        labels = [SpineLabel(name="L1", y_position=200.0, confidence=0.88)]
        result = InferenceResult(
            labels=labels,
            image_path="/path/to/image.nii",
            model_version="1.0.0",
            exclude_c1=False,
        )

        json_str = result.to_json()
        assert "L1" in json_str
        assert "200.0" in json_str


class TestPlaceholderLabels:
    def test_exclude_c1(self):
        labels = _generate_placeholder_labels(exclude_c1=True)
        names = [l.name for l in labels]
        assert "C1" not in names
        assert "C2" in names
        assert "L5" in names

    def test_include_c1(self):
        labels = _generate_placeholder_labels(exclude_c1=False)
        names = [l.name for l in labels]
        assert "C1" in names
        assert "C2" in names
        assert "L5" in names


class TestRunInference:
    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            run_inference("/nonexistent/path/to/file.dcm")

    def test_unsupported_format(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(b"test")
            temp_path = f.name

        with pytest.raises(ValueError, match="Unsupported file format"):
            run_inference(temp_path)

        Path(temp_path).unlink()

    def test_placeholder_inference_dcm(self):
        with tempfile.NamedTemporaryFile(suffix=".dcm", delete=False) as f:
            f.write(b"dummy dicom content")
            temp_path = f.name

        result = run_inference(temp_path, exclude_c1=True)

        assert isinstance(result, InferenceResult)
        assert result.exclude_c1 is True
        assert len(result.labels) > 0
        assert "C1" not in [l.name for l in result.labels]

        Path(temp_path).unlink()
