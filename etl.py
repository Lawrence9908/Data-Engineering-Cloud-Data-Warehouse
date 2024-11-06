import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Populate staging tables from S3.

    Args:
        cur: (cursor) instance of cursor class used to execute database commands.
        conn: (connection) instance of connection class used to manage database connection.

    Returns:
        None
    """
    # Execute each query to copy data from S3 into the staging tables
    for query in copy_table_queries:
        cur.execute(query)  # Execute the copy query for staging
        conn.commit()  # Commit changes to the database


def insert_tables(cur, conn):
    """
    Populate fact and dimension tables from staging tables.

    Args:
        cur: (cursor) instance of cursor class used to execute database commands.
        conn: (connection) instance of connection class used to manage database connection.

    Returns:
        None
    """
    # Execute each query to insert data from staging tables into fact and dimension tables
    for query in insert_table_queries:
        cur.execute(query)  # Execute the insert query for fact and dimension tables
        conn.commit()  # Commit changes to the database


def main():
    """
    Main function to manage the ETL process for loading data into the database.

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
    
    # Load data into staging tables from S3
    load_staging_tables(cur, conn)

    # Insert data into fact and dimension tables from staging tables
    insert_tables(cur, conn)

    # Close the connection to the database
    conn.close()


if __name__ == "__main__":
    main()  # Run the main function to execute the ETL process
