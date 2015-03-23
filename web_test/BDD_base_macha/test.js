(function(){
//parse url arguments
var query = {}
var url = location.href;
if (url.indexOf('?') != -1){
  var queryString = url.split('?')[1];
  var pairs = queryString.split('&');
  for (var i in pairs){
    var kvs = pairs[i].split('=');
    var key = decodeURIComponent(kvs[0]?kvs[0]:'');
    var value = decodeURIComponent(kvs[1]?kvs[1]:'');
    query[key] = value
  }
}

var mobile = query.mobile;
var sms_token = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'.split('').sort(function(){return Math.random()<0.5}).join('').slice(1,33);
var code = '';
var user_token = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'.split('').sort(function(){return Math.random()<0.5}).join('').slice(0,32);
var server_token = '';
var fake_server_token = 'fake';
var uid = '';
var fake_code = 'fake';
//all urls
var query_code_debug = '/debug.code.query';
var loginSMS = '/api.login.sms';
var loginUrl = '/api.login';
var loginCheckUrl = '/api.login.check';
var logoutUrl = '/api.logout';
//define errors
errors = {
  'VerifyCodeInvalid':'40',
  'AuthExpire':'10',
  'PermissionDeny':'20',
}
//define postWithAuth function
var postWithAuth = function(url,data,fn){
  fn = arguments[arguments.length-1]
  if (typeof fn != 'function'){fn = function(){}};
  if (typeof data == 'function'){data = {}};
  if (!data.uid){data.uid = uid};
  if (!data.server_token){data.server_token = server_token};
  if (!data.user_token){data.user_token = user_token};
  $.post(url,data,fn,'json');
}

   describe('APTS', function(){
       describe('Account System', function(){
            it('test login sms with vaild mobile',function(done){
              $.post(loginSMS,{'mobile':mobile,'sms_token':sms_token},function(retval){
                retval.should.be.Object;
                retval.flag.should.equal('ok');
                $.get(query_code_debug,{'mobile':mobile},function(retval){
                  code=retval.match(/\d*\D*(\d*)/)[1];
                  done();
                },'text');
              },'json');
            });
            it('test login with fake code',function(done){
              $.post(loginUrl,{'mobile':mobile,'user_token':user_token,'code':fake_code},function(retval){
                retval.should.be.Object;
                retval.flag.should.equal('error');
                retval.code.should.equal(errors['VerifyCodeInvalid']);
                done();
              },'json');
            });
            it('login with valid code',function(done){
              $.post(loginUrl,{'mobile':mobile,'user_token':user_token,'code':code},function(retval){
                retval.should.be.Object;
                retval.flag.should.equal('ok');
                var data = retval.data;
                data._id.should.be.String;
                data.server_token.should.be.String;
                uid = data._id;
                server_token = data.server_token;
                done();
              },'json');
            });
            it('not login yet check login',function(done){
              $.post(loginCheckUrl,{},function(retval){
                retval.should.be.Object;
                retval.flag.should.equal('error');
                retval.code.should.equal(errors['AuthExpire']);
                done();
              },'json');
            });
            it('check login with fake server_token',function(done){
              postWithAuth(loginCheckUrl,{'server_token':fake_server_token},function(retval){
                retval.should.be.Object;
                retval.flag.should.equal('error');
                retval.code.should.equal(errors['AuthExpire']);
                done();
              });
            });
            it('check login after login',function(done){
              postWithAuth(loginCheckUrl,function(retval){
                retval.should.be.Object;
                retval.flag.should.equal('ok');
                done();
              });
            });
            it('logout after login',function(done){
              postWithAuth(logoutUrl,function(retval){
                retval.should.be.Object;
                retval.flag.should.equal('ok');
                done();
              });
            });
            it('logout before login',function(done){
              postWithAuth(logoutUrl,function(retval){
                retval.should.be.Object;
                retval.code.should.equal(errors['AuthExpire']);
                done();
              });
            });
       });
       describe('Shopping System', function(){
            it('test',function(done){done()});
       });
       describe('Others api', function(){
            it('test',function(done){done()});
       });
   });
})();