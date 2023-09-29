class RenderError(Exception):
    
    def __init__(self):
        super().__init__('Failed to render the asked page. Try setting wait=8 or higher')

class NotFoundError(Exception):
    
    def __init__(self):
        super().__init__('The requested pair does not exist')

class UnknownError(Exception):

    def __init__(self):
        super().__init__('An unknown error has occured. Please restart the program')

class IdentifierError(Exception):

    def __init__(self):
        super().__init__('Identifier error. Valid values of identifier param are: "week", "day"')

class CurrencyError(Exception):

    def __init__(self):
        super().__init__('Invalid currency. Valid values of currency param are: "usd", "eur"')