# This is the back-end implementation of the AFTS platform.

## SETUP:

### Prerequisites:
- [Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04) 20.10.08 or higher installed on your machine
- [Gitlab](https://about.gitlab.com/) account to access the project
- [Postman](https://www.postman.com/downloads/) for API development, testing and access
- [NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) install Node Package Manager:

```
npm install -g npm
```

- [Truffle](https://www.trufflesuite.com/docs/truffle/getting-started/installation) Install Truffle Framework for Smart Contract Development and build

```
npm install -g truffle
```

### Source Code:
Obtain a copy of the source code by cloning this repository
```
sudo git clone https://github.com/dukagjinramosaj1/hp_staking.git
```

### Build Smart Contracts IF NEEDED:
In the blockchain directory run the following command for installing Smart Contracts dependencies:
```
npm install
```
We need to convert the Smart Contracts to byte code format by using:
```
truffle build
```


## Build and Start Application with Docker:
In the root directory of the project run (docker needs to be installed and started):

#### Local: 
```
sudo docker-compose -f docker-compose.yml up --build
