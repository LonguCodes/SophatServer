from handlers import auth
from handler import redirect

handlers = {

    'AUTH': redirect('auth', auth.try_auth)

}