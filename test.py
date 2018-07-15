from web3 import Web3, HTTPProvider
from deployer import Deployer
from eth_bloom.bloom import BloomFilter, get_bloom_bits
from ethereum.utils import sha3
import random
import string
import datetime

w3 = Web3(HTTPProvider('http://localhost:8545'))
d = Deployer(w3)
d.compile_all()

c = d.deploy_contract('Test')

def get_topic_bits():
    return 10000000 + random.randint(0, 2**22 - 1)

def in_bloom(bloom_filter, value):
    return any(
        bloom_filter.value & bloom_bits
        for bloom_bits
        in get_bloom_bits(value)
    )

def in_bloom_last(bloom_filter, value, hits):
    num_hits = sum((bloom_filter.value & bloom_bits) != 0 for bloom_bits in get_bloom_bits(value))
    return num_hits == hits

def bloom_count(filter_value):
    return '{0:b}'.format(filter_value).count('1')

def bloom_complete(filter_value):
    return bloom_count(filter_value) == 2048


bloom_filter = BloomFilter()
events = []
tick = datetime.datetime.now()
max_events = 665

while len(events) < max_events:
    topic = get_topic_bits()
    topic_bytes = topic.to_bytes(32, byteorder='little')
    if not in_bloom(bloom_filter, topic_bytes):
        print(bloom_count(bloom_filter.value))
        bloom_filter.add(topic_bytes)
        events.append(topic)

print('Finding final bits')
while not bloom_complete(bloom_filter.value):
    topic = get_topic_bits()
    topic_bytes = topic.to_bytes(32, byteorder='little')
    if in_bloom_last(bloom_filter, topic_bytes, 2):
        print(bloom_count(bloom_filter.value))
        bloom_filter.add(topic_bytes)
        events.append(topic)

tock = datetime.datetime.now()
print(tock - tick)

calldata = b''.join(e.to_bytes(3, 'little') for e in events)
print('0x' + calldata.hex())
c.testAssembly(calldata, transact={
    'from': w3.eth.accounts[0]
})

block = w3.eth.getBlock('latest')
b = int.from_bytes(block.logsBloom, byteorder='big')
print(len(events))
print(bloom_count(bloom_filter.value))
print(bloom_count(b))
print(block.gasUsed)
print('{0:b}'.format(b))
print(b)