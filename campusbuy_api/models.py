from datetime import datetime, timedelta

import jwt

from app.models import *


# Create your models here.
from campusbuy2_0.settings import SECRET_KEY


class User(User):

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. We're returning the user's fullname
        """
        return f'{self.first_name} {self.last_name}'

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=30)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().
        """
        return self._generate_jwt_token()
