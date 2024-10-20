from common.config import ROLES


def get_roles_list(count: int):
    role_list = []
    for key, val in ROLES[count].items():
        for i in range(val):
            role_list.append(key)
    return role_list
