import streamlit as st
from web3 import Web3
from PIL import Image


# Connect to the local Ethereum blockchain
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

# Load the contract ABI and the deployed contract address
import json
with open('contract_abi.json', 'r') as f:
    contract_abi = json.load(f)

contract_address = "0x" # replace with the deployed contract address

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
    original_minter = contract.functions.getOriginalMinter(invitation_id).call()
    if owner_address.lower() == sender.lower() and sender.lower() == original_minter.lower():
        tx_hash = contract.functions.generateReceipt(invitation_id).transact({
            "from": sender
        })
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return receipt
    else:
        return None
    
def get_contract_balance(owner_address):
    try:
        contract_balance = contract.functions.contractBalance().call({"from": owner_address})
        return contract_balance
    except ValueError as e:
        error_message = str(e)
        if "caller is not the owner" in error_message:
            st.warning("You are not the owner of the contract.")
        else:
            st.error(f"Error: {error_message}")
        return None

def withdraw_contract_balance(owner_address):
    contract_balance = get_contract_balance(owner_address)
    if contract_balance is None:
        return None

    if Web3.isAddress(owner_address):
        if owner_address.lower() == contract.functions.owner().call().lower():
            if contract_balance == 0:
                st.warning("There is no balance to withdraw in the contract.")
                return None

            tx_hash = contract.functions.withdrawBalance().transact({"from": owner_address})
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            return receipt
        else:
            st.warning("You are not the owner of the contract.")
    else:
        st.warning("Invalid owner address.")
        return None


#################
### Streamlit ###
#################

# Set the page title and icon
Img = Image.open('./images/bootcamp.png')
st.set_page_config(page_title="GRAD DINNER", page_icon=Img, layout="wide")

# add background
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://raw.githubusercontent.com/Demigodgeek/from_zero_to_hero/main/background_p3.jpeg");
            background-attachment: fixed;
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
add_bg_from_url()

# Create a sidebar for user type selection
st.sidebar.markdown("<h1 style='text-align: center; color: #990000;'>Welcome to</h1> ", unsafe_allow_html=True)
st.sidebar.markdown("<h1 style='text-align: center; color: #990000;'>UCB FINTECH BOOTCAMP GRAD DINNER</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='background-color: #990000; height: 2px;'>", unsafe_allow_html=True)

user_type = st.sidebar.radio("Select User Type", ("Administrator", "Customer"))

if user_type == "Administrator":
    #################
    ### Contract Owner Section ###
    #################

    st.subheader("Administrator Operations")

     # Dropdown menu to choose operation
    operation = st.sidebar.selectbox("Choose an operation", ("Retrieve Contract Balance", " Withdraw Contract Balance"))

    if operation == "Retrieve Contract Balance":

        # Contract Balance Section
        st.header("Contract Balance")
        st.markdown("<h3 style='color: #990000;'>Retrieve the balance of the smart contract &#x1F4B0;</h3>", unsafe_allow_html=True)

        owner_address = st.text_input("Owner Address")

        if st.button("Get Contract Balance"):
            if Web3.isAddress(owner_address):
                if owner_address.lower() == contract.functions.owner().call().lower():
                    contract_balance = get_contract_balance(owner_address)
                    if contract_balance is not None:
                        st.success(f"Contract balance: {contract_balance} wei")
                    else:
                        st.warning("Failed to retrieve the contract balance. Please try again.")
                else:
                    st.warning("You are not the owner of the contract.")
            else:
                st.warning("Invalid owner address.")

    elif operation == " Withdraw Contract Balance":
        # Withdraw Contract Balance Section
        st.header("Withdraw Contract Balance")
        st.markdown("<h3 style='color: #990000;'>Withdraw the balance from the smart contract &#x1F4B3;</h3>", unsafe_allow_html=True)

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

