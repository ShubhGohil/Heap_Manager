const Doctor = require("../models/doctor");
const Schedule = require("../models/schedule");
const Booking = require("../models/booking");
const userhandler = require("../controller/usercontroller");
const bcrypt = require("bcryptjs");
const passport = require('passport');
const LocalStrategy = require("passport-local").Strategy;
const User = require("../models/user");

var search = async function (email, passwd, res, callback) {
    await Doctor.findOne({emailID: email}, {emailID: 1, passwd: 1, _id: 1}, async function(err, result) {
        if (err) {
            res.status(400).json({error: 'Email not registered'});
        }
        else if(result){
            bcrypt.compare(passwd, result.passwd, function(err, ismatch) {
                if(ismatch) {
                    callback(result._id);
                }
                else {
                    res.status(400).json({error: 'Incorrect password'});
                }
            });
        }
        else {
            res.status(400).json({error: 'Email not registered'});        
        }
    });
};

var create = async function (data, res, callback) {

    await Doctor.findOne({ emailID: data.email},function (err, rec) {
        if (rec) {
            console.log('idhar');
            res.status(400).json({error: "Email already registered"});
        }
        else if (err) {
            console.log(err);
            res.redirect('/');
        }
        else {
            bcrypt.hash(data.newpasswd, 5, async function (err, result) {
                var record = new Doctor({
                    name: data.name,
                    mobile: data.mobile,
                    emailID: data.email,
                    passwd: result,
                    speciality: data.speciality,
                });
        
                await record.save().then(async function() {
                    if (record.isNew === false) {
                        await Doctor.findOne({ emailID: data.email}, function (err, doc) {
                            userhandler.createuser(doc._id, doc.passwd);
                            if (doc){
                                callback(doc._id);
                            }
                        });
                    }
                    else {
                        return "error";
                    }
                });   
            });
        }
    });    
};



var extract = async function(id, res, callback) {
    await Doctor.findOne({_id: id}, {passwd: 0}, async function(err, result) {
        if (err) {
            res.status(400).json({error: 'Server error'});
        }
        else if(result){
            callback(result);
        }
    });
}

var extractall = async function(callback) {
    await Doctor.find(async function(err, result) {
        if(err) {
            res.status(400).json({error: "Server error"});
        }
        else if(result) {
            callback(result);
        }
        else{
            console.log("empty");
        }
    }); 
}

var update = async function(id, fields, callback) {
    if(fields.passwd == '') {
        await Doctor.findOneAndUpdate(
            {_id: id },
            { name: fields.doctor, mobile: fields.mobile, emailID: fields.email, speciality: fields.speciality }
        );
    }
    else {
        bcrypt.hash(fields.passwd, 5, async function(err, result) {
            if(err) {
                console.log("Error while updating with password");
            }
            else {
                Doctor.findOneAndUpdate(
                    {_id: id},
                    { name: fields.doctor, mobile: fields.mobile, emailID: fields.email, passwd: result, speciality: fields.speciality  }
                );
            }
        });
    }
    callback();
}

var deleteschedule = async function(id, res) {
    Schedule.findOneAndRemove({doctorid: id}, async function(err, result) {
        if(err) {
            console.log("Error from remove doctor schedule " + String(err));
        }
        else if(result) {
            console.log("Schedule removed");
            res.redirect('/');
        }
        else {
            res.redirect("/");
        }
    });
}

var deletebookingd = async function(id, res) {
    Booking.findOneAndRemove({doctorid: id}, async function(err, result) {
        if(err) {
            console.log("Error from remove patient booking " + String(err));
        }
        else if(result) {
            console.log("Patient booking removed");
            deleteschedule(id, res);
        } 
    });
}

var deletedoctor = async function(id, res) {
    Doctor.findOneAndRemove({_id: id}, async function(err, result) {
        if(err) {
            console.log(err);
        }
        else if(result) {
            console.log("doctor removed");
            deletebookingd(id, res);
        }
    });
    User.findOneAndRemove({uid: id});
}

const customfields = {
    usernameField: 'email',
    passwordField: 'passwd',
}

var verifyd = async function(username, password, done) {
    Doctor.findOne({emailID: username})
        .then(function(result) {
            if(!result) {
                return done(null, false)
            }

            bcrypt.compare(password, result.passwd, function(err, ismatch) {
                if(ismatch) {
                    done(null, result);
                }
                else {
                    done(null, false);
                }
            });

        })
        .catch(function(err) {
            done(err);
        });
}

const strategyd = new LocalStrategy(customfields, verifyd);

passport.use("local-dlogin", strategyd);

module.exports = {
  search: search,
  create: create,
  extract: extract,
  extractall: extractall,
  update: update,
  deletedoctor: deletedoctor,
};

