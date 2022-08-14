#Simple API Endpoints

#iMport for API calls
from rest_framework.decorators import api_view
from rest_framework.response import Response

#importing the functions for interacting with smart contracts
from hp_staking.integrations.staking import staking,escrow, deployHMToken_Contract, deployEscrowFactory_Contract


#We need to deploy a TOKEN contract which is mandatory for the EscrowFactory contract and pass its contract address to constructor 
@api_view(["POST"])
def deployEscrowFactory(request):
    """
    Deploying Smart Contracts needed: 
    - HMToken.sol :  instance is needed for EscrowFactory
    - EscrowFactory.sol: Inherits the Staking.sol  and all functionalities needed
    """
    
    #The return of HMToken.sol is input as constructor for EscrowFactory.sol
    deployEscrow = deployEscrowFactory_Contract(deployHMToken_Contract())

    #It eturns the Contracts address - Use it for calling other functions
    return Response(deployEscrow, status=200)



@api_view(["POST"])
def Stake(request):
    """
    Staking API Call, @param amount:  is needed for how much staking you want to buy (msg.value) it accepts in wei
    @param contract_address: requires the contracts_addres of the EscrowFactory 
    """

    #Calls staking method and returns the transaction hash if successful or error.
    createStake = staking(amount=request.data.get('amount'), contract_address=request.data.get('contract_address'))
    return Response(createStake, status=200)




@api_view(["POST"])
def Escrow(request):
    """
    #Creating an escrow is only possible if you are a stakeholder 
    # @param trustedHandlers: requires a list trustedHandlers 
    # @param contract_address: requires the contracts_addres of the EscrowFactory 
    """
    #example trusted handlers are some of the accounts from ganache
    trustedHandlers = ['0x189bcD2EF0C0BD0160DAdBb859B15bbDAcee221E', '0x3F22cc5930E169cFbb06879a2a52dcA9E80d817F', '0x935237aF5c0eFb1384e7fBba67b6FeEB9f9559c0', '0xB7e377C31Dffe7075E3CF66c90ea70EA38119830']
    
    #requires a list of handlers/accounts as argument  and the contract address of the EscrowFactory deplyoed contract address
    createEscrow = escrow(trustedHandlers, contract_address=request.data.get('contract_address'))

    return  Response(createEscrow, status=200)


