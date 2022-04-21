from functools import wraps
import jwt
from flask import flash, redirect, request, abort
from flask import current_app
from project.models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt')
        if not token:
            flash(message='Token missing', category='error')
            return redirect('/user/login')
        try:
            # data=
            current_user=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            if current_user is None:
                flash(message='Error: {0}'.format(e), category='error')
                return redirect('/user/login')
            # if not current_user.active:
            #     abort(403)
        except Exception as e:
            flash(message='Error: {0}'.format(e), category='error')
            return redirect('/user/login')

        return f(current_user, *args, **kwargs)

    return decorated