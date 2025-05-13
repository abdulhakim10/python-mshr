# import mysql.connector
# from mysql.connector import Error

# class DBConnector:
#     def __init__(self, host, port,user,password, database):
#         try:
#             self.connection = mysql.connector.connect(
#                 host=host,
#                 port=port,
#                 user=user,
#                 password=password,
#                 database=database
#             )
#             self.err_id = ""
#         except ValueError as e:
#             self.connection = None
#             self.err_id = str(e)

#     def select(self, query):
#         try:
#             cursor = self.connection.cursor(dictionary=True)
#             cursor.execute(query)
#             result = cursor.fetchall()
#             cursor.close()
#             self.err_id = ""
#             return result
#         except ValueError:
#             return []
        
#     def close(self):
#         if self.connection and self.connection.is_connected():
#             self.connection.close()