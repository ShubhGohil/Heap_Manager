module.exports.isAuth = function(req, res, next) {
    if(req.isAuthenticated()) {
        next();
    }
    else {
        res.status(400).send("<ul><li><h3>You are not authorized to access the page.</h3></li><li>If you are directed here after register please login.</li></ul>");
    }
}