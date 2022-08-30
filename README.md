# CLI Manual

Install python3 Requirements 
```shell
$ pip install -r requirements.txt
```

CLI Base Commands
```shell
$ ./nuvla_cli --help

Commands:
  edge
  device
  login
  logout
  clear
  version
```

Edge commands
```shell
$ ./nuvla_cli edge --help

Options:
  --help  Show this message and exit.

Commands:
  create
  list
  remove
  start
  stop
```

edge create options
```shell
Options:
  --name TEXT
  --description TEXT
  --count INTEGER       [default: 1]
  --dummy / --no-dummy  [default: no-dummy]
  --fleet-name TEXT     [default: Testing]
  --help                Show this message and exit.
```
IMPORTANT: Name and description are ignored at this moment. Base name will be [FleetName] NuvlaEdge_#

## Basics
### Create  a single NuvlaEdge
```shell
$ ./nuvla_cli edge create
```
Dummy Nuvlaedge 
```shell
$ ./nuvla_cli edge create --dummy
```

### Create a fleet
```shell
$ ./nuvla_cli edge create --count 10 --fleet-name MyFleet 
```
Dummy NuvlaEdge fleet
```shell
$ ./nuvla_cli edge create --count 10 --fleet-name MyFleet --dummy
```

### Start NuvlaEdges in the same device
This command will start all the non-dummy NuvlaEdges created in this device
```shell
$ ./nuvla_cli edge start <nuvlaedge_uuid>
```

### Remove NuvlaEdges from Nuvla
Real and dummy NEE are removed in different commands
```shell
$ ./nuvla_cli edge remove <nuvlaedge_uuid>
```

## GeoLocation

### Create a GeoLocated Edge (By Country)
This command will:\
    1. Create 10 Edge instances in Nuvla.io\
    2. Locate those Edges withing the selected country\
    3. Start those NuvlaEdges (If not dummy)\

     
```shell
$ ./nuvla_cli fleet create MyFleetName --count 10 --dummy
$ ./nuvla_cli fleet glocate --name MyFleetName --country France
$ ./nuvla_cli fleet start MyFleetName
```
