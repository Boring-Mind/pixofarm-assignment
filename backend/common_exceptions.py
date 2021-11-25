class CommonException(Exception):
    _default_message: str

    def __init__(self, *args, message=None):
        super().__init__(*args)
        if message:
            self.message = message
        else:
            self.message = self._default_message


class CommonExceptionWithResponse(CommonException):
    def __init__(self, *args, response=None, **kwargs):
        super().__init__(*args, **kwargs)
        if response:
            self.message = self.message + f" Response was: \n{response}"

    def __str__(self):
        return f"{self.__class__}: {self.message}"
