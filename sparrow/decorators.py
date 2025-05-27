from sparrow.validators import Validator


def validate(**fields):

    def decorator(func):
        def wrapper(*args, **kwargs):
            serializer_instance = args[0]
            data = serializer_instance.initial_data
            validator_list = []
            for field_name in fields:
                for k, v in fields[field_name].items():
                    validator_list.append(v(field_name))

            validator = Validator(validator_list)
            validator.validate(data)
            return func(*args, **kwargs)
        return wrapper

    return decorator
