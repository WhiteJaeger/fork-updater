import os
import enum
import tempfile
import logging

UPSTREAM_REPO_URL = r'https://github.com/student-org-mock/mock-2021'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_TO_SCRIPTS = os.path.join(CURRENT_DIR, 'scripts')
PATH_TO_LOG_FILE = os.path.join(CURRENT_DIR, 'log.txt')
PATH_TO_ERROR_LOG_FILE = os.path.join(CURRENT_DIR, 'error_log.txt')
GH_USER = 'WhiteJaeger'
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')


class GeneralStatusMessages(enum.Enum):
    def __str__(self):
        return self.value
    recently_added = 'Recently added'
    not_synced_yet = 'has not been synced yet'
    not_updated_yet = 'has not been updated yet'


class UpdateStrategyMessages(enum.Enum):
    def __str__(self):
        return f'Updated with strategy: {self.value}'
    getNew = 'get latest changes'
    keepFork = 'merge in favour of the fork changes'
    keepUpstream = 'merge in favour of the upstream changes'


class SyncStatusMessages(enum.Enum):
    def __str__(self):
        return self.value
    conflict = 'Conflict'
    no_conflict = f'No {conflict}'


_, LOG_FILE = tempfile.mkstemp(text=True, prefix='updater_', suffix='.log')
LOGGER_NAME = 'Python Starter Logger'
LOGGER = logging.getLogger(LOGGER_NAME)
handler = logging.FileHandler(filename=LOG_FILE, mode='a')
formatter = logging.Formatter('[%(levelname)s] %(message)s (%(filename)s, %(funcName)s(), line %('
                              'lineno)d)')
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.DEBUG)
LOGGER.debug(LOGGER_NAME)
