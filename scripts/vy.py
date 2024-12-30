from ape import accounts, project
from scripts.utils import get_value, load_abi, get_event_abi
from hexbytes import HexBytes

#logs = [<<UnknownLogAtAddress_0xAb3769387C804443e60eC2C26630273466Cd0681_AndLogIndex_0> root=b''>, <<UnknownLogAtAddress_0xAb3769387C804443e60eC2C26630273466Cd0681_AndLogIndex_1> root=b''>, <<UnknownLogAtAddress_0xAb3769387C804443e60eC2C26630273466Cd0681_AndLogIndex_2> root=b''>, <<UnknownLogAtAddress_0xAb3769387C804443e60eC2C26630273466Cd0681_AndLogIndex_3> root=b''>, <<UnknownLogAtAddress_0xeeda48Dd015856B618e15B00dEa58c6763B1fc4d_AndLogIndex_4> root=b''>, <<UnknownLogAtAddress_0xeeda48Dd015856B618e15B00dEa58c6763B1fc4d_AndLogIndex_5> root=b''>, <<UnknownLogAtAddress_0xeeda48Dd015856B618e15B00dEa58c6763B1fc4d_AndLogIndex_6> root=b''>, <<UnknownLogAtAddress_0xeeda48Dd015856B618e15B00dEa58c6763B1fc4d_AndLogIndex_7> root=b''>, <<UnknownLogAtAddress_0xAb3769387C804443e60eC2C26630273466Cd0681_AndLogIndex_8> root=b''>, <<UnknownLogAtAddress_0xeeda48Dd015856B618e15B00dEa58c6763B1fc4d_AndLogIndex_9> root=b''>, <<UnknownLogAtAddress_0xAb3769387C804443e60eC2C26630273466Cd0681_AndLogIndex_10> root=b''>, <<UnknownLogAtAddress_0xeeda48Dd015856B618e15B00dEa58c6763B1fc4d_AndLogIndex_11> root=b''>, <<UnknownLogAtAddress_0x30b42766C5A5bAf80B383da3A5B57D5E000451ee_AndLogIndex_12> root=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'>, <<UnknownLogAtAddress_0x30b42766C5A5bAf80B383da3A5B57D5E000451ee_AndLogIndex_13> root=b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05k\xc7^-c\x10\x00\x00'>, <MarketInitialized market_id=b'\xb5\xa1\x1d\xa9\xdfp\x8f?9u\xfa\xcc\xa9\xdaj\x9d\xe8^\xcf\xd5\x15\x1a\xec3g+\xcb\xb6\xb5\xb4A\xdf' outcome1=YES outcome2=NO description=Manchester United Won the 2018 Champions League. outcome1_token=0xAb3769387C804443e60eC2C26630273466Cd0681 outcome2_token=0xeeda48Dd015856B618e15B00dEa58c6763B1fc4d reward=100000000000000000000 required_bond=5000000000000000000000>]


def main():
    abi = load_abi("../.build/abi/experiment.json")
    event_abi = get_event_abi(abi, "MarketInitialized")
    
    print(event_abi)
    
if __name__ == "__main__":
    main()