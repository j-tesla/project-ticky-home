#!/usr/bin/env python3

import re

error = {}
user = {'errors': {}, 'infos': {}}

ERROR_PATTERN = r'ticky: ERROR ([\w ]+) .*\(([\w]+)\)$'
INFO_PATTERN = r'ticky: INFO ([\w ]+) .*\(([\w]+)\)$'

with open('syslog.log') as file:
    while True:
        line = file.readline()
        if not line:
            break
        error_match = re.search(ERROR_PATTERN, line.strip())
        info_match = re.search(INFO_PATTERN, line.strip())
        if error_match:
            error[error_match.groups()[0]] = error.get(error_match.groups()[0], 0) + 1
            user['errors'][error_match.groups()[1]] = user['errors'].get(error_match.groups()[1], 0) + 1
        elif info_match:
            user['infos'][info_match.groups()[1]] = user['infos'].get(info_match.groups()[1], 0) + 1

error = dict(sorted(error.items(), key=(lambda x: x[1]), reverse=True))
user['errors'] = dict(sorted(user['errors'].items(), key=(lambda x: x[0])))
user['infos'] = dict(sorted(user['infos'].items(), key=(lambda x: x[0])))
print(error)
print(user)

with open('error_message.csv', 'w+') as file:
    file.write('Error,Count\n')
    for item in error.items():
        file.write('{},{}\n'.format(item[0], item[1]))

with open('user_statistics.csv', 'w+') as file:
    file.write('Username,INFO,ERROR\n')
    for key in set(user['errors'].keys()).union(set(user['infos'].keys())):
        file.write('{},{},{}\n'.format(key, user['infos'].get(key, 0), user['errors'].get(key, 0)))
