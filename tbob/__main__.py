"""Prepare and maintain an environment under `~/tbob` appropriate for playing
3b1b videos (at https://github.com/3b1b/videos).
"""


import os
import sys
from glob import glob
import venv
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
        repo.heads.master.checkout()  # what about (...) main?
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


def create_venv(path):
    if not os.path.exists(path):
        venv.EnvBuilder(with_pip=True).create(path)


def main():

    init()

    videos_repo_path = os.path.join(TBOB_DIR, "videos")
    manim_repo_path = os.path.join(TBOB_DIR, "manim")
    venv_path = os.path.join(TBOB_DIR, "venv")

    this_script = os.path.basename(__file__)

    help = "\n".join(
        [
            "",
            "USAGE: {this_script} repo-relative/path/to/manim/script.py",
            "",
            "Please note: We are using Grant Sanderson's 3blue1brown version of mainm.",
            "If you are experimenting with manim or using it in a project. Please see this URL:",
            "",
            "    https://www.manim.community/",
            "",
            "The purpose of `tbob` is to make it easier to 'play' the videos featured in",
            "3b1b/videos: We need to figure out what _version_ of 3b1b/manim to use in a",
            "particular context. That's what this tool does.",
            "",
            'You supply a a path of a video and this tool asks "what is the last commit made',
            'to this file?"',
            "",
            "It then uses that timestamp to find the next commit to 3b1b/mainim that occured",
            "_before_ that time, hopefully having the right version of mainim for the file/script",
            "",
            "Your 3b1b video playing environment:",
            "    videos repo: {videos_repo_path}",
            "    manim repo: {manim_repo_path}",
            "    virtual env: {venv_path}",
            "",
            "If you have no idea what I am on about, see here: https://github.com/3b1b",
            "",
        ]
    ).format(**locals())

    if len(sys.argv) < 2:
        print(help)
        sys.exit(0)

    create_venv(venv_path)

    script_path = sys.argv[1]
    videos_repo = get_repo(videos_repo_path, "https://github.com/3b1b/videos.git")
    manim_repo = get_repo(manim_repo_path, "https://github.com/3b1b/manim.git")
    videos_commit = get_last_commit(videos_repo, script_path)
    manim_commit = get_commit_before(manim_repo, videos_commit)
    manim_repo.head.reference = manim_commit

    summary = "\n".join(
        [
            "The last commit to {script_path} was {videos_commit} at {videos_commit.authored_date}",
            "",
            "We found commit {manim_commit} in manim which has epoch {manim_commit.authored_date}",
            "",
            "The repo at {manim_repo_path} has been reverted to this commit",
            "",
        ]
    ).format(**locals())

    print(summary)

    links = glob(os.path.join(venv_path, 'lib', 'python*', 'site-packages', 'manim*.egg-link'))
    if len(links) == 0:
        message = "\n".join([
            "You still must manually do the following but only once:",
            "",
            "    ~$ source {venv_path}/bin/activate"
            "    ~$ cd {manim_repo_path}",
            "    ~$ pip install -e .",
        ]).format(**locals())
        print(message)

    message = "\n".join([
        "Having done the above, you should be able to:",
        "",
        "    ~$ cd {videos_repo_path}",
        "    ~$ source {venv_path}/bin/activate",
        "    ~$ manim-render <options> {script_path} [ClassName]",
        "",
    ]).format(**locals())
    print(message)
