# Fridge App Workspace

This repository is now structured as a workspace that can host multiple apps.

## Current apps

- `apps/api`: FastAPI backend for the fridge inventory application

## Backend development

Serve the backend app directly from the workspace root:

```sh
uv run poe api --dev
```

Run backend tests:

```sh
uv run poe test
```

Run backend linting:

```sh
uv run poe lint
```

If you want to target the backend project explicitly, use:

```sh
uv run --directory apps/api poe lint
```

## Containers

Start the backend container from the workspace root:

```sh
docker compose up app
```

## Notes

Within the Dev Container this is equivalent to:

```sh
poe api
```
- The backend Python package name remains `fridge_app_backend`.
- No frontend app has been added yet; the workspace is only prepared for it.
- Backend-specific setup, including PostgreSQL and Alembic instructions, lives in `apps/api/README.md`.
