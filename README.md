
# Grad Invite Manager: Ethereum-based dApp for Grad Dinner Invitation Trading and Management

---

**Problem**
The traditional process of managing and trading graduation dinner invitations is often tedious, time-consuming, and prone to errors. It typically involves manual tracking, physical paperwork, and reliance on intermediaries to facilitate the exchange of invitations. This process can be inefficient, costly, and lack transparency, leading to frustration and inconvenience for both administrators and customers.

**Solution**
The Ethereum-based Grad Dinner Invitation Trading and Management dApp offers a streamlined solution to address the challenges associated with managing and trading graduation dinner invitations. By leveraging the power of blockchain technology, the dApp provides a secure, transparent, and efficient platform for administrators and customers to interact.

---

## Technologies

- The dApp's backend is built using Solidity, the programming language for Ethereum smart contracts.
- ERC-1155 token standard is imported in the smart contract, which provides the basic functionalities required for creating and managing ERC-1155 tokens.
- Ownable.sol contract from the OpenZeppelin library is imported in the smart contract, which is a basic contract that provides an ownership mechanism. 
- The dApp's frontend is developed using the Streamlit framework, a Python library for building interactive web applications.
- Web3.js is utilized to interact with the Ethereum blockchain and facilitate communication between the dApp and the Ethereum network.
- The dApp utilizes the ABI (Application Binary Interface) to establish a seamless connection between the smart contract and the Streamlit interface.
- Metamask, a browser extension, is used for secure wallet management and transaction signing.
- The project utilizes the Remix IDE and Ganache, for smart contract development, testing, and deployment.

The project follows the best practices for Ethereum development, including security considerations and event-driven programming.
By utilizing these technologies, the Ethereum-based Grad Dinner Invitation Trading and Management dApp provides a robust and efficient solution for managing and trading graduation dinner invitations on the Ethereum blockchain.


---
## Installation Guide

**`Python`** (This code is executed with Python 3.10 & 3.8 & 3.7, here takes Python 3.10 for example)
To install Python 3.10 on your system, please follow these steps:
1. Visit the official Python website at https://www.python.org/downloads/.
2. Scroll down to the "Python Releases for Windows/macOS/Linux" section.
3. In this section, you should see a list of available Python versions. Look for the Python 3.10 version and click on it.
4. On the next page, scroll down to find the installer files. Choose the appropriate installer for your operating system (Windows, macOS, or Linux) and click on the download link.
5. Once the installer is downloaded, locate the file and run it.
6. Follow the instructions provided by the installer. You may be prompted to select installation options and customize settings. By default, it is recommended to select the options that include adding Python to your system's PATH environment variable.
7. Proceed with the installation, and the Python 3.10 interpreter will be installed on your system.
After the installation is complete, you can open a terminal or command prompt and type python --version to verify that Python 3.10 is installed. The command should display the version number.

