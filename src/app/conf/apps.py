DEFAULT_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)
DEPENDENCIES = ("crispy_forms", "crispy_bootstrap5")
MODULES = ("account", "data_aggregator")
INSTALLED_APPS = MODULES + DEPENDENCIES + DEFAULT_APPS
