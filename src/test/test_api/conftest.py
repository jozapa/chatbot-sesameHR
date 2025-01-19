import subprocess
import pytest
import time


@pytest.fixture(scope="function", autouse=True)
def docker_container():
    """
    Pytest fixture to manage a Docker container lifecycle for tests.

    This fixture ensures that a Docker container is started before each test and
    stopped/removed after the test completes. It runs automatically for each test function.

    The container is run with the following configuration:
    - Name: "sesamebot_container"
    - Image: "sesamebot"
    - Port mapping: Exposes container's port 8000 on the host's port 8000.

    Steps:
        1. Stops and removes any existing container with the same name to prevent conflicts.
        2. Starts a new container using the specified image and configuration.
        3. Waits briefly to ensure the container is ready.
        4. After the test completes, stops and removes the container.
    """
    container_name = "sesamebot_container"
    image_name = "sesamebot"
    docker_run_command = [
        "docker", "run", "--name", container_name, "-p", "8000:8000", "-d", image_name
    ]

    try:
        stop_and_remove_docker_container(container_name)
        subprocess.run(docker_run_command, check=True)
        time.sleep(3)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Error on initializing the Docker container: {e}")

    yield  # The test function is executed

    try:
        stop_and_remove_docker_container(container_name)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Error on removing the Docker container: {e}")


def stop_and_remove_docker_container(container_name):
    """
     Stop and remove a Docker container.

    Executes the `docker rm -f` command to forcibly stop and remove a Docker container
    with the specified name.
    :param container_name: the name of the container
    """
    docker_stop_command = ["docker", "rm", "-f", container_name]
    subprocess.run(docker_stop_command, check=False)
