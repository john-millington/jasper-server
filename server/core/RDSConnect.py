import MySQLdb
import MySQLdb.cursors

class RDSConnect:
  def __init__(self):
    self.instance = MySQLdb.connect(
      host="niqolo.c5tt8wo4aytu.eu-west-2.rds.amazonaws.com",
      user="niqolodev",
      passwd="2rU6e*fG",
      db="dev",
      cursorclass=MySQLdb.cursors.DictCursor
    )

    self.instance.ping(True)
    self.cursor = self.instance.cursor()
