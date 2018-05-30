"""
PURPOSE: manage records of all known ladders, both local and remote
"""

from __future__ import absolute_import
from __future__ import division       # python 2/3 compatibility
from __future__ import print_function # python 2/3 compatibility

from builtins import str as text # python 2/3 compatibility
from six import iteritems # python 2/3 compatibility

import glob
import json
import os
import re

from sc2ladderMgmt import constants as c


################################################################################
ladderCache = {} # mapping of Ladder names to Ladder objects


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
    global ladderCache
    if not ladderCache or reset:
        jsonFiles = os.path.join(c.LADDER_FOLDER, "*.json")
        for ladderFilepath in glob.glob(jsonFiles):
            filename = os.path.basename(ladderFilepath)
            name = filename.rstrip("\.json").lstrip("ladder_")
            ladder = Ladder(name)
            ladderCache[ladder.name] = ladder
    return ladderCache


################################################################################
class Ladder(object):
    """represent a given set of settings for a defined Ladder"""
    ############################################################################
    def __init__(self, source=None, **override):
        # define default values and their type
        self.name                   = ""
        self.ipAddress              = c.LOCALHOST
        self.allowNewPlayers        = True
        self.maxLocalGamesAllowed   = 0
        self.inactiveScan           = True
        self.inactivePurge          = False
        # initialize with new values
        if   isinstance(source, text):      self.load(source) # assume a filename to load
        elif isinstance(source, dict):      self.update(source)
        elif isinstance(source, Ladder):    self.update(source.__dict__) # copy constructor
        self.update(override)
        if not self.name:
            raise ValueError("must define 'name' parameter as part of %s source settings"%(self.__class__.__name__))
    ############################################################################
    def __str__(self): return self.__repr__()
    def __repr__(self):
        return "<%s %s>"%(self.__class__.__name__, self.name)
    ############################################################################
    @property
    def filename(self):
        """return the absolute path to the object's filename"""
        return os.path.join(c.LADDER_FOLDER, "ladder_%s.json"%(self.name))
    ############################################################################
    @property
    def attrs(self):
        """provide a copy of this ladder's attributes as a dictionary"""
        return dict(self.__dict__)
    ############################################################################
    def _validateAttrs(self, keys):
        """prove that all attributes are defined appropriately"""
        badAttrsMsg = ""
        for k in keys:
            if k not in self.attrs:
                badAttrsMsg += "Attribute key '%s' is not a valid attribute"%(k)
        if badAttrsMsg:
            raise ValueError("Encountered invalid attributes.  ALLOWED: %s%s%s"\
                %(list(self.attrs), os.linesep, badAttrsMsg))
    ############################################################################
    def load(self, ladderName):
        """retrieve the ladder settings from saved disk file"""
        self.name = ladderName # preset value to load self.filename
        with open(self.filename, "rb") as f:
            data = f.read()
            self.__dict__.update( json.loads(data) )
    ############################################################################
    def save(self):
        """save ladder settings to disk"""
        with open(self.filename, "wb") as f:
            data = str.encode( json.dumps(self.attrs, indent=4, sort_keys=True) )
            f.write(data)
    ############################################################################
    def update(self, attrs):
        """update attributes initialized with the proper type"""
        self._validateAttrs(attrs)
        for k,v in iteritems(attrs):
            typecast = type( getattr(self, k) )
            if typecast==bool and v=="False":   newval = False # "False" evalued as boolean is True because its length > 0
            else:                               newval = typecast(v.lower())
            setattr(self, k, newval)


################################################################################
__all__ = ["addLadder", "getLadder", "delLadder", "getKnownLadders"]

