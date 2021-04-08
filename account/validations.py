def validate_input (data):
    message = []
    if len(data["name"]) == 0:
       message.append("First name field cannot be empty")
    elif len(data["name"]) <= 3:
        message.append("First name is too small")
    else:
        message.append("false")

    if len(data["email"]) == 0:
        message.append("email field cannot be empty")
    elif len(data["name"]) <= 3:
        message.append("email field is too small!! it must be above three characters") 
    else:
        message.append("false") 

    if len(data["password1"]) == 0:
        message.append("Password field cannot be empty")
    elif len(data["password1"]) <= 8:
        message.append("Password is too small !!! it must be above 8 characters")
    else:
        message.append("false")

    if len(data["password2"]) == 0:
       message.append("Confirm Password field cannot be empty") 
    elif len(data["password2"]) <= 3:
        message.append("confirm password is too small !!! it must be above 8 characters")
    elif(data["password1"] != data["password2"]):
        message.append("Password is not identical")
    else:
        message.append("false")
        
    if len(data["username"]) == 0:
        message.append("username field cannot be empty")
    elif(len(data["username"]) <= 8):
        message.append("username is too small !!! it must be above 8 characters")
    else:
        message.append("false")

    return message

def validate_login_form(data):
    message = []
    if len(data["name"]) == 0:
       message.append("name field cannot be empty")
    else:
        message.append("false")
    if len(data["password"]) == 0:
       message.append("password field cannot be empty")
    else:
        message.append("false")

    return message
   
    