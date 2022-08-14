// SPDX-License-Identifier: MIT

pragma solidity 0.6.2;

import "./SafeMath.sol";

contract Staking {
    using SafeMath for uint256;
    //Contract owner
    address public owner;

    //Total staked
    uint public stakes;
    
    // User address => staked amount
    mapping(address => uint) public balanceOf;
    // Map Users contribution to the stake
    mapping(address => uint) public deposits;
    

    mapping (address => uint256) public votesReceived;
    address[] public candidateList;

    //Stakeholders list 
    address[] public stakeholders;

    constructor() public{
        owner = msg.sender;
    }
    
    // mapping(address => uint) balances; 

    //Everyone can become stakeholder/validator by staking more than 1 Wei 
    function staking() external payable  {
        uint _amount = msg.value;
        address _account = msg.sender;
        
        require(msg.sender != address(0));
        require(msg.value >= 1 wei, "You can stake 1 or more Wei"); 
        // require(msg.value != 0);
        
        //Total Amount of Ether staked (to keep track) 
        stakes += _amount;
        //add the amount staked to the contract balance 
        balanceOf[address(this)] +=  _amount ;
        //Keep track each staking that a stakeholder made
        deposits[msg.sender] += _amount;
          
        //Check if this person is already a stakeholder and add them to the list
        (bool _isStakeholder ) = isStakeholder(_account);
            if (!_isStakeholder) stakeholders.push(_account);
       
  }
   
    function withdraw(uint amount) external onlyStakeholder{
        (bool success,)=owner.call{value:amount}("");
        require(success, "Transfer failed!");
        require(deposits[msg.sender] != 0, "You cant withdraw 0");
        require(deposits[msg.sender] > amount, "You dont have that amount of deposits");

        deposits[msg.sender] -= amount;
        stakes -= amount;
        balanceOf[address(this)] -= amount;
        balanceOf[msg.sender] += amount; 
        //DEPOSITS NEEDS TO BE Subscracted.
    }

    // This function returns the total votes a candidate has received so far
    function totalVotesFor(address candidate) view public returns (uint256) {
        // require(validCandidate(candidate));
        return votesReceived[candidate];
    }

    // This function increments the vote count for the specified candidate. This
    // is equivalent to casting a vote
    function voteForCandidate(address candidate) public  onlyStakeholder{
        require(msg.sender != address(0));
        require(candidate != address(0));
        
        //TODO: I dont need this check
        (bool _isCandidate ) = isCandidate(candidate);
        if (!_isCandidate) candidateList.push(candidate);
        votesReceived[candidate] += 1;
    }
  
    function penalty(address _account  ) public  onlyStakeholder {
        require(validCandidate(_account), "This candidate is not in penalty list of participants");
        require(msg.sender != address(0));
        require(currentBalance(_account) != 0, "This account has no balance");
        
        uint amountSlashed = 10 wei; 
        deposits[_account] = deposits[_account].sub(amountSlashed); 
        balanceOf[msg.sender] -= amountSlashed; 
        //Get the tokens from  bad participant penalty and add it to the contract staking pool 
        balanceOf[address(this)] += amountSlashed;
    }

    function rewards(address _account) public  onlyOwner{
        //Check if this participant is in the list of bad actors;
        require(!validCandidate(_account), "This candidate is not in penalty list of participants");
        uint rewardAmount = 5 wei;
        //this user's balance should increase by 5 as rewards stated  
        balanceOf[msg.sender] += rewardAmount; 
        // the Contract which serves as staking pool should have 5 less amount of tokens;
        balanceOf[address(this)] -= rewardAmount;
    }


    //HELPER FUNCTIONS

    function currentBalance(address _account) public view returns(uint) {
        return _account.balance;
    } 


    modifier onlyStakeholder {
        bool found = false;
        for (uint256 s = 0; s < stakeholders.length; s++) {
            if (msg.sender == stakeholders[s]){
                found = true;
            }
        }
        require(found, "User is not a STAKEHOLDER");
        _;
    }

 // Modifier to check that the caller is the owner of
    // the contract.
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        // Underscore is a special character only used inside
        // a function modifier and it tells Solidity to
        // execute the rest of the code.
        _;
    }
    // function getBalance(address _stakeholder) public view returns (uint){
    //     return balanceOf[_stakeholder];
    // }

    function isStakeholder(address _address) internal view returns(bool)
        {
            for (uint256 s = 0; s < stakeholders.length; s += 1){
                if (_address == stakeholders[s]) return (true);
            }
            return (false);
        }

    function isCandidate(address _address) internal view returns(bool)
        {
            for (uint256 s = 0; s < candidateList.length; s += 1){
                if (_address == candidateList[s]) return (true);
            }
            return (false);
        }

    function validCandidate(address candidate) internal view returns (bool) {
        for(uint i = 0; i < candidateList.length; i++) {
        if (candidateList[i] == candidate) {
            return true;
        }
        }
        return false;

}
}