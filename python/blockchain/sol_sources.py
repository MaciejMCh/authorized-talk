from os import path


def sol_named(sol_name: str):
    return path.join("..", "..", "solidity", sol_name + ".sol")
