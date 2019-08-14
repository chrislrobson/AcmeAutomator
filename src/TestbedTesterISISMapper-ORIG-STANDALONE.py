#!/usr/bin/python
"""
Connect to all routers in GEANT, obtain IS-IS adjacency information, graph it
"""
__author__ = """Niall Donaghy (niall@ndonaghy.com)"""

import subprocess
import time

def fetchConfig(command):
  """
  Spawn SSH process, connect to user@jumpboxhost.geant.net and execute 'command', saving output
  """
  #proc = subprocess.Popen(['ssh', 'user@jumpboxhost.geant.net', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = proc.communicate()
  return out

def scrapeConfig():
  """
  Because our list of routers and their co-ordinates are fixed, we just need to compute the ISIS trunks (edges between nodes)
  First we open the base input file 'geant.txt' and find the lines defining each router node
  Next we fetch the relevant JunOS output, namely 'show isis adjacencies' and 'show configuration protocols isis'
  From this output we can determine the edges and write a new file containing both node and edge definitions
  """

  import re

  # open file geant.txt
  try:
    fhr=open("geant.txt","r")
    print("Reading input file: geant.txt")
  except:
    print("File not found!")

  # geant.txt config file has the format, eg:
  # rt1.ams.nl.geant.net,rt1.ams.nl[10000,3000]
  # fqdn, shortname, [x,y] coords

  # store fqdn
  routers=[]
  # store shortname
  routersShortname=[]
  # store each line of config
  routersDef=[]
  # store each line of 'show isis adj' output
  routersAdj=[]
  # store the set command configuration
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
      # fetch info...
      #command = r'ssh -i sshkey -q -o StrictHostKeyChecking=no user@' + fqdn + ' "show isis adj | except Interface"'
      command = ['sshpass', '-p', 'testTest', 'ssh', '-l', 'test', fqdn, '\"show isis adj | except Interface\"']
      # FIXME CISCO command = ['sshpass', '-p', 'cisco', 'ssh', '-l', 'cisco', fqdn, '\"show isis adj\"']
      routersAdj[0] = fetchConfig(command)
      #command = r'ssh -i sshkey -q -o StrictHostKeyChecking=no user@' + fqdn + ' "show configuration protocols isis | display set | match metric | match interface"'
      command = ['sshpass', '-p', 'testTest', 'ssh', '-l', 'test', fqdn,
                 '\"show configuration protocols isis | display set\"']
      #'\"show configuration protocols isis | display set | match metric | match interface\"']
      routersCfg[0] = fetchConfig(command)
  fhr.close()

  # Now we've read in the configuration and retrieved ISIS adjacency data, create graph...
  try:
    fhw=open("geant_dynamic.txt","w")
    print("Writing to output file: geant_dynamic.txt")
  except:
    print("File not found!")

  # magic happens here...
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
        neighbour = parts[1]
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
            print("Found adjacency for " + routersShortname[i] + ": " + neighbour + " on interface " + interface + " with metric " + metric)
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

def createGraph():
  """
  Return a graph from the data in geant_dynamic.txt.
  """
  import math
  import re

  # open file geant_dynamic.txt
  print("GRAPHING...")
  try:
    fh=open("geant_dynamic.txt","r")
    print("Read input file: geant_dynamic.txt")
  except:
    print("File not found!")

  G=pgv.AGraph(name='GEANT')
  G.node_attr['shape']='circle'
  G.node_attr['fixedsize']='true'
  G.node_attr['fontsize']='8'
  G.node_attr['style']='filled'
  G.node_attr['color']='#40e0d0'
  G.graph_attr['outputorder']='edgesfirst'
  G.graph_attr['label']='TypMic Lab ' + time.strftime("%d/%m/%Y") + ' @ ' + time.strftime("%H:%M:%S")
  G.graph_attr['fontsize']='12'
  G.graph_attr['ratio']='\"1.0\"'
  G.edge_attr['color']='#AA00FF'
  G.edge_attr['style']='setlinewidth(3)'
  G.graph_attr['splines']='true'

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
      G.add_edge(routers[0],host,label=cost)
    else: # this line is a router definition
      (router,coord)=line.split("[")
      (fqdn,shortname)=router.split(",")
      routers.insert(0,shortname)
      coord=coord[:-2]
      (y,x)=coord.split(",")
      G.add_node(shortname)
      n=G.get_node(shortname)
      n.attr['pos']="%f,%f)"%(float(x)/17.0,float(y)/17.0)
      # assign node size
      d=1.25
      n.attr['height']="%s"%d
      n.attr['width']="%s"%d
      # assign node color
      n.attr['fillcolor']="#0000%2x"%(int(d*256))
      # label
      n.attr['label']=str('"{}"'.format(shortname))
  return G

if __name__ == '__main__':
  import warnings
  import pygraphviz as pgv

  # ignore Graphviz warning messages
  warnings.simplefilter('ignore', RuntimeWarning)

  scrapeConfig()
  G=createGraph()

  G.string()
  G.write("TypMic-ISIS-Map.dot")
  print("Wrote DOT language output file: TypMic-ISIS-Map.dot")
  print("Wrote final diagram output file: TypMic-ISIS-Map.png")
  G.draw("TypMic-ISIS-Map.png",prog='dot',args='-Tpng')
  #G.draw("geantISIS-X2.png",prog='dot',args='-n2')
  #G.draw("geantISIS-X2.png",prog='neato',args='-n2')
  print("Done!")