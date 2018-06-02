"""
PURPOSE: manage records of all known ladders, both local and remote
"""

from __future__ import absolute_import # python 2/3 compatibility
from __future__ import division        # python 2/3 compatibility
from __future__ import print_function  # python 2/3 compatibility

import glob
import os
import re

from sc2ladderMgmt import constants as c
from sc2ladderMgmt.ladders import ladderCache, Ladder


################################################################################
def addLadder(settings):
    """define a new Ladder setting and save to disk file"""
    ladder = Ladder(settings)
    ladder.save()
    getKnownLadders()[ladder.name] = ladder
    return ladder


################################################################################
def getLadder(name):
    """obtain a specific ladder settings file"""
    try:    return getKnownLadders()[name.lower()]
    except KeyError:
        raise ValueError("given ladder name '%s' is not a known configuration"%(name))


################################################################################
def delLadder(name):
    """forget about a previously defined Ladder setting by deleting its disk file"""
    ladders = getKnownLadders()
    try:
        ladder = ladders[name]
        os.remove(ladder.filename) # delete from disk
        del ladders[name] # deallocate object
        return ladder
    except KeyError:
        raise ValueError("given ladder name '%s' is not a known ladder definition"%(name))


################################################################################
def getKnownLadders(reset=False):
    """identify all of the currently defined ladders"""
    if not ladderCache or reset:
        jsonFiles = os.path.join(c.LADDER_FOLDER, "*.json")
        for ladderFilepath in glob.glob(jsonFiles):
            filename = os.path.basename(ladderFilepath)
            name = re.search("^ladder_(.*?).json$", filename).groups()[0]
            ladder = Ladder(name)
            ladderCache[ladder.name] = ladder
    return ladderCache


################################################################################
__all__ = ["addLadder", "getLadder", "delLadder", "getKnownLadders"]

