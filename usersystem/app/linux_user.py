import subprocess
import uuid

def user_already_exists(name: str) -> bool:
    cmd = "id -u %s" % name
    try:
        output = subprocess.check_output(cmd, shell=True)
        output_str = str(output)
        if "no such user" in output_str:
            return False
        return True
    except subprocess.CalledProcessError:
        return False

def get_unique_name(base_user_name) -> str:
    user_name = base_user_name
    tail = 0
    while user_already_exists(user_name):
        tail += 1
        user_name = "%s%s" % (base_user_name, str(tail))
    return user_name

def create_mail_anonymous_user(user_name: str) -> bool:
    if user_already_exists(user_name):
        return False
    cmd = "useradd -m -G mail %s" % user_name
    try:
        output = subprocess.check_output(cmd, shell=True)
        print(output)
        return user_already_exists(user_name)
    except subprocess.CalledProcessError:
        return False
