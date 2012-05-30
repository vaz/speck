class ExpectationNotMet(AssertionError):
    """
    Raised when an expectation fails, like an AssertionError.
    """
    pass

class NoMatcherError(AttributeError):
    """
    Raised when a matcher is asked for that does not exist.
    """
    pass


