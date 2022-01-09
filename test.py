import typing
from functools import singledispatchmethod


class Gitlab:
    def __init__(self, *args):
        pass


class LicenseChecker(object):
    @singledispatchmethod
    def overloaded_init(self, gl: Gitlab):
        print("from gitlab")
        self.gl = gl

    @overloaded_init.register
    def _(self, url: str, api_key: str):
        print("from url")
        self.gl = Gitlab(url, api_key)

    @typing.overload
    def __init__(self, gl: Gitlab) -> None: ...

    @typing.overload
    def __init__(self, url: str, api_key: str) -> None: ...

    def __init__(self, *args, **kwargs):
        self.overloaded_init(*args, **kwargs)

    def iter_projects(self) -> typing.Iterator[str]:
        ...


lc1 = LicenseChecker(Gitlab())
lc2 = LicenseChecker("myurl", "myapi")