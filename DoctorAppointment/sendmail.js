var node = require("nodemailer");

var transport = node.createTransport({
    service: 'gmail',
    auth: {
        user: 'sgohil0646@gmail.com',
        pass: 'shubhshakti@46',
    }
});

function sendmail(transport, receivermail, doctorname, date, time) {

    var mailOptions = {
        from: 'sgohil0646@gmail.com',
        to: receivermail,
        subject: "Booking confirmation",
        text: 'Your booking has been confirmed. Doctor: ' + doctorname + ', Date: ' + date + ', Time: ' + time
    }

    transport.sendMail(mailOptions, function(err, info) {
        if(err) {
            console.log(err);
        }
        else {
            console.log("Email sent" + info.response);
        }
    });
}

//sendmail(transport, 'gohilsb18.comp@coep.ac.in', "Avasthi", "20-4-2021", "3.00pm");

module.exports = {
    sendmail: sendmail,
    transport: transport,
}