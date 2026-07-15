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
EDA_FOTON="sha256:b2629b72eec7aa990873f49447cc39405b965e5d118c4b0eda77bac547e191d4"
PK_FOTON="sha256:7e9e052871eb4295f8b88bfef2d36d55702d0557333de2c55b57394e9eb912ba"

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
