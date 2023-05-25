pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract TicketMint is ERC1155, Ownable {
    
    uint256 private constant VIP_TICKET_SUPPLY = 100;
    uint256 private constant VIP_TICKET_PRICE = 1 ether;
    
    struct Ticket {
        string seatNumber;
        address owner;
    }
    
    mapping(uint256 => Ticket) private tickets;
    mapping(address => bool) private hasMinted;
    mapping(string => bool) private seatMinted;
    
    uint256 private ticketSupply;
    uint256 private seatCounter;

    event TicketMinted(address owner, uint256 ticketId, string seatNumber);

    constructor() ERC1155("") {
        ticketSupply = VIP_TICKET_SUPPLY;
        seatCounter = 1;
    }

    function mintTicket(address owner, string memory seatNumber) external payable {
        require(ticketSupply > 0, "All VIP tickets sold");
        require(msg.value == VIP_TICKET_PRICE, "Incorrect ticket price");
        require(hasMinted[owner] == false, "User has already minted an NFT");
        require(seatMinted[seatNumber] == false, "Seat number has already been minted");

        uint256 ticketId = seatCounter;
        _mint(owner, ticketId, 1, "");
        hasMinted[owner] = true;
        ticketSupply--;
        seatCounter++;

        tickets[ticketId] = Ticket(seatNumber, owner);

        emit TicketMinted(owner, ticketId, seatNumber);
    }

    function getTicketOwner(uint256 ticketId) external view returns (address) {
        return tickets[ticketId].owner;
    }

    function getTicketSeatNumber(uint256 ticketId) external view returns (string memory) {
        return tickets[ticketId].seatNumber;
    }

    function getTicketSupply() external view returns (uint256) {
        return ticketSupply;
    }

    function isTicketAvailable(uint256 ticketId) external view returns (bool) {
        return ticketSupply > 0 && tickets[ticketId].owner == address(0);
    }

    function refundFailedMinting() external {
        require(hasMinted[msg.sender] == true, "You haven't minted any tickets");

        uint256 ticketId = 0;
        for (uint256 i = 1; i < seatCounter; i++) {
            if (tickets[i].owner == msg.sender) {
                ticketId = i;
                break;
            }
        }

        require(ticketId != 0, "No tickets owned by you");

        _burn(msg.sender, ticketId, 1);
        hasMinted[msg.sender] = false;
        ticketSupply++;
    }

}