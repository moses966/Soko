import sys
import os
from ape import accounts, project
from eth_utils import to_bytes, to_hex
from hexbytes import HexBytes
from scripts.utils import edit_value, get_value
from scripts import constants


class PredictionMarketManager:
    def __init__(self):
        self.deployer = accounts.load("account1")
        self.finder = get_value("finder_address")
        self.oov3 = get_value("OOV3_address")
        self.currency = get_value("currency_address")
        self.ancillary = get_value("ancillary_data_address")
        self.market_address = ""
        self.expanded_token = ""
        self.address_whitelist = get_value("address_whitelist")
        self.outcome_token_factory_address = ""
        self.market_id = b""

    def get_addresses(self):
        """Retrieve and print addresses."""
        oov3_address = project.FinderContract.at(self.finder, fetch_from_explorer=False).getImplementationAddress(
            constants.OptimisticOracleV3,
            sender=self.deployer
        )
        default_currency = project.OOV3.at(self.oov3, fetch_from_explorer=False).defaultCurrency()
        print(f"OptimisticOracleV3 address: {oov3_address}")
        print(f"Currency: {default_currency}")

    def deploy_prediction_market(self):
        """Deploy the prediction market contract."""

        # deploy expanded token blueprint
        expanded_token_blueprint = self.deployer.declare(
            project.ExpandedERC20,
            "Expanded Token",
            "EXT",
            18
        )
        edit_value("expanded_token_blueprint_address", expanded_token_blueprint.contract_address)
        self.expanded_token = expanded_token_blueprint.contract_address

        # deploy outcome token factory
        outcome_token_factory = self.deployer.deploy(
            project.OutComeTokenFactory,
            self.expanded_token
        )
        edit_value("outcome_token_factory_address", outcome_token_factory.address)
        self.outcome_token_factory_address = outcome_token_factory.address

        contract = self.deployer.deploy(
            project.experiment,
            self.finder,
            self.address_whitelist,
            self.oov3,
            self.ancillary,
            self.currency,
            self.outcome_token_factory_address
            
        )
        edit_value("market_address", contract.address)
        self.market_address = contract.address
        print(f"Market deployed at: {self.market_address}")

    def mint_and_approve_tokens1(self):
        """Mint and approve tokens for the market."""
        _address = get_value("market_address")
        token = project.DefaultCurrency.at(self.currency, fetch_from_explorer=False)
        token.mint(self.deployer, constants.reward, sender=self.deployer)
        token.approve(_address, constants.reward, sender=self.deployer)

        allowance = token.allowance(self.deployer, _address)
        balance = token.balanceOf(self.deployer)
        print(f"Minted and approved tokens for market at {_address}")
        print(f"Balance: {balance}")
        print(f"Allowance: {allowance}")

    def init_market(self):
        """Initialize the prediction market."""
    
        # Load the deployed contract
        _address = get_value("market_address")
        
        # Mint and approve tokens for the market
        token = project.DefaultCurrency.at(self.currency, fetch_from_explorer=False)
        token.mint(self.deployer, constants.reward, sender=self.deployer)
        token.approve(_address, constants.reward, sender=self.deployer)

        pred_market = project.experiment.at(_address, fetch_from_explorer=False)
    
        # Call the initialize_market function
        receipt = pred_market.initialize_market(
            constants.outcome_one,
            constants.outcome_two,
            constants.description,
            constants.reward,
            constants.required_bond,
            sender=self.deployer
        )
        contract_balance = token.balanceOf(_address)
        print(f"Market initialized with balance: {contract_balance}")
    
        # Decode logs to find the MarketInitialized event
        decoded_logs = receipt.decode_logs()
        for log in decoded_logs:
            if log.event_name == "MarketInitialized":
                # extract the market_id
                self.market_id = log.market_id.hex()
                edit_value("market_id", self.market_id)

                # extract the outcome token addresses
                outcome_token_one = log.outcome1_token
                edit_value("outcome1_token_address", outcome_token_one)
                outcome_token_two = log.outcome2_token
                edit_value("outcome2_token_address", outcome_token_two)
                break

    def create_outcome_tokens(self):
        """Create the outcome tokens."""
        _address = get_value("market_address")
        _id = get_value("market_id")
        #_market_id = to_bytes(hexstr=_id)
        _market_id = HexBytes(_id)


        token = project.DefaultCurrency.at(self.currency, fetch_from_explorer=False)
        token.mint(self.deployer, constants.amount, sender=self.deployer)
        token.approve(_address, constants.amount, sender=self.deployer)
        print(token.balanceOf(self.deployer))

        pred_market = project.experiment.at(_address, fetch_from_explorer=False)
        pred_market.create_outcome_tokens(_market_id, constants.amount, sender=self.deployer)

        outcome_token_one = get_value("outcome1_token_address")
        outcome_token_two = get_value("outcome2_token_address")
        token_one = project.ExpandedERC20.at(outcome_token_one, fetch_from_explorer=False)
        token_two = project.ExpandedERC20.at(outcome_token_two, fetch_from_explorer=False)
        
        # With an amount 10,000 units of default_currency we get 10,000 outcome1_token and 10,000 outcome2_token tokens
        balance_one = token_one.balanceOf(self.deployer)
        balance_two = token_two.balanceOf(self.deployer)
        print(f"Outcome token 1 balance: {balance_one}")
        print(f"Outcome token 2 balance: {balance_two}")


def main():
    method_flag = os.getenv("APE_METHOD") # get method flag from environment variable
    manager = PredictionMarketManager()

    if method_flag == 'get_addresses':
        manager.get_addresses()
    elif method_flag == 'deploy_market':
        manager.deploy_prediction_market()
    elif method_flag == 'init':
        manager.init_market()
    elif method_flag == 'create':
        manager.create_outcome_tokens()
    else:
        print("Invalid method number.")

if __name__ == "__main__":
    main()
