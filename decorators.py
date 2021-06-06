from functools import wraps

class Decorators:
    '''
    Class of decorator functions.
    https://medium.com/@vadimpushtaev/decorator-inside-python-class-1e74d23107f6
    '''
    @classmethod
    def check_month(cls, func):
        '''
        Decorator to validate month data type and convert it from string to int if required.
        '''
        @wraps(func)
        def _wrapper(self, monat):
            monat, err = cls._validate_month(monat)
            if err:
                raise TypeError(err)
            result = func(self, monat)
            return '{:,.2f}'.format(round(result, 2))
        return _wrapper
    

    @staticmethod
    def _validate_month(monat):
        '''
        Validate data type
        '''
        err = '''
            "Monat" must be an integer value representing the number of month from
            start of the credit or a date value of the format mm.yyyy
        '''
        if isinstance(monat, int) or isinstance(monat, str):
            return monat, ''
        elif isinstance(monat, float):
            return '', err
        else:
            return '', err