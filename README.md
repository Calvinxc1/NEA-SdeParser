# New Eden Analytics Tooklit
# EVE Static Data Export Parser

Since [EVE Online](https://www.eveonline.com/) first launched back in May 2003 I have been a player. I'm heavily industry focused with a side of mining and marketeering/finance. I've very much tried to be a one-man-shop as much as I can, trying to outsmart the game rather than brute force it. The result of this was the development of New Eden Analytics (NEA), my 'toolkit' to augment my EVE Online experience.

NEA is split up into several tools, with this one, the Static Data Export Parser, designed to take EVE Online's [Static Data Export](https://eveonline-third-party-documentation.readthedocs.io/en/latest/sde/) and ETL the proverbial shit out of it so it can gracefully go in the local database I have set up.

## Why do this publicly?
One question that occasionally comes up is why am I making my code open source & publicly available? I could make All T3h Profitz if I hoard this tool for myself. Honestly, that wouldn't be fun at all for me. EVE is a fantastic game, but ultimately is just a game. I want to be challenged, I want people to take what I'm doing and one-up me. I want to be kept on my toes.

## Version History
Version history is located [here](./versions.md).

## Design Backlog
- Refactor SDE functionality as a Flask REST API
- Implement as a deployable container
- Set up as a Python package