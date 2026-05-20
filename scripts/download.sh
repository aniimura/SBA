#!/usr/bin/env bash
# Download Bermuda SBA and Japan ESR regulatory PDFs.
# Run from a machine with outbound internet access to bma.bm and fsa.go.jp.
#
# Usage: bash scripts/download.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BMA_DIR="$REPO_ROOT/docs/bermuda_sba"
FSA_DIR="$REPO_ROOT/docs/japan_solvency"
mkdir -p "$BMA_DIR" "$FSA_DIR"

fetch() {
  local url="$1" out="$2"
  echo ">> $out"
  curl -fL --retry 3 --retry-delay 2 -o "$out" "$url"
}

# ---- Bermuda BMA: SBA / EBS related ----
fetch "https://cdn.bma.bm/documents/2024-03-28-13-20-55-Insurance-Prudential-Standards-Class-C-Class-D-Class-E-Solvency-Requirement-Amendment-Rules-2024.pdf" \
  "$BMA_DIR/Class-C-D-E-Solvency-Amendment-Rules-2024.pdf"

fetch "https://cdn.bma.bm/documents/2024-03-28-13-20-55-Insurance-Prudential-Standards-Group-Solvency-Requirement-Amendment-Rules-2024.pdf" \
  "$BMA_DIR/Group-Solvency-Amendment-Rules-2024.pdf"

fetch "https://cdn.bma.bm/documents/2024-03-28-13-20-54-Insurance-Prudential-Standards-Class-3A-Solvency-Requirement-Amendment-Rules-2024..pdf" \
  "$BMA_DIR/Class-3A-Solvency-Amendment-Rules-2024.pdf"

fetch "https://cdn.bma.bm/documents/2024-03-28-14-21-58-Guidance-Note-for-Statutory-Reporting-Regime-.pdf" \
  "$BMA_DIR/Guidance-Note-Statutory-Reporting-Regime-2024.pdf"

fetch "https://cdn.bma.bm/documents/2025-03-19-11-24-30-Lapse-Liquidity-and-Scenario-Based-Approach-Return---2024-Completion-Instructions.pdf" \
  "$BMA_DIR/Lapse-Liquidity-SBA-Return-2024-Instructions.pdf"

fetch "https://cdn.bma.bm/documents/2024-05-23-13-22-06-2024-Year-End-Long-Term-Instructions-HandbookFinal.pdf" \
  "$BMA_DIR/2024-Year-End-Long-Term-Instructions-Handbook.pdf"

fetch "https://cdn.bma.bm/documents/2024-03-28-13-16-50-2024-Year-End-Insurance-Group-Instructions-Handbook.pdf" \
  "$BMA_DIR/2024-Year-End-Insurance-Group-Instructions-Handbook.pdf"

fetch "https://www.bma.bm/viewPDF/documents/2024-12-02-16-22-05-2024-Year-End-Stress-and-Scenario-Instructions-for-Class-4-3B-and-Insurance-Groups.pdf" \
  "$BMA_DIR/2024-Year-End-Stress-Scenario-Class4-3B-Groups.pdf"

fetch "https://www.bma.bm/viewPDF/documents/2023-07-28-16-11-59-Consultation-Paper---Proposed-Enhancements-to-the-Regulatory-Regime-and-Fees-for-Commercial-Insurers.pdf" \
  "$BMA_DIR/CP2-Proposed-Enhancements-2023-07.pdf"

# ---- Japan FSA: Economic-value-based solvency (ESR) ----
fetch "https://www.fsa.go.jp/policy/economic_value-based_solvency/10.pdf" \
  "$FSA_DIR/ESR_overview_20250723.pdf"

fetch "https://www.fsa.go.jp/news/r7/hoken/20250723/01.pdf" \
  "$FSA_DIR/ESR_publiccomment_result_20250723_01.pdf"

echo "Done. Files saved under docs/."
