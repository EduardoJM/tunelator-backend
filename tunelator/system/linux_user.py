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

def get_unique_name(identifier: str) -> str:
    if len(identifier) > 10:
        identifier = identifier[0:10]
    user_name = str(uuid.uuid4()).replace("-", "")
    if user_already_exists(user_name):
        return get_unique_name(identifier)
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
