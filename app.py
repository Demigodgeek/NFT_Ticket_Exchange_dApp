import streamlit as st
from web3 import Web3
from PIL import Image


Img = Image.open('./images/R.jpeg')
st.set_page_config(page_title = "GRAD DINNER",page_icon = Img)


# Connect to the local Ethereum blockchain
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

# Load the contract ABI and the deployed contract address
import json
with open('contract_abi.json', 'r') as f:
    contract_abi = json.load(f)

contract_address = "0x0d3D871AFd0F2B35918aD35dc3a49b25e130bF00"

# Create a contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Define the invitation price
INVITATION_PRICE = 10 * 10**18  # Assuming the price is set in wei (Ethereum's smallest unit)

# Set the maximum number of invitations
MAX_INVITATIONS = 8


def mint_invitation(sender, invitation_id):
    tx_hash = contract.functions.mintInvitation(invitation_id).transact({
        "from": sender,
        "value": INVITATION_PRICE
    })
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return receipt

def get_available_invitation_ids():
    invitation_ids = contract.functions.getAvailableInvitationIds().call()
    return invitation_ids

def get_invitation_owner(invitation_id):
    owner = contract.functions.getInvitationOwner(invitation_id).call()
    return owner

def gift_invitation(sender, recipient, invitation_id):
    tx_hash = contract.functions.giftInvitation(invitation_id, sender, recipient).transact({
        "from": sender
    })
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return receipt

def generate_receipt(invitation_id, sender):
    owner_address = get_invitation_owner(invitation_id)
    original_owner = contract.functions.getInvitationOwner(invitation_id).call()
    if owner_address.lower() == sender.lower() or original_owner.lower() == sender.lower():
        tx_hash = contract.functions.generateReceipt(invitation_id).transact({
            "from": sender
        })
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return receipt
    else:
        return None

def get_contract_balance(owner_address):
    contract_balance = contract.functions.contractBalance().call({"from": owner_address})
    return contract_balance

def withdraw_contract_balance(owner_address):
    tx_hash = contract.functions.withdrawBalance().transact({"from": owner_address})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return receipt


#################
### Streamlit ###
#################


st.title("Welcome to UCB Fintech Bootcamp Grad Dinner!")

# Mint Invitation and Available Invitation IDs Section
st.header("Purchase Invitation and Available Invitation IDs")
st.text("") # Add instructions 
st.header("The lower the Invitation Number, the closer the seat is to Firas and the TAs.")

# Get the available invitation IDs
available_ids = get_available_invitation_ids()

# Display the grid of images and buttons
for invitation_id in available_ids:
    cols = st.columns(2)
    invitation_image = f"images/invitation_{invitation_id}.jpg"  # Replace with the actual image file name

    with cols[0]:
        sender_key = f"sender_{invitation_id}"
        sender = st.text_input("Your Address", key=sender_key)

        if st.button(f"Purchase Invitation {invitation_id}"):
            mint_result = mint_invitation(sender, invitation_id)
            if mint_result is not None:
                st.success("Invitation minted successfully!")
                st.balloons()

        st.image(invitation_image, use_column_width=True)

# Generate Receipt Section
st.header("Generate Receipt")
st.header("Generate a receipt for your minted invitation")

receipt_invitation_id = st.number_input("Invitation ID", min_value=1, max_value=MAX_INVITATIONS, step=1)
receipt_owner_key = "receipt_owner_address"  # Unique key for the receipt owner text input
receipt_owner = st.text_input("Your Address", key=receipt_owner_key)

if st.button("Generate Receipt"):
    if Web3.isAddress(receipt_owner):
        owner_address = get_invitation_owner(receipt_invitation_id)
        if owner_address.lower() == receipt_owner.lower():
            receipt_result = generate_receipt(receipt_invitation_id, receipt_owner)
            if receipt_result is not None:
                st.success("Receipt generated successfully!")
            else:
                st.error("Failed to generate the receipt. Please try again.")
        else:
            st.warning("You are not the owner of this invitation.")
    else:
        st.warning("Invalid sender address.")


# Gift Invitation Section
st.header("Gift Invitation")
st.header("Gift your invitation to someone else")

gift_invitation_id = st.number_input("Invitation ID to Gift", min_value=1, max_value=MAX_INVITATIONS, step=1)
sender = st.text_input("Your Address")
recipient = st.text_input("Recipient Address")

if st.button("Gift Invitation"):
    if Web3.isAddress(sender) and Web3.isAddress(recipient):
        owner_address = get_invitation_owner(gift_invitation_id)
        if owner_address.lower() == sender.lower():
            gift_result = gift_invitation(sender, recipient, gift_invitation_id)
            if gift_result is not None:
                st.success("You have successfully gifted your invitation!")
                st.balloons()
            else:
                st.error("Failed to gift the invitation. Please try again.")
        else:
            st.warning("You are not the owner of this invitation.")
    else:
        st.warning("Invalid sender or recipient address.")

# Contract Balance Section
st.header("Contract Balance")
st.header("Retrieve the balance of the smart contract")

owner_address = st.text_input("Owner Address")

if st.button("Get Contract Balance"):
    if Web3.isAddress(owner_address):
        contract_balance = get_contract_balance(owner_address)
        st.success(f"Contract balance: {contract_balance} wei")
    else:
        st.warning("Invalid owner address.")

# Withdraw Contract Balance Section
st.header("Withdraw Contract Balance")
st.header("Withdraw the balance from the smart contract")

withdraw_owner_address_key = "withdraw_owner_address"  # Unique key for the withdraw owner address text input
withdraw_owner_address = st.text_input("Owner Address", key=withdraw_owner_address_key)

if st.button("Withdraw Contract Balance"):
    if Web3.isAddress(withdraw_owner_address):
        withdrawal_result = withdraw_contract_balance(withdraw_owner_address)
        if withdrawal_result is not None:
            st.success("Contract balance withdrawn successfully!")
            st.balloons()
        else:
            st.error("Failed to withdraw the contract balance. Please try again.")
    else:
        st.warning("Invalid owner address.")