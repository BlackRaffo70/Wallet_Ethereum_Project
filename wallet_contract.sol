
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract wallet_contract {
    /* ─────────── storage ─────────── */
    address[] public owners;
    uint256   public numConfirmationsRequired;

    struct Transaction {
        address to;
        uint256 value;
        bytes   data;
        bool    executed;
        uint256 numConfirmations;
    }

    Transaction[] public transactions;
    mapping(uint256 => mapping(address => bool)) public isConfirmed;

    /* ─────────── events ─────────── */
    event SubmitTransaction(
        address indexed owner,
        uint256 indexed txIndex,
        address indexed to,
        uint256 value,
        bytes   data
    );
    event ConfirmTransaction(address indexed owner, uint256 indexed txIndex);
    event ExecuteTransaction(address indexed owner, uint256 indexed txIndex);

    /* ─────────── constructor ─────────── */
   constructor(address[] memory _owners, uint256 _req) {
    require(_owners.length > 0,                "at least one owner");
    require(_req > 0 && _req <= _owners.length,"invalid confirmations");

    for (uint i = 0; i < _owners.length; i++) {
        owners.push(_owners[i]);
    }

    numConfirmationsRequired = _req;
}

    /* ─────────── actions ─────────── */
    function submitTransaction(address _to, uint256 _value, bytes memory _data)
        external
    {
        transactions.push(
            Transaction({
                to:    _to,
                value: _value,
                data:  _data,
                executed:       false,
                numConfirmations: 0
            })
        );

        emit SubmitTransaction(msg.sender, transactions.length - 1, _to, _value, _data);
    }

    function confirmTransaction(uint256 _txIndex) external {
        require(_txIndex < transactions.length, "invalid tx index");
        Transaction storage t = transactions[_txIndex];
        require(!t.executed, "already executed");
        require(!isConfirmed[_txIndex][msg.sender], "already confirmed");

        isConfirmed[_txIndex][msg.sender] = true;
        t.numConfirmations += 1;

        emit ConfirmTransaction(msg.sender, _txIndex);
    }

    function executeTransaction(uint256 _txIndex) external {
        Transaction storage t = transactions[_txIndex];
        require(!t.executed,                              "already executed");
        require(t.numConfirmations >= numConfirmationsRequired, "not enough confirmations");

        t.executed = true;
        (bool ok, ) = t.to.call{value: t.value}(t.data);
        require(ok, "tx failed");

        emit ExecuteTransaction(msg.sender, _txIndex);
    }

    /* ─────────── helpers (view) ─────────── */
    function getTransaction(uint256 _i) external view
        returns (address to, uint256 value, bytes memory data, bool executed, uint256 numC)
    {
        Transaction storage t = transactions[_i];
        return (t.to, t.value, t.data, t.executed, t.numConfirmations);
    }

    function getTransactionCount() external view returns (uint256) {
        return transactions.length;
    }

    receive() external payable {}
}