# DewDL

DewDL is intended to enable quick access to products from the Unified Data Library.

## Development

To be developed/deployed against the latest stable release of Python 3.10 or later


1. Clone this repo, you should be in the /your/cloned/directory/dewdl directory. If not, cd to that directory.
2. Source the dev setup script to setup your environment:
1. This script will create a virtual environment, install the required dependencies, activate the new environment and setup pre-commit hooks. If you are using VSCODE, it should recognize the virtual environment install and prompt to configure your python interpreter to use the newly created virtual environment.
1. There are 4 optional arguments:
    * `-v` flag specifies which version of python to use (example: `-v 3.11`)
    * `-d` installs build, dev, and test dependencies in editable mode
    * `-b` installs build dependencies only
    * `-a` installs all dependencies in editable mode/
1. To use the default python version and setup an editable dev environment with all dependencies installed run:

```bash
source scripts/setup_python_environment.sh -a
```

## Getting Started

DewDL can be used by explicitly passing credentials into functions found in `dewdl.requests._udl_httpx_request`; however,
the preferred method is to store credents via the config interface to avoid accidental distribution of passwords.
Follow the steps below to store your credentials in a `dewdl.json` config file:

To explicity pass parameters, create a UDLRequestPayload with the desired parameters and then call UDLRequest._make_request(payload=payload).

* Be aware that the included parameters determine the type of data returned. See the test_udl_request.py class to view examples. 


### Option 1 - Username and Password

> **_NOTE:_**
>
> You can add your password using quotations to avoid parsing issues in the terminal

```console
dewdl config user <your-user>
dewdl config password <your-password>
```

### Option 2 - NPE Certificates

```console
dewdl config crt /path/to/crt/file
dewdl config key /path/to/key/file
```

### Option 3 - User Token

```console
dewdl config token <token>
```

### Review Config Contents

The config file path and contents can be shown at anytime with the following command:

```console
dewdl config show
```
or to view a single config value
```console
dewdl config show user
```

### Delete Config Values

To delete a config value, for example, user, execute the following command:
```console
dewdl config delete user
```

## Making Requests to the UDL

```python
>>> from datetime import datetime
>>> from dewdl.enums import UDLEnvironment, UDLQueryType
>>> from dewdl.requests import UDLRequest

# Define an endpoint to get elsets after Sep 16, 2024
>>> elset_query = UDLQuery(UDLQueryType.ELSET, UDLEnvironment.PROD).after(datetime(2024, 9, 16))

# Make the request
>>> response = UDLRequest.get(elset_query)

# Use the response data as a list
>>> elset_list = response.json()
```

## Running unit tests

There are unit tests that test the code baseline specifically and tests that interact with the UDL. For those tests, the @pytest.mark.skipif decorator is used. For those tests, indicated credentials must be loaded into the dewdl config as described above. If testing both basic auth, user and password, and cert auth using a certificate, ensure only a single type of authentication credentials are loaded into the dewdl config.
