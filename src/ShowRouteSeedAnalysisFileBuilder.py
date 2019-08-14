# FIXME DEBUG import ast
# FIXME DEBUG import collections
debug = False
route_analysis_filename = "10.10.9.20-r94-show-route-analysis-logical-5a1.prf"
route_analysis_fd = None
data_fd = None
prepare_analysis_flag = False
start_analysis_flag = False
start_but_skip_one_analysis_flag = False
router_id = ""

def build_route_analysis_seed_file( data_fd, route_analysis_fd ):
  route_table = []
  for data in data_fd:
    print( data )
    if data.startswith( "i " ):
      route_table.append(  "{" + \
                           "\"show route\":\"show_route\"," \
                           "\"device\":\"cisco\"," \
                           "\"route\":\"{}\"," \
                           "\"next-hop\":\"{}\","
                           "\"interface\":\"{}\"".format( data.split()[1],
                                                          data.split()[5].split(",")[0],
                                                          data.split()[7] ) + \
                           "};")
    elif data.startswith("C "):
      route_table.append("{" + \
                         "\"show route\":\"show_route\"," \
                         "\"device\":\"cisco\"," \
                         "\"route\":\"{}\"," \
                         "\"next-hop\":\"{}\","
                         "\"interface\":\"{}\"".format(data.split()[1],
                                                       data.split()[4].split(",")[0],
                                                       data.split()[6]) + \
                         "};")
    elif data.startswith("L ") or data.startswith("S "):
      try:
        route_table.append("{" + \
                           "\"show route\":\"show_route\"," \
                           "\"device\":\"cisco\"," \
                           "\"route\":\"{}\"," \
                           "\"next-hop\":\"{}\","
                           "\"interface\":\"{}\"".format(data.split()[1],
                                                         data.split()[4].split(",")[0],
                                                         data.split()[6]) + \
                           "};")
      except:
        try:
          route_table.append("{" + \
                             "\"show route\":\"show_route\"," \
                             "\"device\":\"cisco\"," \
                             "\"route\":\"{}\"," \
                             "\"next-hop\":\"{}\",".format( data.split()[1],
                                                            data.split()[4].split(",")[0] ) + \
                             "};")
        except Exception as e:
          print( e )
    else:
      route_table.append( "{" + \
                          "\"show route\":\"show_route\"," \
                          "\"device\":\"cisco\"," \
                          "\"route\":\"{}\"," \
                          "\"next-hop\":\"{}\"".format( data.split()[1],
                                                        data.split()[4].split( "," )[0] ) + \
                          "};")
  for seed_dictionary in route_table:
    # FIXME DEBUG print(seed_dictionary)
    try:
      route_analysis_fd.write(seed_dictionary + "\n")
    except:
      print("Seed dictionary file write failed.")
  return()

try:
  route_analysis_fd = open(route_analysis_filename, "w+")
except:
  print( "Failed to open analysis write file" )
try:
  with open( "./.AcmeAutomator/myARCHIVES/TRUNK-STATUS/10.10.9.20/10.10.9.20-r94-show-route-data-04Jul2017-0812-20", "r" ) as data_fd:
    for data in data_fd:
      if start_analysis_flag:
        build_route_analysis_seed_file( data_fd, route_analysis_fd )
        route_analysis_fd.close()
        data_fd.close()
        break
      elif start_but_skip_one_analysis_flag:
        start_analysis_flag = True
        continue
      elif prepare_analysis_flag and data.startswith( "Gateway of last resort is" ):
        start_but_skip_one_analysis_flag = True
      elif data.startswith( "DUT( r94/10.10.9.20 )-> show route" ):
        prepare_analysis_flag = True
        continue
      else:
        continue
except Exception as e:
  print( "NO data found!" )
