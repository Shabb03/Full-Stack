var express = require('express');
var router = express.Router();

router.get('/', function(req, res, next) {
  res.render('index', { title: 'Sidhur2\'s Fitness Shop' });
});

router.get('/login', function(req, res, next){
  res.render('login', { title: 'Sidhur2\'s Fitness Shop' });
});

router.get('/cart', function(req, res, next){
  res.render('cart', { title: 'Sidhur2\'s Fitness Shop' });
});

router.get('/checkout', function(req, res, next){
  res.render('checkout', { title: 'Sidhur2\'s Fitness Shop' });
});

router.get('/home', function(req, res, next){
  res.render('home', { title: 'Sidhur2\'s Fitness Shop' });
});

router.get('/order', function(req, res, next){
  res.render('order', { title: 'Sidhur2\'s Fitness Shop' });
});

router.get('/productindividual', function(req, res, next){
  res.render('productindividual', { title: 'Sidhur2\'s Fitness Shop' })
});

router.get('/register', function(req, res, next){
  res.render('register', { title: 'Sidhur2\'s Fitness Shop' })
});

module.exports = router;
