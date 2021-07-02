# Create ETH Wallet

## Build

```
docker build -t eth-wallet .
```

## Run

### Create Single Wallet
```
docker run --rm eth-wallet
```

### Create Wallet from mnemonic

```
docker run --rm eth-wallet <m no mo nicdry . . . .>
```

### Create 1,000 wallets


```
docker run --rm -v $PWD:/db eth-wallet 1000
```

All wallets saved to `wallet.db`