else:
    #################
    ### Customer Section ###
    #################

    st.subheader("Customer Operations")

    # Dropdown menu to choose operation
    operation = st.sidebar.selectbox("Choose an operation", ("Purchase Invitation", "Generate Receipt", "Gift Invitation"))

    if operation == "Purchase Invitation":
        # Mint Invitation Section
        st.header("Purchase Invitation")
        st.markdown("<h3 style='color: #990000;'>How to purchase &#x1F4B8;</h3>", unsafe_allow_html=True)
    
        st.markdown("<ul>"
                    "<li style='text-align: left; font-size: 18px;'>"
                    "Each ticket costs <span style='color: #990000;'>10 ETH</span>."
                    "</li>"
                    "<li style='text-align: left; font-size: 18px;'>"
                    "Once an invitation has been purchased, that Invitation Number cannot be minted again."
                    "</li>"
                    "<li style='text-align: left; font-size: 18px;'>"
                    "The lower the Invitation Number, the closer the seat is to Firas and the TAs."
                    "</li>"
                    "<li style='text-align: left; font-size: 18px;'><span style='color: #990000;'>"
                    "If you want to gift the invitation to someone else, please generate a receipt before gifting. You are unable to generate the receipt as you are no longer the owner of the invitation."
                    "</li>"
                    "</ul>", unsafe_allow_html=True)
        
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        # Define the number of rows and columns for the grid
        num_rows = 2
        num_cols = 4

        # Get the available invitation IDs
        available_ids = get_available_invitation_ids()

        # Calculate the number of images that can fit in the grid
        num_images = num_rows * num_cols
        available_ids = available_ids[:num_images]  # Limit the number of images to the grid size

        # Display the grid of images, address inputs, and mint buttons
        for i in range(num_rows):
            cols = st.columns(num_cols)
            for j in range(num_cols):
                index = i * num_cols + j
                if index < len(available_ids):
                    invitation_id = available_ids[index]
                    invitation_image = f"images/invitation_{invitation_id}.png"  # Replace with the actual image file name

                    with cols[j]:
                        sender_key = f"sender_{invitation_id}"
                        sender = st.text_input("Your Wallet Address", key=sender_key)

                        if st.button(f"Purchase Invitation {invitation_id}"):
                            if Web3.isAddress(sender):
                                mint_result = mint_invitation(sender, invitation_id)
                                if mint_result is not None:
                                    st.success("Invitation purchased successfully!")
                                    st.balloons()
                                else:
                                    st.error("Failed to purchase invitation. Please try again.")
                            else:
                                st.warning("Invalid wallet address.")

                        
                        st.image(invitation_image, use_column_width=True)

    elif operation == "Generate Receipt":
        # Generate Receipt Section
        st.header("Generate Receipt")
        st.markdown("<h3 style='color: #990000;'>Generate a receipt for your purchased invitation &#x1F4C3;</h3>", unsafe_allow_html=True)

        receipt_invitation_id = st.number_input("Invitation Number", min_value=1, max_value=MAX_INVITATIONS, step=1)
        receipt_owner_key = "receipt_owner_address"  # Unique key for the receipt owner text input
        receipt_owner = st.text_input("Your Wallet Address", key=receipt_owner_key)

        if st.button("Generate Receipt"):
            if Web3.isAddress(receipt_owner):
                receipt_result = generate_receipt(receipt_invitation_id, receipt_owner)
                if receipt_result is not None:
                    st.success("Receipt generated successfully!")

                    # Display receipt information
                    receipt_info = f"Invitation ID: {receipt_invitation_id}\n" \
                                f"Owner Wallet Address: {receipt_owner}"
                    st.write(receipt_info)
                else:
                    st.warning("You are not the owner and/or you did not mint this invitation. Unable to generate a receipt.")
            else:
                st.warning("Invalid wallet address.")

    elif operation == "Gift Invitation":
        # Gift Invitation Section
        st.header("Gift Invitation")
        st.markdown("<h3 style='color: #990000;'>Gift your invitation to someone else &#x1F381;</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: left; font-size: 18px;'>"
                    " <span style='color: #990000;'>* If you would like to generate a receipt, you must do so before you gift your invitation</span>."
                    "</p>", unsafe_allow_html=True)


        gift_invitation_id = st.number_input("Invitation Number to Gift", min_value=1, max_value=MAX_INVITATIONS, step=1)
        gift_sender = st.text_input("Your Wallet Address")
        recipient = st.text_input("Recipient Wallet Address")

        if st.button("Gift Invitation"):
            if Web3.isAddress(gift_sender) and Web3.isAddress(recipient):
                owner_address = get_invitation_owner(gift_invitation_id)
                if owner_address.lower() == gift_sender.lower() and gift_sender.lower() != recipient.lower():
                    gift_result = gift_invitation(gift_sender, recipient, gift_invitation_id)
                    if gift_result is not None:
                        st.success("You have successfully gifted your invitation!")
                        st.balloons()
                    else:
                        st.error("Failed to gift invitation. Please try again.")
                elif owner_address.lower() != gift_sender.lower():
                    st.warning("You are not the owner of this invitation.")
                else:
                    st.warning("Recipient wallet address should be different from sender wallet address.")
            else:
                st.warning("Invalid sender or recipient wallet address.")


# Footer
footer_html = """
<style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f8f9fa;
        color: #6C63FF;
        text-align: center;
        padding: 10px 0;
        font-size: 14px;
        border-top: 1px solid #ddd;
    }
</style>
<div class="footer">
    Powered by <a href="https://www.streamlit.io" target="_blank">steamlit</a> | Created by [Demi, Jonny, Julio and Cary]
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)