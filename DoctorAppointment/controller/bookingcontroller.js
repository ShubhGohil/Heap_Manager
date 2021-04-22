const Booking = require('../models/booking');

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

/*make(r);
displaydbooking(r.patientid);*/

module.exports = {
    displaydbooking: displaydbooking,
    make: make,
    displaypbooking: displaypbooking,
}