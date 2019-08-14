"""
FILE: MapNetworkAnalysis
CLASS:  MapNetworkAnalysis
Author: Christopher Robson
Copyright by:  Christopher Robson
Copyright date: 01Nov2017
This software is not FREE!  Use or destribution of the software system and its
subsystem modules, libraries, configuration file and "seed" file without the
express permission of the author is strictly PROHIBITED!
FUNCTION:  Module generates an ISIS map of the network.
  ALIGN="CENTER|LEFT|RIGHT|TEXT"
  BALIGN="CENTER|LEFT|RIGHT"
  BGCOLOR="color"
  BORDER="value"
  CELLPADDING="value"
  CELLSPACING="value"
  COLOR="color"
  COLSPAN="value"
  FIXEDSIZE="FALSE|TRUE"
  GRADIENTANGLE="value"
  HEIGHT="value"
  HREF="value"
  ID="value"
  PORT="portName"
  ROWSPAN="value"
  SIDES="value"
  STYLE="value"
  TARGET="value"
  TITLE="value"
  TOOLTIP="value"
  VALIGN="MIDDLE|BOTTOM|TOP"
  WIDTH="value"
"""
"""
LIBRARIES:  Python libraries
"""
from PyQt5.QtWidgets import QMainWindow
import ast
import warnings
from pygraphviz import AGraph
import datetime
import time
from pygraphviz import AGraph, Attribute, ItemAttribute
from random import randint
"""
LIBRARIES:  Testbed Tester specific libraries
"""
from Globals import *
from AnalysisReportGenerator import AnalysisReportGenerator
from RichTextProcessor import RichTextProcessor
from SeedDictionary import SeedCommandDictionaryProcessor
from ColorNameCodes import color_pallete
from WriteListData import *
"""
CLASS: MapNetworkAnalysis:
DESCRIPTION: Generates an ISIS map of all isis adjacency connections
INPUT: 
OUTPUT:
"""
class MapNetworkAnalysis:
  "Map Network Analysis"
  """"""
  def __init__( self, parent = None ):
    self.name = self.__class__.__name__
    self.parent = parent
    self.seed = self.parent.seed
    self.gparent = self.parent.parent.parent.parent
    self.filename_time_extension = self.parent.filename_time_extension
    self.cmd_list = self.parent.cmd_list
    self.analyze_action_instance = self.parent.parent.parent.analyze_class
    self.testcase_number = ""
    self.map_title = ""
    self.dataFD = None
    self.report_map_filename = ""
    self.isis_database =[{}]
    self.bgp_database =[{}]
    self.previous_index = 0
    self.current_index = 0
  """
  CLASS: execute
  DESCRIPTION: ISIS maps the testbed.
  INPUT: "show isis adjacency"
  OUTPUT: data ready for map generating
  """
  def execute( self ):
    self.device = self.cmd_list[SeedCommandDictionaryProcessor.device]
    if self.cmd_list[SeedCommandDictionaryProcessor.verbose] == 'Yes':
      self.message_str = \
        "Creating network map containing adjacency/neighbor associations, generated at: {}.".\
          format( datetime.datetime.now().strftime( "%d%b%Y-%H%M-%S" ) )
      self.gparent.logger_message_signal.emit(self.message_str)
    self.message_str = "Building network map: {}.".\
          format( self.cmd_list[SeedCommandDictionaryProcessor.archivefilename] )
    self.gparent.logger_message_signal.emit( self.message_str )
    """
    Get the file where the creataed map is saved
    """
    self.map_filename = self.cmd_list[SeedCommandDictionaryProcessor.archivefilename]
    """
    Extract the name of the mapping seed file and open up the files for processing
    This file contains additional seed file parameters.
    """
    try:
      self.seedFD = open( self.cmd_list[SeedCommandDictionaryProcessor.commandpath] + \
                          self.cmd_list[SeedCommandDictionaryProcessor.commands], "r" )
    except Exception as error:
      raise Exception("{}: {}".format( self.name, error))
    """
    Extract each line out of the seed file and process the command sequences
    """
    for self.seed_data in self.seedFD:
      if self.seed_data.startswith("#"):
        continue
      try:
        self.seed_dict = ast.literal_eval(self.seed_data.split(";")[0])
      except Exception as error:
        raise Exception("{}: {}".format(self.name, error))
      """
      Generate the report based on device type from analysis data
      """
      if self.device == "juniper":
        self.map_network( device = self.device,
                          seed_dict = self.seed_dict,
                          map_filename = self.map_filename )
      elif self.device == "cisco":
        self.map_network( device = self.device,
                          seed_dict = self.seed_dict,
                          map_filename = self.map_filename )
    self.seedFD.close()
    return()
  """
  METHOD: map_network( self ):
  DESCRIPTION: Build the network map
  INPUT: Master seed file entry for "commands" keyword
  OUTPUT: Network map.
  """
  def map_network( self, device = "", seed_dict = None, map_filename = "" ):
    self.device = device
    self.seed_dict = seed_dict
    self.map_filename = map_filename
    try:
      self.neighborFD = open("{}{}{}".format(self.seed_dict["neighborpath"],
                                             self.seed_dict["neighbordata"],
                                             self.filename_time_extension), "a+")
    except Exception as error:
      raise Exception("{}: {}".format(self.name, error))
    try:
      self.dataFD = open("{}{}{}".format(self.seed_dict["datapath"],
                                         self.seed_dict["data"],
                                         self.filename_time_extension), "r")
      for self.command in self.dataFD:
        self.previous_index = self.current_index
        self.current_index += len( self.command )
        if self.command.startswith("DUT("):
          if self.seed_dict["mapbyname"]:
            self.core_router = self.command.split()[1].split("/")[0]
          else:
            self.core_router = self.command.split()[1]
          if self.command.split("->")[1].split()[1] == "isis":
            self.build_isis_adjacency_database(seed_dict = self.seed_dict,
                                               device = self.device,
                                               dataFD = self.dataFD,
                                               neighborFD = self.neighborFD)
          elif self.command.split("->")[1].split()[1] == "bgp":
            self.build_bgp_neighbor_database(seed_dict = self.seed_dict,
                                             device = self.device,
                                             dataFD = self.dataFD,
                                             neighborFD = self.neighborFD)
    except Exception as error:
      raise Exception("{}: {}".format(self.name, error))
    """
    Build the nodes
    """
    self.map = self.build_node_edge_points(self.seed_dict, self.neighborFD)
    """
    Convert to a dot string
    """
    self.map.string()
    """
    Build each of the image formats for later displaying
    """
    try:
      self.map.write("{}.dot".format(self.map_filename))
      self.map.draw("{}-circo.png".format(self.map_filename),prog='circo',args='-Tpng')
      self.map.draw("{}-twopi.png".format(self.map_filename),prog='twopi',args='-Tpng')
      self.map.draw("{}-neato.png".format(self.map_filename),prog='neato',args='-Tpng')
      self.map.draw("{}-fdp.png".format(self.map_filename),prog='fdp',args='-Tpng')
    except Exception as error:
      raise Exception("{}: {}".format(self.name, error))
    """
    Create a detached window and display the map
    """
    if self.seed_dict["displaymap"]:
      self.display_network_map(title = "Testcase {} {}".format(self.seed_dict["testcase"],
                                                               self.seed_dict["testcasetitle"]),
                               frameless = self.seed_dict["frameless"],
                               map = "{}-{}.png".format(self.map_filename,
                                                        self.seed_dict["maptype"] ))
    self.neighborFD.close()
    return()
  """
   METHOD: build_bgp_neighbor_database( self ):
   DESCRIPTION: Build the database of BGP neighbors
   INPUT: "show bgp neighbor" data
   OUTPUT: neighbor database
   """
  def build_bgp_neighbor_database(self, seed_dict = None, device = "", dataFD = None, neighborFD = None):
    self.seed_dict = seed_dict
    self.device = device
    self.dataFD = dataFD
    self.neighborFD = neighborFD
    self.database_list = []
    if self.device == "juniper":
      for self.data in self.dataFD:
        self.previous_index = self.current_index
        self.current_index += len( self.data )
        if self.data.startswith("\n") or self.data.startswith(" ") or self.data == "":
          continue
        if self.data.startswith("DUT("):
          self.dataFD.seek(self.previous_index)
          break
        if self.data.startswith("Peer:"):
          self.random_color_number_index = randint(17,230)
          self.color_number_index = 16
          for (self.color_name, self.color_number) in color_pallete.items():
            self.color_number_index += 1
            if self.color_number_index == self.random_color_number_index:
              break
            elif self.color_number_index >= 230:
              break
          self.data_list = self.data.split()
          """
          Now look ahead for state to set the spline color
          """
          for self.spline_data in self.dataFD:
            self.previous_index = self.current_index
            self.current_index += len( self.spline_data )
            self.spline_data = self.spline_data.lstrip()
            self.spline_color = "#ff0000"
            if self.spline_data.startswith("Last State:"):
              break
            if self.spline_data.startswith("Type:") and self.spline_data.find("State:") != -1:
              if self.spline_data.split("State:")[1].split()[0].startswith("Established"):
                self.spline_color = "#008000"
              else:
                self.spline_color = "#ff0000"
          self.database_list.append("{{\"datetimestamp\":\"{}\","
                                    "\"core router\":\"{}\","
                                    "\"edge router\":\"{}\","
                                    "\"interface\":\"{}\","
                                    "\"state\":\"{}\","
                                    "\"line color\":\"{}\","
                                    "\"fill color\":\"{}\"}};\n".format(self.filename_time_extension[1:],
                                                                        self.core_router,
                                                                        self.data_list[1],
                                                                        "NONE",
                                                                        self.spline_data.split("State:")[1].split()[0],
                                                                        self.spline_color,
                                                                        self.color_number))
          continue
    elif self.device == "cisco":
      for self.data in self.dataFD:
        self.previous_index = self.current_index
        self.current_index += len( self.data )
        if self.data.startswith("\n") or self.data.startswith(" ") or self.data == "":
          continue
        if self.data.startswith("DUT("):
          self.dataFD.seek(self.previous_index)
          break
        if self.data.startswith("BGP neighbor is"):
          self.random_color_number_index = randint(17,230)
          self.color_number_index = 16
          for (self.color_name, self.color_number) in color_pallete.items():
            self.color_number_index += 1
            if self.color_number_index == self.random_color_number_index:
              break
            elif self.color_number_index >= 230:
              break
          self.data_list = self.data.split()
          for self.spline_data in self.dataFD:
            self.previous_index = self.current_index
            self.current_index += len( self.spline_data )
            self.spline_data = self.spline_data.lstrip()
            self.spline_color = "#ff0000"
            if self.spline_data.startswith("NSR State:"):
              break
            if self.spline_data.startswith("BGP state ="):
              a= self.spline_data.split("BGP state = ")[1].split()[0]
              if self.spline_data.split("BGP state = ")[1].split()[0].startswith("Established"):
                self.spline_color = "#008000"
              else:
                self.spline_color = "#ff0000"
          self.database_list.append("{{\"datetimestamp\":\"{}\","
                                    "\"core router\":\"{}\","
                                    "\"edge router\":\"{}\","
                                    "\"interface\":\"{}\","
                                    "\"state\":\"{}\","
                                    "\"line color\":\"{}\","
                                    "\"fill color\":\"{}\"}};\n".
                                    format(self.filename_time_extension[1:],
                                           self.core_router,
                                           self.data_list[3],
                                           "NONE",
                                           self.spline_data.split("BGP state = ")[0].split()[0],
                                           self.spline_color,
                                           self.color_number))
          continue
    else:
      raise Exception("{}: invalid device: {}".format(self.name, self.device))
    for self.db_element in self.database_list:
      try:
        self.neighborFD.write(self.db_element)
      except Exception as error:
        raise Exception("{}: {}".format(self.name, error))
    return()
  """
  METHOD: build_isis_adjacency_database( self ):
  DESCRIPTION: Build the database of ISIS adjacencies
  INPUT: "show isis adjacency" data
  OUTPUT: adjacency neighbor database
  """
  def build_isis_adjacency_database( self, seed_dict, device = "", dataFD = None, neighborFD = None ):
    self.seed_dict = seed_dict
    self.device = device
    self.dataFD = dataFD
    self.neighborFD = neighborFD
    self.database_list = []
    self.color_indexer = 33
    self.color_number_index = 0
    if self.device == "juniper":
      self.started = False
      for self.data in self.dataFD:
        self.previous_index = self.current_index
        self.current_index += len( self.data )
        if self.data.startswith("DUT("):
          self.dataFD.seek(self.previous_index)
          break
        if self.data.startswith("\n") and not self.started:
          continue
        if self.data.startswith("\n") and self.started:
          break
        if self.data.startswith("Interface"):
          self.started = True
          continue
        if self.started:
          self.random_color_number_index = randint(17,230)
          self.color_number_index = 16
          for (self.color_name, self.color_number) in color_pallete.items():
            self.color_number_index += 1
            if self.color_number_index == self.random_color_number_index:
              break
            elif self.color_number_index >= 230:
              break
          self.data_list = self.data.split()
          self.database_list.append("{{\"datetimestamp\":\"{}\","
                                    "\"core router\":\"{}\","
                                    "\"edge router\":\"{}\","
                                    "\"interface\":\"{}\","
                                    "\"state\":\"{}\","
                                    "\"line color\":\"{}\","
                                    "\"fill color\":\"{}\"}};\n".format(self.filename_time_extension[1:],
                                                                        self.core_router,
                                                                        self.data_list[1],
                                                                        self.data_list[0],
                                                                        self.data_list[3],
                                                                        "#000080",
                                                                        self.color_number))
          continue
    elif self.device == "cisco":
      self.started = False
      for self.data in self.dataFD:
        self.previous_index = self.current_index
        self.current_index += len( self.data )
        if self.data.startswith("DUT("):
          self.dataFD.seek(self.previous_index)
          break
        for self.line in self.data.split("\n"):
          if self.line.startswith("\n") or self.line.startswith(" ") or self.line == "":
            continue
          if self.line.startswith("System Id"):
            self.started = True
            continue
          if self.started and self.line.startswith("Total"):
            break
          if self.started:
            self.random_color_number_index = randint(17,230)
            self.color_number_index = 16
            for (self.color_name, self.color_number) in color_pallete.items():
              self.color_number_index += 1
              if self.color_number_index == self.random_color_number_index:
                break
              elif self.color_number_index >= 230:
                break
            self.line_list = self.line.split()
            self.database_list.append("{{\"datetimestamp\":\"{}\","
                                      "\"core router\":\"{}\","
                                      "\"edge router\":\"{}\","
                                      "\"interface\":\"{}\","
                                      "\"state\":\"{}\","
                                      "\"line color\":\"{}\","
                                      "\"fill color\":\"{}\"}};\n".format(self.filename_time_extension[1:],
                                                                          self.core_router,
                                                                          self.line_list[0],
                                                                          self.line_list[1],
                                                                          self.line_list[3],
                                                                          "#000080",
                                                                          self.color_number))
            continue
    else:
      raise Exception("{}: invalid device: {}".format(self.name, self.device))
    for self.db_element in self.database_list:
      try:
        self.neighborFD.write(self.db_element)
      except Exception as error:
        raise Exception("{}: {}".format(self.name, error))
    return(self.neighborFD)
  """
  METHOD: build_node_edge_points( self ):
  DESCRIPTION: Build the network map node to edge points
  INPUT: Edge to node list
  OUTPUT: Graph map attributes structure.
  """
  def build_node_edge_points(self, seed_dict, neighborFD):
    self.seed_dict = seed_dict
    self.neighborFD = neighborFD
    self.neighborFD.seek(0)
    self.map = AGraph(name = 'TestbedTester')
    # Sets the shape of the node/edges
    self.map.node_attr['fillcolor'] = "#FF0000"
    # Sets the core node shape
    self.map.node_attr['shape'] = 'oval'
    #self.map.node_attr['shape'] = 'box3d'
    #self.map.node_attr['shape'] = 'diamond'
    #self.map.node_attr['shape'] = 'cylinder'
    # FIXME NO EFFEC ?? self.map.node_attr['valign'] = "top"
    self.map.node_attr['fixedsize'] = 'false'
    self.map.node_attr['fontsize'] = '8'
    self.map.node_attr['fontcolor'] = '#000000'
    # FIXME NO EFFECT WHY ?? self.map.node_attr['pack'] = 'false'
    # FIXME NO EFFECT WHY ?? self.map.node_attr['defaultdist'] = '500'
    # Sets the thickness of the nodes edge when used as part of the node setup
    self.map.node_attr['penwidth'] = '1'
    # FIXME Need to figure out how to do dark on light and light on dark font colors!
    # FIXME self.map.node_attr['fontcolor'] = '#008700'
    self.map.node_attr['style'] = 'filled'
    self.map.graph_attr['outputorder'] = 'edgesfirst'
    self.map.graph_attr['fontsize'] = '12'
    self.map.graph_attr['ratio'] = '\"1.0\"'
    self.map.graph_attr['fontcolor'] = '#0087ff'
    # Sets the shape of the node
    self.map.edge_attr['shape'] = "box"
    # The following will set the interconnecting line between node and edge color
    # Since its based on ISIS or BGP get color from neighbor database
    self.map.edge_attr['color'] = '#000000'
    # Sets the text size/color of the interconncting line labels
    self.map.edge_attr['fontsize'] = '6'
    self.map.edge_attr['fontcolor'] = '#000000'
    # Sets line label, but being set below in decoding loop
    # G.edge_attr['label'] = str("{}-{}".format("isis", "neighbor"))
    # The following will set the interconnecting line between node and edge thickness
    self.map.edge_attr['style'] = 'setlinewidth(1)'
    self.map.graph_attr['splines'] = 'false'
    self.map.graph_attr['splines'] = 'curved'
    self.x = 1
    self.y = 1
    for self.router_database in self.neighborFD:
      try:
        self.router_database_dict = ast.literal_eval(self.router_database.split(";")[0])
      except Exception as error:
        raise Exception("{}: {}".format(self.name, error))
      try:
        self.core_router = self.router_database_dict["core router"].split()[1].split("/")[0]
      except:
        self.core_router = self.router_database_dict["core router"]
      self.map.graph_attr['label'] = "Testcase: {} {} {} View {}".format(self.seed_dict['testcase'],
                                                                         self.seed_dict['testcasetitle'],
                                                                         self.core_router,
                                                                         self.filename_time_extension[1:])
      self.map.add_node(self.router_database_dict["edge router"])
      self.node_attr = self.map.get_node(self.router_database_dict["edge router"])
      # FIXME Need to figure out how to do dark on light and light on dark font colors!
      # FIXME self.map.node_attr['fontcolor'] = '#ffff00'
      # Sets the text color of the nodes
      self.node_attr.attr['fontcolor'] = "#000000"
      # Sets the positions of the nodes
      self.node_attr.attr['pos'] = "%f,%f"%(float(self.x)/1.0,float(self.y)/1.0)
      # Sets the circles ouside line to a color
      self.node_attr.attr['color'] = "#000000"
      self.node_attr.attr['shape'] = "cylinder"
      # Setting fillcolor here sets outside circles to a color!
      self.node_attr.attr['fillcolor'] = self.router_database_dict["fill color"]
      self.height = .05
      self.width = .05
      self.node_attr.attr['height'] = "%s" % (self.height / 16.0 + 0.5)
      self.node_attr.attr['width'] = "%s" % (self.width / 16.0 + 0.5)
      self.node_attr.attr['label'] = str('"{}"'.format(self.router_database_dict["edge router"]))
      self.map.add_edge(self.router_database_dict["core router"], self.router_database_dict["edge router"])
      self.edge_attr = self.map.get_edge(self.router_database_dict["core router"],
                                    self.router_database_dict["edge router"])
      # Sets the name for the interconnecting line between nodes and edges
      self.edge_attr.attr['label'] = str("{}<->{}".format(self.router_database_dict["core router"],
                                                   self.router_database_dict["edge router"]))
      self.edge_attr.attr['color'] = self.router_database_dict["line color"]
      # Sets the thickness of the line when used as part of the edge setup
      self.edge_attr.attr['penwidth'] = '3'
    return( self.map )
  """
  METHOD: display_network_map( self ):
  DESCRIPTION: Display the map
  INPUT: Image file of network map
  OUTPUT: Detached window of map.
  """
  def display_network_map(self, title = "", frameless = True, map = ""):
    self.map = map
    self.title = title
    self.frameless = frameless
    self.image_parent_window = QMainWindow()
    self.image_display_window = MessagesWindow()
    self.image_display_window.message_window_initializer(
                                                         self.image_parent_window,
                                                         parent_background_color = "#ffffff",
                                                         child_background_color = "#ffffff",
                                                         font = "normal 12pt times new roman",
                                                         title = self.title,
                                                         left = 10, top = 50, width = 1000, height = 700,
                                                         background_image = self.map,
                                                         resize_to_image = True,
                                                         frameless = self.frameless
                                                         )
    return ()
"""
END of FILE
"""
