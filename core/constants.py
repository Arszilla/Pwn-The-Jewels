"""
Loads bot configuration from YAML files.
"""

import logging

import yaml

log = logging.getLogger(__name__)

with open("config.yml", "r", encoding="UTF-8") as config:
    settings = yaml.safe_load(config)


def check_required(keys):
    """
    Verifies that keys that are set to be required are present in 
    the loaded configuration.
    """

    for key_path in keys:
        lookup = settings
        try:
            for key in key_path.split('.'):
                lookup = lookup[key]

                if lookup is None:
                    raise KeyError(key)

        except KeyError:
            log.critical(
                f"A configuration for `{key_path}` is required, but was not found. "
                "Please set it in `config.yml` or setup an environment variable and try again."
            )
            raise


try:
    required_keys = settings['config']['required_keys']

except KeyError:
    pass

else:
    check_required(required_keys)


class YAMLGetter(type):
    """
    Implements a custom metaclass used for accessing
    configuration data by simply accessing class attributes.
    Supports getting configuration from up to two levels
    of nested configuration through `section` and `subsection`.
    """

    subsection = None

    def __getattr__(cls, name):
        name = name.lower()

        try:
            if cls.subsection is not None:
                return settings[cls.section][cls.subsection][name]
            return settings[cls.section][name]
        except KeyError:
            dotted_path = '.'.join(
                (cls.section, cls.subsection, name)
                if cls.subsection is not None else (cls.section, name)
            )
            log.critical(
                f"Tried accessing configuration variable at `{dotted_path}`, but it could not be found.")
            raise

    def __getitem__(cls, name):
        return cls.__getattr__(name)

    def __iter__(cls):
        """
        Return generator of key: value pairs of current constants class' config values.
        """
        for name in cls.__annotations__:
            yield name, getattr(cls, name)


class Bot(metaclass=YAMLGetter):
    section = "bot"

    prefix: str
    token: str


class Guild(metaclass=YAMLGetter):
    section = "guild"

    id: int
    invite: str
