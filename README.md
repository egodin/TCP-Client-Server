# TCP-Client-Server

TCP-Client-Server is a simple proof of concept for a TCP client and server.

## Installation
TODO for the `client` machine and the `server` machine

1. Make a directory for the project and navigate to it
```shell
mkdir TCP-Client-Server
cd TCP-Client-Server
```
2. Download the archive `TCP-Client-Server.tar.gz`
3. Extract the archive
```shell
tar -xvf TCP-Client-Server.tar.gz
```
4. Create a virtual environment and activate it
```shell
python3 -m venv venv
source venv/bin/activate
```

## Usage

### 1. Server



Launch the server. 
**Note:** The server must be launched using `root` account. `sudo` will not work.

```shell
su
python3 server.py -p port -s IP
```
where 
`port` is an open port on the server machine and the `IP` address is the IP address of the server machine.

To see the help:
```shell
python3 server.py -h
```
For example, to start a server:
```shell
su
python3 server.py -p 1234 -s 192.168.1.101
```
where `1234` is an open port on the server machine and `192.168.1.101` is the IP address of the server machine.

### 2. Client

```shell
python3 client.py -p port -s IP
```
where `port` is the port on the server machine and the `IP` address is the IP address of the server machine.

To see the help:
```shell
python3 client.py -h
```
For example to connect to a server:
```shell
python3 client.py -p 1234 -s 192.168.1.101
```
where `1234` is the port on the server machine and `192.168.1.101` is the IP address of the server machine.

Once in, there is a prompt listing the available commands:
```shell
Available commands:
    - TIME: get the current time
    - IP: get the IP address of the server
    - OS: get the OS of the server
    - FICHIER: get a dummy file from the server
    - EXIT: exit the client
```

