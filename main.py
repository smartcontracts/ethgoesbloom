from ethgoesbloom.miner import mine_topics, topics_to_calldata


def main():
    topics = mine_topics()
    calldata = topics_to_calldata(topics)
    print('0x' + calldata.hex())


if __name__ == '__main__':
    main()
