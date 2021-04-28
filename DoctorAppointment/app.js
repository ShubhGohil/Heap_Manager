const express = require("express");
const patienthandler = require("./controller/patientcontroller");
const doctorhandler = require("./controller/doctorcontroller");
const adminhandler = require("./controller/admincontroller");
const bookinghandler = require("./controller/bookingcontroller");
const schedulehandler = require("./controller/schedulecontroller");
const passport = require("passport");
const session = require("express-session");
const mongoose = require("mongoose");
const authhandler = require("./controller/authMiddleware"); 
mongoose.Promise = global.Promise;
const multer = require("multer");

mongoose.connect('mongodb://localhost:27017/trail', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    useCreateIndex: true,
    useFindAndModify: false,
});

mongoose.connection.once('open', function() {
    console.log('connection established');
}).on('error', function(error) {
    console.log('Connection error: ',  error);
});

const MongoStore = require("connect-mongo");
const { connect } = require("mongodb");

var app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));
app.set("view engine", "ejs");

const sessionStore = new MongoStore({
    mongoUrl: 'mongodb://localhost:27017/trail',
    collectionName: 'sessions',
});

app.use(session({
    secret: "keepitsafe",
    resave: false,
    saveUninitialized: true,
    store: sessionStore,
    cookie: {
        maxAge: 1000 * 60 * 60 * 24,
    }
}));

app.use(passport.initialize());
app.use(passport.session());

/*app.use(function(req, res, next) {
    console.log(req.session);
    console.log(req.user);
    next();
});*/

app.listen(3000);
var urlpatient, urldoctor, urladmin;

app.get("/", function (req, res) {
  res.render("login");
});


app.post("/loginpatient", passport.authenticate("local-plogin"), function(req, res) {
            
            if(req.user) {
                urlpatient = '/profile/patient.' + String(req.user._id);
                res.redirect('/profile/patient.' + String(req.user._id));
            }
            else if(!req.user) {
                res.redirect("/");
            }
});

app.post("/logindoctor", passport.authenticate("local-dlogin"), function(req, res) {
    if(req.user) {
        urldoctor = '/profile/doctor.' + String(req.user._id);
        res.redirect('/profile/doctor.' + String(req.user._id));
    }
    else if(!req.user) {
        res.redirect("/");
    }
});

app
.route("/loginadmin")
.get(function(req, res) {
    res.render("adminlogin");
})
.post(passport.authenticate("local-alogin"), function(req, res) {
    if(req.user) {
        urladmin = '/profile/admin.' + String(req.user._id);
        res.redirect('/profile/admin.' + String(req.user._id));
    }
    else if(!req.user) {
        res.redirect("/");
    }
});

app.post("/register", async function (req, res) {
    var role = req.body.role;
    if (role === "Patient") {
        await patienthandler.create(req.body, res, function(response) {
            urlpatient = '/profile/patient.' + String(response);
            res.redirect('/profile/patient.' + String(response));
        });
    } 
    else if (role === "Doctor") {
        await doctorhandler.create(req.body, res, function(response) {
            urldoctor = '/profile/doctor.' + String(response);
            res.redirect("/profile/doctor." + String(response));
        });
    } 
    /*else if (role === "Admin") {
        await adminhandler.create(req.body, res, function(response) {
            urladmin = '/profile/admin.' + String(response);
            res.redirect("/profile/admin." + String(response));
        });
    }*/
});

app.get("/profile/:role.:id", authhandler.isAuth, async function (req, res) {
    let info, bookinginfo;
    if(req.params.role === 'patient') {
        await patienthandler.extract(req.params.id, res, async function(response) {
            info = response;
            await bookinghandler.displaydbooking(req.params.id, async function(binfo) {
                res.render("patientprofile", {url: urlpatient, information: info, bookinginfo: binfo});
            });
        }); 
    }
    else if(req.params.role === 'doctor') {
        await doctorhandler.extract(req.params.id, res, async function(response) {
            info = response;
            await bookinghandler.displaypbooking(req.params.id, async function(binfo) {        
                bookinginfo = binfo;
                res.render("doctorprofile", {url: urldoctor, information: info, bookinginfo: bookinginfo});    
            });
        });
    }
    else if(req.params.role === 'admin') {
        await adminhandler.extract(req.params.id, res, function(response) {
            res.render("adminprofile", {information: response, url: urladmin});
        });
    }
});

app
    .route("/profile/patient.:id/makebooking/:status?")
    .get(authhandler.isAuth, async function (req, res) {
        let records;
        await patienthandler.extract(req.params.id, res, async function(response) {
            records = response;
            await schedulehandler.get(async function(dn) {
                if(req.params.status == undefined) {
                    res.render("appointment_form", {information: records, url: urlpatient, doctorname: dn, status: "2"});
                }
                else {
                    res.render("appointment_form", {information: records, url: urlpatient, doctorname: dn, status: req.params.status});
                }
            }); 
        });
    })
    .post(async function (req, res) {

        await schedulehandler.make(req.body, req.params.id, res);    

    });

app.get("/profile/patient.:id/viewdoctors", authhandler.isAuth, async function(req, res) {
    await patienthandler.extract(req.params.id, res, async function(response) {
        records = response;
        await doctorhandler.extractall(async function(d) {
            res.render("pviewdoctor", {information: records, url: urlpatient, doctor: d});
        }); 
    });
});

