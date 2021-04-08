
def validate_file_extension(value,redirect,request):
    from django.core.exceptions import ValidationError
    if value == False:
        return  {"state": True,"message":"File was not selected"}
    elif not value.name.endswith(".csv"):
        if(ValidationError(u'Unsupported file extension.')):
            return {"state": True, "message":"This is an Invalid file !!! Upload a CSV file"}
    else:
        # to avoid typeerror
        return {"state":False}
    
        
