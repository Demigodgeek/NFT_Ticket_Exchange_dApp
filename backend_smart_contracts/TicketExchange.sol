pragma solidity ^0.8.0;

import "./TicketMint.sol";

contract TicketExchange {
    TicketMint private ticketMint;

    constructor(address ticketMintAddress) {
        ticketMint = TicketMint(ticketMintAddress);
    }

    function exchangeTickets(uint256 ticketId1, uint256 ticketId2) external {
        address sender = msg.sender;

        address owner1 = ticketMint.getTicketOwner(ticketId1);
        address owner2 = ticketMint.getTicketOwner(ticketId2);

        require(owner1 == sender || owner2 == sender, "Sender does not own either ticket");

        ticketMint.safeTransferFrom(owner1, owner2, ticketId1, 1, "");
        ticketMint.safeTransferFrom(owner2, owner1, ticketId2, 1, "");
    }
}