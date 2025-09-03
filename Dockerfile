FROM node:24.7.0-trixie-slim
WORKDIR /workspace
COPY --from=ghcr.io/astral-sh/uv:0.8.14 /uv /uvx /bin/
RUN npm install -g @anthropic-ai/claude-code@1.0.98
# For running Semgrep, otherwise following error occurs:
# Fatal error: exception Failure: ca-certs: no trust anchor file found, looked into /etc/ssl/certs/ca-certificates.crt, /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem, /etc/ssl/ca-bundle.pem.
RUN apt-get update && apt-get install --no-install-recommends -y ca-certificates \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
# The uv command also errors out when installing semgrep:
# - Getting semgrep-core in pipenv · Issue #2929 · semgrep/semgrep
#   https://github.com/semgrep/semgrep/issues/2929#issuecomment-818994969
ENV SEMGREP_SKIP_BIN=true
COPY pyproject.toml /workspace/
RUN uv sync
COPY . /workspace/
ENTRYPOINT [ "uv", "run" ]
CMD ["invoke", "test.coverage"]
