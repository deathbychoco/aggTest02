# Errata

## commit 1ca8b11

The free-text body of commit `1ca8b11` mis-transcribed the summarise reproduces-claim id:

```
# wrong (commit message text only):
sha256:082701844a1c2565a63d94778639e7a41c40be2c727b6b35d103d55b5b4abew5
# correct:
sha256:082701844a1c2565a63d94778639e7a41c40be2c727b6b35d103d55b5b4abeb5
```

The committed object file (`nekton-data/objects/sha256/082701844a1c2565a63d94778639e7a41c40be2c727b6b35d103d55b5b4abeb5.json`)
and the signed claim itself are unaffected — only the commit message human-readable text was wrong.
