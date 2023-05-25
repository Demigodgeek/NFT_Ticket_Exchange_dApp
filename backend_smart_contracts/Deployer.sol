pragma solidity ^0.8.0;

import "./TicketMint.sol";
import "./TicketExchange.sol";

contract Deployer {
    TicketMint public ticketMint;
    TicketExchange public ticketExchange;

    constructor() {
        ticketMint = new TicketMint();
        ticketExchange = new TicketExchange(address(ticketMint));
    }

    function getTicketMintAddress() public view returns (address) {
        return address(ticketMint);
    }

    function getTicketExchangeAddress() public view returns (address) {
        return address(ticketExchange);
    }
}
 
