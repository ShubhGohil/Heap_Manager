const mongoose = require("mongoose");

const FileSchema = mongoose.Schema({
    patientid: {type: mongoose.Schema.Types.ObjectId, required: true},
    filepath: {type: String, required: true},
}, {collection: "filemodel"});

const filemodel = mongoose.model("filemodel", FileSchema);

module.exports = filemodel;