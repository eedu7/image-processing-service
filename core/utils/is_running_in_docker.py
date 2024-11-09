import os


def is_running_in_docker() -> bool:
    """
    Checks if the application is running inside a Docker container.

    Returns:
        bool: True if running inside Docker, False otherwise.
    """
    # Check for Docker-specific environment file
    if os.path.exists("/.dockerenv"):
        return True

    # Check for control group info that Docker containers typically use
    try:
        with open("/proc/1/cgroup", "r") as file:
            if "docker" in file.read():
                return True
    except FileNotFoundError:
        pass

    return False


if __name__ == "__main__":
    if is_running_in_docker():
        print("The application is running inside a Docker container.")
    else:
        print("The application is not running inside a Docker container.")
