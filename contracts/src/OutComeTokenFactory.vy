# pragma version ^0.4.0

"""
@title OutComeTokenFactory
@author Phage-Chain Labs
@notice Factory contract to deploy outcome tokens.
"""

target: public(immutable(address))


@deploy
@payable
def __init__(_target: address):
    target = _target

@external
def deploy_outcome_token(
    _name: String[22],
    _symbol: String[5],
    _decimals: uint8
) -> address:
    """
    @notice Generically Deploys a new outcome token.
    @param _name Name of the token.
    @param _symbol Symbol of the token.
    @param _decimals Decimals of the token.
    @return address Address of the deployed token.
    """

    new_contract_address: address = create_from_blueprint(
        target,
        _name,
        _symbol,
        _decimals,
    )

    return new_contract_address