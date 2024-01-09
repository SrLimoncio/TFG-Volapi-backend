# Esta clase se encarga de la autenticacion y la seguridad de las credenciales de los usuarios.
import bcrypt
import re

# Hanadlers
from src.utils.DatabaseHandler import DatabaseHandler
# UserModel
from src.models.UserModel import UserModel

from src.utils.Logger import Logger


class AuthModel:
    @classmethod
    def verify_password(cls, provided_password, hashed_password):
        # Método para verificar si la contraseña proporcionada coincide
        # con la contraseña almacenada en la base de datos.
        if isinstance(provided_password, str):
            provided_password = provided_password.encode('utf-8')
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')

        return bcrypt.checkpw(provided_password, hashed_password)

    @classmethod
    def authenticate_user(cls, email, provided_password):
        # Método para autenticar a un usuario mediante la verificación de credenciales.
        user_data = UserModel.get_user_by_email(email)
        if user_data and cls.verify_password(provided_password, user_data['password']):
            return UserModel(user_data['id'], email, user_data['password'], user_data['username'], user_data['name'])  # Usuario autenticado
        else:
            return None  # Autenticación fallida

    @classmethod
    def generate_password_hash(cls, password):
        # Método para generar un hash seguro de una contraseña antes de almacenarla en la base de datos.
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    @classmethod
    def validate_login(cls, email, provided_password):

        if email or provided_password:
            user = UserModel.get_user_by_email(email)
            if user:
                if cls.verify_password(provided_password, user.password):
                    return user
                # if UserModel.user_exists_email(email):  # Correo ya en uso
                # errors['email'] = "The email address is already in use. Please choose another one."
        return None

    @classmethod
    def validate_registration(cls, email, password, password2, username, name):
        errors = {}

        email_regex = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"
        if not email:  # Correo en blanco
            errors['email'] = "The e-mail field is required."
        if not re.match(email_regex, email):  # Correo formato invalido
            errors['email'] = "Please enter a valid email address. "
        if UserModel.user_exists_email(email):  # Correo ya en uso
            errors['email'] = "The email address is already in use. Please choose another one."

        password_regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
        if not password:  # Password en blanco
            errors['password'] = "The password field is required."
        if not re.match(password_regex, password):  # Password formato invalido
            errors['password'] = ("The password must be at least 8 characters long, one number, "
                                  "a lowercase letter and an uppercase letter.")
        if not password2 or password != password2:  # Password1 y password2 no coinciden
            errors['password2'] = "The passwords you provide do not match."

        username_regex = r"^[a-zA-Z0-9_]{3,20}$"
        if not username:
            errors['username'] = "The username field is required."
        if not re.match(username_regex, username):
            errors['username'] = "The username must contain only 3 to 20 alphanumeric characters or underscores."
        if UserModel.user_exists_username(username):  # Correo ya en uso
            errors['username'] = "The username is already in use. Please choose another one."

        name_regex = r"^[a-zA-Z0-9 ]$"
        if not name:
            errors['name'] = "The name field is required."
        if not re.match(name_regex, name) and len(name.split()) < 2:
            errors['name'] = "The full name contains characters that are not allowed or is not complete."

        return errors
