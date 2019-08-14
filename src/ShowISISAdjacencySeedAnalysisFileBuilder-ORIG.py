# FIXME DEBUG import ast
# FIXME DEBUG import collections
debug = False
isis_adjacency_analysis_filename = "./.AcmeAutomator/SHOW-ADJ-TEST-SEED-FILE.prf"
isis_adjacency_analysis_fd = None
isis_data_fd = None
prepare_analysis_flag = False
start_analysis_flag = False
start_but_skip_one_analysis_flag = False
isis_router_id = ""

def build_adjacency_analysis_seed_file( isis_data_fd, isis_adjacency_analysis_fd, isis_router_id ):
  isis_adjacency_table = []
  # FIXME DEBUG print( "IS-IS Router ID: {}".format( isis_router_id )  )
  for isis_data in isis_data_fd:
    if isis_data.startswith( "\n" ) or isis_data.startswith( "Total" ):
      break
    else:
      isis_adjacency_table.append(
                                   "{" + \
                                   "\"show isis adjacency\":\"show_isis_adjacency\",\"device\":\"cisco\"," \
                                   "\"is-is router id\":\"{}\",".format( isis_router_id ) + \
                                   "\"system id\":\"{}\",\"interface\":\"{}\",\"snpa\":\"{}\",\"state\":\"{}\"," \
                                   "\"hold\":\"{}\",\"change\":\"{}\",\"nsf\":\"{}\",\"ipv4\":\"{}\"," \
                                   "\"ipv6\":\"{}\"".format( isis_data.split()[0],
                                                               isis_data.split()[1],
                                                               isis_data.split()[2],
                                                               isis_data.split()[3],
                                                               isis_data.split()[4],
                                                               isis_data.split()[5],
                                                               isis_data.split()[6],
                                                               isis_data.split()[7],
                                                               isis_data.split()[8] ) + \
                                   "};")
  for seed_dictionary in isis_adjacency_table:
    # FIXME DEBUG print(seed_dictionary)
    try:
      isis_adjacency_analysis_fd.write(seed_dictionary + "\n")
    except:
      print("Seed dictionary file write failed.")
  return()

try:
  isis_adjacency_analysis_fd = open(isis_adjacency_analysis_filename, "w+")
except:
  print( "Failed to open analysis write file" )
try:
  with open( "./.AcmeAutomator/SHOW-ADJ-TEST.prf", "r" ) as isis_data_fd:
    for isis_data in isis_data_fd:
      if start_analysis_flag:
        build_adjacency_analysis_seed_file( isis_data_fd, isis_adjacency_analysis_fd, isis_router_id )
        isis_adjacency_analysis_fd.close()
        isis_data_fd.close()
        break
      elif start_but_skip_one_analysis_flag:
        start_analysis_flag = True
        continue
      elif isis_data.startswith( "IS-IS" ):
        isis_router_id = isis_data.split()[1]
      elif prepare_analysis_flag and isis_data.startswith( "System Id      Interface        SNPA" ):
        start_but_skip_one_analysis_flag = True
      elif isis_data.startswith( "DUT( r94/10.10.9.20 )-> show isis adjacency" ):
        prepare_analysis_flag = True
        continue
      else:
        continue
except Exception as e:
  print( "NO data found!" )
