.. image:: http://www.repostatus.org/badges/latest/active.svg
    :target: http://www.repostatus.org/#active
    :alt: Project Status: Active — The project has reached a stable, usable
          state and is being actively developed.

.. image:: https://github.com/jwodder/ghrepo/workflows/Test/badge.svg?branch=master
    :target: https://github.com/jwodder/ghrepo/actions?workflow=Test
    :alt: CI Status

.. image:: https://codecov.io/gh/jwodder/ghrepo/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/ghrepo

.. image:: https://img.shields.io/pypi/pyversions/ghrepo.svg
    :target: https://pypi.org/project/ghrepo/

.. image:: https://img.shields.io/github/license/jwodder/ghrepo.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/ghrepo>`_
| `PyPI <https://pypi.org/project/ghrepo/>`_
| `Issues <https://github.com/jwodder/ghrepo/issues>`_
| `Changelog <https://github.com/jwodder/ghrepo/blob/master/CHANGELOG.md>`_

``ghrepo`` extracts a GitHub repository's owner & name from various GitHub URL
formats (or just from a string of the form ``OWNER/REPONAME`` or ``REPONAME``),
and the resulting object provides properties for going in reverse to determine
the possible URLs.  Also included is a function for determining the GitHub
owner & name for a local Git repository, plus a couple of other useful Git
repository inspection functions.

Installation
============
``ghrepo`` requires Python 3.6 or higher.  Just use `pip
<https://pip.pypa.io>`_ for Python 3 (You have pip, right?) to install it::

    python3 -m pip install ghrepo


API
===

``GHRepo``
----------

.. code:: python

    class GHRepo(typing.NamedTuple):
        owner: str
        name: str

A pair of a GitHub repository's owner and base name.  Stringifying a ``GHRepo``
instance produces a repository "fullname" of the form ``{owner}/{name}``.

.. code:: python

    property api_url: str

The base URL for accessing the repository via the GitHub REST API; this is a
string of the form ``https://api.github.com/repos/{owner}/{name}``.

.. code:: python

    property clone_url: str

The URL for cloning the repository over HTTPS

.. code:: python

    property git_url: str

The URL for cloning the repository via the native Git protocol

.. code:: python

    property html_url: str

The URL for the repository's web interface

.. code:: python

    property ssh_url: str

The URL for cloning the repository over SSH

.. code:: python

    classmethod parse_url(url: str) -> GHRepo

Parse a GitHub repository URL.  The following URL formats are recognized:

- ``[https://[<username>[:<password>]@]][www.]github.com/<owner>/<name>[.git][/]``
- ``[https://]api.github.com/repos/<owner>/<name>``
- ``git://github.com/<owner>/<name>[.git]``
- ``[ssh://]git@github.com:<owner>/<name>[.git]``

All other formats produce a ``ValueError``.

.. code:: python

    classmethod parse(
        spec: str,
        default_owner: Optional[Union[str, Callable[[], str]]] = None,
    ) -> GHRepo

Parse a GitHub repository specifier.  This can be either a URL (as accepted by
``parse_url()``) or a string in the form ``{owner}/{name}``.  If
``default_owner`` is specified (as either a string or a zero-argument callable
that returns a string), strings that are just a repository name are also
accepted, and the resulting ``GHRepo`` instances will have their ``owner`` set
to the given value.


Functions & Constants
---------------------

**Note**: All of the functions require Git to be installed in order to work.  I
am not certain of the minimal viable Git version, but the functions should work
with any Git as least as far back as version 1.7.

.. code:: python

    get_local_repo(dirpath: Optional[AnyPath] = None, remote: str = "origin") -> GHRepo

Determine the GitHub repository for the Git repository located at or containing
the directory ``dirpath`` (default: the current directory) by parsing the URL
for the specified remote.  Raises a ``subprocess.CalledProcessError`` if the
given path is not in a GitHub repository or the given remote does not exist.

.. code:: python

    get_branch_upstream(branch: str, dirpath: Optional[AnyPath] = None) -> GHRepo

*(New in version 0.5.0)* Determine the GitHub repository for the upstream
remote of the given branch in the Git repository located at or containing the
directory ``dirpath`` (default: the current directory).

Raises a ``subprocess.CalledProcessError`` if the given path is not in a GitHub
repository or the given branch does not have an upstream remote configured.

.. code:: python

    get_current_branch(dirpath: Optional[AnyPath] = None) -> str

Get the current branch for the Git repository located at or containing the
directory ``dirpath`` (default: the current directory).  Raises a
``subprocess.CalledProcessError`` if the given path is not in a GitHub
repository or if the repository is in a detached HEAD state.

.. code:: python

    is_git_repo(dirpath: Optional[AnyPath] = None) -> bool

Tests whether the given directory (default: the current directory) is either a
Git repository or contained in one

.. code:: python

    GH_USER_RGX: str

A regular expression string (unanchored) for a valid GitHub username or
organization name.

.. code:: python

    GH_REPO_RGX: str

A regular expression string (unanchored) for a valid GitHub repository name
(without ".git" extension).


Command
=======

``ghrepo`` also provides a command of the same name for getting the GitHub
repository associated with a local Git repository::

    ghrepo [<options>] [<dirpath>]

By default, the ``ghrepo`` command just outputs the repository "fullname" (a
string of the form ``{owner}/{name}``).  If the ``-J`` or ``--json`` option is
supplied, a JSON object is instead output, containing fields for the repository
owner, name, fullname, and individual URLs, like so:

.. code:: json

    {
        "owner": "jwodder",
        "name": "ghrepo",
        "fullname": "jwodder/ghrepo",
        "api_url": "https://api.github.com/repos/jwodder/ghrepo",
        "clone_url": "https://github.com/jwodder/ghrepo.git",
        "git_url": "git://github.com/jwodder/ghrepo.git",
        "html_url": "https://github.com/jwodder/ghrepo",
        "ssh_url": "git@github.com:jwodder/ghrepo.git"
    }

Options
-------

-J, --json                  Output JSON

-r REMOTE, --remote REMOTE  Parse the GitHub URL from the given remote
                            [default: origin]
