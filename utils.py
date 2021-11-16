import requests
from typing import Dict


def get_forks() -> Dict[str, str]:
    forks_data = requests.get('https://api.github.com/repos/fipl-hse/2021-2-level-labs/forks').json()
    forks = {}
    for fork in forks_data:
        forks[fork['owner']['login']] = fork['html_url']

    return forks
