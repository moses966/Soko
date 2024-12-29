import sys
import os
from ape import accounts, project
from scripts.oracle_sand_box.utils import edit_value, get_value
from scripts.oracle_sand_box import constants


class PredictionMarketManager:
    def __init__(self):
        self.deployer = accounts.load("account1")
        self.finder = get_value("finder_address")
        self.oov3 = get_value("OOV3_address")
        self.currency = get_value("currency_address")
        self.market_address = ""
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
        contract = self.deployer.deploy(
            project.experiment,
            self.finder,
            self.currency,
            self.oov3
        )
        edit_value("market", contract.address)
        self.market_address = contract.address
        print(f"Market deployed at: {self.market_address}")

    def mint_and_approve_tokens(self):
        """Mint and approve tokens for the market."""
        token = project.ERC20.at(self.currency)
        token.mint(constants.reward, sender=self.deployer)
        token.approve(self.market_address, constants.reward, sender=self.deployer)
        print(f"Minted and approved tokens for market at {self.market_address}")

    def init_market(self):
        """Initialize the prediction market."""
        pred_market = project.experiment.at(self.market_address)
        p = pred_market.initialize_market(
            constants.outcome_one,
            constants.outcome_two,
            constants.description,
            constants.reward,
            constants.required_bond,
            sender=self.deployer
        )
        self.market_id = p.return_value
        edit_value("market_id", self.market_id)
        print(f"Market initialized with ID: {self.market_id}")


def main():
    #method_flag = sys.argv[1]
    method_flag = os.getenv("APE_METHOD") # get method flag from environment variable
    manager = PredictionMarketManager()

    if method_flag == 'get_addresses':
        manager.get_addresses()
    elif method_flag == 'deploy_market':
        manager.deploy_prediction_market()
    elif method_flag == 'mint':
        manager.mint_and_approve_tokens()
    elif method_flag == 'init':
        manager.init_market()
    else:
        print("Invalid method number.")

if __name__ == "__main__":
    main()
