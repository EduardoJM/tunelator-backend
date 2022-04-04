from system.linux_user import user_already_exists, get_unique_name, create_mail_anonymous_user

print(
    create_mail_anonymous_user(
        get_unique_name("inventare")
    )
)
#print(user_already_exists("root"))

