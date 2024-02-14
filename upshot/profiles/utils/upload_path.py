def profile_upload(instance, filename):
    return "/".join(["profiles", instance.user.username, filename])
