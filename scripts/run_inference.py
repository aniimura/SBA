#!/usr/bin/env python3
"""
脊椎番号付け推論CLIスクリプト

Usage:
    python scripts/run_inference.py /path/to/input.dcm -o output.json
    python scripts/run_inference.py /path/to/input.nii.gz --include-c1
"""

import argparse
import sys
from pathlib import Path

# パッケージのインポートパスを追加
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from spine_num.inference import run_inference


def main():
    parser = argparse.ArgumentParser(
        description="脊椎番号付け推論を実行する",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "input",
        type=str,
        help="入力ファイルパス（DICOM or NIfTI）",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="出力JSONファイルパス（省略時は標準出力）",
    )
    parser.add_argument(
        "--checkpoint-dir",
        type=str,
        default=None,
        help="モデルcheckpointのディレクトリ",
    )
    parser.add_argument(
        "--include-c1",
        action="store_true",
        help="C1（環椎）を出力に含める",
    )

    args = parser.parse_args()

    try:
        result = run_inference(
            input_path=args.input,
            checkpoint_dir=args.checkpoint_dir,
            exclude_c1=not args.include_c1,
        )

        json_output = result.to_json()

        if args.output:
            output_path = Path(args.output)
            output_path.write_text(json_output, encoding="utf-8")
            print(f"Results saved to: {output_path}")
        else:
            print(json_output)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
