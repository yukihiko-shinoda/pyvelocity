FROM futureys/claude-code-python-development:20260515203000
COPY pyproject.toml /workspace/
RUN uv sync
COPY . /workspace/
ENTRYPOINT [ "uv", "run" ]
CMD ["invoke", "test.coverage"]
