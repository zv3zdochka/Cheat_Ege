## Instructions for Running a Docker Container on Yandex Cloud Service

### Preparation
1. Register on the [Yandex Cloud service](https://cloud.yandex.com/) and [install Yandex Cloud (CLI)](https://cloud.yandex.com/docs/cli/quickstart).
2. Obtain an authentication token.
3. Install [Docker Desktop](https://www.docker.com/products/docker-desktop) and enable virtualization support if necessary.

### Building and Publishing the Image
1. Using the Dockerfile, build the image:
    ```
    docker build -t search .
    ```
    Note the dot at the end!
2. Run the container locally based on the image and expose port 80 externally:
    ```
    docker run -d search
    ```
3. Verify the bot's functionality.
4. Connect the "container registry" from Yandex and publish the image there:
    ```
    yc container registry create test-registry
    yc container registry configure-docker
    ```
5. Obtain your registry ID and publish the file there:
    ```
    docker tag search cr.yandex/crp******/search:test
    docker push cr.yandex/crp******/search:test
    ```
    Here `crp******` is your registry ID.

### Creating a Virtual Machine with the Container
1. Go to the [virtual machines section](https://console.cloud.yandex.com/folders) on the Yandex Cloud console.
2. Create a new virtual machine and specify the image link instead of choosing the operating system.
3. Specify the service account and SSH public key.
4. Create and start the virtual machine.
5. Connect to it using SSH; otherwise, the bot will not start.

### Conclusion
The publication was successful.