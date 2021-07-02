#!/usr/bin/env python3

from eth_wallet import Wallet
from eth_wallet.utils import generate_mnemonic, is_mnemonic

import json
import sys
from tqdm import tqdm
import cowsay

args = sys.argv

# Or generate mnemonic
# MNEMONIC = generate_mnemonic(language="korean", strength=128)
# Secret passphrase/password
PASSPHRASE = None  # str("meherett")
# Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese & korean
LANGUAGE = "english"  # default is english

MNEMONIC = ''
if len(args) == 13:
    # 12 word mnemonic seed
    MNEMONIC = str(' '.join(sys.argv[1:]))

    # Checking 12 word mnemonic seed
    assert is_mnemonic(mnemonic=MNEMONIC, language=LANGUAGE), \
          "Invalid %s 12 word mnemonic seed." % LANGUAGE

def create_wallet(mnemonic=None):
    if not mnemonic:
        mnemonic: str = generate_mnemonic(language="english", strength=128)
    # Initialize wallet
    wallet = Wallet()
    # Get Ethereum wallet from mnemonic
    wallet.from_mnemonic(mnemonic=mnemonic, passphrase=PASSPHRASE, language=LANGUAGE)

    # Derivation from path
    # wallet.from_path("m/44'/60'/0'/0/0")
    # Derivation from index
    wallet.from_index(44, harden=True)
    wallet.from_index(60, harden=True)
    wallet.from_index(0, harden=True)
    wallet.from_index(0)
    wallet.from_index(0, harden=True)

    # Print all wallet information's
    # print(json.dumps(wallet.dumps(), indent=4, ensure_ascii=False))

    #print("Entropy:", wallet.entropy())
    #print("Mnemonic:", wallet.mnemonic())
    #print("Language:", wallet.language())
    #print("Passphrase:", wallet.passphrase())
    #print("Seed:", wallet.seed())
    #print("Root Private Key:", wallet.root_private_key())
    #print("Root Public Key:", wallet.root_public_key())
    #print("Uncompressed:", wallet.uncompressed())
    #print("Compressed:", wallet.compressed())
    #print("Chain Code:", wallet.chain_code())
    #print("Private Key:", wallet.private_key())
    #print("Public Key:", wallet.public_key())
    #print("Wallet Import Format:", wallet.wallet_import_format())
    #print("Finger Print:", wallet.finger_print())
    #print("Path:", wallet.path())

    wallet = {
            'mnemonic': mnemonic,
            'address': wallet.address(),
            'private_key': wallet.private_key(),
            }
    return wallet
    #print("Mnemonic:", mnemonic)
    #print("Address:", wallet.address())
    #print("Private Key:", wallet.private_key())

    #print("---- Serialized ----")

    #print("Private Key Hex:", wallet.extended_key(private_key=True, encoded=False))
    #print("Public Key Hex:", wallet.extended_key(private_key=False, encoded=False))
    #print("Private Key Base58:", wallet.extended_key(private_key=True, encoded=True))
    #print("Public Key Base58:", wallet.extended_key(private_key=False, encoded=True))

if __name__ == '__main__':
    if len(args) == 1:
        print(json.dumps(create_wallet(), indent=2, ensure_ascii=False))
    elif len(args) == 2:
        try:
            count = int(args[1])
        except:
            print("Usage : {} 10".format(args[0]))
            print("Create 10 addresses")
            exit(1)

        print(cowsay.ghostbusters('Creating {:,} wallets'.format(count)))

        import sqlite3
        con = sqlite3.connect('wallet.db')
        cur = con.cursor()
        CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS wallet (
                            address text,
                            seed text
                        )'''
        cur.execute(CREATE_TABLE)

        for i in tqdm(range(count)):
            wallet = create_wallet() 
            INSERT = '''INSERT INTO wallet
                        VALUES ('{}','{}')'''.format(wallet['address'], wallet['mnemonic'])
            cur.execute(INSERT)
            # print(json.dumps(wallet, indent=2, ensure_ascii=False))
        con.commit()
        con.close()
    else:
        print(json.dumps(create_wallet(MNEMONIC), indent=2, ensure_ascii=False))
