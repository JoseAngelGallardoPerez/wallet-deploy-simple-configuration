import os
import subprocess
import sys
import re

import ruamel.yaml
from colorama import Fore, Style
from dotenv import dotenv_values

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True
yaml.indent(sequence=3, offset=2)

docker_compose_path = os.path.abspath('./docker-compose.yaml')

migration_image_name_suffix = '-db-migration'

images_with_migrations = [
    'wallet-accounts',
    'wallet-currencies',
    'wallet-customization',
    'wallet-files',
    'wallet-logs',
    'wallet-messages',
    'wallet-notifications',
    'wallet-permissions',
    'wallet-settings',
    'wallet-users',
    'wallet-kyc',
]

def replace_env_vars(string, vars):
    var_templates = re.findall("(\$\{([^\}]*)\})", string)
    for var_template in var_templates:
        if var_template[1] in vars:
            string = string.replace(var_template[0], vars[var_template[1]])

    return string

with open(docker_compose_path, 'r') as file:
    docker_compose = yaml.load(file)

docker_network = docker_compose['networks']['default']['external']['name']

migration_data = []

for service in docker_compose['services']:
    service_image = docker_compose['services'][service]['image']

    # Service ENV
    service_env = os.environ.copy()

    if 'env_file' in docker_compose['services'][service]:
        for env_file in docker_compose['services'][service]['env_file']:
            values = dotenv_values(env_file)
            service_env = {**service_env, **values}

    image_path, image_tag = service_image.split(':')

    image_name = image_path.split('/')[-1]

    if image_name not in images_with_migrations:
        continue

    migration_image_full_path = image_path + migration_image_name_suffix + ':' + image_tag
    migration_image_full_path = replace_env_vars(migration_image_full_path, service_env)

    env = docker_compose['services'][service]['environment']
    db = {}
    for item in env:
        name, val = item.split('=')
        replaced_val = replace_env_vars(val, service_env)

        if name.endswith('_DB_HOST'):
            db['host'] = replaced_val

        if name.endswith('_DB_PORT'):
            db['port'] = replaced_val

        if name.endswith('_DB_NAME'):
            db['db_name'] = replaced_val

        if name.endswith('_DB_USER'):
            db['user'] = replaced_val

        if name.endswith('_DB_PASS'):
            db['pass'] = replaced_val

    if not all(key in db for key in ('host', 'port', 'db_name', 'user', 'pass')):
        raise Exception(
            f'{Fore.RED}The db config of service `{image_name}` is not well packed: {",".join(db.keys())}{Fore.RESET}')

    migration_data.append({
        'service_image': image_name,
        'tag': image_tag,
        'migration': migration_image_full_path,
        'db': db,
    })

migrations_count = len(migration_data)

print(Style.BRIGHT)
print(f"{Fore.MAGENTA}Trying to migrate:{Fore.RESET}")
for idx, migration in enumerate(migration_data):
    print(
        f"{1 + idx}. {Fore.YELLOW}{migration['service_image']}{Fore.RESET}:\t{Fore.BLUE}{migration['tag']}{Fore.RESET}")

    # docker run -e "DB_HOST=localhost" -e "DB_PORT=3306" -e "DB_DATABASE=example" -e "DB_USERNAME=root" -e "DB_PASSWORD=secret" --rm a1xp/laravel-migrate
    cmd = [
        'docker',
        'run',
        '-e',
        f"DB_HOST={migration['db']['host']}",
        '-e',
        f"DB_PORT={migration['db']['port']}",
        '-e',
        f"DB_DATABASE={migration['db']['db_name']}",
        '-e',
        f"DB_USERNAME={migration['db']['user']}",
        '-e',
        f"DB_PASSWORD={migration['db']['pass']}",
        f'--network={docker_network}',
        '--rm',
        migration['migration']
    ]

    print(f'Command: {" ".join(cmd)}')

    result = subprocess.run(cmd, stdout=subprocess.PIPE)

    if result.returncode != 0:
        print(f'{Fore.RED}An error occurred:{Fore.RESET}')
        print(result.stdout.decode('utf-8'))
        exit(1)
    else:
        print(f'{Fore.GREEN}Completed!{Fore.RESET}')

    print('')
