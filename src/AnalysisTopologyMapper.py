####################################################################################################################
# Python Qt5 Testbed Tester Analysis Topology Mapper
# MODULE:  AnalysisTopologyMapper
# Origianl Author: Niall Donaghy (niall@ndonaghy.com)
# This module has been modified to fit the Testbed Tester model
# FUNCTION:  Maps the network based on ISIS
####################################################################################################################
from PyQt5 import QtCore
import warnings
import pygraphviz as pgv
import subprocess
import time
import re
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Home grown
#------------------------------------------------------------------------------------------------------------------
from Globals import *
from Exceptions import *
#------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
# Show Device Information/Status/Configuration
#------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
# FIXME MAYEB THREAD LATER class Mapper( QtCore.QThread ):
class AnalysisTopologyMapper:
  " Analysis Topology Mapper"
  #-----------------------------------------------------------------------------------------------------------------
  def __init__(self, parent = None ):
    self.parent = parent
    self.name = " Analysis Topology Mapper"
    self.ggparent = parent.parent.parent.parent
    self.seed = parent.seed
    self.ip = parent.ip
    self.ssh_handle = parent.ssh_handle
    self.filename_time_extension = parent.filename_time_extension
    self.report_file_list = parent.report_file_list
    self.process_reply = parent.process_reply
    self.cmd_list = parent.cmd_list
    self.is_search_item = parent.analysis_results
    self.seed_list = []
    self.testcase_name = ""
    self.analysis_data_filename = ""
    self.map = ""
  #-----------------------------------------------------------------------------------------------------------------
  def analysis_topology_mapper( self, map ):
    self.map = map
    # ignore Graphviz warning messages
    warnings.simplefilter('ignore', RuntimeWarning)
    #
    try:
      fhr=open("./.AcmeAutomator/myARCHIVES/profiles/TRUNK-STATUS/Testbed-devices.prf","r")
    except:
      print("File not found!")
    self.scrapeConfig( fhr )
    G = self.createGraph()
    G.string()
    G.write("./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-ISIS-Map.dot")
    print("Wrote DOT language output file: Testbed-ISIS-Map.dot")
    print("Wrote final diagram output file: Testbed-ISIS-Map.png")
    G.draw("{}.png".format( "./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-ISIS" ),prog='neato',args='-Tpng')
    #G.draw("{}.png".format( "./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-ISIS" ),prog='dot',args='-Tpng')
    return()
  #-----------------------------------------------------------------------------------------------------------------
  def fetchConfig( self, command ):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    return out
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
    print("Discovering router definitions in input file...")
    for line in fhr.readlines():
      if line.startswith("#"): # skip comments
        continue
      numfind=re.compile("^\d+,*")
      if numfind.match(line): # this line is IS-IS cost information
        print("Erroneous line in input file, ignoring: " + line)
      else: # this line is a router definition
        (router,coord)=line.split("[")
        (fqdn,shortname)=router.split(",")
        routers.insert(0,fqdn)
        print("Found " + fqdn + ", fetching configuration...")
        routersDef.insert(0,line)
        routersShortname.insert(0,shortname)
        routersAdj.insert(0,"")
        routersCfg.insert(0,"")
        command = ['sshpass', '-p', 'geTest', 'ssh', '-l', 'test',
                   fqdn, '\"show isis adj | except Interface\"']
        a = " ".join(command)
        # FIXME CISCO command = ['sshpass', '-p', 'cisco', 'ssh', '-l', 'cisco', fqdn, '\"show isis adj\"']
        routersAdj[0] = self.fetchConfig(command)
        command = ['sshpass', '-p', 'geTest', 'ssh', '-l', 'test', fqdn,
                   '\"show configuration protocols isis | display set | match metric | match interface\"']
        routersCfg[0] = self.fetchConfig(command)
    fhr.close()
    #---------------------------------------------------------------------------------------------------------------
    # Now we've read in the configuration and retrieved ISIS adjacency data, create graph...
    try:
      fhw=open("./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-ISIS-dynamic.prf","w")
    except:
      print("File not found!")
    print("Processing configuration and generating graph data...")
    for i in range(len(routersDef)):
      fhw.write(routersDef[i])
      adjacencies = routersAdj[i].decode("utf-8").split("\n")
      for line in adjacencies:
        interface=""
        neighbour=""
        # For established adjacencies...
        if "Up" in line:
          parts = line.split()
          interface = parts[0]
          neighbour = parts[1].split( "-" )[0]
          match = re.search(".re\d$", neighbour)
          if match:
            neighbour = neighbour[:-4]
          metric = 0
          configuration = routersCfg[i].decode("utf-8").split("\n")
          for line in configuration:
            match = re.search(interface, line)
            if match:
              print("Found match: " + line)
              metric = line.split()[8]
              print("Found adjacency for " + routersShortname[i] + ": " +
                    neighbour + " on interface " + interface + " with metric " + metric)
              # Ignore non-backbone ISIS neighbours...
              if "NCC" in neighbour:
                print("Ignoring NCC router...")
              elif "0620.4010.4090" in neighbour:
                print("Ignoring NetReflex...")
              # Or write output for backbone ISIS neighbours...
              else:
                fhw.write(str(metric) + "," + neighbour + "\n")
              print("NEIGHBOUR: " + neighbour)
    fhw.close()
  #-----------------------------------------------------------------------------------------------------------------
  def createGraph( self ):
    # open file geant_dynamic.txt
    print("GRAPHING...")
    try:
      fh=open("./.AcmeAutomator/myARCHIVES/NETWORK-MAP/Testbed-ISIS-dynamic.prf","r")
    except:
      print("File not found!")
    G=pgv.AGraph(name='TestbedTester')
    G.node_attr['shape']='oval'
    #G.node_attr['shape']='circle'
    G.node_attr['fixedsize']='false'
    G.node_attr['fontsize']='8'
    G.node_attr['style']='filled'
    G.node_attr['color']='#40e0d0'
    G.graph_attr['outputorder']='edgesfirst'
    G.graph_attr['label']='Testbed Tester Lab Topology ' + time.strftime("%d/%m/%Y") + ' @ ' + time.strftime("%H:%M:%S")
    G.graph_attr['fontsize']='12'
    G.graph_attr['ratio']='\"1.0\"'
    G.edge_attr['color']='#AA00FF'
    G.edge_attr['style']='setlinewidth(3)'
    G.graph_attr['splines']='true'
    G.graph_attr['splines']='curved'
    routers=[]
    for line in fh.readlines():
      if line.startswith("#"): # skip comments
        continue
      numfind=re.compile("^\d+,*")
      if numfind.match(line): # this line is IS-IS cost information
        cost,host=line.split(",")
        host=str(host)
        host=host.strip()
        cost=str(cost)
        cost=cost.strip()
        G.add_edge( routers[0], host, label=cost, fontsize="8" )
      else: # this line is a router definition
        (router,coord)=line.split("[")
        (fqdn,shortname)=router.split(",")
        routers.insert(0,shortname)
        coord=coord[:-2]
        (y,x)=coord.split(",")
        G.add_node(shortname)
        n=G.get_node(shortname)
        n.attr['pos']="%f,%f)"%(float(x)/1.0,float(y)/1.0)
        #n.attr['pos']="%f,%f)"%(float(x)/17.0,float(y)/17.0)
        # assign node size
        fcd=1.25
        d=.85
        n.attr['height']="%s"%d
        n.attr['width']="%s"%d
        # assign node color
        n.attr['fillcolor']="#0000%2x"%(int(fcd*256))
        # label
        n.attr['label']=str('"{}"'.format(shortname))
    return( G )
####################################################################################################################

