const mongodb = require('mongodb');
const MongoClient = mongodb.MongoClient;

let _db;

const mongoConnect = callback => {
  
  MongoClient.connect(process.env.DB_URI)
      .then(client => {
        console.log("Connnected To MongoDB!");

        _db = client.db();

        callback();
      })
      .catch(err => {
        console.log(err);
        throw err;
      });

};

const getDb = () => {
  if(_db) {
    return _db;
  }
  throw 'No Database Found!'
}

module.exports = {
  mongoConnect : mongoConnect,
  getDb : getDb
};