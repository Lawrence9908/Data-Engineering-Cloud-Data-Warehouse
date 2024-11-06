import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drop all existing staging, fact, and dimension tables from the database.

    Args:
        cur: (cursor) instance of cursor class used to execute database commands.
        conn: (connection) instance of connection class used to manage database connection.

    Returns:
        None
    """
    # Execute each query in the list to drop tables
    for query in drop_table_queries:
        cur.execute(query)  # Execute the drop table query
        conn.commit()  # Commit changes to the database


def create_tables(cur, conn):
    """
    Create staging, fact, and dimension tables in the database.

    Args:
        cur: (cursor) instance of cursor class used to execute database commands.
        conn: (connection) instance of connection class used to manage database connection.

    Returns:
        None
    """
    # Execute each query in the list to create tables
    for query in create_table_queries:
        cur.execute(query)  # Execute the create table query
        conn.commit()  # Commit changes to the database


def main():
    """
    Main function to manage the workflow of dropping and creating tables.

    Returns:
        None
    """
    # Initialize the config parser to read the configuration file
    config = configparser.ConfigParser()
    config.read('dwh.cfg')  # Read the database configuration file

    # Establish the connection to the database using parameters from the config
    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values())
    )
    
    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    # Drop existing tables to start fresh
    drop_tables(cur, conn)

    # Create new tables as per the defined schema
    create_tables(cur, conn)

    # Close the connection to the database
    conn.close()


if __name__ == "__main__":
    main()  # Run the main function to execute the script
