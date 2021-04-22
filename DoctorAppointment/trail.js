const { ObjectId } = require('bson');
//const Booking = require('./models/booking');
const Schedule = require('./models/schedule');

const mongodb = require("./connection");

mongodb.dbconnect();

var r = {
    doctorid: ObjectId("607afbf2604af24e461ce2cf"),
    date: '24-4-2021',
    timeslot: '18.00',
}

function make(r) {
    var record = new Schedule ({
        doctorid: r.doctorid,
        date: r.date,
        timeslot: r.timeslot,
    });
    record.save().then(function() {
        if(record.isNew === false) {
            console.log("recorded");
            //callback(r.patientid);
        }
    });
}

/*var displaydbooking = async function(id) {
    
    await Booking.find({patientid: id}).
    populate('doctorid', 'name').
    exec(function(err, doctor) {
        if(err) {
            console.log(err);
        }
        else if(doctor){
            doctor.forEach(function(reco) {
                console.log(reco);
            });
        }
        else {
            console.log("alag hi chalra yahanpe");
        }
    });
}*/

//make(r, displaydbooking);
//displaydbooking(r.patientid);
make(r);

/*module.exports = {
    displaydbooking: displaydbooking,
}*/