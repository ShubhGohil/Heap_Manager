var mongoose = require('mongoose');

const DoctorSchema = new mongoose.Schema({
    name: {type: String, required: true},
    mobile: {type: String, required: true},
    speciality: {type: String, required: true},
    emailID: {type: String, required: true, unique:true},
    passwd: {type: String, required: true},
}, {collection: 'doctormodel'});

const doctormodel = mongoose.model('doctormodel', DoctorSchema);

module.exports = doctormodel;