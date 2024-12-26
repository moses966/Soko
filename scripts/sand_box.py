import os
import json
from ape import project, accounts

# parameters
default_identifier = f"ASSERT_TRUTH"
minimum_bond = int(100e18)
default_liveness = int(7200) # 2 hrs
default_currency_name = f"Phage Token"
default_currency_symbol = f"PUSDT"
currency_initial_supply = int(1000000e18)
currency_name_eip712 = f"Currency"
currency_version_eip712 = f"1"
default_currency_decimal = int(18)
token1_name = f"Outcome1 Token"
token1_symbol = f"OUT1"
token2_name = f"Outcome2 Token"
token2_symbol = f"OUT2"
_decimals = int(18)
empty_address = f"0x0000000000000000000000000000000000000000"

# Initialize FixedPoint.Unsigned structures with raw values
fixed_oracle_fee = {"rawValue": 0}  # Represents FixedPoint.Unsigned(0)
weekly_delay_fee = {"rawValue": 0}  # Represents FixedPoint.Unsigned(0)

base_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = f"./deployments.json"

def edit_value(_key, _value):
    file_path = os.path.join(base_dir, relative_path)
    with open(file_path, "r") as file:
        data = json.load(file)
    
    data[_key] = _value

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def get_value(_key):
    file_path = os.path.join(base_dir, relative_path)
    with open(file_path, "r") as file:
        data = json.load(file)
    
    return data[_key]

def deploy_contracts():
    
    deployer = accounts.load('account1') # load deployer address

    # deploy store
    store_contract = deployer.deploy(
        project.StoreContract,
        fixed_oracle_fee,
        weekly_delay_fee,
        empty_address
    )
    edit_value("store_contract_address", store_contract.address)

    # deploy ancillary data contract
    ancillary_data_contract = deployer.deploy(project.AncillaryDataInterface)
    edit_value("ancillary_data_address", ancillary_data_contract.address)
    
    # deploy finder contract
    finder_contract = deployer.deploy(project.FinderContract)
    edit_value("finder_address", finder_contract.address)

    # deploy mock oracle ancillary contract
    mock_oracle_ancillary_contract = deployer.deploy(
        project.MockAncillaryContract,
        finder_contract.address,
        empty_address
    )
    edit_value("mock_oracle_address", mock_oracle_ancillary_contract.address)

    # deploy default courrency(token) address
    default_currency_contract = deployer.deploy(
        project.DefaultCurrency,
        default_currency_name,
        default_currency_symbol,
        default_currency_decimal,
        currency_initial_supply,
        currency_name_eip712,
        currency_version_eip712
    )
    edit_value("currency_address", default_currency_contract.address)

    # deploy AddressWhitelistContract
    address_whitelist_contract = deployer.deploy(project.AddressWhitelistContract)
    edit_value("address_whitelist", address_whitelist_contract.address)

    # deploy outome_tokens
    outcome1_token_contract = deployer.deploy(
        project.ExpandedERC20,
        token1_name,
        token1_symbol,
        _decimals
    )
    outcome2_token_contract = deployer.deploy(
        project.ExpandedERC20,
        token2_name,
        token2_symbol,
        _decimals
    )
    edit_value("outcome1_token_address", outcome1_token_contract.address)
    edit_value("outcome2_token_address", outcome2_token_contract.address)

def main():

    # 1. Deploy UMA ecosystem contracts with mocked oracle and selected currency.
    deploy_contracts()

if __name__ == "__main__":
    main()