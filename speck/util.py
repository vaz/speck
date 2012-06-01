import unicodedata
import collections


# TODO: Py3k compatibility

def callable(x):
    "abcs are cool but removing callable() was stupid"
    return isinstance(x, collections.Callable)


def ascii(s):
    if type(s) == str:
        return s
    else:
        return unicodedata.normalize("NFKD", s).encode("ascii", "ignore")


def words(words_list):
    """
    Abstraction for flexible representation of "lists of words".

    If words_list is a string, it will be split on whitespace-and-commas
    and the list of strings will be returned.

    Otherwise, words_list will be passed through as-is. 
    The words_list can be an iterable of strings, each containing one
    word, or it can be a single string of words separated by whitespace
    and/or commas.

    Returns a list of bytestrings, each representing one word.

    TODO: What to do on Py3k? Return native strings, or still bytestrings?

    Example:

    >>> a = words("cat dog rat pig")
    >>> b = words("cat, dog, rat, pig")
    >>> c = words("cat , dog,rat pig")
    >>> d = words(["cat", "dog", "rat", "pig"])
    >>> e = words("cat", "dog", "rat", "pig")

    >>> a == b == c == d == e
    True

    >>> list(words(1, "cat", u"dog", True))
    ["1", "cat", "dog", "True"]
    """
    try:
        words_list = words_list.replace(",", " ").split()
    except AttributeError:
        pass
    return [ascii(word) for word in words_list]
