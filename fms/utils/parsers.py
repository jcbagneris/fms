#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Parsers
"""

import sys
import os
import logging
import yaml

from fms.utils import CSVDELIMITERS, OPTS_VAL, OPTS_BOOL
from fms.utils.exceptions import MissingParameter

logger = logging.getLogger('fms.utils.parsers')

class _ParamsParser(dict):
    """
    Common methods to all param parsers
    """

    def __init__(self, filename):
        """
        Constructor. Sets verbose attribute.
        """
        logger.info("Reading config file %s" % filename)
        self.outputfile = sys.stderr
        self.orderslogfile = None

    def splitclassname(self, fullclassname):
        """
        Split composed classnames in config files, if necessary.

        Returns compound module name and classname in a tuple, i.e.
        >>> from fms.utils.parsers import _ParamsParser
        >>> theparser = _ParamsParser({})
        >>> theparser.splitclassname('this.module.classname') == ['this.module', 'classname']
        True
        >>> theparser.splitclassname('simpleclassname') == [None, 'simpleclassname']
        True

        """
        classnameaslist = fullclassname.rsplit('.',1)
        if len(classnameaslist) > 1:
            return classnameaslist
        else:
            return [None, classnameaslist[0]]

    def create_files(self, turn):
        """
        Create all necessary files
        """
        if self['outputfilename'] != 'sys.stdout':
            if '-%03d' in self['outputfilename']:
                outputfilename = self['outputfilename'] % turn
            else:
                outputfilename = self['outputfilename']
            logger.info("Creating %s" % outputfilename)
            self.outputfile = open(outputfilename, 'w')
        else:
            self.outputfile = sys.stdout

        if self['orderslogfilename']:
            if '-%03d' in self['orderslogfilename']:
                orderslogfilename = self['orderslogfilename'] % turn
            else:
                orderslogfilename = self['orderslogfilename']
            logger.info("Creating %s" % orderslogfilename)
            self.orderslogfile = open(orderslogfilename, 'w')

    def close_files(self, turn):
        """
        Close all output files
        """
        if self['outputfilename'] != 'sys.stdout':
            if '-%03d' in self['outputfilename']:
                outputfilename = self['outputfilename'] % turn
            else:
                outputfilename = self['outputfilename']
            logger.info("Closing %s" % outputfilename)
            try:
                self.outputfile.close()
            except IOError:
                pass
        if self['orderslogfilename']:
            if '-%03d' in self['orderslogfilename']:
                orderslogfilename = self['orderslogfilename'] % turn
            else:
                orderslogfilename = self['orderslogfilename']
            logger.info("Closing %s" % orderslogfilename)
            try:
                self.orderslogfile.close()
            except IOError:
                pass


    def printparams(self):
        """
        Prints parameters read from configuration file
        """
        logger.info("== %s ==" % self['name'])
        for optional in OPTS_VAL + tuple(OPTS_BOOL):
            if optional in self:
                logger.info("%s : %s" % (optional, self[optional]))
        if 'args' in self['world']:
            logger.info("World : %s %s" % (self['world']['classname'],
                self['world']['args']))
        else:
            logger.info("World : %s" % (self['world']['classname'],))
        logger.info("Engines : ")
        for engine in self['engines']:
            if 'args' in engine:
                if 'args' in engine['market']:
                    logger.info(
                            " %s (%s): %d days of %d instants on %s market (%s)" % 
                            (engine['classname'],
                             engine['args'],
                             engine['days'],
                             engine['daylength'],
                             engine['market']['classname'],
                             engine['market']['args']))
                else:
                    logger.info(
                            " %s (%s): %d days of %d instants on %s market" % 
                            (engine['classname'],
                             engine['args'],
                             engine['days'],
                             engine['daylength'],
                             engine['market']['classname'],))
            else:
                logger.info(" %s : %d days of %d instants on %s market" % 
                        (engine['classname'],
                         engine['days'],
                         engine['daylength'],
                         engine['market']['classname']))
        logger.info("Agents :")
        for a in self['agents']:
            if 'args' in a:
                logger.info(" %d %s with $%.2f and %d stocks, %s" % 
                        (a['number'], a['classname'], 
                         a['money'], a['stocks'], a['args']))
            else:
                logger.info(" %d %s with $%.2f and %d stocks" % 
                        (a['number'], a['classname'], a['money'], a['stocks']))

    def printfileheaders(self):
        """
        Outputs headers to result and log file
        """
        print >> self.outputfile, "# %s" % self['name']
        print >> self.outputfile, "time;transaction;price;volume"
        self.outputfile.flush()

        if self['orderslogfilename']:
            print >> self.orderslogfile, "# %s orders log" % self['name']
            print >> self.orderslogfile, "# direction : buy=0, sell=1"
            print >> self.orderslogfile, "# direction;price;volume;agent"
            self.orderslogfile.flush()


class XmlParamsParser(_ParamsParser):
    """
    Get all possible parameters from xml config file,
    replacing missing values by sensible defaults
    when possible, exiting with error otherwise.

    This class if provided for comptaibility with Derveeuw's
    config files. The use of YAML config files is encouraged,
    as they give more flexibility.
    """

    def __init__(self, xmlfilename):
        """
        Constructor. Reads XML config file.
        """
        try:
            from lxml import etree
        except ImportError:
            logger.critical(
                    "Please install the lxml module to use XML config files.")
            logger.critical("See http://codespeak.net/lxml/ for installation.")
            sys.exit(2)

        _ParamsParser.__init__(self, xmlfilename)
        
        config = etree.parse(xmlfilename).getroot()
        try:
            self.exp_path = os.path.dirname(xmlfilename)
        except AttributeError:
            self.exp_path = None

        experimentname = config.find(".//name")
        try:
            self['name'] = experimentname.text
        except AttributeError:
            self['name'] = "%s experiment" % xmlfilename

        outputfilename = config.find(".//outputFilename")
        try:
            self['outputfilename'] = os.path.join(self.exp_path,
                    outputfilename.text)
        except AttributeError:
            self['outputfilename'] = "sys.stdout"

        orderslogfilename = config.find(".//ordersLogFilename")
        try:
            self['orderslogfilename'] = os.path.join(self.exp_path,
                    orderslogfilename.text)
        except AttributeError:
            self['orderslogfilename'] = None

        randomseed = config.find(".//randomSeed")
        try:
            self['randomseed'] = randomseed.text
        except AttributeError:
            self['randomseed'] = None

        world = config.find(".//world")
        try:
            worldclass = world.find("className")
            self['world'] = {}
            try:
                self['world']['classname'] = worldclass.text.split('.')[-1]
            except AttributeError:
                raise MissingParameter, 'world classname'
            worldargs = world.find("args")
            worldargslist = []
            try:
                for a in worldargs:
                    if '.' in a.text:
                        worldargslist.append(float(a.text))
                    else:
                        worldargslist.append(int(a.text))
                if worldargslist:
                    self['world']['args'] = worldargslist
            except TypeError:
                pass
        except AttributeError:
            raise MissingParameter, 'world'

        engine = config.find(".//simulationEngine")
        try:
            engineclass = engine.find("className")
            self['engines'] = []
            self['engines'].append({})
            try:
                self['engines'][0]['classname'] = \
                        engineclass.text.split('.')[-1]
            except AttributeError:
                raise MissingParameter, 'engine classname'
            engineargs = engine.find("args")
            engineargslist = []
            try:
                for a in engineargs:
                    if '.' in a.text:
                        engineargslist.append(float(a.text))
                    else:
                        engineargslist.append(int(a.text))
                if engineargslist:
                    self['engines'][0]['args'] = engineargslist
            except TypeError:
                pass
        except AttributeError:
            raise MissingParameter, 'engine'

        days = config.find(".//numberDays")
        try:
            self['engines'][0]['days'] = int(days.text)
        except AttributeError:
            self['engines'][0]['days'] = 1

        daylength = config.find(".//dayLength")
        try:
            self['engines'][0]['daylength'] = int(daylength.text)
        except AttributeError:
            self['engines'][0]['daylength'] = 1

        self['engines'][0]['clearbooksateod'] = True

        market = config.find(".//market")
        try:
            self['engines'][0]['market'] = {}
            marketclass = market.find("className")
            try:
                self['engines'][0]['market']['classname'] = \
                        marketclass.text.split('.')[-1]
            except AttributeError:
                raise MissingParameter, 'engine[\'market\'][\'classname\']'
            marketargs = market.find("args")
            marketargslist = []
            try:
                for a in marketargs:
                    if '.' in a.text:
                        marketargslist.append(float(a.text))
                    else:
                        marketargslist.append(int(a.text))
                if marketargslist:
                    self['engines'][0]['market']['args'] = marketargslist
            except TypeError:
                pass
        except AttributeError:
            raise MissingParameter, 'engine[\'market\']'

        agents = config.find(".//agents")
        self['agents'] = []
        try:
            for a in agents:
                agent = {}
                agent['classname'] = a.find("className").text.split('.')[-1]
                agent['number'] = int(a.find("number").text)
                agent['money'] = int(a.find("initialMoney").text)
                agent['stocks'] = int(a.find("initialStocks").text)
                agentargs = a.find("args")
                agentargslist = []
                try:
                    for aa in agentargs:
                        if '.' in aa.text:
                            agentargslist.append(float(aa.text))
                        else:
                            agentargslist.append(int(aa.text))
                except TypeError:
                    pass
                agent['args'] = agentargslist
                self['agents'].append(agent)
        except TypeError:
            raise MissingParameter, 'agents'
        if not self['agents']:
            raise MissingParameter, 'agent'

        logger.info("Config file %s parsed." % xmlfilename)


class YamlParamsParser(_ParamsParser):
    """
    Get all possible parameters from yaml config file,
    replacing missing values by sensible defaults
    when possible, exiting with error otherwise.

    The class gets 2 attributes:
    - ouputfile: file handler where to write transactions
    - orderslogfile: file handler, might be missing, where to
      log agents orders (desires)

    This class is a dict subclass, with following keys:
    - name: experiment name, config filename if missing
    - randomseed: seed for random lib, None if missing
    - outputfilename: 'sys.stdout' if missing
    - orderslogfilename: logs all agents desires, None if missing
    - csvdelimiter: csv output files delimiter
    - unique_by_agent: unique order per agent in books
    - world: error if missing
    - engines: list of engines, error if missing (one engine minimum)
    - agents: list of agents classes, error if missing (at least one)

    self['world'] should have a 'classname' key.
    
    self['engines'] is a list of dicts with following keys:
    - classname: error if missing
    - days: int, 1 if missing
    - daylength: int, 1 if missing
    - market: class, error if missing
    - args: list, None if missing

    self['engines'][n]['market] is a dict, with keys:
    - classname: error if missing
    - args: list, None if missing

    All 'classname' params are splitted in 'modulename','classname'
    if classname contains one or more '.'
    """

    def __init__(self, yamlfilename):
        """
        Constructor. Reads YAML config file.
        Adds sensible defaults for missing values
        """
        _ParamsParser.__init__(self, yamlfilename)

        try:
            yamlfile = open(yamlfilename, 'r')
            yamlconf = yaml.load(yamlfile)
            self.exp_path = os.path.dirname(yamlfilename)
        except (IOError, TypeError):
            yamlconf = yaml.load(yamlfilename)
            self.exp_path = None

        for key, value in yamlconf.items():
            self[key] = value

        if not 'name' in self:
            self['name'] = '%s experiment' % yamlfilename

        if not 'repeat' in self:
            self['repeat'] = 1

        if not 'randomseed' in self:
            self['randomseed'] = None

        if not 'unique_by_agent' in self:
            self['unique_by_agent'] = True

        if 'csvdelimiter' in self:
            if not self['csvdelimiter'] in CSVDELIMITERS:
                self['csvdelimiter'] = ';'
        else:
            self['csvdelimiter'] = ';'


        if 'outputfilename' in self:
            self['outputfilename'] = os.path.join(self.exp_path, 
                    self['outputfilename'])
        else:
            self['outputfilename'] = 'sys.stdout'

        if 'orderslogfilename' in self:
            self['orderslogfilename'] = os.path.join(self.exp_path,
                    self['orderslogfilename'])
        else:
            self['orderslogfilename'] = None

        for paramkey in ('world', 'engines', 'agents'):
            if not paramkey in self:
                raise MissingParameter, paramkey

        if not 'classname' in self['world']:
            raise MissingParameter, 'world classname'

        self['world']['modulename'], self['world']['classname'] =\
                self.splitclassname(self['world']['classname'])

        for paramkey in ('engines', 'agents'):
            for item in self[paramkey]:
                if not 'classname' in item:
                    raise MissingParameter, paramkey+' classname'
                item['modulename'], item['classname'] =\
                        self.splitclassname(item['classname'])

        for paramkey in ('number', 'stocks', 'money'):
            for agent in self['agents']:
                if not paramkey in agent:
                    agent[paramkey] = 1

        for paramkey in ('days', 'daylength', 'clearbooksateod'):
            for engine in self['engines']:
                if not paramkey in engine:
                    engine[paramkey] = 1

        for engine in self['engines']:
            if not 'market' in engine:
                raise MissingParameter, 'engine[\'market\']'
            if not 'classname' in engine['market']:
                raise MissingParameter, 'engine[\'market\'][\'classname\']'
            engine['market']['modulename'], engine['market']['classname'] =\
                    self.splitclassname(engine['market']['classname'])

        logger.info("Config file %s parsed." % yamlfilename)

