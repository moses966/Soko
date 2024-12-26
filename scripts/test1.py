from ape import accounts, project, Project

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

def main():
    deployer = accounts.load("my_wallet")

    # Initialize FixedPoint.Unsigned structures with raw values
    '''fixed_oracle_fee = {"rawValue": 0}  # Represents FixedPoint.Unsigned(0)
    weekly_delay_fee = {"rawValue": 0}  # Represents FixedPoint.Unsigned(0)

    # Deploy the StoreContract
    project.StoreContract.deploy(
        fixed_oracle_fee,
        weekly_delay_fee,
        "0x0000000000000000000000000000000000000000",  # Timer address
        sender=deployer
    )'''
    default_currency_contract = deployer.deploy(
        project.DefaultCurrency,
        default_currency_name,
        default_currency_symbol,
        default_currency_decimal,
        currency_initial_supply,
        currency_name_eip712,
        currency_version_eip712
    )

    '''# deploy optimistic oracle
    optimistic_oracle_contract = deployer.deploy(
        project.OOV3,
        finder_contract.address,
        default_currency_contract.address,
        default_liveness
    )
    edit_value("OOV3_address", optimistic_oracle_contract.address)
'''
    
if __name__ == "__main__":
    main()
