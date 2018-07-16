import datetime
from web3 import Web3, HTTPProvider
from ethgoesbloom.miner import mine_topics, topics_to_calldata
from ethgoesbloom.deployer import Deployer


def main():
    w3 = Web3(HTTPProvider('http://localhost:8545'))
    deployer = Deployer(w3)

    print('Compiling EthGoesBloom contract...')
    deployer.compile_all()
    
    print('Deploying EthGoesBloom contract...')
    log_contract = deployer.deploy_contract('EthGoesBloom')

    print('Mining for topics...')
    tick = datetime.datetime.now()
    topics = mine_topics()
    tock = datetime.datetime.now()
    print('Mined requried topics in {0}'.format(tock - tick))

    print('Sending EthGoesBloom.sendLogs transaction...')
    calldata = topics_to_calldata(topics)
    log_contract.sendLogs(calldata, transact={
        'from': w3.eth.accounts[0]
    })

    print('Getting latest bloom filter...')
    bloom_filter = w3.eth.getBlock('latest').logsBloom

    print('Latest bloom filter:')
    print('{0:b}'.format(int.from_bytes((bloom_filter), byteorder='big')))


if __name__ == '__main__':
    main()
