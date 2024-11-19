from signin import signin

@signin.route('/signin')
def signin():
    return "Sign In / Sign Up"