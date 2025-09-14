FROM futureys/claude-code-python-development:20250915024000
COPY pyproject.toml /workspace/
RUN uv sync
COPY . /workspace/
ENTRYPOINT [ "uv", "run" ]
CMD ["invoke", "test.coverage"]
