const mongoose = require('mongoose');
const Doctor = require('./doctor');

const BookingSchema = new mongoose.Schema({
    patientid: {type: mongoose.Schema.Types.ObjectId, ref: "patientmodel", required: true},
    doctorid: {type: mongoose.Schema.Types.ObjectId, ref: Doctor, required: true},
    date: {type: String, required: true},
    timeslot: {type: String, required: true},
}, {collection: 'bookingmodel'});

const bookingmodel = mongoose.model('bookingmodel', BookingSchema);

module.exports = bookingmodel;