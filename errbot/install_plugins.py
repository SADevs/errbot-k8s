import os
import pathlib
import sys
import logging
import delegator
import json
from typing import Dict, List

confg = None
log = logging.getLogger()
log.setLevel(logging.getLevelName(os.environ.get("LOG_LEVEL", "ERROR").upper()))

def _load_config():
    global config
    pre_config_log = logging.getLogger()
    execution_dir = os.getcwd()
    sys.path.insert(0, execution_dir)
    config_path = execution_dir + '/' + 'config.py'

    if not os.path.exists(config_path):
        pre_config_log.error(f"Cannot find the config file {config_path}")
        exit(1)

    loaded_config = None
    try:
        loaded_config = __import__(os.path.splitext(os.path.basename(config_path))[0])
        pre_config_log.info('Bot config loaded.')
    except Exception as exc:
        pre_config_log.exception(f"Unable to load config file {config_path}")
        pre_config_log.exception(str(exc))
        exit(1)

    config = loaded_config
    return loaded_config

def _read_plugin_file(file_path:str) -> Dict:
    """
    Reads in a plugin file, json loads it, and applies defaults
    """
    with open(file_path, 'r') as stream:
        plugins = json.load(stream)

    return plugins

def _clone_git_repos(base_dir: str, repos: List[Dict[str, str]]) -> None:
    """
    Clones repositories from a list (repos) into a directory (base_dir)

    """
    # if we don't have any configured repos, nothing to clone
    if len(repos) == 0:
        return

    log.debug("Repos to clone: %s", repos)
    for repo in repos:
        log.debug("This repo: %s", repo)

        if 'branch' not in repo:
            repo['branch'] = 'master'

        repo_loc = f"{base_dir}/{repo['name']}"
        log.debug("repo_location: %s", repo_loc)
        print(repo_loc)
        # If the repo exists, delete it, we'll clone it clean and then create the path for us to clone into
        if os.path.exists(repo_loc):
            log.debug("Repo exists, pulling %s", repo_loc)
            gitpull = delegator.run(f"git -C {repo_loc} pull")
            if gitpull.err != "":
                log.error("Error while pulling in %s. Error: %s", repo_loc, gitpull.err)
                print(f"Error {gitpull.err}")
            print(gitpull.out)
            continue

        pathlib.Path(repo_loc).mkdir(parents=True, exist_ok=True)

        gitcmd = delegator.run(f"git clone -b {repo['branch']} --single-branch {repo['url']} {repo_loc}")
        if gitcmd.return_code != 0:
            print(gitcmd.err)
            log.error("Error while cloning to %s. Repo: %s Error: %s", repo_loc, repo, gitcmd.err)
        else:
            print(f"Successful clone to {gitcmd.out}")
            log.info(f"Successfully cloned {repo['name']}/{repo['branch']} to {repo_loc} from {repo['url']}")

if __name__ == '__main__':
    config = _load_config()
    plugins = _read_plugin_file(config.PLUGINS_FILE)
    _clone_git_repos(base_dir=config.BOT_EXTRA_PLUGIN_DIR,
                     repos=plugins['plugins']['git_repos'])
    if 'backends' in plugins:
        _clone_git_repos(base_dir=config.BOT_EXTRA_BACKEND_DIR,
                         repos=plugins['backends']['git_repos'])