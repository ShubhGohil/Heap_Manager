const passport = require("passport");
const LocalStrategy = require("passport-local").Strategy;
const Patient = require('./models/patient');
const bcrypt = require('bcryptjs');
const Doctor = require('./models/doctor');
const Admin = require('./models/admin');

const customfields = {
    usernameField: 'email',
    passwordField: 'passwd',
}

var verifyp = async function(username, password, done) {
    //console.log("hjvcy");
    //console.log(username);
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

var verifyd = async function(username, password, done) {
    //console.log("hjvcy");
    //console.log(username);
    Doctor.findOne({emailID: username})
        .then(function(result) {
            //console.log(result);
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

var verifya = async function(username, password, done) {
    //console.log("hjvcy");
    //console.log(username);
    Admin.findOne({emailID: username})
        .then(function(result) {
            //console.log(result);
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

const strategyp = new LocalStrategy(customfields, verifyp);
const strategyd = new LocalStrategy(customfields, verifyd);
const strategya = new LocalStrategy(customfields, verifya);

passport.serializeUser(function(user, done) {
    console.log(user.id);
    done(null, user._id);
});

passport.deserializeUser(function(userID, done) {
    Patient.findById(userID)
        .then(function(user) {
            done(null, user);
        })
        .catch(function(err) {
            done(err);
        });
});

module.exports = function(passport) {
    passport.use("local-plogin", strategyp);
    passport.use("local-dlogin", strategyd);
    passport.use("local-alogin", strategya);
}

