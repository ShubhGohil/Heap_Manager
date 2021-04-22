module.exports.dbconnect = function() {
    const mongoose = require("mongoose");
    mongoose.Promise = global.Promise;

    var connectiondb = mongoose.connect('mongodb://localhost:27017/trail', {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        useCreateIndex: true,
        useFindAndModify: false,
    });

    mongoose.connection.once('open', function() {
        console.log('connection established');
    }).on('error', function(error) {
        console.log('Connection error: ',  error);
    });
}

//module.exports.connectiondb = connectiondb;