import sqlite3
import sys
sys.path.append("../plugins")
from easy_cdclient import cdclient_tables

conn = sqlite3.connect("../res/cdclient.sqlite")
c = conn.cursor()
c.execute("SELECT * FROM Objects WHERE id = 6010")
results = c.fetchone()
a = cdclient_tables.ObjectsTable.filter_return_results(results)
print(results)
print((a.id, a.name, a.placeable, a.type, a.description, a.localize, a.npcTemplateID, a.displayName,
       a.interactionDistance, a.nametag, a._internalNotes, a.locStatus, a.gate_version, a.HQ_valid))