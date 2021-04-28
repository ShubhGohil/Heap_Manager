const Schedule = require('../models/schedule');
const Booking = require('../models/booking');
const Doctor = require('../models/doctor');
const mail = require('../controller/sendmail');
const Patient = require('../models/patient');
const { ObjectId } = require('bson');

var get = async function(callback) {
    var doctorname = [];
    
    Schedule.find().
    populate("doctorid", 'name').
    exec(async function(err, result) {
        if(err) {
            console.log(err);
        }
        else if(result) {
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

var make = async function(req, patientid, res) {
    Doctor.findOne({name: req.doctor}, {_id: 1}, async function(err, result) {
        if(err) {
            console.log(err);
        }
        else if(result){
            findtimeslot(req.doctor, result._id, String(req.date), patientid, res, editbooking);     
        }
    });
}


var findtimeslot = function(doctorname, doctorid, date, patientid, res, callback) {
    let t = new Date();
    var time, d = date;
    d += '-' + t.getMonth() + '-' + t.getFullYear();

    Schedule.findOne({doctorid: doctorid, date: d}, async function(err, result) {
        if(err) {
            console.log(err);
        }
        else if(result) {
            time = result.timeslot[0];
            removetimeslot(doctorid, time);
            getemail(patientid, doctorname, d, time);
            callback(doctorid, d, patientid, time, res);
        }
        else{
            console.log("no slots available");
            res.redirect("/profile/patient." + String(patientid) + "/makebooking/0");
        }
    })
}

var editbooking = function(doctorid, date, patientid, timeslot, res) {

    var record = new Booking({
        doctorid: doctorid,
        date: date,
        patientid: patientid,
        timeslot: timeslot,
    });
    record.save().then(function(err, result) {
        if(record.isNew === false) {
            console.log("booking saved");
            res.redirect("/profile/patient." + String(patientid) + "/makebooking/1");
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

var removetimeslot = async function(id, time) {
    await Schedule.findOneAndUpdate({doctorid: id}, { $pull: { timeslot: time } }, function(err, result) {
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

var addschedule = async function(id, info, callback) {
    const t = new Date;
    var d = info.body.date + '-' + t.getMonth() + '-' + t.getFullYear();
    console.log(d);
    var record = new Schedule({
        doctorid: id,
        date: d,
        timeslot: info.body.timeslot,
    });

    record.save().then(function(err, result) {
        if(record.isNew === false) {
            console.log("schedule saved");
        }
        else if(err) {
            console.log(err);
        }
    });
    callback();
}

module.exports = {
    get: get,
    make: make,
    findtimeslot: findtimeslot,
    addschedule: addschedule,
}