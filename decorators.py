from functools import wraps

class Decorators:
    '''
    Since any function defined inside the class becomes an instance method of the class,
    the functions are changed from inner function to inner class
    https://medium.com/@vadimpushtaev/decorator-inside-python-class-1e74d23107f6
    '''
    @classmethod
    def check_month(cls, func):
        '''
        Decorator to validate month data type and convert it from string to int if required.
        '''
        @wraps(func)
        def __wrapper(self, monat):
            monat, err = cls.__validate_month(monat)
            if err:
                raise TypeError(err)
            result = func(self, monat)
            return result
        return __wrapper
    

    @staticmethod
    def __validate_month(monat):
        '''
        Validate data type
        '''
        err = '''
            "Monat" must be an integer value representing the number of month from
            start of the credit or a date value of the format mm.yyyy
        '''
        if isinstance(monat, int):
            return monat, ''
        elif isinstance(monat, float):
            return '', err
        elif isinstance(monat, str):
            return monat, ''
        else:
            return '', err