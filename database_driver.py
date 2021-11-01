import mongoengine as me
import certifi

def connect_to_db():
    # Connection information
    address = "mongodb+srv://dbUser:potkan420@cluster0.bkic2.mongodb.net/public_health_system?retryWrites=true&w=majority"
    database_name = "public_health_system"
    certificate = certifi.where()

    me.connect(db=database_name, host=address, tlsCAFile=certificate)


