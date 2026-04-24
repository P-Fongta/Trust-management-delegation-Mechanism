Trust Management Delegation Mechanism - A proof-of-concept implementation of the trust management delegation protocol
This package is a proof-of-concept implementation of the trust management delegation protocol. The implementation is written in the Python language. aiocoap is leveraged to facilitate data and message transfers between entities in the proposed protocol, SQLite3 is used to store trust management and delegation information, and scikit-fuzzy for implementing trust computation models

System requirements:
To run the implementation, the user should prepare a machine or testbed capable of executing the protocol components. The following software prerequisites are recommended:
  •	Python 3.8 or later.
  •	SQLite3.
  •	phpLiteAdmin
  •	aiocoap.library, available at https://github.com/chrysn/aiocoap
  •	Scikit-fuzzy, available at https://github.com/scikit-fuzzy/scikit-fuzzy
Installation and setup:
  1.	Install the required software and libraries.
  2.	Clone the repository from GitHub onto the nodes that will act as the delegator, delegate, TSS, and trustee: git clone https://github.com/P-Fongta/Trust-management-delegation-Mechanism.git 
  3.	Start all protocol components according to the following execution sequence:
       1. Start the Trust Service Server (TSS).
       2. Start one or more delegate nodes and register their offered delegation services with the TSS.
       3.	Configure the required trust model, evidence types, and delegation roles on the delegator node and start the delegator node.
       4.	Experimental results are saved in text files.

