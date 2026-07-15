#!/usr/bin/env bash
# author_claims.sh
# Authors signed nekton claims attesting to the plankton fotons in plankton-data/
# (see author_fotons.sh). Run from /mnt/c/dev/MCP in WSL.
#
# Prerequisites:
#   - nekton binary in PATH (build from plankton/plankton/nekton/reference:
#       cd plankton/plankton/nekton/reference && go build -o ~/gopath/bin/nekton ./cmd/nekton)
#   - wolfgang.key (same Ed25519 keypair used for plankton fotons — nekton's keyid
#     scheme is byte-identical to plankton's, so the same key signs both)
set -euo pipefail

REPO_DIR="/mnt/c/dev/MCP"
KEY_NAME="wolfgang"
WHEN="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

cd "$REPO_DIR"
mkdir -p nekton-data

# Foton ids (the action-key hash plankton assigned each foton — from `plankton producer <output-hash>`)
# Corrected 2026-07-15: the original fotons (b2629b72.../7e9e0528...) were authored with the
# wrong predicateType (kton.dev/foton/v0 instead of plankton.dev/foton/v0) and absolute paths,
# so kton mirror silently skipped them. Re-authored via author_fotons.sh with relative paths —
# these are the correct ids.
EDA_FOTON="sha256:b8d48ed1410bb4ed7c85e7d5ce747cdbf20a011352f5d95bb5b2f15820c9d2a5"
PK_FOTON="sha256:f3a2740adcebfc607c29aca82d9276da22e1a165da46ceeb443a05645aca7ab8"

# ---------- 1. Claim — authored F_eda ----------
cat > /tmp/claim_eda.json <<EOF
{
  "subject": [{"hash": "${EDA_FOTON}"}],
  "predicate": "https://kton.dev/v/authored",
  "by": "${KEY_NAME}",
  "when": "${WHEN}",
  "why": "Authored the warfarin EDA foton (Rscript eda_warfarin.R) from nca_summary.csv + demographics.csv"
}
EOF
nekton claim /tmp/claim_eda.json "${KEY_NAME}.key" nekton-data/c_eda_authored.dsse.json

# ---------- 2. Claim — authored F_pk_saem ----------
cat > /tmp/claim_pk.json <<EOF
{
  "subject": [{"hash": "${PK_FOTON}"}],
  "predicate": "https://kton.dev/v/authored",
  "by": "${KEY_NAME}",
  "when": "${WHEN}",
  "why": "Authored the 1-compartment SAEM PK fit foton (Rscript pk_model_warfarin.R) from nca_summary.csv + demographics.csv"
}
EOF
nekton claim /tmp/claim_pk.json "${KEY_NAME}.key" nekton-data/c_pk_saem_authored.dsse.json
rm -f /tmp/claim_eda.json /tmp/claim_pk.json

# ---------- 3. Register into the registry ----------
NEKTON_DIR=./nekton-data nekton add nekton-data/c_eda_authored.dsse.json
NEKTON_DIR=./nekton-data nekton add nekton-data/c_pk_saem_authored.dsse.json

# ---------- 4. Verify ----------
echo ""
echo "=== Registry contents ==="
find nekton-data -type f
echo ""
nekton verify nekton-data/c_eda_authored.dsse.json "${KEY_NAME}.pub"
nekton verify nekton-data/c_pk_saem_authored.dsse.json "${KEY_NAME}.pub"

# ---------- 5. Commit and push ----------
echo ""
echo "=== Ready to push ==="
echo "Run the following to publish to the federation:"
echo ""
echo "  cd /mnt/c/dev/MCP"
echo "  git add nekton-data/ author_claims.sh"
echo "  git commit -m 'feat: add nekton authored-claims for the warfarin fotons'"
echo "  git push"
echo ""
echo "Done. The aggregator will pick up the new claims within 30 min (or trigger manually)."
