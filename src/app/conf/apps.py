DEFAULT_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)
DEPENDENCIES = ("crispy_forms",)
MODULES = ("account","crispy_bootstrap5")
INSTALLED_APPS = MODULES + DEPENDENCIES + DEFAULT_APPS
