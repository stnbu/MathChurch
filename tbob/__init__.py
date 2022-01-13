"""Prepare and maintain an environment under `~/tbob` appropriate for playing
3b1b videos (at https://github.com/3b1b/videos).
"""


import os
import subprocess
from git import Repo

TBOB_DIR = None


def init():
    global TBOB_DIR
    TBOB_DIR = os.path.expanduser("~/tbob")
    os.makedirs(TBOB_DIR, exist_ok=True)


def clean(path):
    """The missing `repo.clean`"""
    proc = subprocess.Popen(
        "git clean -qfdx".split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=path,
    )
    out, err = proc.communicate()
    assert len(out) == 0
    assert len(out) == 0
    assert proc.returncode == 0

    proc = subprocess.Popen(
        "git checkout ./".split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=path,
    )
    out, err = proc.communicate()
    assert len(out) == 0
    assert len(out) == 0
    assert proc.returncode == 0


def get_repo(path, origin=None):
    """Returns a `Repo` instance corresponding to `path`. If `path` does not
    exist, clones from `origin` (URL) and then returns the `Repo` instance of the
    newly-cloned repo at `path`.
    """
    repo = None
    if not os.path.exists(path):
        if origin is None:
            raise Exception("%s does not exist and no remote URL was supplied" % path)
        repo = Repo.clone_from(url=origin, to_path=path)
    else:
        clean(path)
        repo = Repo(path)
        repo.remote().pull()
    return repo


def get_last_commit(repo, path=None):
    """Gets the last (most recent) commit to `repo`, modulo `path` if supplied."""
    kwargs = {}
    if path is not None:
        kwargs = {"paths": path}
    for c in repo.iter_commits(**kwargs):
        return c
    else:
        raise Exception("No commits found")


def get_commit_before(repo, commit):
    """Going backwards through time, get the first commit from `repo` that
    occurred before (in time) the supplied `commit`.
    """
    for c in repo.iter_commits():
        if c.authored_date < commit.authored_date:
            return c
    else:
        raise Exception(
            "No commit occurs before %s (@%d)" % (commit, commit.authored_date)
        )


if __name__ == "__main__":

    init()

    videos_repo_path = os.path.join(TBOB_DIR, "3b1b_videos")
    manim_repo_path = os.path.join(TBOB_DIR, "3b1b_manim")
    manim_venv_path = os.path.join(TBOB_DIR, "3b1b_venv")

    videos_repo = get_repo(videos_repo_path,
                           "https://github.com/3b1b/videos.git")
    manim_repo = get_repo(manim_repo_path,
                          "https://github.com/3b1b/manim.git")

    videos_commit = get_last_commit(videos_repo, "_2021/newton_fractal.py")
    manim_commit = get_commit_before(manim_repo, videos_commit)

    print("videos_commit: %s" % videos_commit)
    print("manim_commit: %s" % manim_commit)
