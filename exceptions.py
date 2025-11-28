class ShortenerBaseError(Exception):
    pass


class NoUserUrlFoundError(ShortenerBaseError):
    pass
