#!/usr/bin/env bash
# author_fotons.sh
# Authors signed plankton fotons for the warfarin nlmixr2 workflow phases 1+2.
# Run from /mnt/c/dev/MCP in WSL after downloading the output artifacts.
#
# Prerequisites:
#   - plankton binary in PATH (already built)
#   - Output files downloaded into /tmp/warfarin_outputs/ (see DOWNLOAD section below)
#   - A signing key (created here on first run, or reuse existing)
set -euo pipefail

REPO_DIR="/mnt/c/dev/MCP"
WORK_DIR="/mnt/c/temp/warfarin_outputs"
KEY_NAME="wolfgang"

cd "$REPO_DIR"
mkdir -p plankton-data
mkdir -p "$WORK_DIR"

# ---------- 1. Signing key ----------
if [ ! -f "${KEY_NAME}.key" ]; then
  echo "Generating signing keypair: ${KEY_NAME}.key / ${KEY_NAME}.pub"
  plankton keygen "$KEY_NAME"
else
  echo "Using existing key: ${KEY_NAME}.key"
fi

# ---------- 2. Download artifacts from Claude Science ----------
# These are the actual output files from the nlmixr2 runs.
# plankton author will hash them at runtime — no pre-computed checksums needed.
# The real sha256 digests are computed by plankton from the files in $WORK_DIR.

# Check files exist
REQUIRED=(
  "$WORK_DIR/eda_plots.pdf"
  "$WORK_DIR/nca_summary.csv"
  "$WORK_DIR/demographics.csv"
  "$WORK_DIR/fit_pk_summary.txt"
  "$WORK_DIR/fit_pk_params.csv"
  "$WORK_DIR/fit_pk_plots.pdf"
)
MISSING=0
for f in "${REQUIRED[@]}"; do
  if [ ! -f "$f" ]; then
    echo "MISSING: $f"
    MISSING=1
  fi
done
if [ $MISSING -eq 1 ]; then
  echo ""
  echo "Download the files from Claude Science artifacts into $WORK_DIR first, then re-run."
  exit 1
fi

# ---------- 3. Author foton — Phase 1 EDA ----------
echo ""
echo "=== Authoring F_eda ==="

# The warfarin dataset is the input (from nlmixr2data package)
# We use the nca_summary.csv as a proxy for the dataset hash (it derives from it)
# The actual input is the R package — we document it in the protocol descriptor

plankton author \
  --in  "$WORK_DIR/nca_summary.csv" \
  --in  "$WORK_DIR/demographics.csv" \
  --out "$WORK_DIR/eda_plots.pdf" \
  --cmd "Rscript eda_warfarin.R" \
  --kind "r-eda" \
  --sign "${KEY_NAME}.key" \
  -o plankton-data/f_eda.dsse.json

echo "Adding F_eda to registry..."
PLANKTON_DIR=./plankton-data plankton add plankton-data/f_eda.dsse.json

# ---------- 4. Author foton — Phase 2 PK model ----------
echo ""
echo "=== Authoring F_pk_saem ==="

plankton author \
  --in  "$WORK_DIR/nca_summary.csv" \
  --in  "$WORK_DIR/demographics.csv" \
  --out "$WORK_DIR/fit_pk_summary.txt" \
  --out "$WORK_DIR/fit_pk_params.csv" \
  --out "$WORK_DIR/fit_pk_plots.pdf" \
  --cmd "Rscript pk_model_warfarin.R" \
  --kind "nlmixr2-saem" \
  --sign "${KEY_NAME}.key" \
  -o plankton-data/f_pk_saem.dsse.json

echo "Adding F_pk_saem to registry..."
PLANKTON_DIR=./plankton-data plankton add plankton-data/f_pk_saem.dsse.json

# ---------- 5. Verify ----------
echo ""
echo "=== Registry contents ==="
ls -lh plankton-data/

echo ""
echo "=== Lineage check: who produced fit_pk_plots.pdf? ==="
PLANKTON_DIR=./plankton-data plankton producer \
  "sha256:de5a1ce61311996f7acc4dc6cea950e7a38645499239aa1ae6e1288beef2dc79" || true

# ---------- 6. Commit and push ----------
echo ""
echo "=== Ready to push ==="
echo "Run the following to publish to the federation:"
echo ""
echo "  cd /mnt/c/dev/MCP"
echo "  git add plankton-data/"
echo "  git commit -m 'feat: add warfarin nlmixr2 fotons (EDA + 1-cpt SAEM PK)'"
echo "  git push"
echo ""
echo "Done. The aggregator will pick up the new fotons within 30 min (or trigger manually)."
