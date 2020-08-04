class DataTypeValidator:
    @staticmethod
    def validate_data_type(variable, data_type, exception_error_message):
        if isinstance(variable, data_type):
            return variable
        else:
            raise ValueError(exception_error_message)
