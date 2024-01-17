# Esta clase se encarga de la autenticacion y la seguridad de las credenciales de los usuarios.
import re

# Hanadlers
from src.utils.DatabaseHandler import DatabaseHandler
# UserModel
from src.models.UserModel import UserModel
from src.utils.Security import Security

from src.exceptions.AuthExceptions import InvalidCredentialsException, UserNotFoundException


class AuthModel:
    @classmethod
    def authenticate_user(cls, email, provided_password):
        """
        Autentica a un usuario en el sistema.

        Args:
            email (str): Email del usuario a autenticar.
            provided_password (str): Contraseña proporcionada por el usuario.

        Returns:
            UserModel: El modelo del usuario autenticado.

        Raises:
            InvalidCredentialsException: Si el email o la contraseña son incorrectos.
            UserNotFoundException: Si el usuario no se encuentra.
        """

        if not email or not provided_password:
            raise InvalidCredentialsException("Error Auth: Email and password are required.")

        user = UserModel.get_user_by_email(email)

        if not user:
            raise UserNotFoundException("Error Auth: User not found.")

        if Security.verify_password(provided_password, user.password):
            return user
        else:
            raise InvalidCredentialsException("Error Auth: Invalid password.")

    @classmethod
    def validate_registration(cls, email, password, password2, username, name):
        """
        Valida los datos de registro de un nuevo usuario.

        Args:
            email (str): Email del usuario.
            password (str): Contraseña del usuario.
            password2 (str): Confirmación de la contraseña.
            username (str): Nombre de usuario.
            name (str): Nombre completo del usuario.

        Returns:
            dict: Un diccionario con errores de validación, si los hay.
        """

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
