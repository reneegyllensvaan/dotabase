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
    constraints.table_name as key_from,  
    table_usage.table_name as key_to,
    checks.check_clause IS NULL as nullable
    
FROM 
    information_schema.table_constraints as constraints 
    JOIN
        information_schema.constraint_table_usage as table_usage
    ON 
        constraints.constraint_name = table_usage.constraint_name
    JOIN
        information_schema.key_column_usage as column_usage
    ON 
        constraints.constraint_name = column_usage.constraint_name AND 
        constraints.table_name = column_usage.table_name
    LEFT JOIN
        (
        SELECT 
            table_constraints.table_name as check_table,
            SUBSTR(
                check_constraints.check_clause,
                1,
                POSITION(' ' in check_constraints.check_clause)-1
            ) as check_column,
            check_constraints.check_clause as check_clause
        FROM 
            information_schema.table_constraints 
        JOIN 
            information_schema.check_constraints 
        ON 
            table_constraints.constraint_name = check_constraints.constraint_name 
        WHERE 
            check_constraints.check_clause like '% IS NOT NULL' 
            AND check_constraints.constraint_schema = 'public'
        ) as checks
    ON 
        checks.check_column = column_usage.column_name AND 
        checks.check_table = constraints.table_name
WHERE 
    constraints.constraint_type = 'FOREIGN KEY' AND 
    constraints.table_schema = 'public';
""")

# Render graphviz visualization
print "digraph G {"
for rule in rules:
    print("    {};".format(rule))
print ""
for from_table, to_table, nullable in cur.fetchall():
    print("    {} -> {}{};".format(
        from_table, 
        to_table, 
        "[style=dashed]" if nullable else ""
    ))
print "}"

