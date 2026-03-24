[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/rchretien/fridge-app-backend) [![Open in GitHub Codespaces](https://img.shields.io/static/v1?label=GitHub%20Codespaces&message=Open&color=blue&logo=github)](https://github.com/codespaces/new/rchretien/fridge-app-backend)

# Fridge App Backend

A backend REST API that supports a fridge inventory UI

## Using

To serve this app, run:

```sh
docker compose up app
```

and open [localhost:8000](http://localhost:8000) in your browser.

Within the Dev Container this is equivalent to:

```sh
poe api
```

## 💾 Development Setup with PostgreSQL

This section explains how to set up a local development environment using Docker, PostgreSQL, and Alembic migrations for the Fridge Inventory App Backend.

---

### 1. Create a `.env-dev` file

Create a file named `.env-dev` in the project root:

```env
# Environment
ENVIRONMENT=dev
DB_TYPE=postgres
API_NAME=Fridge Inventory App Backend

# Application DB config
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_NAME=fridge_inventory_dev
DB_HOST=localhost
DB_PORT=5432

# PostgreSQL container init variables
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=fridge_inventory_dev
```
### 2. Start the PostgreSQL container

```bash
docker compose --env-file .env-dev --profile postgres up -d postgres
```
Verify the container is running:

```bash
docker ps
```

### 3. Verify the database connection

From your host machine:
```
psql -h localhost -U postgres -d fridge_inventory_dev
```
### 4. Start the FastAPI app
```
ENVIRONMENT=dev uv run uvicorn fridge_app_backend.api.app:app --reload

```
The API will connect to the PostgreSQL database using the .env-dev configuration. Alembic will run the migration at api start up.

### 5. Stop the database when finished
```
docker compose --profile postgres down
```

## 🛠️ Automatic Deployment with Watchtower

To keep the Raspberry Pi deployment up-to-date, the project uses Watchtower, a lightweight tool that automatically pulls new Docker images and restarts the corresponding containers.

This allows the Raspberry Pi to update itself whenever a new version of the API image is published to the container registry.

### 🚀 What Watchtower Does

Watchtower runs in a dedicated container and:

1. Periodically checks the registry for new versions of your Docker images.

2. If an update is found:

    - pulls the new image
    - stops the old container 
    - restarts the container using the updated image (with the same configuration)
    - removes old images (when cleanup is enabled)

Thanks to this, no manual SSH deployment is required.

### 🧩 Watchtower Configuration

Example service definition in docker-compose.yml:
```
watchtower:
  image: nickfedor/watchtower:latest
  restart: always
  environment:
    WATCHTOWER_SCHEDULE: "0 3 * * *"
    WATCHTOWER_CLEANUP: "true"
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock
```

#### Explanation of the settings

| Variable | 	Description |
|----------|--------------|
|WATCHTOWER_SCHEDULE	|Cron expression defining when updates should be checked. "0 3 * * *" → every day at 03:00.|
|WATCHTOWER_CLEANUP	|Deletes old images after updating to save disk space.|
|/var/run/docker.sock	|Required so Watchtower can control Docker and restart containers.

### 🕒 Scheduling Updates

Watchtower supports two modes:

#### Option 1 — Cron schedule (recommended)
```
WATCHTOWER_SCHEDULE="0 3 * * *"
```
Runs a single check every day at 03:00.

#### Option 2 — Interval checks (for development)
```
WATCHTOWER_POLL_INTERVAL=300

```
Runs every 5 minutes.
➡️ Do not use both polling and schedule at the same time.

### 🔍 Checking Watchtower Logs

To follow update cycles:
```
docker compose logs -f watchtower
```

Example output when an update is detected:
```
Found new image ghcr.io/...:dev
Stopping container
Started new container
Removing old image
Update session completed: scanned=1 updated=1
```

## Contributing

<details>
<summary>Prerequisites</summary>

<details>
<summary>1. Set up Git to use SSH</summary>

1. [Generate an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key) and [add the SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).
1. Configure SSH to automatically load your SSH keys:
    ```sh
    cat << EOF >> ~/.ssh/config
    
    Host *
      AddKeysToAgent yes
      IgnoreUnknown UseKeychain
      UseKeychain yes
      ForwardAgent yes
    EOF
    ```

</details>

<details>
<summary>2. Install Docker</summary>

1. [Install Docker Desktop](https://www.docker.com/get-started).
    - _Linux only_:
        - Export your user's user id and group id so that [files created in the Dev Container are owned by your user](https://github.com/moby/moby/issues/3206):
            ```sh
            cat << EOF >> ~/.bashrc
            
            export UID=$(id --user)
            export GID=$(id --group)
            EOF
            ```

</details>

<details>
<summary>3. Install VS Code or PyCharm</summary>

1. [Install VS Code](https://code.visualstudio.com/) and [VS Code's Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers). Alternatively, install [PyCharm](https://www.jetbrains.com/pycharm/download/).
2. _Optional:_ install a [Nerd Font](https://www.nerdfonts.com/font-downloads) such as [FiraCode Nerd Font](https://github.com/ryanoasis/nerd-fonts/tree/master/patched-fonts/FiraCode) and [configure VS Code](https://github.com/tonsky/FiraCode/wiki/VS-Code-Instructions) or [configure PyCharm](https://github.com/tonsky/FiraCode/wiki/Intellij-products-instructions) to use it.

</details>

</details>

<details open>
<summary>Development environments</summary>

The following development environments are supported:

1. ⭐️ _GitHub Codespaces_: click on _Code_ and select _Create codespace_ to start a Dev Container with [GitHub Codespaces](https://github.com/features/codespaces).
1. ⭐️ _Dev Container (with container volume)_: click on [Open in Dev Containers](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/rchretien/fridge-app-backend) to clone this repository in a container volume and create a Dev Container with VS Code.
1. _Dev Container_: clone this repository, open it with VS Code, and run <kbd>Ctrl/⌘</kbd> + <kbd>⇧</kbd> + <kbd>P</kbd> → _Dev Containers: Reopen in Container_.
1. _PyCharm_: clone this repository, open it with PyCharm, and [configure Docker Compose as a remote interpreter](https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html#docker-compose-remote) with the `dev` service.
1. _Terminal_: clone this repository, open it with your terminal, and run `docker compose up --detach dev` to start a Dev Container in the background, and then run `docker compose exec dev zsh` to open a shell prompt in the Dev Container.

</details>

<details>
<summary>Developing</summary>

- This project follows the [Conventional Commits](https://www.conventionalcommits.org/) standard to automate [Semantic Versioning](https://semver.org/) and [Keep A Changelog](https://keepachangelog.com/) with [Commitizen](https://github.com/commitizen-tools/commitizen).
- Run `poe` from within the development environment to print a list of [Poe the Poet](https://github.com/nat-n/poethepoet) tasks available to run on this project.
- Run `poetry add {package}` from within the development environment to install a run time dependency and add it to `pyproject.toml` and `poetry.lock`. Add `--group test` or `--group dev` to install a CI or development dependency, respectively.
- Run `poetry update` from within the development environment to upgrade all dependencies to the latest versions allowed by `pyproject.toml`.
- Run `cz bump` to bump the app's version, update the `CHANGELOG.md`, and create a git tag.

</details>
