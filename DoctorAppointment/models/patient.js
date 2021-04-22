var mongoose = require('mongoose');

const PatientSchema = new mongoose.Schema({
    name: {type: String, required: true},
    mobile: {type: Number, required: true},
    emailID: {type: String, required: true, unique:true},
    address: {type: String},
    passwd: {type: String, required: true},
}, {collection: 'patientmodel'});

const patientmodel = mongoose.model('patientmodel', PatientSchema);

module.exports = patientmodel;