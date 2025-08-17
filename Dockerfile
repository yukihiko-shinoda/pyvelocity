FROM node:24.6.0-trixie-slim
WORKDIR /workspace
COPY --from=ghcr.io/astral-sh/uv:0.8.11 /uv /uvx /bin/
RUN npm install -g @anthropic-ai/claude-code@1.0.83
# The uv command also errors out when installing semgrep:
# - Getting semgrep-core in pipenv · Issue #2929 · semgrep/semgrep
#   https://github.com/semgrep/semgrep/issues/2929#issuecomment-818994969
ENV SEMGREP_SKIP_BIN=true
COPY pyproject.toml /workspace/
RUN uv sync
COPY . /workspace/
ENTRYPOINT [ "uv", "run" ]
CMD ["invoke", "test.coverage"]
