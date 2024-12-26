# pragma version ^0.4.0

from snekmate.tokens import erc20 as token
from snekmate.auth import ownable as ow

initializes: ow
initializes: token[ownable := ow]
exports: token.__interface__


@deploy
@payable
def __init__(
    name_: String[25],
    symbol_: String[5],
    decimals_: uint8,
    initial_supply_: uint256,
    name_eip712_: String[50],
    version_eip712_: String[20],
):
    ow.__init__()
    token.__init__(name_, symbol_, decimals_, name_eip712_, version_eip712_)

    token._mint(msg.sender, initial_supply_ * 10 ** convert(decimals_, uint256))
