const Admin = require('../models/admin');
const bcrypt = require('bcryptjs');
const userhandler = require("../controller/usercontroller");
const User = require("../models/user");
const LocalStrategy = require("passport-local").Strategy;
const passport = require('passport');



var search = async function(email, passwd, res, callback) {
    await Admin.findOne({emailID: email}, {emailID: 1, passwd: 1, _id: 1}, async function(err, result) {
        if (err) {
            console.log("idhar");
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
    });
};

var create = async function(data, res, callback) {

    await Admin.findOne({ emailID: data.email},async function (err, rec) {
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
                var record = new Admin({
                    name: data.name,
                    emailID: data.email,
                    passwd: result,
                });
        
                await record.save().then(async function() {
                    if (record.isNew === false) {
                        await Admin.findOne({ emailID: data.email}, function (err, doc) {
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
    await Admin.findOne({_id: id}, {passwd: 0}, async function(err, result) {
        if (err) {
            res.status(400).json({error: 'Server error'});
        }
        else if(result){
            callback(result);
        }
    });
}

var deleteadmin = async function(id, res) {
    Admin.findOneAndRemove({_id: id}, async function(err, result) {
        if(err) {
            console.log(err);
        }
        else if(result) {
            User.findOneAndRemove({uid: id});
            console.log("Admin removed");
            res.redirect("/");
        }
    });
}

const customfields = {
    usernameField: 'email',
    passwordField: 'passwd',
}

var verifya = async function(username, password, done) {
    Admin.findOne({emailID: username})
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

const strategya = new LocalStrategy(customfields, verifya);

passport.use("local-alogin", strategya);

module.exports = {
    search: search,
    create: create,
    extract: extract,
    deleteadmin: deleteadmin,
};