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


+-----------+----------------------------------------------------------------------------------------------------------------+
|  Project  |                                                     Funds                                                      |
+-----------+----------------------------------------------------------------------------------------------------------------+
| arweave   |  ['MultiCoin', 'Coinbase', 'a16z', 'Arrington XRP Capital', 'Blockchain Capital']                              |
| keep      |  ['MultiCoin', 'Coinbase', 'a16z', 'Fabric Ventures']                                                          |
| nervos    |  ['MultiCoin', '1Confirmation', 'Blockchain Capital', 'Dragonfly Capital']                                     |
| 1inch     |  ['Binance', 'Blockchain Capital', 'Dragonfly Capital', 'Fabric Ventures']                                     |
| oasislabs |  ['Binance', 'a16z', 'Blockchain Capital', 'Dragonfly Capital']                                                |
| Staked    |  ['Coinbase', 'Digital Currency Group', 'Fabric Ventures', 'Winklevoss Capital']                               |
| Messari   |  ['Coinbase', 'Blockchain Capital', 'Fabric Ventures', 'Winklevoss Capital']                                   |
| Orca      |  ['Coinbase', 'Arrington XRP Capital', 'Placeholder Ventures', 'Three Arrows Capital']                         |
| Hashflow  |  ['Coinbase', 'Arrington XRP Capital', 'Digital Currency Group', 'Fabric Ventures']                            |
| Forta     |  ['Coinbase', '1Confirmation', 'a16z', 'Placeholder Ventures']                                                 |
| Polkadot  |  ['1Confirmation', 'Arrington XRP Capital', 'Fabric Ventures', 'Placeholder Ventures', 'Three Arrows Capital'] |
| Coinbase  |  ['1Confirmation', 'Blockchain Capital', 'Digital Currency Group', 'Fabric Ventures']                          |
+-----------+----------------------------------------------------------------------------------------------------------------+