**`Solidity`**
To install Solidity, you can follow these steps:
1. Open your command-line interface (CLI) or terminal.
2. Check if you have Node.js installed by running the command `node -v`. If Node.js is not installed, you can download and install it from the official Node.js website (https://nodejs.org).
3. Once you have Node.js installed, you can install Solidity by running the command `npm install -g solc`. This command installs the Solidity compiler globally on your system.
4. After the installation is complete, you can verify if Solidity is installed correctly by running the command `solc --version`. This command will display the version of Solidity installed on your system.

**Create new environment for this project**
1. After you install both Python and Solidity, you can create a new virtual environment for this project by running the following command: `python -m venv web3`
2. Activate the newly created environment by running the following command: `conda activate web3`
3. When the environment is activated, you should see the environment name in your terminal prompt.

**`web3`**
The web3 library should be installed separately to interact with the Ethereum blockchain and smart contracts.
To install web3, you can use the command: `pip install web3`

**`PIL`**
To install the Python Imaging Library (PIL), you can follow these steps:
1. Open a terminal or command prompt.
2. Run the following command in your terminal or command prompt:`pip install Pillow` PIL has been deprecated and Pillow is the recommended fork that provides the same functionality.
3. After the installation is complete, you can verify that PIL is installed correctly by running the following command: `python -c "from PIL import Image; print(Image.__version__)"` This command will display the installed version of PIL.

**`Visual Studio Code`**
To install Visual Studio Code (VS Code), follow these steps:
1. Visit the official website of Visual Studio Code at https://code.visualstudio.com/.
2. Click on the "Download" button, which should detect your operating system automatically and provide the appropriate download option.
3. Once the download is complete, locate the installer file and run it.
4. Follow the instructions provided by the installer. These may vary depending on your operating system.
5. During the installation, you may be prompted to select additional components or configure certain settings. You can choose the options that suit your preferences or go with the default settings.
6. After the installation is finished, you can launch Visual Studio Code from your applications or programs menu.

**`Ganache`**
To install Ganache, you can follow these steps:
1. Visit the official Ganache website at https://www.trufflesuite.com/ganache and navigate to the "Downloads" section.
2. Select the appropriate version of Ganache for your operating system (Windows, macOS, or Linux) and download the installer.
3. Run the installer and follow the on-screen instructions to complete the installation process.

**`MetaMask`**
To install MetaMask, follow these steps:
1. Open your preferred web browser (Chrome, Firefox, Brave, or Edge).
2. Go to the MetaMask website: https://metamask.io/
3. Click on the "Get Chrome Extension" (or "Get Firefox Extension", etc.) button, depending on your browser.
4. You will be redirected to the respective browser extension store (e.g., Chrome Web Store for Chrome).
5. Click on the "Add to Chrome" (or "Add to Firefox", etc.) button to start the installation.
6. A pop-up will appear, asking for confirmation. Click on "Add extension" to proceed.
7. After the installation is complete, you will see the MetaMask icon in your browser's toolbar.
8. Click on the MetaMask icon to open the extension.
9. Follow the on-screen instructions to create a new MetaMask wallet or import an existing one.
10. Set up a password and backup seed phrase as per the instructions.
11. Once your wallet is set up, you can use MetaMask to connect to Ethereum networks and interact with dApps.

**`Streamlit`**
To install Streamlit, you can follow these steps:
1. Open a terminal or command prompt.
2. Ensure that you have Python installed on your system. You can check by running the command python --version. If Python is not installed, please install it first.
3. Once you have Python installed, you can install Streamlit using the pip package manager. Run the following command in your terminal or command prompt:
`pip install streamlit` This command will download and install Streamlit and its dependencies.
4. After the installation is complete, you can verify that Streamlit is installed correctly by running the following command: `streamlit --version` This command will display the installed version of Streamlit.

## Launch
 
### Deploy a Test Network with MetaMask & Ganache

Click[Here](https://docs.metamask.io/wallet/get-started/run-development-network/). For Instructions on how to connect Ganache using your MetaMask Extension.

### Compile and Deploy the Smart Contract on Remix.

1. Upload and compile the smart contract.
+ Click [Here](https://remix.ethereum.org/). To Launch remix.etherum.org

+ On Remix, upload the folder cloned from github.
![](images/Deploy_1.png)

+ Click on "InvitationMint.sol" found in "nft_invitation_dApp>>Contract>>InvitationMint.sol"

![](images/Deploy_2.png)

+ Click on Solidity Compile Icon on left bar, choose compiler 0.8.18, and then click on Compile invitationMint.sol

![](images/Compile.png)

+ Green Check = Success!

2. Deploy the smart contract

+ Click on the Deploy & run transactions icon, 

![](images'Deploy&RunIcon.png)

+ Chose environment “Dev-Ganache Provider”
     ![](images/Launch_1.png)

+ In the prompt menu, change RPC Endpoint from  8545 to 7545, click OK
     ![](images/Launch_2.png)                 

+ Change GAS LIMIT to 100000000, 

+ Copy paste index 0 address from Ganache, this address should be taken as the contract owner's address
   
+ Choose InvitationMint contract, click Deploy contract. 
     ![](images/Launch_3.png)

+ In the MetaMask prompt, click confirm button.

### Connect contract with the streamlit

1. Open the `app.py` in VScode.

2. In the Deployed Contracts section, you can see “INVITATIONMINT” contract, click the `copy` icon beside it to obtain the contract address.

3. Naviget to `contract address` in line 14 in `app.py`, paste the contract address you copied into the quotation to replace the string in it.   

### Run Streamlit page

To run the streamlit page, 

1. locate the nft_invitation_dApp from the command line interface

![](images/lit_1.png)

2. enter the following command. `streamlit run app.py`

Then You should see this in your terminal along with the streamlit page popping up.
 
![](images/lit_2.png)

How to Purchase an Invitation
![](images/purchase.gif)

How to Withdraw
![](images/WithdrawContractBalance.gif)

---

## Limitation

- Due to time constraints, we were unable to develop a more comprehensive secondary market smart contract. 
- For the convenience of graders, we did not establish a set of smart contracts that include Deployer.sol. 
- In order to facilitate page display, we have set the number of invitations to a smaller value of 8.

---

## Contributors

Demi Gao, 
Jonathan Cruz, 
Julio Rodriguez, 
Cary Gutknecht

## License

// SPDX-License-Identifier: MIT 
