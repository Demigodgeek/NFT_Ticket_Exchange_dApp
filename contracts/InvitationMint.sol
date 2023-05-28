// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract InvitationMint is ERC1155, Ownable {
    using Counters for Counters.Counter;

    uint256 public constant INVITATION_PRICE = 10 ether;
    uint256 public constant MAX_INVITATIONS = 8;

    Counters.Counter private mintedInvitationCount;
    mapping(address => bool) private hasMintedInvitation;
    mapping(uint256 => bool) private hasMintedId;
    mapping(uint256 => address) private invitationOwners;

    event InvitationMinted(uint256 invitationId);
    event InvitationGifted(uint256 invitationId, address from, address to);
    event ReceiptGenerated(address recipient, uint256 invitationId, uint256 timestamp);

    constructor() ERC1155("") {
        mintedInvitationCount._value = 0;
    }

    function mintInvitation(uint256 invitationId) external payable {
        require(msg.value == INVITATION_PRICE, "Wrong price");
        require(mintedInvitationCount.current() < MAX_INVITATIONS, "No more invitations available");
        require(!hasMintedInvitation[msg.sender], "User has already minted an invitation");
        require(!hasMintedId[invitationId], "Invitation has already been minted");
        require(invitationId > 0 && invitationId <= MAX_INVITATIONS, "Invalid invitationId");

        hasMintedInvitation[msg.sender] = true;
        hasMintedId[invitationId] = true;
        mintedInvitationCount.increment();
        invitationOwners[invitationId] = msg.sender;

        _mint(msg.sender, invitationId, 1, "");

        emit InvitationMinted(invitationId);
    }
    
    function getInvitationOwner(uint256 invitationId) external view returns (address) {
        return invitationOwners[invitationId];
    }
    
    function generateReceipt(uint256 invitationId) external {
        require(hasMintedInvitation[msg.sender], "User has not minted an invitation");
        require(hasMintedId[invitationId], "Invalid invitationId");

        emit ReceiptGenerated(msg.sender, invitationId, block.timestamp);
    }

    function giftInvitation(uint256 invitationId, address from, address to) external {
        require(invitationOwners[invitationId] == from, "You are not the owner of the ticket");
        require(to != address(0), "Invalid recipient address");
        require(from != address(0), "Invalid sender address");

        safeTransferFrom(from, to, invitationId, 1, "");

        invitationOwners[invitationId] = to; // Update the invitation owner

        emit InvitationGifted(invitationId, from, to);
    }

    function getAvailableInvitationIds() external view returns (uint256[] memory) {
        uint256[] memory availableIds = new uint256[](MAX_INVITATIONS - mintedInvitationCount.current());
        uint256 currentIndex = 0;

        for (uint256 i = 1; i <= MAX_INVITATIONS; i++) {
            if (!hasMintedId[i]) {
                availableIds[currentIndex] = i;
                currentIndex++;
            }
        }

        return availableIds;
    }

    function contractBalance() external view onlyOwner returns (uint256) {
        return address(this).balance;
    }
    
    function withdrawBalance() external onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
    }
}