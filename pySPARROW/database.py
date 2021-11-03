from tables import File #see http://www.pytables.org

class DB:
    def __init__(self):
        """A hdf5 file that contains the input values for a river basin."""
        
        self._f = None
        self. _mode = None
        self._table = None
        #hard code path to database for now.
        self._filename = r"C:\user\jon\code\pySPARROW_v2\db\neuse_river_basin\data_v301.h5"

    def open(self, path, mode = "r"):
        self._f = File(path, mode)
        self._mode = mode
        
    def close(self):
        """Closes the database"""
        self._f.close()
        
    def flush(self):
        """makes changes permanent"""
        self._f.flush()

    def isopen(self):
        """determines whether the DB object is open"""
        if self._f:
            if self._f.isopen:
                return 1
        else:
            return 0
       
    def get_table(self, version = '0'):
        """Returns the h5 table representing the given network version."""
        if self._f.isopen:
            try:
                t = self._f.getNode('/', 'networks/network' + str(version))
            except:
                raise "must create table first"
            return t
        else:
            raise "db must be opened first (db.open())"
        
    def get_row(self, ComID, version= '0'):
        """Returns a dictionary of the attributes for a reach object from the db. """
        table = self.get_table(str(version))
        row = None
        for row in table.where("(ComID == '" + str(ComID) + "')"): break
        if row == None: 
            raise 'Reach with ComID ' + str(ComID) + ' and version '\
                + str(version) + ' not in database'
        else:
            return row
        
    def get_rows(self, ComIDs, version= '0'):
        """Returns a dictionary of the attributes for a reach object from the db. """
        table = self.get_table(str(version))
        #build string
        query = ""
        i = 1
        for ComID in ComIDs:
            if i != len(ComIDs):
                query += "(ComID == '" + str(ComID) + "') | " 
            else:
                query += "(ComID == '" + str(ComID)+ "')"
            i +=1
        rows = {}
        for row in table.where(query):
            rows[row['ComID']] = row
        return rows
