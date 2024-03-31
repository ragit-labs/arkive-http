# Arkive Web Service + DB

To setup run "./scripts/install.sh"
Requires python 3.10


Requires an instance of postgres14 running.

There's a .env.example to setup environment variables.

Database migrations in "migrations" folder. Use alembic for running migrations.

>alembic upgrade head

To run migrations, database uri needs to be put in "alembic.ini" at line 63

# To run setup scripts, use yarn
> yarn

> yarn format
to format the code

> yarn test
to run lint and type-checking
