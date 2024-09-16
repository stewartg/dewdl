# DewDL

DewDL is intended to enable quick access to products from the Unified Data Library.

## Getting Started

DewDL can be used by explicitly passing credentials into functions found in `dewdl.requests._udl_request`; however,
the preferred method is to store credents via the config interface to avoid accidental distribution of passwords.
Follow the steps below to store your credentials in a `dewdl.json` config file:

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

### Review Config Contents

The config file path and contents can be shown at anytime with the following command:

```console
dewdl config show
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
