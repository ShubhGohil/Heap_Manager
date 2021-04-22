var mongoose = require('mongoose');

const AdminSchema = new mongoose.Schema({
    name: {type: String, required: true},
    emailID: {type: String, required: true, unique:true},
    passwd: {type: String, required: true},
}, {collection: 'adminmodel'});

const adminmodel = mongoose.model('adminmodel', AdminSchema);

module.exports = adminmodel;