"""
Модуль для чтения/сохранения настроек приложения.

"""
import yaml

file_path = 'settings.yaml'


def write_settings(settings):
    with open(file_path, 'w') as file:
        yaml.dump(settings, file)


def read_settings():
    try:
        with open(file_path, 'r') as file:
            settings = yaml.safe_load(file)
        return settings
    except Exception as ex:
        print(f"error: {ex}")
        return None


def save_server_url(url: str):
    try:
        settings = {"server_url": url}
        write_settings(settings)
    except Exception as ex:
        print(f"error: {ex}")


def get_server_url() -> str:
    settings = read_settings()

    if settings is None:
        settings = {"server_url": ""}
        write_settings(settings)
    return settings["server_url"]
