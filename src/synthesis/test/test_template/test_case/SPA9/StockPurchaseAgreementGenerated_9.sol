pragma solidity 0.5.16;
contract StockPurchaseAgreement {
    address payable public seller;
    address payable[] public buyer;
    string public sellerName;
    string[] public buyerName;
    uint public EffectiveTime;
    uint public CloseTime;
    uint public OutSideClosingDate;
    uint[1] public pricePayedByBuyer;
    bool[1] public purchaseSellerConfirmed;
    bool[1] public purchaseBuyerConfirmed;
    mapping(string => uint32) fileHashMap;
    bool[1] public terminateSellerConfirmed;
    bool[1] public terminateBuyerConfirmed;
    enum State {
        Created, Locked, Release, Transfered, Inactive }
    State[1] public state;
    event Payed(uint paymentIndex);
    event Released(uint paymentIndex);
    event Terminated(uint buyerIndex);
    event Terminated_OutOfDate();
    event Closed();
    constructor() public payable {
        EffectiveTime = 1257091200;
        CloseTime = 0;
        OutSideClosingDate = 0;
        sellerName = "";
        seller = address(0);
        buyerName =[""];
        buyer =[address(0)];
    }
    function pay_0() public payable {
        require(state[0] == State.Created || state[0] == State.Locked);
        require(msg.sender == buyer[0]);
        require(now <= CloseTime);
        uint256 price = 60000;
        require(msg.value == price);
        emit Payed(0);
        pricePayedByBuyer[0] += price;
        state[0] = State.Locked;
    }
    function purchaseConfirm(uint32 buyerIndex) public {
        require(buyerIndex < buyer.length);
        if(msg.sender == seller) {
            purchaseSellerConfirmed[buyerIndex] = true;
            return;
        }
        uint buyerNum = buyerName.length;
        for(uint i = 0;
        i < buyerNum;
        i ++) {
            if(msg.sender == buyer[i]) {
                purchaseBuyerConfirmed[i] = true;
                return;
            }
        }
    }
    function payRelease_0() public {
        require(msg.sender == buyer[0]);
        require(now <= CloseTime);
        require(purchaseBuyerConfirmed[0]);
        require(purchaseSellerConfirmed[0]);
        emit Released(0);
        state[0] = State.Release;
        seller.transfer(pricePayedByBuyer[0]);
        pricePayedByBuyer[0] = 0;
    }
    function uploadFileHash(string memory fileName, uint32 hashCode) public {
        bool validSender = false;
        if(msg.sender == seller) {
            validSender = true;
        }
        else {
            uint buyerNum = buyerName.length;
            for(uint i = 0;
            i < buyerNum;
            i ++) {
                if(msg.sender == buyer[i]) {
                    validSender = true;
                    break;
                }
            }
        }
        require(validSender);
        fileHashMap[fileName] = hashCode;
    }
    function close() public {
        require(now >= CloseTime);
        emit Closed();
        uint buyerNum = buyerName.length;
        for(uint i = 0;
        i < buyerNum;
        i ++) {
            state[i] = State.Inactive;
        }
    }
}
