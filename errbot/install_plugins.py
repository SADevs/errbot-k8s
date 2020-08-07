import os
import pathlib
import sys
import logging
from dulwich import porcelain

confg = None
log = logging.getLogger()

def load_config():
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


def clone_repos(base_dir: str, repos: list) -> None:
    """
    Clones repositories from a list (repos) into a directory (base_dir)
    Args:
        base_dir (str):
        repos:

    Returns:

    """
    # if we don't have any configured repos, nothing to clone
    if len(repos) == 0:
        return

    for repo_config in repos:
        print(repo_config)
        repo_config = repo_config.split(',')
        repo_loc = f"{base_dir}/{repo_config[0]}"
        log.debug("repo_location: %s", repo_loc)
        print(repo_loc)
        # If the repo exists, delete it, we'll clone it clean and then create the path for us to clone into
        if os.path.exists(repo_loc):
            log.debug("Repo exists, pulling %s", repo_loc)
            try:
                porcelain.pull(repo_loc)
            except porcelain.Error as exc:
                log.error("Exception pulling %s. Error: %s", repo_loc, str(exc))
            break

        pathlib.Path(repo_loc).mkdir(parents=True, exist_ok=True)
        try:
            repo = porcelain.clone(repo_config[1], repo_loc)
            git_config = repo.get_config()
            git_config.set(('branch', repo_config[2]), 'remote', 'origin')
            git_config.set(('branch', repo_config[2]), 'merge', f"refs/heads/{repo_config[2]}")
            git_config.write_to_path()
            porcelain.pull(repo_loc)
            log.info(f"Successfully cloned {repo_config[0]}/{repo_config[2]} to {repo_loc} from {repo_config[1]}")
        except porcelain.Error as exception:
            log.error(f"Exception cloning {repo_config[0]} from {repo_config[1]}. Error: {str(exception)}")


if __name__ == '__main__':
    config = load_config()
    clone_repos(base_dir=config.BOT_EXTRA_PLUGIN_DIR,
                repos=config.REPOS_LIST)
