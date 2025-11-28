class ShortenerBaseError(Exception):
    pass


class NoUserUrlFoundError(ShortenerBaseError):
    pass


class SlugAlreadyExistsError(ShortenerBaseError):
    pass


class NotValidUserUrl(ShortenerBaseError):
    pass
