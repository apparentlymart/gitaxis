
import os.path
import os

from dulwich.repo import Repo
from dulwich.errors import NotGitRepository
from dulwich.objects import Commit, Tree, Blob, Tag

from gitaxis.models import *


def get_global_repos():
    from django.conf import settings
    rootdir = settings.GLOBAL_REPO_ROOT
    entries = os.listdir(rootdir)
    for entry in entries:
        if not entry.endswith(".git"):
            continue
        name = entry[:-4]
        try:
            repo = Repo(os.path.join(rootdir, entry))
        except NotGitRepository:
            continue
        yield (name, repo)


def get_repo(name, username=None):
    if username is not None:
        # Don't support per-user repositories yet
        raise KeyError(name)

    from django.conf import settings
    if "/" in name:
        raise KeyError(name)
    if name[0] == ".":
        raise KeyError(name)

    rootdir = settings.GLOBAL_REPO_ROOT
    repodir = os.path.join(rootdir, name + ".git")
    try:
        return Repo(repodir)
    except NotGitRepository:
        raise KeyError(name)


