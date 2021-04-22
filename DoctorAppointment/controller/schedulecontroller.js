const Schedule = require('../models/schedule');
const Booking = require('../models/booking');
const Doctor = require('../models/doctor');
const mail = require('../controller/sendmail');
const Patient = require('../models/patient');
const { ObjectId } = require('bson');
//const alert = require('alert');

var get = async function(callback) {
    var doctorname = [];
    
    Schedule.find().
    populate("doctorid", 'name').
    exec(async function(err, result) {
        if(err) {
            console.log(err);
        }
        else if(result) {
            //console.log(result.length);
            //console.log(result);
            if (result.length != 0) {
            result.forEach(function(records) {
                    if(!doctorname.includes(records.doctorid.name)) {
                        doctorname.push(records.doctorid.name);
                    } 
            });
        }
            callback(doctorname);
        }
        else {
            callback('none');
        }
    });
}

var make = async function(req, patientid) {
    Doctor.findOne({name: req.doctor}, {_id: 1}, async function(err, result) {
        if(err) {
            console.log(err);
        }
        else if(result){
            //console.log(result);
            //console.log(req.date);
            findtimeslot(req.doctor, result._id, String(req.date), patientid, editbooking);
             
        }
    });
}


/*var record = new Booking({
    patientid: id,
    doctorid: result,
    date: req.date,
    timeslot: req.time,
});
record.save().then(function() {
    alert("record saved");
    callback();
});*/



var findtimeslot = function(doctorname, doctorid, date, patientid, callback) {
    let t = new Date();
    var time, d = date;
    d += '-' + t.getMonth() + '-' + t.getFullYear();
    //console.log(d);
    Schedule.findOne({doctorid: doctorid, date: d}, async function(err, result) {
        if(err) {
            console.log(err);
        }
        else if(result) {
            time = result.timeslot[0];
            removetimeslot(doctorid, time);
            getemail(patientid, doctorname, d, time);
            callback(doctorid, d, patientid, time);
        }
        else{
            console.log("No available slots");
        }
    })
}

var editbooking = function(doctorid, date, patientid, timeslot) {
    let d = new Date();
    var record = new Booking({
        doctorid: doctorid,
        date: date,
        patientid: patientid,
        timeslot: timeslot,
    });
    record.save().then(function(err, result) {
        if(record.isNew === false) {
            console.log("booking saved");
            }
        else if(err) {
            console.log("Something is wrong with booking");
        }
    });
}

function getemail(patientid, doctorname, date, time) {
    console.log(patientid);
    Patient.findOne({_id: patientid}, {emailID: 1}, function (err, result) {
        if(err) {
            console.log(err);
        }
        else {
            mail.sendmail(mail.transport, result.emailID, doctorname, date, time);
        }
    });
}

var removetimeslot = function(id, time) {
    Schedule.updateOne({_id: id}, { $pull: { timeslot: [time] } }, function(err, result) {
        if(err) {
            console.log(err);
        }
        else if(result) {
            console.log('deleted one timeslot');
        }
        else {
            console.log("Nothing returned");
        }
    });
}

module.exports = {
    get: get,
    make: make,
    findtimeslot: findtimeslot,
}