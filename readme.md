# Simple starter pack via docker-compose

This package contains some predefined configs to run a simple configuration of Wallet.

The configuration requires 2 servers:

* For Backend
* For Frontend

Also, it expects that both servers have domain names.

The SSL certificates are obtained via "**Let's Encrypt**" automatically.

## Requirements

**OS**: ``Ubuntu 18`` 

#### Prerequisites

* Docker
* Docker-Compose
* AWS CLI v2 ( if AWS ECR is used )
* Python 3.6 ( backend only )
* MySQL-client 5.7 ( backend only )

The ``./scripts/prerequisites/ubuntu_18_04.sh`` script installs all prerequisites.

## Setup Instructions

Clone command:

```bash
git clone --single-branch --branch release/1 git@bitbucket.org:velmie/wallet-starter-pack-simple.git
```


### Backend 

* First - clone this git repository on the backend server.
* To install all prerequisites just run the command below:
```bash
./scripts/prerequisites/ubuntu_18_04.sh
```
After the script finished work, it **will logout the user**. 
So please don't forget to **login back** on the backend server.  

* Create ``docker-compose.yaml`` file form the sample:

```bash
cp docker-compose-be.yaml.sample docker-compose.yaml
```

* Then create ``.env`` file form the sample:
```bash
cp .env.be_sample .env
```
* Edit ``.env``:
    * ``AWS_ACCOUNT_ID`` - The ID of the AWS account where service images are located.
    * ``AWS_DEFAULT_REGION`` - The region of the AWS ECR where service images are located.
    * ``WALLET_DB_HOST`` - RDBMS host (mysql).
    * ``WALLET_DB_USER`` - RDBMS user.
    * ``WALLET_DB_PASS`` - RDBMS user's password.
    * ``WALLET_FILES_AWS_S3_BUCKET`` - The name of the S3 bucket for the "File service".
    * ``WALLET_FILES_AWS_REGION`` - The region of the S3 bucket for the "File service".
    * ``WALLET_FIELS_AWS_ACCESS_KEY_ID`` - AWS S3 credentials.
    * ``WALLET_FIELS_AWS_SECRET_ACCESS_KEY`` - AWS S3 credentials.
    * ``LETSENCRYPT_EMAIL`` - email address of a person responsible for server administration. "Let's Encrypt" will use it for notifications.
    * ``LETSENCRYPT_BACKEND_VIRTUAL_HOST`` - The domain name of the backend server. Required for SSL.

* After, you need to create databases for each service by running the following command:
```bash
./scripts/init_external_db.sh
```

* Create a public and a private key for JWT via command:
```bash
./scripts/jwt-keys.sh
``` 

* After, run the script to create the docker network:
```bash
./scripts/docker_network_create.sh
```

---

* Please, make sure the server has an access to the *private registry* with docker images of services.

For example, the access can be set up via ``ENV variables`` or by ``AWS IAM role``.

* Then login docker in to a *private registry* with command:
```bash
./scripts/aws_docker_login.sh
```

* To run databases migration run the following command:
```bash
./scripts/run_migrations.sh
```
Each service has its own migrations wrapped into a docker image.
Migration image's ``tag`` matches service image's ``tag``.

* When the migrations are completed, you should start the services by docker-compose:
```bash
docker-compose up -d
```

---

* The final step is to create a **root user** (super-admin) via running the following command (don't forget to change the email and password parameters):
```bash
docker exec users sh -c "/app/service_users -cmd 'create-root-user?email=root@email.com&password=Password1@'"
```


### Frontend

* The first step is to clone this git repository on the frontend server.
* To install all prerequisites just run the command below:
```bash
./scripts/prerequisites/ubuntu_18_04.sh
```
After the script finished work, it **will logout the user**. 
So please don't forget to **login back** on the backend server.  

* Create ``docker-compose.yaml`` file form the sample:

```bash
cp docker-compose-fe.yaml.sample docker-compose.yaml
```

* Then create ``.env`` file form the sample:
```bash
cp .env.fe_sample .env
```
* Edit ``.env``:
    * ``AWS_ACCOUNT_ID`` - The ID of AWS account where service images are located.
    * ``AWS_DEFAULT_REGION`` - The region of AWS ECR where service images are located.
    * ``API_BASE_URL`` - URL of the backend server.
    * ``LETSENCRYPT_EMAIL`` - email address of a person responsible for server administration. "Let's Encrypt" will use it for notifications.
    * ``LETSENCRYPT_FRONTEND_VIRTUAL_HOST`` - The domain name of the frontend server. Required for SSL.

---

* Please, make sure the server has an access to the *private registry* with docker images of services.

For example, the access can be set up via ``ENV variables`` or by ``AWS IAM role``.

* Then login docker into a *private registry* with the command:
```bash
./scripts/aws_docker_login.sh
```

* The final step is to start the services by docker-compose:
```bash
docker-compose up -d
```