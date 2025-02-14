# asr-api

The search-ui is accessible [here](http://54.254.246.129/).

## Instructions to run code

### General Setup

1. **Fork and clone this repository.**

2. **Set up the data directory:**

   - Create a folder called `data` in the project root.
   - Download the dataset using [this link](https://www.dropbox.com/scl/fi/i9yvfqpf7p8uye5o8k1sj/common_voice.zip?rlkey=lz3dtjuhekc3xw4jnoeoqy5yu\&dl=0).
   - Extract the zip file into the `data/` directory.
   - The directory structure should look like:
     ```
     data/
     └── common_voice/
       ├── cv-invalid/
       ├── cv-other-dev/
       ├── cv-other-test/
       ├── cv-other-train/
       ├── cv-valid-dev/
       ├── cv-valid-test/
       ├── cv-valid-train/
       ├── cv-invalid.csv
       ├── cv-other-dev.csv
       ├── cv-other-test.csv
       ├── cv-other-train.csv
       ├── cv-valid-dev.csv
       ├── cv-valid-test.csv
       ├── cv-valid-train.csv
       ├── LICENSE.txt
       └── README.txt
     ```

3. **Set up the Conda environment:**

   ```sh
   conda create -n asr-api python=3.11
   conda activate asr-api
   pip install -r requirements.txt  # See note below
   ```

   **Note:** The `requirements.txt` includes dependencies for task 2 and later tasks 4, 5, 6 (ElasticSearch and dotenv). If you only need Task 2, install dependencies without these two packages.

4. **Ensure Docker is installed**

   - If not installed, [install Docker](https://docs.docker.com/engine/install/).
   - Ensure the Docker daemon is running.

---

## Task 2 - API for Automatic Speech Regcognition

1. **Build the Docker image:**
* Check that you are in project root, then run the following command to build the Docker image
  ```
  docker build --no-cache -t asr-api:v1 -f asr/Dockerfile .
  ```
- `--no-cache`: Forces a fresh build without using cached layers.
- `-t asr-api:v1`: Tags the built image as `asr-api:v1`.
- `-f asr/Dockerfile`: Specifies the Dockerfile inside the `asr/` directory.
2. **Run the Docker container:**
* Use the following command to start Docker container:
  ```
  docker run -d --name asr-api -p 8001:8001 \
      -v $(pwd)/data/common_voice/cv-valid-dev:/mnt/cv-valid-dev \
      -v $(pwd)/data/common_voice/cv-valid-dev.csv:/mnt/cv-valid-dev.csv \
      asr-api:v1
  ```
- `-d`: Runs the container in detached mode.
- `--name asr-api`: Assigns the name `asr-api` to the container.
- `-p 8001:8001`: Maps port `8001` of the container to `8001` on the host.
- `-v $(pwd)/data/...:/mnt/...`: Mounts local data directories inside the container.


3. **Run the ASR processing script inside the container:**
  ```
  docker exec -it asr-api python asr/cv-decode.py
  ```
- `exec -it`: Runs an interactive process inside the running container.

---

## Tasks 4, 5, 6 - Cloud Deployment on AWS EC2 for Indexing and Searching
The following instructions are for deploying on an AWS EC2 instance.

1. **Set up an EC2 instance:**
* Set up an EC2 instance, including setting up a key pair. You'll save the key locally as a .pem file. Change the permissions for this file:
  ```
  chmod 400 <path-to-.pem-file>
  ```
* Get the IPv4 address of the instance, and ssh into the instance:
  ```
  ssh -i <path to .pem file> ec2-user@your-ec-2-public-ip
  ```
2. **Install Docker & Docker Compose on EC2:**
    ```
    sudo dnf install docker
    sudo systemctl start docker
    sudo systemctl enable docker
    ```

    ```
    mkdir -p ~/.docker/cli-plugins/
    curl -SL https://github.com/docker/compose/releases/download/v2.30.2/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
    chmod +x ~/.docker/cli-plugins/docker-compose
    docker compose version
    ```
3. **Clone the repository on EC2:**
* Generate a Personal Access Token (PAT) in GitHub.
* Git clone the repository to the EC2 instance using the PAT:
  ```
  git clone https://<your-github-username>:<your-token-here>@github.com/<your-github-username>/asr-api.git
  ```

4. **Set up Elasticsearch**
* Sign up for a free account on [elasticsearch](https://www.elastic.co/elasticsearch). Create a deployment and generate 2 API keys:
  * API Key 1: with "create_index", "write", "all" privileges
  * API Key 2: with only "read" previleges

* Update environment variables of search-ui service in `deployment-design/docker-compose.yml`:
     ```yaml
     search-ui:
       build:
         context: ../search-ui
         dockerfile: Dockerfile
       container_name: search-ui
       environment:
         - REACT_APP_ELASTIC_ENDPOINT=http://54.254.246.129:9200
         - REACT_APP_INDEX_NAME=cv-transcriptions
         - REACT_APP_ELASTIC_API_KEY=<API-Key-2>
       ports:
         - "3000:3000"
       depends_on:
         - elasticsearch-node1
     ```

5. **Export your EC2 credentials to the terminal**
    ```
      * export REACT_APP_ELASTIC_KEY=<API-Key-2>
      * ELASTIC_API_KEY_ID=<id-of-API-Key-1>
      * ELASTIC_API_KEY_SECRET=<api_key-of-API-Key-1>
      ```

6. **Deploy the application using Docker Compose:**
* Ensure you are in project root (asr-api), then run the docker compose command:
  ```
  docker compose -f deployment-design/docker-compose.yml up -d
  ```
7. **Access the Search UI:**

   - Navigate to `http://<your-EC2-IPv4-instance>:80` in a browser.

8. **Stop Docker services when needed:**

   ```sh
   docker compose -f deployment-design/docker-compose.yml down
   ```

   - This stops and removes the containers but preserves volumes.

---

## Troubleshooting

### 1. Docker permission issues (Linux)

If you get a permission error when running Docker commands, add yourself to the `docker` group:

```sh
sudo usermod -aG docker $USER
newgrp docker
```

