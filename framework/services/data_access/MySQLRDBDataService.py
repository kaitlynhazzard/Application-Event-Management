import pymysql
from .BaseDataService import DataDataService


class MySQLRDBDataService(DataDataService):
    """
    A generic data service for MySQL databases. The class implement common
    methods from BaseDataService and other methods for MySQL. More complex use cases
    can subclass, reuse methods and extend.
    """

    def __init__(self, context):
        super().__init__(context)

    def _get_connection(self):
        connection = pymysql.connect(
            host=self.context["host"],
            port=self.context["port"],
            user=self.context["user"],
            passwd=self.context["password"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return connection

    def check_connection(self, database_name: str, table_name: str):
        """
        Check if the connection to the database is successful by selecting all data
        from a specific table.
        Args:
            - database_name: Name of the database to query.
            - table_name: Name of the table to fetch all records from.
        Returns:
            - A dictionary with connection status and result of the query (all rows).
        Raises:
            - Exception if the connection or query execution fails.
        """
        connection = None
        try:
            # Establish a connection
            connection = self._get_connection()

            # Create a cursor and execute a query to select all rows from the given table
            cursor = connection.cursor()
            query = f"SELECT * FROM {database_name}.{table_name}"
            cursor.execute(query)

            # Fetch all the results (each row will be a dictionary)
            result = cursor.fetchall()

            # Return the result
            return {"status": "connected", "data": result}

        except Exception as e:
            # In case of any failure, raise an exception with a message
            raise Exception(f"Database connection failed: {str(e)}")

        finally:
            # Ensure the connection is closed after the check
            if connection:
                connection.close()

    def get_data_object(self,
                        database_name: str,
                        collection_name: str,
                        key_field: str,
                        key_value: str):
        """
        See base class for comments.
        """

        connection = None
        result = None

        try:
            sql_statement = f"SELECT * FROM {database_name}.{collection_name} " + \
                        f"where {key_field}=%s"
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, [key_value])
            result = cursor.fetchone()
        except Exception as e:
            if connection:
                connection.close()

        return result

    def insert_data_object(self, database_name: str, collection_name: str, data: dict) -> bool:
        """
        Inserts a data object into the specified table in the database.

        Args:
            - database_name: Name of the database.
            - collection_name: Name of the table to insert data into.
            - data: A dictionary representing the data to be inserted.

        Returns:
            - True if insertion was successful, otherwise raises an Exception.
        """
        connection = None
        try:
            # Construct the SQL insert statement
            columns = ", ".join(data.keys())
            values_placeholders = ", ".join(["%s"] * len(data))
            sql_statement = f"INSERT INTO {database_name}.{collection_name} ({columns}) VALUES ({values_placeholders})"

            # Get the values from the dictionary as a tuple
            values = tuple(data.values())

            # Establish a connection and execute the query
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, values)

            # Commit the transaction
            connection.commit()

            return True

        except Exception as e:
            if connection:
                connection.rollback()
            raise Exception(f"Failed to insert data object: {str(e)}")

        finally:
            if connection:
                connection.close()





