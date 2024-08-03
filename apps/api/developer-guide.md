## Discovery API: Developer Guide

This document is aimed at developers who want to understand, contribute to, or extend the Discovery API. It provides a technical overview of the API's architecture, components, and how to work with it.

### Project Structure

* **`discovery`:** The core API code resides here.
    * **`app.py`:**  The main FastAPI application entry point. Defines the API endpoints, lifespan events, and routing.
    * **`core`:**  Contains core modules:
        * **`config.py`:**  Configuration settings for database, Celery, Docker, Pusher, and S3.
        * **`logger.py`:**  Logging setup and utilities.
        * **`celery.py`:**  Celery app configuration and worker lifecycle management (database connections).
        * **`pusher.py`:**  Integration with the Pusher service for real-time notifications.
        * **`s3.py`:**  Handles interaction with Amazon S3 for volume persistence.
    * **`containers`:**  Components for Docker container management:
        * **`container.py`:**  Handles container creation, execution, and lifecycle.
        * **`volume.py`:**  Manages container volumes, including file I/O, S3 uploads, and cleanup.
    * **`db`:**  Database-related modules:
        * **`__init__.py`:**  Database initialization using Tortoise ORM.
        * **`models.py`:**  Defines the database models (e.g., `Run`).
        * **`repositories`:**  Contains repositories that abstract data access:
            * **`runs.py`:**  Repository for managing `Run` objects, including filtering and pagination.
        * **`repository.py`:**  Base repository class with generic CRUD operations.
    * **`routes`:**  API route definitions:
        * **`runs.py`:**  Defines routes for managing assessment runs.
    * **`runs`:**  Core logic for defining and executing runs:
        * **`registry.py`:**  Central task registry for registering and invoking security tools.
        * **`run.py`:**  Base `Run` class with common functionality for container execution, volume management, and event handling.
        * **`tasks`:**  Contains specific implementations of security tools as Celery tasks:
            * **`projectdiscovery`:**  Tools from the ProjectDiscovery ecosystem.
                * **`subfinder.py`:**  Implementation of the `subfinder` tool.
    * **`utils.py`:**  Utility functions for route naming, domain validation, etc.
    * **`ws`:**  WebSockets-related modules:
        * **`manager.py`:**  Manages WebSocket connections and sending responses.
        * **`runs.py`:**  WebSocket handler for managing run-related interactions.

### Getting Started

1. **Configuration:**
   * Set environment variables in a `.env` file (see `docker/api/.env.dev` for available options).
   * Make sure the database is running and accessible.
   * Ensure Docker is installed and running.
   * Configure Pusher and S3 credentials, Celery

2. **Running the API:**
   * Use `poetry install` to install project dependencies.
   * Run the API server using `poetry run uvicorn discovery.app:app --reload`.
   * Alternatively, use `nx run api:dev` to start the API with Docker Compose. 

### Integrating New Tools

To integrate a new security tool:

1. **Create a Celery Task:**
   * Create a new module in `discovery/runs/tasks` (e.g., `new_tool.py`).
   * Define a `Task` class that inherits from `discovery.runs.run.Run`.
   * Implement the required methods (`run`, `on_finished`, etc.) to define the tool's execution logic and result handling.
   * Use `discovery.containers.container.Container` and `discovery.containers.volume.ContainerVolume` to manage the container and its volume.

2. **Register the Task:**
   * Add an entry to the `discovery.runs.registry.Registry.tasks` dictionary, mapping the tool's name to its Celery task module path.

3. **Validate Parameters:**
   * Optionally define a `ParamsValidator` class for the tool's parameters in the same module.

### Using the API

* **Runs Endpoints:**  Use the `/runs` endpoints to manage assessment runs (create, list, retrieve, filter). 
* **WebSockets:**  Connect to the `/runs/ws` endpoint to receive real-time run status updates.
* **Pusher:**  Subscribe to the "runs" channel to listen for run-related events.
