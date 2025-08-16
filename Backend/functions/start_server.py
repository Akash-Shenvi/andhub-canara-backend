from Andhub.Main import app
import pymysql
import os
pymysql.install_as_MySQLdb()
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
