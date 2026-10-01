import os
import sys


def get_app_data():

    # Normal Python execution
    if not getattr(sys, "frozen", False):

        base = os.path.join(
            os.environ.get(
                "APPDATA",
                os.path.expanduser("~")
            ),
            "Axiom"
        )

    # Compiled executable
    else:

        base = os.path.join(
            os.environ.get(
                "APPDATA",
                os.path.expanduser("~")
            ),
            "Axiom"
        )

    os.makedirs(
        base,
        exist_ok=True
    )

    return base


APP_DATA = get_app_data()


MEMORY_PATH = os.path.join(
    APP_DATA,
    "memory"
)


os.makedirs(
    MEMORY_PATH,
    exist_ok=True
)


SETTINGS_FILE = os.path.join(
    MEMORY_PATH,
    "settings.json"
)


MEMORY_FILE = os.path.join(
    MEMORY_PATH,
    "memory.json"
)


REMINDERS_FILE = os.path.join(
    MEMORY_PATH,
    "reminders.json"
)


APPS_FILE = os.path.join(
    APP_DATA,
    "apps.json"
)