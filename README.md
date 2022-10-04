# Nuvla Command-Line interface client
Nuvla CLI client. Allows to control some Nuvla functionalities from a terminal. It 
currently supports the creation of Edges and Fleets, as well as  geolocation.

---
### First steps
To use this library it is required to have an account in https://nuvla.io. If you don't have one, go to [Nuvla](https://nuvla.io/ui/sign-up) and start with the User Interface.

Once the account is created, you will need to create an API Key credential in Nuvla/UI credentials sections. Due to security reasons, the CLI does not support user/password authentications.

### 1. Install Nuvla CLI

The package can be installed directly from PyPi repository for convenience. 
```shell
$ pip install nuvla-cli
```

Or download the pre-compiled packages from [here](https://pypi.org/project/nuvla-cli/#files)

#### Requirements
 * All the dependencies are installed with pip.
 * Python >= 3.8


### 2. Create credentials in Nuvla
As mentioned before, to use the CLI it is required to have API credentials in Nuvla.io.

To create them:
 1. Go to [credentials](https://nuvla.io/ui/credentials) tab. 
 2. Click on add in the top left corner.
 3. Select Nuvla API-Key and provide the name and description that suits better for your needs.
 4. Copy the key-secret as this is the only time it will be provided. If lost, you will need to delete this credential and create a new one.


### 3. Login the CLI
The CLI provides two login possibilities: environmental variables or cli options.

**ENV Variables:**
```shell
$ export NUVLA_API_KEY='your_api_key'
$ export NUVLA_API_SECRET='your_secret_key'
$ nuvla-cli login
```

**CLI Options**
```shell
$ nuvla-cli login --key 'your_api_key' --secret 'your_secret_key'
```

---
The session is persistent and stored in the user's path under ~/.nuvla/. To remove the session just logout using the CLI.

For further details, the whole help depiction on the CLI can be found [here](help_documentation.md) 