app
    .route("/profile/admin.:id/doctors")
    .get(authhandler.isAuth, async function(req, res) {
        await adminhandler.extract(req.params.id, res, async function(response) {
            records = response;
            await doctorhandler.extractall(async function(d) {
                res.render("aviewdoctor", {information: records, url: urladmin, doctor: d});
            }); 
        });
    })
    .post(authhandler.isAuth, async function(req, res) {
        await doctorhandler.deletedoctorfromadmin(req.body, res);
    });

app
    .route("/profile/admin.:id/patients")
    .get(authhandler.isAuth, async function(req, res) {
        await adminhandler.extract(req.params.id, res, async function(response) {
            records = response;
            await patienthandler.extractall(async function(p) {
                res.render("aviewpatient", {information: records, url: urladmin, patient: p});
            }); 
        });
    })
    .post(authhandler.isAuth, async function(req, res) {
        await patienthandler.deletepatientfromadmin(req.body, res);
    });

app
    .route("/profile/patient.:id/updateprofile/:status?")
    .get(authhandler.isAuth, async function(req, res) {
        await patienthandler.extract(req.params.id, res, async function(response) {
            if(req.params.status==undefined) {
                res.render("updatepatientprofile", {information: response, url: urlpatient, status: "2"});
            }
            else {
                res.render("updatepatientprofile", {information: response, url: urlpatient, status: req.params.status});
            } 
        });
    })
    .post(async function(req, res) {
        await patienthandler.update(req.params.id, req.body, res, async function() {
            res.redirect("/profile/patient." + String(req.params.id) + "/updateprofile/1");
        });
    });

app
    .route("/profile/patient.:id/cancelbooking")
    .get(authhandler.isAuth, async function(req, res) {
        await patienthandler.extract(req.params.id, res, async function(response) {
            info = response;
            await bookinghandler.displaydbooking(req.params.id, async function(binfo) {
                res.render("cancelbooking", {url: urlpatient, information: info, bookinginfo: binfo});
            });
        });
    })
    .post(async function(req, res) {
        await bookinghandler.deletebooking(req.params.id, req.body, async function() {
            res.redirect("/profile/patient." + String(req.params.id) + "/cancelbooking");
        });
    });

app
    .route("/profile/doctor.:id/updateprofile/:status?")
    .get( authhandler.isAuth, async function(req, res) {
        await doctorhandler.extract(req.params.id, res, async function(response) {
            if(req.params.status == undefined) {
                res.render("updatedoctorprofile", {information: response, url: urldoctor, status: "2"}); 
            }
            else {
                res.render("updatedoctorprofile", {information: response, url: urldoctor, status: req.params.status});
            }
        });
    })
    .post(async function(req, res) {
        await doctorhandler.update(req.params.id, req.body, res, async function() {
            res.redirect("/profile/doctor." + String(req.params.id) + "/updateprofile/1");
        });
    });

app
    .route("/profile/doctor.:id/setschedule")
    .get( authhandler.isAuth, async function(req, res) {
        await doctorhandler.extract(req.params.id, res, async function(response) {
            res.render("doctorsetschedule", {information: response, url: urldoctor}); 
        });
    })
    .post(async function(req, res) {
        await schedulehandler.addschedule(req.params.id, req, async function () {
            res.redirect("/profile/doctor."+ req.params.id +"/setschedule");
        });
    });

app.get("/profile/patient.:id/faq/", authhandler.isAuth, async function (req, res) {
    await patienthandler.extract(req.params.id, res, async function(response) {
        res.render("faq", {information: response, url: urlpatient});
    });
});

app.get("/profile/doctor.:id/faq/", authhandler.isAuth, async function (req, res) {
    await doctorhandler.extract(req.params.id, res, async function(response) {
        res.render("faq", {information: response, url: urldoctor});
    });
});

/*app
    .route("/profile/patient.:id/uploadfile")
    .get("/profile/patient.:id/uploadfile", authhandler.isAuth, async function(req, res) {
        await doctorhandler.extract(req.params.id, res, async function(response) {
            await filehandler.get(response, async function() {
                res.render("faq", {information: response, url: urlpatient});
            });
        }); 
    })*/
    
app.get("/profile/patient.:id/removepatientaccount/", authhandler.isAuth, async function (req, res) {
    req.logout();
    await patienthandler.deletepatient(req.params.id, res);
});

app.get("/profile/doctor.:id/removedoctoraccount/", authhandler.isAuth, async function (req, res) {
    req.logout();
    await doctorhandler.deletedoctor(req.params.id, res);
});

app.get("/profile/admin.:id/removeadminaccount/", authhandler.isAuth, async function (req, res) {
    req.logout();
    await adminhandler.deleteadmin(req.params.id, res);
});

app.get("/profile/patient.:id/logoutpatient/", authhandler.isAuth, async function (req, res) {
    req.logout();
    res.redirect("/");
});

app.get("/profile/doctor.:id/logoutdoctor/", authhandler.isAuth, async function (req, res) {
    req.logout();
    res.redirect("/");
});

app.get("/profile/admin.:id/logoutadmin/", authhandler.isAuth, async function (req, res) {
    req.logout();
    res.redirect("/");
});