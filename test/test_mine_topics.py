from ethgoesbloom.constants import BLOOM_FILTER_BITS
from ethgoesbloom.miner import topics_to_calldata, num_filled_bits
from eth_bloom.bloom import BloomFilter


def test_mine_topics_should_succeed(mined_topics):
    bloom_filter = BloomFilter()
    for topic in mined_topics:
        topic_bytes = topic.to_bytes(32, byteorder='little')
        bloom_filter.add(topic_bytes)

    assert num_filled_bits(bloom_filter) == BLOOM_FILTER_BITS


def test_mine_topics_should_fill_real_filter(mined_topics, w3, deploy_contract):
    log_contract = deploy_contract('EthGoesBloom')

    calldata = topics_to_calldata(mined_topics)

    log_contract.sendLogs(calldata, transact={
        'from': w3.eth.accounts[0]
    })
    bloom_filter = w3.eth.getBlock('latest').logsBloom

    assert bloom_filter.count(b'\xff') == 256
