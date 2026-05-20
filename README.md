# Regulatory Documents: Bermuda SBA & Japan ESR

保険会社の経済価値ベース健全性規制に関する公式資料のインデックス。

- **`docs/bermuda_sba/`** — Bermuda Monetary Authority (BMA) の Scenario-Based
  Approach (SBA) 関連規則・ガイダンス。2024年3月31日施行の改正に対応。
- **`docs/japan_solvency/`** — 金融庁の経済価値ベースのソルベンシー規制
  (ESR 規制) 関連告示・施行規則。2025年7月23日公布、2026年3月31日適用。

各ディレクトリの `README.md` に文書一覧と直接 URL を掲載。

## PDF の取得

```bash
bash scripts/download.sh
```

`bma.bm` および `fsa.go.jp` への HTTPS アウトバウンドが必要。

> **注**: このリポジトリの作成環境ではネットワークポリシーにより
> `bma.bm` / `fsa.go.jp` への接続がブロックされていたため、PDF 本体は
> コミットしていません。インターネット接続のある端末で上記スクリプトを
> 実行してください。
