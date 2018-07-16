import pytest
from web3 import Web3, HTTPProvider
from ethgoesbloom.miner import mine_topics
from ethgoesbloom.deployer import Deployer


# Only compile and mine topics once to speed things up
deployer = Deployer()
deployer.compile_all()

print('Mining topics, this might take a while...')
topics = mine_topics()
print('Mined topics, starting tests!')


@pytest.fixture
def mined_topics():
    return topics


@pytest.fixture
def w3():
    return Web3(HTTPProvider('http://localhost:8545'))


@pytest.fixture
def deploy_contract():
    def deploy(contract_name):
        return deployer.deploy_contract(contract_name)
    return deploy
