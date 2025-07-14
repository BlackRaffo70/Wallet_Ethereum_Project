const WalletContract = artifacts.require("wallet_contract");

module.exports = async function (deployer, network, accounts) {
  const owners = [accounts[0], accounts[1]];  // almeno uno
  const requiredConfirmations = 1;           // tra 1 e owners.length

  console.log("Deploying with owners:", owners);
  console.log("Required confirmations:", requiredConfirmations);

  await deployer.deploy(WalletContract, owners, requiredConfirmations);
};
