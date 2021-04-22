const Patient = require('../models/patient');
const Booking = require('../models/booking');
const passport = require('passport');
const LocalStrategy = require("passport-local").Strategy;
const bcrypt = require('bcryptjs');
const Doctor = require('../models/doctor');
const Admin = require('../models/admin');
const User = require('../models/user');
const userhandler = require('../controller/usercontroller');



var patient=0, doctor=0, admin=0;

const customfields = {
    usernameField: 'email',
    passwordField: 'passwd',
}

var verify = async function(username, password, done) {
    Patient.findOne({emailID: username})
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

var search = async function(email, passwd, res, callback) {
    await Patient.findOne({emailID: email}, {emailID: 1, passwd: 1, _id: 1}, async function(err, result) {
        if (err) {
            res.status(400).json({error: 'Server error'});
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
}


var create = async function(data, res, callback) {

    await Patient.findOne({ emailID: data.email},function (err, rec) {
        if (rec) {
            res.status(400).json({error: "Email already registered"});
        }
        else if (err) {
            console.log(err);
            res.redirect('/');
        }
        else {
            bcrypt.hash(data.newpasswd, 5, async function (err, result) {
                var record = new Patient({
                    name: data.name,
                    mobile: data.mobile,
                    emailID: data.email,
                    passwd: result,
                });
        
                await record.save().then(async function() {
                    if (record.isNew === false) {
                        await Patient.findOne({ emailID: data.email}, function (err, doc) {
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
    await Patient.findOne({_id: id}, {passwd: 0}, async function(err, result) {
        if (err) {
            //console.log(err);
            res.status(400).json({error: 'Server error in extract function'});
        }
        else if(result){
            callback(result);
        }
    });
}

var extractall = async function(callback) {
    await Patient
    .find(async function(err, result) {
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
    //console.log(fields);
    if(fields.passwd == '') {
        let doc = await Patient.findOneAndUpdate(
            {_id: id },
            { name: fields.patient, mobile: fields.mobile, emailID: fields.email, address: fields.address },
            { new: true }
        );
        //console.log(doc);
    }
    else {
        bcrypt.hash(fields.passwd, 5, async function(err, result) {
            if(err) {
                console.log("Error while updating with password");
            }
            else {
                let doc = Patient.findOneAndUpdate(
                    {_id: id},
                    { name: fields.patient, mobile: fields.mobile, emailID: fields.email, passwd: result, address: fields.address  },
                    { new: true}
                );
                //console.log(doc);
            }
        });
    }
    callback();
}

var deletebookingp = async function(id, res) {
    Booking.findOneAndRemove({patientid: id}, async function(err, result) {
        if(err) {
            console.log("Error from remove patient booking " + String(err));
        }
        else if(result) {
            console.log("Patient booking removed");
            res.redirect("/");
        }
        else {
            res.redirect("/");
        } 
    });
}

var deletepatient = async function(id, res) {
    Patient.findOneAndRemove({_id: id}, async function(err, result) {
        if(err) {
            console.log(err);
        }
        else if(result) {
            //console.log(result);
            deletebookingp(id, res);
        }
    });
    User.findOneAndRemove({uid: id});
}

const strategy = new LocalStrategy(customfields, verify);

passport.use("local-plogin", strategy);

passport.serializeUser(function(user, done) {
    done(null, user._id);
});

passport.deserializeUser(function(userID, done) {
        User.findOne({uid: userID})
            .then(function(user) {
                done(null, user);
            })
            .catch(function(err) {
                done(null, false);
            });
});

module.exports = {
    search: search,
    create: create,
    extract: extract,
    extractall: extractall,
    update: update,
    deletepatient: deletepatient,
};
