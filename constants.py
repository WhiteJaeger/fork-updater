import os
import enum


UPSTREAM_REPO_URL = r'https://github.com/student-org-mock/mock-2021'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_TO_LOG_FILE = os.path.join(CURRENT_DIR, 'log.txt')
PATH_TO_ERROR_LOG_FILE = os.path.join(CURRENT_DIR, 'error_log.txt')
GH_USER = 'WhiteJaeger'


class UpdateStrategy(enum.Enum):
    getNew = 'get latest changes'
    keepFork = 'merge in favour of the fork changes'
    keepUpstream = 'merge in favour of the upstream changes'
