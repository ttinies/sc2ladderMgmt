[![PyPI](https://img.shields.io/pypi/v/sc2ladderMgmt.svg)](https://pypi.org/project/sc2ladderMgmt/)
[![Build Status](https://travis-ci.org/ttinies/sc2ladderMgmt.svg?branch=master)](https://travis-ci.org/ttinies/sc2ladderMgmt)
[![Coverage Status](https://coveralls.io/repos/github/ttinies/sc2ladderMgmt/badge.svg?branch=master)](https://coveralls.io/github/ttinies/sc2ladderMgmt?branch=master)
![Crates.io](https://img.shields.io/crates/l/rustc-serialize.svg)

# sc2ladderMgmt

Define available servers for Starcraft 2 AI & bot matches.

### About
A ladder system that allows you to play Starcraft2 outside of battle.net on your local machine or across the internet
playing as a human, AI or scripted bot.

### Purpose
The ladderMgmt package primarily ensures that the [scgameLobby](https://github.com/ttinies/sc2gameLobby) understands
which ladder servers that are available. It should also be the basic definitions for any actual ladder server
implementation.  If there is a ladder server that allows human and AI Starcraft 2 matches over a network, that
definition ishould be made here. 

### Rationale

Because this package is tied to the [sc2gameLobby](https://github.com/ttinies/sc2gameLobby),  its rationale for existing
is also for the [same reason that sc2gaemLobby is developed](https://github.com/ttinies/sc2gameLobby#rationale-why-create-this-repository).
Also, sc2ladderMgmt is separated into its own package for the sake of being more modular and extensible by other
packages independently from the sc2gameLobby.

### Functional Overview

A [simple interface](https://github.com/ttinies/sc2ladderMgmt/sc2ladderMgmt/blob/master/__init__.py) is provided to add,
retrieve and remove available ladders.  The package then accesses its own internal storage system (a json file) to
perform the specified action without requiring manual edits.  That's it.  Not much to it.

# Installation

Reference this package [hosted on pypi.org]() which is installed via [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)).

> EXAMPLE: `pip install sc2ladderMgmt`

#### A Note to Bot and AI developers or human players

If your primary interest is in playing on the ladders either as yourself or with an AI / bot you developed, this package
should install automatically with the [sc2gameLobby](https://github.com/ttinies/sc2gameLobby).  There really isn't
anything you should _need_ to do with this package.

# Usage

For general use, unless incorporated into external python code, the command-line interface is the primary means to
acquire player information.  After specifying the command to invoke this package, the remaining parameters specify the
operation to be performed and any parameters for that operation.  Only the --add option accepts additional parameters to
define the properties of the to-be-added ladder. (**NOTE:** specifying no arguments after the package name simply
displays all known ladders.)

> EXAMPLE: `python -m sc2ladderMgmt <operation <parameters>`

> EXAMPLE: `python -m sc2ladderMgmt --help`

#### Locality

By default, all get/add/remove actions are performed on the user's local installation.  If changes are made, they affect
no other users.  To ensure these changes are available for other users or publically available packages, [the sc2ladderMgmt GitHub source project](https://github.com/ttinies/sc2ladderMgmt)
must be updated.  Kindly make your change and submit a pull request.

#### Create your own ladder server

1. Create and host the ladder functionality on the internet.
	* This new ladder server implementation must follow the protocol established by [sc2gameLobby connections to the server](https://github.com/ttinies/sc2gameLobby/blob/master/sc2gameLobby/connectToServer.py).

2. Create the ladder definition.  Each possible criteria definition is shown below.  Only specify items that are
applicable to the new server.  The parameters `name`, `ipAddress` and `serverPort` are required.  The rest are
optionally defined.  If undefined, they acquire default values.
```
name                    the name of the ladder server.
ipAddress               the IPV4 or IPV6 address where the ladder server exists and is publically accessible.
serverPort              the TCP port the server listens on.
allowNewPlayers         whether previously unknown players specified in the ladder request may be accepted and created on the remote server. (Default: enabled)
maxLocalGamesAllowed    the maximum number of games that the server can host at any given time. (Default: 0)
inactivePurge           whether players that haven't played in a while are automatically forgotten. (Default: disabled)
inactiveScan            whether inactive player detection is enabled. (Default: enabled)
```
> EXAMPLE: `python -m sc2ladderMgmt --add name=stairs ipAddress=1.2.3.4 serverPort=27182`

3. Publicize your new ladder by issuing a pull request at [sc2ladderMgmt](https://github.com/ttinies/sc2ladderMgmt).


#### Modify or delete a ladder definition

Feel free to modify the definitions as you like.  This effectively only changes your own system's knowledge of the
Starcraft 2 AI/human ladder ecosystem.  If these changes should be available publicly, a pull request must be made.  The
currently available ladder definitions are available [here](https://github.com/ttinies/sc2ladderMgmt/tree/master/dataLadder).

