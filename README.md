# doxxcaster

Bot: [`@doxxbot`](https://warpcast.com/doxxbot)

Anyone can drop a mention to `@doxxbot` in a cast to snoop on a Farcaster user's other social hangouts and top 10 ERC-20 stash, all without leaving Warpcast.

Just for the heck of it, the doxxed user is also notified via a message on [XMTP](https://xmtp.org/) with the replied cast's URL.

_Why?_ It's a seamless way to unmasking identities and spotting potential biases. On the flipside, if you're all about that privacy, the bot's got your back – check how exposed you are and dial it down.

Submitted as part of [ETHIndia 2023, Bangalore, India](https://devfolio.co/projects/doxxcaster-bd92).

## Bot Usage

Reply with `@doxxbot` on a user's cast or `@doxxbot <farcaster_username>` to trigger a reply.

Video demo: https://www.youtube.com/shorts/awYpu3ZR9NU

## Example

<img alt="screenshot 1" src="https://github.com/eshaan7/doxxcaster/assets/16389167/45eee6a9-99ee-464c-b8fc-f97125ee5efe" width="300" height="560"/>
<img alt="screenshot 2" src="https://github.com/eshaan7/doxxcaster/assets/16389167/35fefbc8-e715-4ee8-8e11-25778e72eacf" width="300" height="560"/>

## Installation

Requires: Python, node.js.

```bash
$ git clone https://github.com/eshaan7/doxxcaster
$ cd doxxcaster/
$ doxxcaster >> pip install poetry
$ doxxcaster >> poetry install
$ doxxcaster >> npm i
$ doxxcaster >> npm run build # to build the dist/index.js for xmtp binary
$ doxxcaster >> chmod +x xmtp # to make xmtp executable
$ doxxcaster >> python doxxcaster/bot/main.py # starts listener for notification stream
[2023-12-10 01:00:00 +0530] [42069] [INFO] Starting notification stream in main
```