#!/usr/bin/env python2

rules = [
    "node [shape=rectangle]",
]

import psycopg2 as ps

conn = conn = ps.connect(
    dbname="MYDATABASE", 
    user="MYUSER", 
    host="localhost",
)

cur = conn.cursor()
cur.execute("""
SELECT 
    constraints.table_name, table_usage.table_name
FROM 
    information_schema.table_constraints as constraints 
    JOIN
        information_schema.constraint_table_usage as table_usage
    ON 
        constraints.constraint_name = table_usage.constraint_name
WHERE 
    constraints.constraint_type = 'FOREIGN KEY' AND 
    constraints.table_schema = 'public';
""")

# Render graphviz visualization
print "digraph G {"
for rule in rules:
    print("    {};".format(rule))
print ""
for a, b in cur.fetchall():
    print("    {} -> {};".format(a, b))
print "}"

