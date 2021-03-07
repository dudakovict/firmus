import os, sys, config.settings


APP_ENVIRONMENT = os.environ.get("APP_ENVIRONMENT", "Development")

_current = getattr(sys.modules["config.settings"], f"{APP_ENVIRONMENT}Config")()

for atr in [f for f in dir(_current) if not "__" in f]:
    val = os.environ.get(atr, getattr(_current, atr))
    setattr(sys.modules[__name__], atr, val)


def as_dict():
    res = {}
    for atr in [f for f in dir(config) if not "__" in f]:
        val = getattr(config, atr)
        res[atr] = val
    return res
