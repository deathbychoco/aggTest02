# Pharmacometrics Docker image
# Base: rocker/r2u — CRAN packages as Ubuntu apt binaries (no source compilation)
FROM rocker/r2u:24.04

LABEL maintainer="pharmacometrics-nlmixr2"
LABEL description="nlmixr2 / rxode2 pharmacometrics environment for Claude Science"

# System dependencies (cmake, mpfr, gmp, libpng, zlib, etc.) resolved automatically by r2u/apt
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    openssh-server \
    curl \
    wget \
    git \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libfontconfig1-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libfreetype6-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    cmake \
    libmpfr-dev \
    libgmp-dev \
    && rm -rf /var/lib/apt/lists/*

# Install R packages via r2u binary apt layer (fast — no compilation)
RUN install2.r --error --skipinstalled --ncpus -1 \
    rxode2 \
    nlmixr2 \
    nlmixr2est \
    nlmixr2extra \
    nlmixr2data \
    nlmixr2lib \
    xpose \
    vpc \
    tidyverse \
    ggplot2 \
    patchwork \
    ggpubr \
    dplyr \
    tidyr \
    PKNCA \
    table1 \
    gt \
    gtsummary \
    flextable \
    officer \
    rmarkdown \
    knitr \
    kableExtra \
    plotly \
    DT

# Install xpose.nlmixr2 (may not be in r2u binary layer — fallback to CRAN source)
RUN Rscript -e "if (!requireNamespace('xpose.nlmixr2', quietly=TRUE)) install.packages('xpose.nlmixr2')"

# Set up SSH server
RUN mkdir -p /var/run/sshd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && \
    echo "AllowUsers pmx" >> /etc/ssh/sshd_config

# Create non-root pmx user
RUN useradd -m -s /bin/bash pmx && \
    mkdir -p /home/pmx/.ssh && \
    chmod 700 /home/pmx/.ssh && \
    chown -R pmx:pmx /home/pmx/.ssh

# Working directory for analyses
RUN mkdir -p /home/pmx/work && chown pmx:pmx /home/pmx/work
WORKDIR /home/pmx/work

# Default R library path — writable by pmx user
RUN mkdir -p /home/pmx/R/library && \
    chown -R pmx:pmx /home/pmx/R && \
    echo '.libPaths(c("/home/pmx/R/library", .libPaths()))' >> /home/pmx/.Rprofile && \
    chown pmx:pmx /home/pmx/.Rprofile

EXPOSE 22

# Entrypoint: start SSH daemon
CMD ["/usr/sbin/sshd", "-D"]
