    const mongoose = require("mongoose");
    const bcrypt = require("bcryptjs");
    
    //mongoose.Promise = global.Promise;

    mongoose.connect('mongodb://localhost/trail2', {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        useCreateIndex: true,
    });

    mongoose.connection.once('open', function() {
        console.log('connection established');
    }).on('error', function(error) {
        console.log('Connection error: ',  error);
    });

    const PatientSchema = new mongoose.Schema({
        name: {type: String, required: true},
        mobile: {type: Number, required: true},
        emailID: {type: String, required: true, unique:true},
        address: {type: String},
        passwd: {type: String, required: true},
    }, {collection: 'patientmodel'});
    
    const patientmodel = mongoose.model('patientmodel', PatientSchema);
    
    module.exports = patientmodel;
    
    data = {
        name: 'abcd efgh',
        mobile: '1234567890',
        emailID: 'abcd@gmail.com',
        passwd: 'abcd',   
    }
    console.log(data.passwd);
    bcrypt.hash(data.passwd, 5, function(err, result) {
        if(err) {
            console.log(err);
        }
        else {
            console.log(result);
            var record = new patientmodel({
                name: data.name,
                mobile: data.mobile,
                emailID: data.emailID,
                passwd: result,
            });
            
            record.save().then(function() {
                if(record.isNew === false) {
                    patientmodel.findOne({emailID: 'abcd@gmail.com'}, function(err, result) {
                        if(err) {
                            console.log(err);
                        }
                        else {
                            console.log(result);
                        }
                    });
                }
                else {
                    return 'error';
                }
            });
        }
    });
   