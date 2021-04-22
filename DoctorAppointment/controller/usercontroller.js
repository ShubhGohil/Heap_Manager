const User = require("../models/user");

var createuser = function(id, passwd) {

    var record = new User({
        uid: id,
        passwd: passwd,
    });

    record.save();

}

module.exports = {
    createuser: createuser,
}