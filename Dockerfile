# ---- Builder stage ----
# Installs Python dependencies from requirements.txt into an isolated
# prefix (/install) using pip, without a venv, so only the resulting
# site-packages get copied into the runtime image — no build tools,
# pip cache, or source wheels end up in the final image.
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN python -m pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt

# ---- Runtime stage ----
# Minimal image containing only the installed dependencies and the
# application package (app/) — no build tools, tests, docs, or other
# repo content are copied in.
FROM python:3.11-slim AS runtime

WORKDIR /app

COPY --from=builder /install /usr/local

COPY app/ ./app/

# ---- Non-root user ----
# Runs the app as an unprivileged user ("app") instead of root, limiting
# the impact of a container compromise. The app directory is owned by
# this user so it can read the code it needs to run.
RUN useradd --create-home --shell /usr/sbin/nologin app \
    && chown -R app:app /app

USER app

EXPOSE 8000

# ---- Health check ----
# Polls GET /health using only Python's standard library (urllib) so no
# extra tool (curl/wget) or dependency needs to be installed. A non-2xx
# response or a request error causes Docker to mark the container unhealthy.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request, sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2).status == 200 else 1)"

# ---- Container startup command ----
# Runs the production ASGI server directly (no --reload) bound to all
# interfaces on port 8000, matching the EXPOSE above.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
