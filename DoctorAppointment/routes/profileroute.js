const express = require('express');
let router = express.Router();

router.get('/', async function(req, res) {
    console.log(req.params);
});
    
module.exports = router;