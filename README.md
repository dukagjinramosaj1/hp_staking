# This is theimplementation of the Human Protcol Technical Task.

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

### Build Smart Contracts (if needed):
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
```


### Project Overview:
### Please find at the root of this directory the architecture.png and Staking_Escrow.png for understanding the data flow

### Smart Contracts: Features of the Staking Contract
  - **Staking** makes you automatically a validator/stakeholder,  you need to stake some amount of (wei, gwei, ether..etc) there is no time related implementation or epoch)  
     - The stake is automatically added to the Smart Contract balance and keeps track of the deposits made from each stakeholder. 
  - **Withdraw of stake** - withdraw what you staked (keeps track for balances). (There are no rules on calculation of stake per period of time implemented) 
  - **Voting**: Only Stakeholders can vote other participants on the network to be penalized, calculation of votes is done (no hard rules regarding time period)
  - **Penalty**: Only the participant which appear on candidateList (which were voted by validators/stakeholders) can be penalized. There is hardcoded penalty of 10 wei reduction to the bad actor and adding this money to the Contract Balance which can serve as reward. (this could be future work on calculating the penalty) 
  - **Rewards**: Rewards can be given to other participants taken from the Smart Contract balance which serves as pool 
  
### API Endpoints: Web server runs on 0.0.0.0:8080
Deploying Contracts: **It returns the Contract's Address, use it for calling other API endpoints**  
```
http://0.0.0.0:8080/deployEscrowFactory/
 ```
 
 Calling Staking: requires a parameter "amount" 
 ```
http://0.0.0.0:8080/stake/
 ```
 Example call: http://0.0.0.0:8080/stake/?amount=100

 Calling EscrowFacotry: requires a list of  trustedHandlers for creating a single Escrow (for testing purposes this list of public keys is taken from ganache generated accounts.
 ```
http://0.0.0.0:8080/escrow/
 ```
 Example call: http://0.0.0.0:8080/escrow/


Future work (not included for this Technical Challenge):  

- UI for interacting with the Smart Contract 
- More API endpoints for other contract call actions can be implemented 
- Authentication mechanism protecting API endponits

