const mongoose = require('mongoose');

const ScheduleSchema = new mongoose.Schema({
    doctorid: {type: mongoose.Schema.Types.ObjectId, ref: "doctormodel", required: true},
    date: {type: String, required: true},
    timeslot: [{type: String, required: true}],
}, {collection: 'schedulemodel'});
ScheduleSchema.index({ doctorid: 1, date: 1 }, { unique: true });

const schedulemodel = mongoose.model('schedulemodel', ScheduleSchema);

module.exports = schedulemodel;