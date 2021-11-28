import requests
import random
import string
from typing import Dict


def get_forks() -> Dict[str, str]:
    # forks_data = requests.get('https://api.github.com/repos/fipl-hse/2021-2-level-labs/forks?per_page=100').json()
    forks_data = requests.get('https://api.github.com/repos/student-org-mock/mock-2021/forks?per_page=100').json()
    forks = {}
    for fork in forks_data:
        forks[fork['owner']['login']] = fork['html_url']

    return forks


def generate_random_string() -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
