from rest_framework.exceptions import ValidationError


class RequiredValidator:
    def __init__(self, field_name):
        self.field_name = field_name

    def validate(self, data):
        if self.field_name not in data:
            raise ValidationError(f"{self.field_name} is required")


class NotNoneValidator:
    def __init__(self, field_name):
        self.field_name = field_name

    def validate(self, data):
        if data.get(self.field_name) is None:
            raise ValidationError(f"{self.field_name} can't be None")


class PatternValidator:
    def __init__(self, field_name, pattern):
        self.field_name = field_name
        self.pattern = pattern

    def validate(self, data):
        import re
        value = data.get(self.field_name)
        if value is not None and not re.match(self.pattern, str(value)):
            raise ValidationError(f"{self.field_name} does not match pattern")


class Validator:
    def __init__(self, validators):
        self.validators = validators

    def validate(self, data):
        for validator in self.validators:
            validator.validate(data)

