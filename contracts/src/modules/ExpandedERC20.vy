# pragma version ^0.4.0

from snekmate.auth import access_control as ctl
import ERC20 as erc20
from .interfaces import ExpandedIERC20

implements: ExpandedIERC20

initializes: ctl
initializes: erc20
exports: (
    ctl.__interface__,
    erc20.__interface__
)

MINT_ROLE: public(constant(bytes32)) = keccak256("MINT_ROLE")
BURN_ROLE: public(constant(bytes32)) = keccak256("BURN_ROLE")
MANAGER_ROLE: public(constant(bytes32)) = keccak256("MANAGER_ROLE")

@deploy
@payable
def __init__(
    _name: String[15],
    _symbol: String[5],
    _decimals: uint8
):
    """
    @notice Constructs the ExpandedERC20.
    """
    erc20.__init__(_name, _symbol, _decimals)
    ctl.__init__()
    
    # set 'admin_role' as "role's" admin role
    ctl._set_role_admin(MINT_ROLE, MANAGER_ROLE)
    ctl._set_role_admin(BURN_ROLE, MANAGER_ROLE)

    # set role admin
    ctl._grant_role(MANAGER_ROLE, msg.sender)

@external
def mint(_recipient: address, _value: uint256):
    """
    @dev Mints `_value` tokens to `_recipient`, returning true on success.
    @param _recipient address to mint to.
    @param _value amount of tokens to mint.
    """
    ctl._check_role(MINT_ROLE, msg.sender)
    erc20._mint(_recipient, _value)
    
@external
def burn(_value: uint256):
    """
    @dev Burns `_value` tokens owned by `msg.sender`.
    @param _value amount of tokens to burn.
    """
    ctl._check_role(BURN_ROLE, msg.sender)
    erc20._burn(msg.sender, _value)

@external
def burn_from(_recipient: address, amount: uint256):
    """
    @dev Destroys `amount` tokens from `owner`,
         deducting from the caller's allowance.
    @notice Note that `msg.sender` must have
        `BURN_ROLE`.
    @param _recipient address to burn tokens from.
    @param amount The 32-byte token amount to be destroyed.
    """
    ctl._check_role(BURN_ROLE, msg.sender)
    erc20._burn(_recipient, amount)

@external
def add_minter(_account: address):
    """
    @notice Grant Minter Role to an account.
    @dev The caller must have the `MANAGER_ROLE` or `DEFAULT_ADMIN_ROLE` roles.
    @param _account The address to which the Minter role is added.
    """
    ctl._grant_role(MINT_ROLE, _account)
    
@external
def add_burner(account: address):
    """
    @notice Grant Burner role to account.
    @dev The caller must have the `MANAGER_ROLE` or `DEFAULT_ADMIN_ROLE` role.
    @param account The address to which the Burner role is added.
    """
    ctl._grant_role(BURN_ROLE, account)