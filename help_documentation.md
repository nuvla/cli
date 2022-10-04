# `nuvla-cli`
**Usage**:

```console
$ nuvla-cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `clear`: Clears all the Edges instances for the user...
* `edge`: Edge management commands
* `fleet`: Fleet management commands
* `login`: Login to Nuvla.
* `logout`: Removes the local Nuvla persistent session...
* `user`: User management commands

## `nuvla-cli clear`

Clears all the Edges instances for the user created by the CLI

:return: None

**Usage**:

```console
$ nuvla-cli clear [OPTIONS]
```

**Options**:

* `--force / --no-force`: Force skip clear confirmation [Not recommended  [required]
* `--help`: Show this message and exit.

## `nuvla-cli edge`

Edge management commands

**Usage**:

```console
$ nuvla-cli edge [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Creates a new NuvlaEdge
* `delete`: Removes a NuvlaEdge from Nuvla
* `geolocate`: Generates a random coordinate within the...
* `list`: Lists the CLI created edges in the logged-in...
* `start`: Starts a NuvlaEdge engine in the device...
* `stop`: Stops a local NuvlaEdge with the Nuvla ID

### `nuvla-cli edge create`

Creates a new NuvlaEdge

**Usage**:

```console
$ nuvla-cli edge create [OPTIONS]
```

**Options**:

* `--name TEXT`: Edges name to be created  [default: ]
* `--description TEXT`: Edge descriptions  [default: ]
* `--dummy / --no-dummy`: Create a dummy Edge  [default: False]
* `--fleet-name TEXT`: Attach created Edge to existent fleet  [default: ]
* `--help`: Show this message and exit.

### `nuvla-cli edge delete`

Removes a NuvlaEdge from Nuvla

**Usage**:

```console
$ nuvla-cli edge delete [OPTIONS]
```

**Options**:

* `--nuvla-id TEXT`: Unique Nuvla ID of the NuvlaEdgeidentifier  [default: ]
* `--help`: Show this message and exit.

### `nuvla-cli edge geolocate`

Generates a random coordinate within the provided country and locates the provided
NuvlaEdge on those coordinates

**Usage**:

```console
$ nuvla-cli edge geolocate [OPTIONS]
```

**Options**:

* `--nuvla-id TEXT`: Unique Nuvla ID of the NuvlaEdge identifier  [required]
* `--country TEXT`: Country to generate a randomcoordinates within  [required]
* `--help`: Show this message and exit.

### `nuvla-cli edge list`

Lists the CLI created edges in the logged-in user

**Usage**:

```console
$ nuvla-cli edge list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `nuvla-cli edge start`

Starts a NuvlaEdge engine in the device running this CLI.

If the NuvlaEdge entity is created as dummy, it will perform the activation and
commissioning process

**Usage**:

```console
$ nuvla-cli edge start [OPTIONS]
```

**Options**:

* `--nuvla-id TEXT`: Unique Nuvla ID of the NuvlaEdge identifier  [default: ]
* `--help`: Show this message and exit.

### `nuvla-cli edge stop`

Stops a local NuvlaEdge with the Nuvla ID

**Usage**:

```console
$ nuvla-cli edge stop [OPTIONS]
```

**Options**:

* `--nuvla-id TEXT`: Unique Nuvla ID of the NuvlaEdge identifier  [default: ]
* `--help`: Show this message and exit.

## `nuvla-cli fleet`

Fleet management commands

**Usage**:

```console
$ nuvla-cli fleet [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Creates a new Fleet of Edges in Nuvla
* `geolocate`: Randomly locates the given fleet within a...
* `list`: Retrieves and prints the list of fleet names...
* `remove`: Removes a Fleet of Nuvlaedge provided the...
* `start`: Starts a Fleet in the device running this...

### `nuvla-cli fleet create`

Creates a new Fleet of Edges in Nuvla

**Usage**:

```console
$ nuvla-cli fleet create [OPTIONS]
```

**Options**:

* `--name TEXT`: Fleet name desired. Must be unique, as it works as identifier  [required]
* `--count INTEGER`: # of Edges to create within the fleet  [default: 10]
* `--dummy / --no-dummy`: Create a fleet of dummy edges  [default: False]
* `--help`: Show this message and exit.

### `nuvla-cli fleet geolocate`

Randomly locates the given fleet within a country

**Usage**:

```console
$ nuvla-cli fleet geolocate [OPTIONS]
```

**Options**:

* `--name TEXT`: Fleet name to be geolocated  [required]
* `--country TEXT`:  Country within to locate the fleet  [required]
* `--help`: Show this message and exit.

### `nuvla-cli fleet list`

Retrieves and prints the list of fleet names created by CLI

**Usage**:

```console
$ nuvla-cli fleet list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `nuvla-cli fleet remove`

Removes a Fleet of Nuvlaedge provided the unique fleet name

**Usage**:

```console
$ nuvla-cli fleet remove [OPTIONS]
```

**Options**:

* `--name TEXT`: Fleet unique name  [required]
* `--help`: Show this message and exit.

### `nuvla-cli fleet start`

Starts a Fleet in the device running this CLI. Only for dummy fleets

If the fleet entity is created as dummy, it will perform the activation and
commissioning process

**Usage**:

```console
$ nuvla-cli fleet start [OPTIONS]
```

**Options**:

* `--fleet-name TEXT`: Fleet name to be started  [required]
* `--help`: Show this message and exit.

## `nuvla-cli login`

Login to Nuvla. The login is persistent and only with API keys. To create the Key pair
go to Nuvla/Credentials sections and add a new Nuvla API credential.

Login is possible via 3 ways: Environmental variables (NUVLA_API_KEY and
NUVLA_API_SECRET), arguments (key and secret) or via toml configuration file

**Usage**:

```console
$ nuvla-cli login [OPTIONS]
```

**Options**:

* `--key TEXT`: Nuvla API key  [default: ]
* `--secret TEXT`: Nuvla API Secret  [default: ]
* `--config-file TEXT`: Optional configuration file path where the keys are stored.  [default: ]
* `--help`: Show this message and exit.

## `nuvla-cli logout`

Removes the local Nuvla persistent session and stops any open connection

**Usage**:

```console
$ nuvla-cli logout [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `nuvla-cli user`

User management commands

**Usage**:

```console
$ nuvla-cli user [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `login`: Login to Nuvla.
* `logout`: Removes the local Nuvla persistent session...

### `nuvla-cli user login`

Login to Nuvla. The login is persistent and only with API keys. To create the Key pair
go to Nuvla/Credentials sections and add a new Nuvla API credential.

Login is possible via 3 ways: Environmental variables (NUVLA_API_KEY and
NUVLA_API_SECRET), arguments (key and secret) or via toml configuration file

**Usage**:

```console
$ nuvla-cli user login [OPTIONS]
```

**Options**:

* `--key TEXT`: Nuvla API key  [default: ]
* `--secret TEXT`: Nuvla API Secret  [default: ]
* `--config-file TEXT`: Optional configuration file path where the keys are stored.  [default: ]
* `--help`: Show this message and exit.

### `nuvla-cli user logout`

Removes the local Nuvla persistent session and stops any open connection

**Usage**:

```console
$ nuvla-cli user logout [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
