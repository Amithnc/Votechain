pragma solidity 0.4.20;

contract Election {
    // Model a Candidate
    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

address public chairperson;
    
    mapping(address=>bool)public status;

    // Store accounts that have voted
    mapping(address => bool) public voters;
    // Store Candidates
    // Fetch Candidate
    mapping(uint => Candidate) public candidates;
    // Store Candidates Count
    uint public candidatesCount;

    // voted event
    event votedEvent (
        uint indexed _candidateId
    );
    function Election() public{
        chairperson = msg.sender;
    }

    function addCandidate (string _name) public {
        require(msg.sender == chairperson);
        candidatesCount ++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, 0);
    }
    
    function approve (address _address) public {
        require(
            msg.sender == chairperson);
        status[_address]=true;
    }
  

    function vote (uint _candidateId) public {
        // require that they haven't voted before
        require(status[msg.sender]);
        require(!voters[msg.sender]);

        // require a valid candidate
        require(_candidateId > 0 && _candidateId <= candidatesCount);

        // record that voter has voted
        voters[msg.sender] = true;

        // update candidate vote Count
        candidates[_candidateId].voteCount ++;

        // trigger voted event
        votedEvent(_candidateId);
    }
}