"""
CLASS:   Mapper
Origianl Author: Niall Donaghy (niall@ndonaghy.com)
This module has been modified to fit the Testbed Tester model
FUNCTION:  Maps the network based on ISIS
"""
"""
Python libraries
"""
from PyQt5 import QtCore
import sys
import warnings
import pygraphviz as pgv
import subprocess
import time
"""
Testbed Tester libraries
"""
from Globals import *
from Exceptions import *
from ColorNameCodes import *
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show Device Information/Status/Configuration
#------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
"""
CLASS: Mapper:
DESCRIPTION: Generates an ISIS map of all isis adjacency connections
INPUT: 
OUTPUT:
"""
class Mapper:
  " Mapper"
  #-----------------------------------------------------------------------------------------------------------------
  def __init__(self, parent = None ):
    self.parent = parent
    self.name = self.__class__.__name__
    self.map = ""
    self.start_mapping = False
    self.core_node2 = "vMXRE3"
    self.core_node1 = "vMXRE2"
    self.core_node = "vMXRE1"
  #-----------------------------------------------------------------------------------------------------------------
  def mapper( self ):
    # ignore Graphviz warning messages
    warnings.simplefilter('ignore', RuntimeWarning)
    #-------------------------------------------------------------------------------------------------------------
    # MAP Juniper devices
    #-------------------------------------------------------------------------------------------------------------
    #
    try:

      #FIXME !!!!!!!!!!!
      # Make this a file associated to indivudla router seed file so the testers map is specific to the testers test
      # FIXME !!!!!!!!!!!!
      fhr=open("/usr/local/TestbedTester/etc/profiles/Mapper-ISIS-devices-list.prf","r")

    except:
      print("File not found!")
    self.scrapeConfig( fhr )
    G = self.createGraph()
    G.string()
    # G.write("./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-Juniper-ISIS-Map.dot")
    # print("Wrote DOT language output file: Testbed-ISIS-Juniper-Map.dot")
    # print("Wrote final diagram output file: Testbed-ISIS-Juniper-Map.png")
    # G.draw("{}.png".format( "./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-Juniper-ISIS" ),prog='neato',args='-Tpng')
    # #-------------------------------------------------------------------------------------------------------------
    # # MAP Cisco devices
    # #-------------------------------------------------------------------------------------------------------------
    # try:
    #   fhr=open("./.AcmeAutomator/myARCHIVES/profiles/TRUNK-STATUS/Testbed-Cisco-ISIS-devices.prf","r")
    # except:
    #   print("File not found!")
    # self.scrapeConfig( fhr )
    # G = self.createGraph()
    # G.string()
    # G.write("./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-Cisco-ISIS-Map.dot")
    # print("Wrote DOT language output file: Testbed-ISIS-Cisco-Map.dot")
    # print("Wrote final diagram output file: Testbed-ISIS-Cisco-Map.png")
    # G.draw("{}.png".format( "./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-Cisco-ISIS" ),prog='neato',args='-Tpng')
    #G.draw("{}.png".format( "./Testbed-Cisco-ISIS" ),prog='neato',args='-Tpng')
    G.write("{}.dot".format( "./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-ISIS-DOT" ))
    G.draw("{}.png".format( "./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-ISIS-CIRCO" ),prog='circo')
    G.draw("{}.png".format( "./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-ISIS-FDP" ),prog='fdp',args="-Tpng")
    G.draw("{}.png".format( "./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-ISIS-TWOPI" ),prog='twopi',args="-Tpng")
    G.draw("{}.png".format( "./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-ISIS-NEATO" ),prog='neato',args="-Tpng")
    return("./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-Tester-ISIS-Map")
  #-----------------------------------------------------------------------------------------------------------------
  def fetchConfig( self, command ):
    #self.command = command
    #if self.start_mapping:
    #  print("Mapping started for:   {}".format( self.command[6] ))
    #try:
    #  proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #  out, err = proc.communicate()
    #except Exception as error:
    #  raise Exception( "EXCEPTION: {}\nERR: {}\nRECEIVED OUTPUT: {}\n".format( error, err, out ))
    #if not self.start_mapping:
    #  print("Mapping completed for: {}".format( self.command[6] ))
    #out = "Mon Dec 18 07:34:14.536 UTC\n\nIS-IS 27064 neighbors:\nSystem Id      Interface        SNPA           State Holdtime Type IETF-NSF\nR91XRv         Gi0/0/0/1        *PtoP*         Up    24       L2   Capable \nR94XRv         Gi0/0/0/4        *PtoP*         Up    24       L2   Capable \nR95XRv         Gi0/0/0/5        *PtoP*         Up    24       L2   Capable \nTotal neighbor count: 1\nRP/0/0/CPU0:R93XRv#"
    return(self.preprocess_data())

  def preprocess_data(self):
    data = "Mon Dec 18 07:34:14.536 UTC\n\nIS-IS 27064 neighbors:\nSystem Id      Interface        SNPA           State Holdtime Type IETF-NSF\n" \
           "R91XRv         Gi0/0/0/1        *PtoP*         Up    24       L2   Capable \n" \
           "R92XRv         Gi0/0/0/2        *PtoP*         Up    24       L2   Capable \n" \
           "R93XRv         Gi0/0/0/3        *PtoP*         Up    24       L2   Capable \n" \
           "R94XRv         Gi0/0/0/4        *PtoP*         Up    24       L2   Capable \n" \
           "R95XRv         Gi0/0/0/5        *PtoP*         Up    24       L2   Capable \n" \
           "R96XRv         Gi0/0/0/6        *PtoP*         Up    24       L2   Capable \n" \
           "R97XRv         Gi0/0/0/7        *PtoP*         Up    24       L2   Capable \n" \
           "R98XRv         Gi0/0/0/8        *PtoP*         Up    24       L2   Capable \n" \
           "Total neighbor count: 1\n" \
           "RP/0/0/CPU0:R93XRv#"
    out_list = []
    started = False
    for line in data.split("\n"):
      if line.startswith("\n") or line.startswith(" ") or line == "":
        continue
      if line.startswith("System Id"):
        started = True
        continue
      if started and line.startswith("Total"):
        break
      if started:
        out_list.append(line)
        continue
    out = "\n".join(out_list)
    self.preprocess_data2(out)
    return(out)
  def preprocess_data2(self, out):
    data = "Mon Dec 18 07:34:14.536 UTC\n\nIS-IS 27064 neighbors:\nSystem Id      Interface        SNPA           State Holdtime Type IETF-NSF\n" \
           "R123XRv         ten0/0/0/1        *PtoP*         Up    24       L2   Capable \n" \
           "R123XRv         ten0/0/0/2        *PtoP*         Up    24       L2   Capable \n" \
           "R123XRv         ten0/0/0/3        *PtoP*         Up    24       L2   Capable \n" \
           "R123XRv         ten0/0/0/4        *PtoP*         Up    24       L2   Capable \n" \
           "R123XRv         ten0/0/0/5        *PtoP*         Up    24       L2   Capable \n" \
           "R123XRv         ten0/0/0/6        *PtoP*         Up    24       L2   Capable \n" \
           "R123XRv         ten0/0/0/7        *PtoP*         Up    24       L2   Capable \n" \
           "R123XRv         ten0/0/0/8        *PtoP*         Up    24       L2   Capable \n" \
           "Total neighbor count: 1\n" \
           "RP/0/0/CPU0:R93XRv#"
    out_list = []
    started = False
    for line in data.split("\n"):
      if line.startswith("\n") or line.startswith(" ") or line == "":
        continue
      if line.startswith("System Id"):
        started = True
        continue
      if started and line.startswith("Total"):
        break
      if started:
        out_list.append(line)
        continue
    out += "\n".join(out_list)
    return(out)
  #-----------------------------------------------------------------------------------------------------------------

  def scrapeConfig( self, fhr ):
    # open file geant.txt
    #try:
    #  fhr=open("./.AcmeAutomator/myARCHIVES/profiles/TRUNK-STATUS/Testbed-devices.prf","r")
    #except:
    #  print("File not found!")
    routers=[]
    routersShortname=[]
    routersDef=[]
    routersAdj=[]
    routersCfg=[]
    device_type = ""
    print("Discovering router definitions in input file...")
    for line_type in fhr.readlines():
      if line_type.startswith("#"): # skip comments
        continue
      device_type = line_type.split( ":" )[0]
      line = line_type.split( ":" )[1]

      ## FIXME !!!!!!!!!!!!!!!!
      ## USE isdigit() the below command dumb as shit!!!!!!!!!!!!
      #numfind=re.compile("^\d+,*") # FIXME THIS SHOULD BE "isdigit()" CALL!!!!!

      #if numfind.match(line): # this line is IS-IS cost information
      #  print("Erroneous line in input file, ignoring: " + line)
      #else: # this line is a router definition
      (router,coord)=line.split("[")
      (fqdn,edge_router)=router.split(",")
      routers.insert(0,fqdn)
      # # FIXME DEBUG print("Found " + fqdn + ", fetching configuration...")
      routersDef.insert(0,line)
      routersShortname.insert(0,edge_router)
      #routersAdj.insert(0,"")
      routersCfg.insert(0,"")
      # if device_type == "juniper":
      #   command = ['sshpass', '-p', 'geTest', 'ssh', '-l', 'test',
      #              fqdn, '\"show isis adj | except Interface\"']
      # else:
      #   command = ['sshpass', '-p', 'geTest', 'sshxrv','test', "10.168.1.120", '\"show isis neighbor\"']
      #   #command = ['sshpass', '-p', 'geTest', 'ssh', '-l', 'test', fqdn, '\"show isis neighbor\"']
      # self.start_mapping = True

      # #FIXME PRE-process the show comamnd data to create an input with ONLY isis info.
      # the method used bwefore my shcnage was dumb as shit!!!!
      #routersAdj[0] = self.fetchConfig(command)
      routersAdj.append( self.preprocess_data() )

      # if device_type == "juniper":
      #   command = ['sshpass', '-p', 'geTest', 'ssh', '-l', 'test', fqdn,
      #              '\"show configuration protocols isis | display set | match metric | match interface\"']
      #   self.start_mapping = False
      #   routersCfg[0] = self.fetchConfig(command)
    fhr.close()
    #---------------------------------------------------------------------------------------------------------------
    # Now we've read in the configuration and retrieved ISIS adjacency data, create graph...
    try:
      fhw=open("./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-ISIS-dynamic.prf","w")
    except:
      print("File not found!")
    print("Processing configuration and generating graph data...")
    index = 33 # get down to lighter colors on chart
    for adj in routersAdj:
      for line in adj.split("\n"):
        index += 1
        number_index = 0
        fillcolor = 1
        for (color_name, color_number) in color_pallete.items():
          number_index += 1
          if index == number_index:
            fillcolor = color_number
            break
        interface=""
        neighbour=""
        state = ""
        if "Up" in line:
          state = "up"
        else:
          state = "down"
        parts = line.split()
        if device_type == "cisco":
          interface = parts[1]
          neighbour = parts[0]
        else:
          interface = parts[0]
          neighbour = parts[1]
        fhw.write( "{},{},{},{},{}\n".format( self.core_node,neighbour,interface,state,fillcolor) )
    for adj in routersAdj:
      for line in adj.split("\n"):
        index += 1
        number_index = 0
        fillcolor = 1
        for (color_name, color_number) in color_pallete.items():
          number_index += 1
          if index == number_index:
            fillcolor = color_number
            break
        interface=""
        neighbour=""
        state = ""
        if "Up" in line:
          state = "up"
        else:
          state = "down"
        parts = line.split()
        if device_type == "cisco":
          interface = parts[1]
          neighbour = parts[0]
        else:
          interface = parts[0]
          neighbour = parts[1]
        fhw.write( "{},{},{},{},{}\n".format( self.core_node1,neighbour,interface,state,fillcolor) )

    for adj in routersAdj:
      for line in adj.split("\n"):
        index += 1
        number_index = 0
        fillcolor = 1
        for (color_name, color_number) in color_pallete.items():
          number_index += 1
          if index == number_index:
            fillcolor = color_number
            break
        interface=""
        neighbour=""
        state = ""
        if "Up" in line:
          state = "up"
        else:
          state = "down"
        parts = line.split()
        if device_type == "cisco":
          interface = parts[1]
          neighbour = parts[0]
        else:
          interface = parts[0]
          neighbour = parts[1]
        fhw.write( "{},{},{},{},{}\n".format( self.core_node2,neighbour,interface,state,fillcolor) )
    fhw.close()
  #-----------------------------------------------------------------------------------------------------------------
  def createGraph( self ):
    print("GRAPHING...")
    try:
      fh=open("./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-ISIS-dynamic.prf","r")
    except:
      print("File not found!")
    G=pgv.AGraph(name='TestbedTester')
    # Sets the shape of the node/edges
    G.node_attr['fillcolor'] = "#FF0000"
    G.node_attr['shape']='oval'
    G.node_attr['fixedsize']='false'
    G.node_attr['fontsize']='8'
    G.node_attr['fontcolor']='#008700'
    G.node_attr['style']='filled'
    G.graph_attr['outputorder']='edgesfirst'
    G.graph_attr['label']='Testbed Tester Lab Topology ' + time.strftime("%d/%m/%Y") + ' @ ' + time.strftime("%H:%M:%S")
    G.graph_attr['fontsize']='12'
    G.graph_attr['ratio']='\"1.0\"'
    G.graph_attr['fontcolor']='#0087ff'
    # Sets the shape of the node
    G.edge_attr['shape'] = "box"
    # The following will set the interconnecting line between node and edge color
    G.edge_attr['color']='#FF0000'
    # Sets the text size/color of the interconncting line labels
    G.edge_attr['fontsize']='6'
    G.edge_attr['fontcolor']='#000000'
    # Sets line label, but being set below in decoding loop
    # G.edge_attr['label'] = str("{}-{}".format("isis", "neighbor"))
    # The following will set the interconnecting line between node and edge thickness
    G.edge_attr['style']='setlinewidth(1)'
    G.graph_attr['splines']='false'
    G.graph_attr['splines']='curved'
    x = 1
    y = 1
    for line in fh.readlines():
      if line.startswith("#"): # skip comments
        continue
      isis_router = line.split(",")[0]
      edge_router = line.split(",")[1]
      G.add_node(edge_router)
      node_attr = G.get_node(edge_router)
      # Sets the text color of the nodes
      node_attr.attr['fontcolor'] = "#ffff00"
      # Sets the positions of the nodes
      node_attr.attr['pos'] = "%f,%f"%(float(x)/1.0,float(y)/1.0)
      # Sets the circiles ouside line to a color
      node_attr.attr['color'] = "#ff0000"
      # Setting fillcolor here sets outside circles to a color!
      node_attr.attr['fillcolor'] = line.split(",")[4].split("\n")[0]
      height = .05
      width = .05
      node_attr.attr['height'] = "%s" % (height / 16.0 + 0.5)
      node_attr.attr['width'] = "%s" % (width / 16.0 + 0.5)
      node_attr.attr['label'] = str('"{}"'.format(edge_router))
      G.add_edge(isis_router, edge_router)
      edge_attr = G.get_edge(isis_router, edge_router)
      # Sets the name for the interconnecting line between nodes and edges
      edge_attr.attr['label'] = str("{}-{}".format(isis_router, edge_router))
    return( G )
####################################################################################################################

