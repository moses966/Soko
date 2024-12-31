from ape import project, accounts

def main():
    deployer = accounts.load("account1")
    contract = deployer.deploy(project.ExpandedERC20, "Expanded Token", "EXT", 18)
    #contract.add_minter(deployer, sender=deployer)
    contract.mint(deployer, int(100e18), sender=deployer)
    print(contract.balanceOf(deployer) / 1e18)

if __name__ == "__main__":
    main()
