import random
from eth_bloom.bloom import BloomFilter, get_bloom_bits
from ethgoesbloom.constants import BLOOM_FILTER_BITS


def num_disjoint_bits(data, bloom_filter):
    """Determines how many bits this data fills in the filter.

    Args:
        data (bytes): Data to add to the filter.
        bloom_filter (BloomFilter): Bloom filter object to check against.

    Returns:
        int: Number of bits that would be filled by this data.
    """

    return sum((bloom_filter.value & bloom_bits) == 0 for bloom_bits in get_bloom_bits(data))


def num_filled_bits(bloom_filter):
    """Determines how many bits in a filter are filled.

    Args:
        bloom_filter (BloomFilter): Bloom filter object to check.

    Returns:
        int: Number of filled bits in the filter.
    """

    return '{0:b}'.format(bloom_filter.value).count('1')


def get_random_topic(num_bits=24):
    """Returns a random integer with a specified number of bits.

    Args:
        num_bits (int): Number of bits in the integer.

    Returns:
        int: Integer with the specified number of bits.
    """

    return random.getrandbits(num_bits - 1) + (1 << (num_bits - 1))


def mine_topics():
    """Mines required topics to fill the filter.

    Returns:
        bytes[]: List of required topics.
    """

    bloom_filter = BloomFilter()
    topics = []
    filled_bits = 0
    required_hits = 3
    while filled_bits < BLOOM_FILTER_BITS:
        topic = get_random_topic()
        topic_bytes = topic.to_bytes(32, byteorder='little')
        if num_disjoint_bits(topic_bytes, bloom_filter) == required_hits:
            bloom_filter.add(topic_bytes)
            filled_bits = num_filled_bits(bloom_filter)
            if filled_bits > 2000:
                required_hits = 2
            if filled_bits == 2047:
                required_hits = 1
            topics.append(topic)
    return topics


def topics_to_calldata(topics, bytes_per_topic=3):
    """Converts a list of topics to calldata.

    Args:
        topics (bytes[]): List of topics.
        bytes_per_topic (int): Byte length of each topic.

    Returns:
        bytes: Topics combined into a single string.
    """

    return b''.join(topic.to_bytes(bytes_per_topic, byteorder='little') for topic in topics)
