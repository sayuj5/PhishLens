# Administrator Guide

## Overview
This guide provides instructions for system administrators to manage and maintain the BlackFalcon platform in a production environment.

## User Management
Currently, users are managed directly in the database. To promote a user to an admin role or reset a password manually, you can use the backend console or a database client.

## System Configuration
The following environment variables control system behaviour:
- `DATABASE_URL`: Connection string for the database (e.g., PostgreSQL).
- `SECRET_KEY`: Used to sign JWT tokens. Must be strong and rotated periodically.
- `FRONTEND_URL`: Used for CORS policies. Set this to the exact URL of your deployed frontend.

## Database Migrations
We use SQLAlchemy `metadata.create_all` for initial setup. In future updates, Alembic will be used for schema migrations.

## Log Management
Backend logs are output to `stdout` in structured format. Ensure your container orchestrator (e.g., Kubernetes, Docker) captures these logs.

## Troubleshooting
If the Discovery Engine is stuck, restart the backend service. The worker pool will cleanly reinitialise on startup.
