
import functools

from django.http import HttpResponse, Http404
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse as reverse_url
from django.shortcuts import redirect
from dulwich.errors import (
    NotCommitError,
    NotTagError,
    NotBlobError,
    NotTreeError,
)

import gitaxis.git as git


def url_kwargs(**kwargs):
    """
    Silly little utility function to remove all of the ``None``s from
    the given kwargs, pretending that they weren't there. This is
    useful when we're trying to make a link to a username-less page
    since otherwise django will stringify our ``None``.
    """
    ret = {}
    for k in kwargs:
        if kwargs[k] is not None:
            ret[k] = kwargs[k]
    return ret


def index(request):
    global_repos = git.get_global_repos()
    return TemplateResponse(request, "gitaxis/index.html", context={
        "global_repos": global_repos,
    })


def repo_detail(request, repo_name, username=None):
    try:
        repo = git.get_repo(repo_name, username)
    except KeyError:
        raise Http404
    head_ref = repo.refs.read_ref('HEAD')
    if head_ref is None:
        head_ref = "ref: refs/heads/master"

    target_url = None

    if head_ref.startswith("ref: "):
        if head_ref[5:16] == "refs/heads/":
            branch_name = head_ref[16:]
            target_url = reverse_url(
                "repo_branch_detail",
                kwargs=url_kwargs(
                    repo_name=repo_name,
                    username=username,
                    branch_name=branch_name,
                ),
            )
    else:
        target_url = reverse_url(
            "repo_commit_detail",
            kwargs=url_kwargs(
                repo_name=repo_name,
                username=username,
                commit_id=head_ref,
            ),
        )

    if target_url is None:
        return TemplateResponse(
            request,
            "gitaxis/emptyrepo.html",
            context={
                "username": username,
                "repo_name": repo_name,
                "repo": repo,
            },
        )

    return redirect(target_url)


def repo_branch_detail(request, repo_name, branch_name, username=None):
    try:
        repo = git.get_repo(repo_name, username)
    except KeyError:
        raise Http404

    ref_name = "refs/heads/" + branch_name
    try:
        commit_id = repo.ref(ref_name)
    except KeyError:
        raise Http404

    try:
        commit = repo.commit(commit_id)
    except (KeyError, NotCommitError):
        raise Http404

    return TemplateResponse(
        request,
        "gitaxis/repo_branch_detail.html",
        context={
            "username": username,
            "repo_name": repo_name,
            "repo": repo,
            "branch_name": branch_name,
            "commit_id": commit_id,
            "commit": commit,
        },
    )


def repo_commit_detail(request, repo_name, commit_id, username=None):
    pass
