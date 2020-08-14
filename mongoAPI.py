from flask import Flask, request
from bson.json_util import dumps
from flask_cors import CORS, cross_origin
import pymongo


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
@app.route("/Data")
@cross_origin()
def dummy_api():
    Arg1=request.args['KeyWord']
    myclient = pymongo.MongoClient("mongodb://AdminZ:AdminPWD@cluster0-shard-00-00-gfv3w.mongodb.net:27017,cluster0-shard-00-01-gfv3w.mongodb.net:27017,cluster0-shard-00-02-gfv3w.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")

    db = myclient.test
    print("Mongo DataBase:", db)
    mydb = myclient["ScrapedDB"]
    mycol = mydb["ScrapedData"]
    if(Arg1==''):
        return dumps(mycol.find())

    else :
        myquery = {"$or": [{"headline": {"$regex": ".*" + Arg1 + ".*"}}, {"link": {"$regex": ".*" + Arg1 + ".*"}},
                           {"summary": {"$regex": ".*" + Arg1 + ".*"}}]}

        return dumps(mycol.find(myquery))

if __name__ =="__main__":
    app.debug = True
    app.run()
