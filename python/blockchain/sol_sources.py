from os import path


def root_dir():
    return path.dirname(path.abspath(__file__))


def sol_named(sol_name: str):
    return path.join(root_dir(), "..", "..", "solidity", sol_name + ".sol")
