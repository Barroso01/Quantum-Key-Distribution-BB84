# BB84 Quantum Key Distribution

Cryptography is the process for enabling secure communication between two or more parties; often referred to as Alice and Bob. In this context, there's also a potential eavesdropper named Eve, whose presence highlights the need for secure methods. This repository showcases the methodology behind the quantum key distribution (QKD) protocol known as the BB84 scheme. The main objective of this protocol is to establish a secure encryption-decryption key between Alice and Bob using the principles of quantum mechanics.

## Getting Started

These instructions will get you a copy of the BB84 Quantum Key Distribution project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Before running this project, you need to have Python installed on your machine (preferably Python 3.7 or higher), as well as `pip` for package management. You'll also need Git to clone the repository. The project uses Qiskit, which requires that you have Anaconda or Miniconda installed if you do not wish to manage dependencies manually.

You can download Python [here](https://www.python.org/downloads/).
You can download Git [here](https://git-scm.com/downloads).
You can download Anaconda [here](https://www.anaconda.com/products/individual).

### Installation

First, clone the BB84 repository from GitHub to your local machine using Git:

```bash
git clone https://github.com/Barroso01/Quantum-Key-Distribution-BB84.git
cd Quantum-Key-Distribution-BB84
``` 
It's recommended to create a virtual environment to manage the dependencies for the project:

```bash
python -m venv bb84-env
# On Windows:
bb84-env\Scripts\activate
# On MacOS/Linux:
source bb84-env/bin/activate
```
With the virtual environment activated, install the required dependencies:
```bash
pip install -r requirements.txt
``` 

### Examples

The examples directory contains a file that simulates the BB84 protocol: bb84_simulation.py. Run the file to see the protocol in action!

## Author
ER. Eduardo Barroso 




