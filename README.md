# Crypto VC Fund Tracker

Crypto BC Fund Tracker is a program that is used to scrape different websites of venture capitalists in the crypto space to see if there is an overlap in the projects they currently invest in.

The program is run simply by filtering out the amount of funds you want invested in the project for it to display
```
usage: main.py [-h] [--filter FILTER] [--output]

Track Fund Investments for different Crypto Projects

optional arguments:
  -h, --help       show this help message and exit
  --filter FILTER  This can be used to filter out the amount of funds invested into a project to display it, defualt 2
  --output         Will Output a JSON Object of Funds and their investments
```

The output will then tell you the funds and coins at the end.

arweave has 5 invested.. ['MultiCoin', 'Coinbase', 'a16z', 'Arrington XRP Capital', 'Blockchain Capital']
keep has 4 invested.. ['MultiCoin', 'Coinbase', 'a16z', 'Fabric Ventures']
nervos has 4 invested.. ['MultiCoin', '1Confirmation', 'Blockchain Capital', 'Dragonfly Capital']
1inch has 4 invested.. ['Binance', 'Blockchain Capital', 'Dragonfly Capital', 'Fabric Ventures']
oasislabs has 4 invested.. ['Binance', 'a16z', 'Blockchain Capital', 'Dragonfly Capital']
Staked has 4 invested.. ['Coinbase', 'Digital Currency Group', 'Fabric Ventures', 'Winklevoss Capital']
Messari has 4 invested.. ['Coinbase', 'Blockchain Capital', 'Fabric Ventures', 'Winklevoss Capital']
Orca has 4 invested.. ['Coinbase', 'Arrington XRP Capital', 'Placeholder Ventures', 'Three Arrows Capital']
Hashflow has 4 invested.. ['Coinbase', 'Arrington XRP Capital', 'Digital Currency Group', 'Fabric Ventures']
Forta has 4 invested.. ['Coinbase', '1Confirmation', 'a16z', 'Placeholder Ventures']
Polkadot has 5 invested.. ['1Confirmation', 'Arrington XRP Capital', 'Fabric Ventures', 'Placeholder Ventures', 'Three Arrows Capital']
Coinbase has 4 invested.. ['1Confirmation', 'Blockchain Capital', 'Digital Currency Group', 'Fabric Ventures']
