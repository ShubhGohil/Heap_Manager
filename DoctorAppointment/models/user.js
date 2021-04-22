var mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
    uid: {type: mongoose.Schema.Types.ObjectId, required: true},
    passwd: {type: String, required: true},
}, {collection: 'usermodel'});

const usermodel = mongoose.model('usermodel', UserSchema);

module.exports = usermodel;