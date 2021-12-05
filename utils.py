import requests
import random
import string
from typing import Dict


def get_forks_from_github() -> Dict[str, str]:
    # forks_data = requests.get('https://api.github.com/repos/fipl-hse/2021-2-level-labs/forks?per_page=100').json()
    forks_data = requests.get('https://api.github.com/repos/student-org-mock/mock-2021/forks?per_page=100').json()
    forks = {}
    for fork in forks_data:
        forks[fork['owner']['login']] = fork['html_url']

    return forks


def generate_random_string() -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


def write_log(path_to_log_file: str, output_log: str):
    with open(path_to_log_file, 'a', encoding='utf-8') as log_file:
        log_file.write('START LOG...\n\n')
        log_file.write(output_log)
        log_file.write('\nEND LOG')
        log_file.write('\n\n')
