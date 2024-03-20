from dynaconf import Dynaconf

settings = Dynaconf(
    envvar="DYNACONF",
    settings_file=["settings.yaml", "settings.toml"],
    environments=True,
    load_dotenv=True,
)
