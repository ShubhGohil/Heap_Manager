const express = require("express");
const patienthandler = require("./controller/patientcontroller");
//const { update } = require("./controller/patientcontroller");
const doctorhandler = require("./controller/doctorcontroller");
const adminhandler = require("./controller/admincontroller");
const bookinghandler = require("./controller/bookingcontroller");
const schedulehandler = require("./controller/schedulecontroller");
const passport = require("passport");
const session = require("express-session");
const mongoose = require("mongoose");
const authhandler = require("./controller/authMiddleware"); 
mongoose.Promise = global.Promise;

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

 app.use(function(req, res, next) {
    console.log(req.session);
    console.log(req.user);
    next();
});

app.listen(3000);
var urlpatient, urldoctor, urladmin;

app.get("/", function (req, res) {
  res.render("login");
});

app.post("/loginpatient", passport.authenticate("local-plogin"), function(req, res) {
            console.log("hre");
            if(req.user) {
                console.log("ljghfdgs");
                urlpatient = '/profile/patient.' + String(req.user._id);
                res.redirect('/profile/patient.' + String(req.user._id));
            }
            else if(!req.user) {
                console.log("iasygc");
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

app.post("/loginadmin", passport.authenticate("local-alogin"), function(req, res) {
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
    else if (role === "Admin") {
        await adminhandler.create(req.body, res, function(response) {
            urladmin = '/profile/admin.' + String(response);
            res.redirect("/profile/admin." + String(response));
        });
    }
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
            info = response;
            res.render("adminprofile", {information: info, url: urladmin});
        });
    }
});

app
    .route("/profile/patient.:id/makebooking")
    .get(authhandler.isAuth, async function (req, res) {
        let records;
        await patienthandler.extract(req.params.id, res, async function(response) {
            records = response;
            await schedulehandler.get(async function(dn) {
                res.render("appointment_form", {information: records, url: urlpatient, doctorname: dn});
            }); 
        });
    })
    .post(async function (req, res) {

        await schedulehandler.make(req.body, req.params.id, res);
        res.redirect("/profile/patient." + String(req.params.id) + "/makebooking");    

    });

app.get("/profile/patient.:id/viewdoctors", authhandler.isAuth, async function(req, res) {
    await patienthandler.extract(req.params.id, res, async function(response) {
        records = response;
        await doctorhandler.extractall(async function(d) {
            //console.log(d);
            res.render("pviewdoctor", {information: records, url: urlpatient, doctor: d});
        }); 
    });
});

app.get("/profile/admin.:id/doctors", authhandler.isAuth, async function(req, res) {
    await adminhandler.extract(req.params.id, res, async function(response) {
        records = response;
        await doctorhandler.extractall(async function(d) {
            //console.log(d);
            res.render("dviewadmin", {information: records, url: urladmin, doctor: d});
        }); 
    });
});

app.get("/profile/admin.:id/patients", authhandler.isAuth, async function(req, res) {
    await adminhandler.extract(req.params.id, res, async function(response) {
        records = response;
        await patienthandler.extractall(async function(p) {
            //console.log(d);
            res.render("pviewadmin", {information: records, url: urladmin, patient: p});
        }); 
    });
});

app
    .route("/profile/patient.:id/updateprofile")
    .get(authhandler.isAuth, async function(req, res) {
        //console.log(req.params.id);
        await patienthandler.extract(req.params.id, res, async function(response) {
            //console.log(response);
            res.render("updatepatientprofile", {information: response, url: urlpatient}); 
        });
    })
    .post(async function(req, res) {
        await patienthandler.update(req.params.id, req.body, async function() {
            res.redirect("/profile/patient." + String(req.params.id) + "/updateprofile");
        });
    });

app
    .route("/profile/doctor.:id/updateprofile")
    .get( authhandler.isAuth, async function(req, res) {
        //console.log(req.params.id);
        await doctorhandler.extract(req.params.id, res, async function(response) {
            //console.log(response);
            res.render("updatedoctorprofile", {information: response, url: urldoctor}); 
        });
    })
    .post(async function(req, res) {
        await doctorhandler.update(req.params.id, req.body, async function() {
            res.redirect("/profile/doctor." + String(req.params.id) + "/updateprofile");
        });
    });

app.get("/profile/patient.:id/removepatientaccount/", authhandler.isAuth, async function (req, res) {
    req.logout();
    await patienthandler.deletepatient(req.params.id, res);
});

app.get("/profile/doctor.:id/removepatientaccount/", authhandler.isAuth, async function (req, res) {
    req.logout();
    await doctorhandler.deletedoctor(req.params.id, res);
});

app.get("/profile/admin.:id/removepatientaccount/", authhandler.isAuth, async function (req, res) {
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