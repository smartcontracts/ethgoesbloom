pragma solidity ^0.4.0;

import "./ByteUtils.sol";

contract Test {
    function testAssembly(bytes logData) public {
        for (uint i = 0; i < logData.length / 3; i += 4) {
            assembly {
                log4(0x80,
                     0x0,
                     and(calldataload(add(68, mul(i, 3))), 0xffffff0000000000000000000000000000000000000000000000000000000000),
                     and(calldataload(add(68, mul(add(i, 1), 3))), 0xffffff0000000000000000000000000000000000000000000000000000000000),
                     and(calldataload(add(68, mul(add(i, 2), 3))), 0xffffff0000000000000000000000000000000000000000000000000000000000),
                     and(calldataload(add(68, mul(add(i, 3), 3))), 0xffffff0000000000000000000000000000000000000000000000000000000000))
            }
        }
    }
}
