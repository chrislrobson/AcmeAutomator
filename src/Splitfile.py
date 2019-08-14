#--------------------------------------------------------------------------------------------------------------------
class SplitLargeFile:
  "Split Large Files"
  #------------------------------------------------------------------------------------------------------------------
  def __init__(self):
    self.name = "Split Large Files"
  #------------------------------------------------------------------------------------------------------------------
  def split_large_file( self, baseline_file, upgrade_file, archiveFD ):
    self.chunksize = 100000
    self.chunkcount = 0
    self.file_list = [ baseline_file, upgrade_file ]
    for self.file in self.file_list:
      self.fileID = 1
      with open( self.file ) as self.infile:
          self.f = open( "%s_%d" % ( self.file, self.fileID ), 'w' )
          for self.i, self.line in enumerate( self.infile ):
            self.f.write( self.line )
            self.chunkcount += len( self.line )
            if self.chunkcount >= self.chunksize:
              self.f.close( )
              self.fileID += 1
              self.f = open( "%s_%d" % ( self.file, self.fileID ), 'w' )
              self.chunkcount = 0
          self.f.close( )
    return()
