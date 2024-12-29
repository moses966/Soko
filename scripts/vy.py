from ape import accounts, project
import time


def main():
    deployer = accounts.load("account1")
    
    # Deploy Blueprint
    blueprint_contract = deployer.declare(project.BlueprintExample)
    print(f"Blueprint Address: {blueprint_contract.contract_address}")
    
    # Deploy Factory
    factory = deployer.deploy(
        project.BluePrintFactory,
        blueprint_contract.contract_address
    )
    
    # deploy new copy
    blueprint = factory.deploy_blueprint(sender=deployer)
    address = blueprint.return_value

    contract = project.BlueprintExample.at(address)
    number = contract.number()
    
    print(f"Number after deployment: {number}")
    print(contract.add(3, 4, sender=deployer))
    print(f"Address: {address}")

    number = contract.number()
    print(f"Number after add(x,y): {number}")
    
if __name__ == "__main__":
    main()