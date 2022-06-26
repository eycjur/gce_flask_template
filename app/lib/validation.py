import inspect
import functools
import datetime


class ValidateRequestParam:
    def __init__(self, request, schema):
        if request.method == "GET":
            self.data = request.args
        elif request.method == "POST":
            self.data = request.form
        else:
            raise ValueError("Invalid method")

        self.schema = Schema(schema)

    def __getattr__(self, __name: str):
        self.schema.get(self.data, __name)

class Schema:
    def __init__(self, schema):
        """
        Args:
            schema: dict

        Example:
            schema = {
                "message": {
                    "type": str,
                    "required": True,
                    "default": "Hello"
                }
            }
        """
        self.schema = schema

    def get(self, params, key):
        constraints = self.schema[key]
        if key not in params:
            if self.schema[key]:
                if constraints["required"]:
                    raise ValueError("{} is required".format(key))
                else:
                    return constraints["default"]

        try:
            if constraints["type"] == datetime.date:
                return datetime.date(*[int(i) for i in params[key].split("-")])
            return constraints["type"](params[key])

        except TypeError as e:
            raise ValueError(f"{key}:{params[key]} is invalid")


def args_type_check(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        import logging
        logging.warning((sig.parameters, sig.bind(*args, **kwargs).arguments))
        for name, value in sig.parameters.items():
            if value.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                if value.default == inspect.Parameter.empty:
                    if name not in kwargs:
                        raise ValueError("{} is required".format(name))
                else:
                    if name not in kwargs:
                        kwargs[name] = value.default
        return func(*args, **kwargs)
    return wrapper
