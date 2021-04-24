const Booking = require('../models/booking');
const Doctor = require('../models/doctor');
const Schedule = require('../models/schedule');

function make(r) {
    let record = new Booking ({
        patientid: r.patientid,
        doctorid: r.doctorid,
        date: r.date,
        timeslot: r.timeslot,
    });
    record.save().then(function() {
        if(record.isNew === false) {
            console.log("pass");
        }
    });
}

var displaydbooking = async function(id, callback) {
    
    await Booking.find({patientid: id}).
    populate('doctorid', 'name').
    exec(async function(err, doctor) {
        if(err) {
            console.log(err);
        }
        else if(doctor){
            callback(doctor);
        }
        else {
            callback('none');
        }
    });
}

var displaypbooking = async function(id, callback) {
    
    await Booking.find({doctorid: id}).
    populate('patientid', 'name').
    exec(async function(err, patient) {
        if(err) {
            console.log(err);
        }
        else if(patient) {
            callback(patient);
        }
        else {
            callback('none');
        }
    });
}

var deletebooking =  function(patientid, body, callback) {
    Doctor.findOne({name: body.doctor},{_id: 1}, async function(err, result) {
        if(err) {
            console.log(err);
        }
        else if(result) {
            Booking.findOneAndRemove({patientid: patientid, doctorid: result._id, date: body.date}, async function(err, result1) {
                if(err) {
                    console.log(err);
                }
                else if(result1) {
                    Schedule.findOneAndUpdate({doctorid: result._id}, { $addToSet: { timeslot : body.time } }, async function(err, result2) {
                        if(err) {
                            console.log(err);
                        }
                        else if(result2){
                            callback();
                        }
                    });
                }
            });
        }
    });
}

module.exports = {
    displaydbooking: displaydbooking,
    make: make,
    displaypbooking: displaypbooking,
    deletebooking: deletebooking,
}