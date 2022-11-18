from app import app
import ibm_db

try:
    conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=rvm88889;PWD=nCp4LTEEPiIAsqpX", '', '')
    print("Connected to database: ", conn)
except:
    print("Unable to connect to the database")
