
![Logo](https://i.postimg.cc/65pf0z9R/logo.jpg)


# Trade Alchemy

A 100% pure python implementation of the Alpaca Markets API by way of direct API requests.


## Badges

[![Platform](https://img.shields.io/badge/Cross%20Platform-iOS%20%7C%20Android%20%7C%20Win%20%7C%20Linux%20%7C%20macOS-blue)](https://github.com/AltKrypto)
[![Python](https://img.shields.io/badge/Language-Python-green)](https://github.com/AltKrypto)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/AltKrypto)

## Features

- 100% Pure Python
- Runs ANYWHERE python is supported
- Built as "Mobile First"
- Cross platform

## Requirements

- pandas
- numpy
- matplotlib

## Setup

- You will need to provide a .env in the root directory formatted as:

```txt
paper_api = <paper api key>
paper_secret = <paper secret key>
live_api = <live api key>
live_secret = <live secret key>
```

## Roadmap

- Complete code coverage for entire API
- Improve bots
- Database integration
- UI
- Passing tests
- Release

## What Bots Are Included?

- SMA based grid bot
- Historical data based grid bot
- Historical, sma, rsi, bollinger grid bot

## What routines are included?

- Dollar Cost Averaging, buys set amount of an asset if its current price is lower than the average buy price

## FAQ

#### Why when there are already Python SDKs for Alpaca?

I primarily write code on mobile, crazy I know however, that being the case I cant install most packages with C-Dependancies which led me here.

#### Why on Earth would you write code on mobile?

Im a man of many hats, I work a full-time job, I'm a husband, a Father and somewhat of a gamer. My time to sit at a desk or with a laptop is limited these days. 


## Acknowledgements

These apps played a HUGE part in development of this project. Special shout out to Ole Zorn for the absolutely amazing decelopment environment which is Pythonista. 

 - [Pythonista](http://www.omz-software.com/pythonista/)
 - [Working Copy](https://workingcopyapp.com/)
 - [Runestone](https://runestone.app/)


## Disclaimer

The trading algorithms used in this program are provided for educational and informational purposes only and should not be relied upon as the sole basis for any investment decision. The algorithms are not intended to provide legal, tax, or investment advice. The end user of this program is solely responsible for any investment decisions made using the algorithms and assumes all liability for any losses that result from the use of the program. The program is provided "as is" without warranty of any kind, either express or implied, including but not limited to the implied warranties of merchantability, fitness for a particular purpose, or non-infringement. The program may not be suitable for all investors and the end user should ensure that they understand the risks involved and seek independent advice if necessary.


## Contributions

I am not publicly making this project known but if you stumble across this project and it peeks your interest I am most definately open to suggestions 

## License

[MIT](https://choosealicense.com/licenses/mit/)

