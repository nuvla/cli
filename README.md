# Nuvla Command-Line interface client
Nuvla CLI client. Allows to control some Nuvla functionalities from a terminal. It 
currently supports the creation of Edges and Fleets, as well as  geolocation.

Login is only supported via API keys. 

Install library 
```shell
$ pip install dist/nuvla_cli-0.1.0-py3-none-any.whl
```

CLI Base Commands
```shell
$ ./nuvla_cli --help

Commands:
 clear     Clears all the Edges instances for the user created by the CLI                                                                                                                                    
 edge      Edge management commands                                                                                                                                                                          
 fleet     Fleet management commands                                                                                                                                                                         
 login     Login to Nuvla. The login is persistent and only with API keys. To create the Key pair go to Nuvla/Credentials sections and add a new Nuvla API credential.                                       
 logout    Removes the local Nuvla persistent session and stops any open connection                                                                                                                          
 user      User management commands            
```
