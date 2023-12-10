# Esta clase se encarga de la gestión y manipulación de datos relacionados con los usuarios.

# Hanadlers
from src.utils.DatabaseHandler import DatabaseHandler

from src.utils.Logger import Logger


class UserModel:
    def __init__(self, id, email, hashed_password, username, name, activation_token=None):
        self.id = id
        self.email = email
        self.password = hashed_password
        self.username = username
        self.name = name
        self.activation_token = activation_token

        # Puedes agregar más atributos de usuario según tus necesidades, como nombre, rol, etc.

    @classmethod
    def create_user(cls, email, password, username, name):
        # Método para crear un nuevo usuario en la base de datos.
        query = "INSERT INTO users (email, password, username, name, account_status) VALUES (%s, %s, %s, %s, %s)"
        values = (email, password, username, name, "ACTIVE")
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.INSERT)

    @classmethod
    def user_exists_email(cls, email):
        # Método para verificar si un usuario con el mismo correo electrónico ya existe en la base de datos.
        query = "SELECT COUNT(*) FROM users WHERE email = %s"
        values = (email,)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.SELECT)
        return bool(data and data[0][0] > 0)

    @classmethod
    def user_exists_username(cls, username):
        # Método para verificar si un usuario con el mismo correo electrónico ya existe en la base de datos.
        query = "SELECT COUNT(*) FROM users WHERE username = %s"
        values = (username,)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.SELECT)
        return bool(data and data[0][0] > 0)

    @classmethod
    def get_user_by_email(cls, email):
        # Método para recuperar información de usuario basada en su dirección de correo electrónico.
        query = "SELECT id, email, password, username, name FROM users WHERE email = %s"
        values = (email,)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.SELECT)
        return cls(*data[0]) if data else None

    @classmethod
    def get_project_active(cls, user_id):
        # Método para extraer el proyecto activo de un usuario
        query = "SELECT project_active FROM users WHERE id = %s"
        values = (user_id,)
        data = DatabaseHandler.execute_query(query, values, DatabaseHandler.SELECT)
        return data[0][0] if data else None
