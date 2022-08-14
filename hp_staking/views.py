#Simple API Endpoints

#iMport for API calls
from rest_framework.decorators import api_view
from rest_framework.response import Response

#importing the functions for interacting with smart contracts
from hp_staking.integrations.staking import staking,escrow, deployHMToken_Contract, deployEscrowFactory_Contract


#We need to deploy a TOKEN contract which is mandatory for the EscrowFactory contract and pass its contract address to constructor 
@api_view(["POST"])
def deployEscrowFactory(request):
    # needs amount of how much to spend for staking
    #Calls staking method and returns the transaction hash if successful or error.
    
    deployEscrow = deployEscrowFactory_Contract(deployHMToken_Contract())

    return Response(deployEscrow, status=200)


#Staking API Call, @param amount is needed for how much staking you want to buy (msg.value) it accepts in wei
@api_view(["POST"])
def Stake(request):
    # needs amount of how much to spend for staking
    #Calls staking method and returns the transaction hash if successful or error.

    createStake = staking(amount=request.data.get('amount'))
    return Response(createStake, status=200)



#Creating an escrow is only possible if you are a stakeholder 
@api_view(["POST"])
def Escrow(request):
    
    #example trusted handlers are some of the accounts from ganache
    trustedHandlers = ['0x189bcD2EF0C0BD0160DAdBb859B15bbDAcee221E', '0x3F22cc5930E169cFbb06879a2a52dcA9E80d817F', '0x935237aF5c0eFb1384e7fBba67b6FeEB9f9559c0', '0xB7e377C31Dffe7075E3CF66c90ea70EA38119830']
    
    #requires a list of handlers/accounts as argument 
    createEscrow = escrow(trustedHandlers)

    return  Response(createEscrow, status=200)


