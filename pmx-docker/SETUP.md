# Pharmacometrics Docker Setup — WSL + Claude Science

## 1. Save these files in WSL

Copy `Dockerfile`, `docker-compose.yml`, and this file into a directory in WSL, e.g.:

```bash
mkdir ~/pmx-docker && cd ~/pmx-docker
# paste or copy the Dockerfile and docker-compose.yml here
```

## 2. Generate an SSH key for Claude Science

```bash
ssh-keygen -t ed25519 -f ~/.ssh/pmx_claude -N "" -C "claude-science-pmx"
cat ~/.ssh/pmx_claude.pub   # copy this — you'll need it in step 4
```

## 3. Build and start the container

```bash
cd ~/pmx-docker
docker compose build        # ~5 min first time (downloading r2u binaries)
docker compose up -d
```

## 4. Install Claude Science's public key into the container

```bash
# Add YOUR public key (from step 2) to the container's pmx user
docker exec pmx-nlmixr2 bash -c \
  "echo 'PASTE_YOUR_PUBLIC_KEY_HERE' >> /home/pmx/.ssh/authorized_keys && \
   chmod 600 /home/pmx/.ssh/authorized_keys && \
   chown pmx:pmx /home/pmx/.ssh/authorized_keys"
```

## 5. Test SSH access from WSL

```bash
ssh -i ~/.ssh/pmx_claude -p 2222 pmx@localhost \
    "R --version | head -1 && Rscript -e 'library(nlmixr2); cat(\"nlmixr2\", as.character(packageVersion(\"nlmixr2\")), \"OK\n\")'"
```

Expected output:
```
R version 4.x.x (...)
nlmixr2 5.x.x OK
```

## 6. Add as Claude Science compute host

In Claude Science:  **Customize → Compute → Add SSH Host**

- Host: `localhost`  (or `127.0.0.1`)
- Port: `2222`
- User: `pmx`
- Private key: contents of `~/.ssh/pmx_claude`
- Working dir: `/home/pmx/work`

Once added, Claude Science can dispatch pharmacometric model fits directly
to this container and harvest results automatically.

## Useful commands

```bash
docker compose logs -f          # watch container logs
docker compose restart          # restart after reboot
docker compose down             # stop
docker exec -it pmx-nlmixr2 R  # interactive R session in container
```

## Packages pre-installed

- **nlmixr2** 5.x + nlmixr2est, nlmixr2extra, nlmixr2data, nlmixr2lib
- **rxode2** 5.x (ODE solver + simulation)
- **xpose** + xpose.nlmixr2 (diagnostics)
- **vpc** (visual predictive checks)
- **PKNCA** (non-compartmental analysis)
- tidyverse, ggplot2, patchwork, ggpubr, plotly
- rmarkdown, knitr, gt, gtsummary, flextable (reporting)
