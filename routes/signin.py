from fastapi import APIRouter, Request, HTTPException, Cookie, Form, Query, BackgroundTasks
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from routes.jwt import create_access_token, get_user_by_cookie
from database.database import user_data, payment_due, get_user_by_email, payment_history, get_membership_plan, offline_payments
from bson import ObjectId
from passlib.context import CryptContext
from datetime import datetime, timedelta
import random
from email.utils import formataddr
import smtplib
from email.mime.text import MIMEText
import razorpay
from dateutil.parser import parse as parse_datetime
from typing import Optional



signin_router = APIRouter()
templates = Jinja2Templates(directory="template")
pwd_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")


otp_storage = {}  # { email: { 'otp': '123456', 'expires': datetime }}



client = razorpay.Client(auth=("rzp_test_pibrBAMVpfKNFN", "nzEjD1hevJTvRenH2oJzz1Gn"))

# ✅ Define safe parser
def safe_parse_date(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return parse_datetime(value)
        except Exception:
            return None
    return None

def calculate_next_due_date(payment_date: str) -> str:
    """Calculate next due date (payment date + 30 days)"""
    payment_dt = datetime.strptime(payment_date, "%Y-%m-%d")
    next_due = payment_dt + timedelta(days=30)
    return next_due.strftime("%Y-%m-%d")

def get_payment_cycle_range(date_str: str):
    """Returns current month and year to next month and year (e.g., August, 2025 → September, 2025)"""
    payment_dt = datetime.strptime(date_str, "%Y-%m-%d")

    current_month_first = payment_dt.replace(day=1)
    if payment_dt.month == 12:
        next_month_first = payment_dt.replace(year=payment_dt.year + 1, month=1, day=1)
    else:
        next_month_first = payment_dt.replace(month=payment_dt.month + 1, day=1)

    # Format to "Month, Year"
    cycle_start = current_month_first.strftime("%B, %Y")  # e.g., August, 2025
    cycle_end = next_month_first.strftime("%B, %Y")       # e.g., September, 2025

    return cycle_start, cycle_end

def send_approval_status_email(to_email: str, name: str, mobile: str, plan: str, status: str):
    sender_email = "rohithvaddepally4@gmail.com"
    sender_name = "The Gym By Johnson"
    sender_password = "majjjuadrgtxybqv"

    subject = f"Offline Payment {status.title()} - {plan} Plan"
    
    color = "green" if status == "approved" else "red"

    body = f"""
    <p>Hi {name},</p>
    <p>Your offline payment request for the <strong>{plan}</strong> plan has been 
    <b style="color:{color}; text-transform:uppercase;">{status}</b>.</p>
    <p><b>Mobile:</b> 8009884440 </p>
    <p>If you have any questions, feel free to contact us.</p>
    <br>
    <p>Thanks,<br><strong>{sender_name}</strong></p>
    """

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = formataddr((sender_name, sender_email))
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print(f"✅ Status email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")


def send_payment_status_email(receiver_email: str, customer_name: str, status: str):
    sender_email = "rohithvaddepally4@gmail.com"
    sender_name = "The Gym By Johnson"
    sender_password = "majjjuadrgtxybqv"  # Use app password, not actual Gmail password

    subject = f"Payment Reminder: {status.replace('_', ' ').title()}"
    body = f"""
    <p>Hi {customer_name},</p>
    <p>This is a friendly reminder from <strong>{sender_name}</strong>.</p>
    <p>Your payment status is: <b style="color:red;">{status.replace('_', ' ').upper()}</b>.</p>
    <p>Please make your payment as soon as possible to avoid service interruption.</p>
    <p>Thank you for being a valued member!</p>
    """

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = formataddr((sender_name, sender_email))
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"✅ Email sent to {receiver_email}")
    except Exception as e:
        print(f"❌ Failed to send to {receiver_email}: {e}")

def send_offline_request_email(receiver_email: str, user_email: str, plan: str, amount: int):
    sender_email = "rohithvaddepally4@gmail.com"
    sender_name = "The Gym By Johnson"
    sender_password = "majjjuadrgtxybqv"  # Use App Password

    subject = f"New Offline Payment Request: {plan} Plan"

    body = f"""
    <p>Dear Admin,</p>
    <p><strong>{user_email}</strong> has submitted an offline payment request.</p>
    <p><b>Plan:</b> {plan}<br>
    <b>Amount:</b> ₹{amount}<br>
    <b>Status:</b> <span style="color:orange;">PENDING</span></p>
    <p>Please verify and collect payment manually at the gym.</p>
    <hr>
    <p style="font-size: 12px; color: gray;">This is an automated notification from <strong>{sender_name}</strong>.</p>
    """

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = formataddr((sender_name, sender_email))
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"✅ Offline request email sent to {receiver_email}")
    except Exception as e:
        print(f"❌ Failed to send to {receiver_email}: {e}")


def send_email_otp(receiver_email: str, otp: str):
    sender_email = "rohithvaddepally4@gmail.com"
    sender_name = "The Gym By Johnson"
    sender_password = "majjjuadrgtxybqv"

    subject = "Your OTP for Password Reset"
    body = f"Your OTP to reset your password is: <b>{otp}</b>. It is valid for 10 minutes."

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = formataddr((sender_name, sender_email))
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())



@signin_router.get("/signin")
async def serve_signin_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@signin_router.get("/select-payment-method")
async def select_payment_method(request: Request, amount: int, plan: str):
    user = get_user_by_cookie(request)
    if user:
        return templates.TemplateResponse("select-payment-method.html", {
        "request": request,
        "amount": amount,
        "plan": plan
        })
    else:
        return RedirectResponse("/signin", status_code=303)

# async def serve_signin_page(request: Request):
   
#         return templates.TemplateResponse("select-payment-method.html", {"request": request})


@signin_router.post("/signin")
async def signin_user(request: Request):
    try:
        data = await request.json()
        mobile = data.get("mobile")
        password = data.get("password")
        captcha = data.get("captcha")
        captcha_gen = data.get("actualCaptcha")

        if not all([mobile, password, captcha]):
            raise HTTPException(status_code=400, detail="All fields are required")

        if captcha != captcha_gen:
            raise HTTPException(status_code=400, detail="Captcha not matched")

        user = user_data.find_one({"mobile": mobile})
        if not user or not pwd_hash.verify(password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({
            "sub": user["email"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }, expires_in=timedelta(minutes=40))

        response = JSONResponse(content={
            "message": "Login successful",
            "username": user["username"],
            "mobile": user["mobile"],
            "email": user["email"],
            "role": user["role"]
        })
        response.set_cookie(
            key="access_token",
            value=f"Bearer {token}",
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=40 * 60
        )
        return response

    except HTTPException as e:
        return JSONResponse(content={"detail": e.detail}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"detail": f"Server error: {str(e)}"}, status_code=500)



from datetime import datetime

@signin_router.get("/logout")
async def logout_via_get():
    response = RedirectResponse(url="/signin", status_code=302)
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,  # ⚠️ For localhost use False (only use True with HTTPS)
        samesite="Lax"
    )
    return response


@signin_router.get("/verify-token")
def verify_token(request: Request):
    try:
        user = get_user_by_cookie(request)
        return {"status": "valid", "email": user.get("email")}
    except HTTPException as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

@signin_router.get("/pro")
async def user_profile(request: Request):
    user = get_user_by_cookie(request)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    last_payment_str = user.get("last_payment_date")
    next_due_str = user.get("next_due_date")

    last_payment_date = safe_parse_date(last_payment_str)
    next_due_date = safe_parse_date(next_due_str)

    if last_payment_date and next_due_date:
        payment_cycle = f"{last_payment_date.strftime('%B %d, %Y')} → {next_due_date.strftime('%B %d, %Y')}"
    else:
        payment_cycle = "Monthly (30 days)"

    if next_due_date:
        days_until_due = (next_due_date - datetime.utcnow()).days

        if days_until_due < 0:
            payment_status = "overdue"

        elif days_until_due <= 7:
            payment_status = "due_soon"
            
        else:
            payment_status = "active"
    else:
        days_until_due = 0  # 👈 fallback to 0 instead of None
        payment_status = "inactive"


    cleaned_user = {
        "id": user.get("id"),
        "name": user.get("name", user.get("username")),
        "username": user.get("username"),
        "email": user.get("email"),
        "mobile": user.get("mobile"),
        "gender": user.get("gender", ""),
        "role": user.get("role"),
        "joining_date": user.get("joining_date"),
        "last_payment_date": last_payment_str,
        "next_due_date": next_due_str
    }

    # 🔍 Fetch the latest membership from payment_history
    latest_payment = payment_history.find_one(
        {"user_id": user["id"], "membership": {"$ne": "NA"}},
        sort=[("date", -1)]
    )
    membership_type = latest_payment.get("membership", "NA") if latest_payment else "NA"

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": cleaned_user,
        "payment_status": payment_status,
        "days_until_due": days_until_due,
        "payment_cycle": payment_cycle,
        "membership_type": membership_type
    })



@signin_router.post("/api/update-profile")
async def update_profile(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    mobile: str = Form(...),
    gender: str = Form(...),
    token: str = Cookie(default=None)
):
    user = get_user_by_cookie(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # 🛠️ Fetch the user collection and update fields
    update_fields = {
        # "name": name,
        "email": email,
        "mobile": mobile,
        "gender": gender,
        "updated_at": datetime.utcnow()
    }

    # ✂️ Make sure user cannot update joining_date if they are a regular user
    if user["role"] != "user" and "joining_date" in request.form():
        update_fields["joining_date"] = request.form().get("joining_date")

    # 🔁 Update in MongoDB
    result = user_data.update_one(
        {"id": user["id"]},
        {"$set": update_fields}
    )

    if result.modified_count > 0:
        return {"status": "success", "message": "Profile updated successfully"}
    else:
        return {"status": "info", "message": "No changes made"}



@signin_router.post("/api/update-payment")
async def update_payment(
    request: Request,
    payment_date: str = Form(...),
):
    """Update payment info using JWT from cookie"""
    user = get_user_by_cookie(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if user["role"] != "admin":
        return JSONResponse({"status": "error", "message": "Unauthorized"}, status_code=403)


    # Calculate next due date
    next_due = calculate_next_due_date(payment_date)

    # Calculate payment cycle range
    cycle_start, cycle_end = get_payment_cycle_range(payment_date)

    # Update user payment data
    user_data.update_one(
        {"id": user["id"]},
        {"$set": {
            "last_payment_date": payment_date,
            "next_due_date": next_due,
            "updated_at": datetime.now(),
            "payment_cycle": f"{cycle_start} to {cycle_end}"
        }}
    )

    payment_due.update_one(
        {"user_id": user["id"]},
        {"$set": {
            "last_payment": payment_date,
            "next_due": next_due,
            "status": "active",
            "updated_at": datetime.now(),
            "payment_cycle": f"{cycle_start} to {cycle_end}"
        }},
        upsert=True
    )

    return {
        "status": "success",
        "message": "Payment updated successfully",
        "next_due": next_due,
        "payment_cycle": f"{cycle_start} to {cycle_end}"
    }


@signin_router.get("/api/user-data")
async def get_user_data(request: Request):
    user = get_user_by_cookie(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payment_info = payment_due.find_one({"user_id": user["id"]}) or {}

    return {
        "user": {
            "id": user.get("id"),
            "name": user.get("name"),
            "username": user.get("username"),
            "email": user.get("email"),
            "mobile": user.get("mobile"),
            "gender": user.get("gender"),
            "role": user.get("role"),
            # "joining_date": user.get("joining_date"),
            "last_payment_date": user.get("last_payment_date"),
            "next_due_date": user.get("next_due_date"),
            "payment_info": user.get("payment_info")
        },
        "payment_info": {
            "joining_date": user.get("joining_date"),
            "status": payment_info.get("status", "-"),
            "next_due_date": payment_info.get("next_due", "-")
        }
    }



@signin_router.get("/users")
async def admin_dashboard(request: Request):
    user = get_user_by_cookie(request)
    if not user or user.get("role") != "admin":
        return JSONResponse(status_code=403, content={"status": "error", "detail": "Unauthorized"})
    
    return templates.TemplateResponse("admin.html", {"request": request})
@signin_router.get("/api/users")
async def api_get_users(request: Request, page: int = Query(1), limit: int = Query(5), search: str = ""):
    user = get_user_by_cookie(request)
    if not user or user.get("role") != "admin":
        return JSONResponse(status_code=403, content={"status": "error", "detail": "Unauthorized"})

    # Always exclude admin users
    base_filter = {"role": {"$ne": "admin"}}

    if search:
        user_ids_with_status = [
            p["user_id"] for p in payment_due.find(
                {"status": {"$regex": search, "$options": "i"}}, {"user_id": 1}
            )
        ]

        # Combine with search filters
        base_filter["$or"] = [
            {"id": {"$regex": search, "$options": "i"}},
            {"username": {"$regex": search, "$options": "i"}},
            {"id": {"$in": user_ids_with_status}}
        ]

    skip = (page - 1) * limit
    users_cursor = user_data.find(base_filter, {
        "_id": 0,
        "id": 1,
        "username": 1,
        "mobile": 1,
        "gender": 1,
        "joining_date": 1,
        "last_payment_date": 1,
        "next_due_date": 1
    }).skip(skip).limit(limit)

    users = list(users_cursor)

    for u in users:
        # Fix datetime fields
        if isinstance(u.get("joining_date"), datetime):
            u["joining_date"] = u["joining_date"].strftime("%Y-%m-%d")
        if isinstance(u.get("last_payment_date"), datetime):
            u["last_payment_date"] = u["last_payment_date"].strftime("%Y-%m-%d")
        if isinstance(u.get("next_due_date"), datetime):
            u["next_due_date"] = u["next_due_date"].strftime("%Y-%m-%d")

        # Add status
        payment = payment_due.find_one({"user_id": u["id"]}, {"_id": 0, "status": 1})
        u["status"] = payment["status"] if payment else "unknown"

        # Add membership
        latest_payment = payment_history.find_one(
            {"user_id": u["id"]},
            sort=[("next_due", -1)],
            projection={"membership": 1}
        )
        u["membership"] = latest_payment["membership"] if latest_payment and "membership" in latest_payment else "NA"

    total_users = user_data.count_documents(base_filter)
    total_pages = (total_users + limit - 1) // limit

    return JSONResponse(status_code=200, content={
        "status": "success",
        "users": users,
        "page": page,
        "total_pages": total_pages,
        "total_users": total_users  # ✅ now excludes admin
    })


#forgot-password
@signin_router.get("/forgot-password")
async def serve_forgot_password_page(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})

@signin_router.post("/forgot-password/send-otp")
async def send_otp(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    email = data.get("email")

    if not email:
        raise HTTPException(status_code=400, detail="Email required")

    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="Email not found in database")

    otp = f"{random.randint(100000, 999999)}"
    expiry = datetime.utcnow() + timedelta(minutes=10)

    otp_storage[email] = {"otp": otp, "expires": expiry}

    background_tasks.add_task(send_email_otp, email, otp)

    return JSONResponse({"message": "OTP sent to your email."})


@signin_router.post("/forgot-password/reset")
async def reset_password(request: Request):
    data = await request.json()
    email = data.get("email")
    otp = data.get("otp")
    new_password = data.get("password")

    # ✅ Check for empty fields
    if not email or not otp or not new_password:
        raise HTTPException(status_code=400, detail="All fields required")

    stored = otp_storage.get(email)
    if not stored or stored["otp"] != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    if stored["expires"] < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")


    hashed_pwd = pwd_hash.hash(new_password)
    user_data.update_one({"email": email}, {"$set": {"password": hashed_pwd}})
    del otp_storage[email]

    return JSONResponse(content={"message": "Password updated successfully"})


#smtp


#verify-otp
@signin_router.post("/verify-otp-reset")
async def verify_otp_reset(request: Request):
    data = await request.json()
    email = data.get("email")
    otp = data.get("otp")
    new_password = data.get("newPassword")

    if not all([email, otp, new_password]):
        raise HTTPException(status_code=400, detail="All fields are required")

    if email not in otp_storage:
        raise HTTPException(status_code=400, detail="OTP not requested for this email")

    stored = otp_storage[email]
    if stored["otp"] != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    if stored["expires"] < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP has expired")

    hashed_pwd = pwd_hash.hash(new_password)
    result = user_data.update_one({"email": email}, {"$set": {"password": hashed_pwd}})
    
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update password")

    del otp_storage[email]

    return JSONResponse({"message": "Password reset successful."})

#send_reminder_emails
@signin_router.post("/send_reminder_emails")
async def send_reminder_emails(
    request: Request,
    status_filter: str = Form(...)
):
    # ✅ Authenticate and authorize
    user = get_user_by_cookie(request)
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")

    # ✅ Find users by payment status (from `payment_due`)
    payment_users = payment_due.find({"status": status_filter})

    for record in payment_users:
        user_record = user_data.find_one({"id": record["user_id"]})
        if user_record:
            send_payment_status_email(
                receiver_email=user_record["email"],
                customer_name=user_record.get("name", user_record.get("username")),
                status=status_filter
            )

    # ✅ Confirm message via redirection
    return RedirectResponse(
        url=f"/users?status_filter={status_filter}&email_sent=true",
        status_code=302
    )

#create order

@signin_router.post("/create-order")
async def create_order(request: Request):
    user = get_user_by_cookie(request)
    if not user:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    body = await request.json()
    amount = body.get("amount")
    if not amount:
        return JSONResponse(status_code=400, content={"detail": "Amount required"})

    try:
        # Razorpay expects amount in paise
        razorpay_order = client.order.create({
            "amount": amount * 100,
            "currency": "INR",
            "payment_capture": 1
        })

        return {
            "order_id": razorpay_order["id"],
            "amount": razorpay_order["amount"]
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})


# verify payment
@signin_router.post("/verify-payment")
async def verify_payment(request: Request):
    user = get_user_by_cookie(request)
    if not user:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    data = await request.json()
    payment_id = data.get("razorpay_payment_id")
    amount = data.get("amount")

    try:
        payment = client.payment.fetch(payment_id)
        if payment["status"] != "captured":
            return JSONResponse(status_code=400, content={"detail": "Payment not captured"})

        timestamp = datetime.fromtimestamp(payment["created_at"])

        # 🟢 Get membership
        membership = get_membership_plan(amount)

        # 🟢 Update user last_payment_date
        user_data.update_one(
            {"id": user["id"]},
            {"$set": {"last_payment_date": timestamp}}
        )

        # 🟢 Update payment due
        next_due = timestamp + timedelta(days=30)
        payment_due.update_one(
            {"user_id": user["id"]},
            {
                "$set": {
                    "last_payment": timestamp.strftime("%Y-%m-%d"),
                    "next_due": next_due.strftime("%Y-%m-%d"),
                    "status": "active",
                    "membership": membership
                }
            }
        )

        # 🟢 Store in payment history
        payment_history.insert_one({
            "user_id": user["id"],
            "payment_id": payment_id,
            "amount": amount,
            "status": "paid",
            "date": timestamp,
            "method": "razorpay",
            "membership": membership,
            "remarks": "Plan Payment"
        })

        return JSONResponse(status_code=200, content={"message": "Payment successful"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})


@signin_router.post("/offline-payment-request")
async def offline_payment_request(request: Request, amount: int = Form(...)):
    user = get_user_by_cookie(request)
    if not user or "email" not in user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    email = user.get("email")
    user_id = user.get("user_id")  # 👈 Your custom user_id

    try:
        plan = get_membership_plan(amount)

        offline_payments.insert_one({
            "user_id": user_id,
            "email": email,
            "amount": amount,
            "plan": plan,
            "status": "pending",
            "requestedAt": datetime.utcnow()
        })

        send_offline_request_email(
            # receiver_email="Thegymbyjohnson@gmail.com",
            receiver_email="rohithvaddepally4@gmail.com",
            user_email=email,
            plan=plan,
            amount=amount
        )

        return JSONResponse(status_code=200, content={"message": "Offline request recorded."})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record request: {str(e)}")



# Admin HTML page
@signin_router.get("/offline-requests")
async def admin_offline_page(request: Request):
    user = get_user_by_cookie(request)
    if not user or user.get("role") != "admin":
        return JSONResponse(status_code=403, content={"detail": "Unauthorized"})
    return templates.TemplateResponse("offline_requests.html", {"request": request})


# API to get offline payment requests

@signin_router.get("/api/offline-requests")
async def get_offline_requests(
    request: Request,
    page: int = Query(1),
    limit: int = Query(5),
    search: str = "",
    status: str = ""
):
    user = get_user_by_cookie(request)
    if not user or user.get("role") != "admin":
        return JSONResponse(status_code=403, content={"status": "error", "detail": "Unauthorized"})

    query = {}
    if search:
        query["email"] = {"$regex": search, "$options": "i"}
    if status:
        query["status"] = status

    skip = (page - 1) * limit
    total = offline_payments.count_documents(query)
    results_cursor = offline_payments.find(query).skip(skip).limit(limit).sort("requestedAt", -1)

    requests = []
    for r in results_cursor:
        email = r.get("email")
        user_doc = user_data.find_one({"email": email})

        user_id = user_doc.get("id", "NA") if user_doc else "NA"
        mobile = user_doc.get("mobile", "NA") if user_doc else "NA"

        requests.append({
            "user_id": user_id,
            "email": email,
            "mobile": mobile,
            "amount": r.get("amount", 0),
            "plan": r.get("plan", "NA"),
            "status": r.get("status", "pending"),
            "requestedAt": r.get("requestedAt").strftime("%Y-%m-%d %H:%M") if r.get("requestedAt") else "N/A"
        })


    return JSONResponse(status_code=200, content={
        "status": "success",
        "requests": requests,
        "page": page,
        "total_pages": (total + limit - 1) // limit
    })


#approve request

@signin_router.post("/api/offline-requests/{user_id}/approve")
async def approve_offline_request(user_id: str, request: Request):
    db = request.app.database
    offline_requests = db["offline_payments"]
    users = db["Users"]

    # Find user
    user = await users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    email = user.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="User email not found")

    # Get latest pending offline request
    req_doc = await offline_requests.find_one(
        {"email": email, "status": "pending"},
        sort=[("requestedAt", -1)]
    )
    if not req_doc:
        raise HTTPException(status_code=404, detail="No pending request found")

    plan = req_doc.get("plan", "").lower()
    requested_at = req_doc.get("requestedAt")

    if not requested_at:
        raise HTTPException(status_code=400, detail="Missing requestedAt")

    if isinstance(requested_at, str):
        try:
            requested_at = safe_parse_date(requested_at)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid requestedAt format")

    # Set duration based on plan
    if plan == "basic":
        new_due_date = requested_at + timedelta(days=30)
    elif plan == "premium":
        new_due_date = requested_at + timedelta(days=7)
    elif plan == "pro":
        new_due_date = requested_at + timedelta(days=30)
    else:
        raise HTTPException(status_code=400, detail="Unknown membership plan")

    # Update offline request status
    await offline_requests.update_one(
        {"_id": req_doc["_id"]},
        {"$set": {"status": "approved", "resolved_at": datetime.utcnow()}}
    )

    # Update user data
    await users.update_one(
        {"id": user_id},
        {
            "$set": {
                "last_payment_date": requested_at,
                "next_due_date": new_due_date,
                "status": "active"
            }
        }
    )

    return {"status": "success", "message": f"User {user_id} approved successfully"}

#update request
@signin_router.post("/admin/offline-request/update")
async def update_offline_request(request: Request):
    admin_user = get_user_by_cookie(request)  # ✅ Confirm admin is logged in
    if not admin_user or admin_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")

    data = await request.json()
    user_id = data.get("user_id")
    action = data.get("action")

    if not user_id or not action:
        raise HTTPException(status_code=400, detail="Missing user_id or action")

    if action not in ["approve", "reject"]:
        raise HTTPException(status_code=400, detail="Invalid action")

    # ✅ Lookup the target user by ID
    target_user = user_data.find_one({"id": user_id})
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    if target_user.get("role") == "admin":
        raise HTTPException(status_code=400, detail="Cannot approve membership for admin")

    email = target_user.get("email")
    if not email:
        raise HTTPException(status_code=404, detail="User email not found")

    # ✅ Fetch the user's pending offline request
    offline_request = offline_payments.find_one(
        {"email": email, "status": "pending"},
        sort=[("requestedAt", -1)]
    )
    if not offline_request:
        raise HTTPException(status_code=404, detail="No pending request found for this user")

    amount = offline_request.get("amount")
    if not amount:
        raise HTTPException(status_code=400, detail="Request missing amount")

    if action == "approve":
        plan = get_membership_plan(amount)
        requested_at = offline_request.get("requestedAt")

        if not requested_at:
            raise HTTPException(status_code=400, detail="Missing requestedAt timestamp")

        if isinstance(requested_at, str):
            requested_at = safe_parse_date(requested_at)

        due_date = requested_at + timedelta(days=30)
        now = datetime.utcnow()

        # ✅ Step 1: Update offline payment record
        offline_payments.update_one(
            {"email": email, "status": "pending"},
            {"$set": {"status": "approved", "resolved_at": now}}
        )

        # ✅ Step 2: Update target user's user_data
        user_data.update_one(
            {"id": user_id},
            {
                "$set": {
                    "status": "active",
                    "last_payment_date": requested_at,
                    "next_due_date": due_date
                }
            }
        )

        # ✅ Step 3: Update or upsert payment_due
        payment_due.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "last_payment": requested_at,
                    "next_due": due_date,
                    "status": "active"
                }
            },
            upsert=True
        )

        # ✅ Step 4: Insert into payment_history only if not duplicate
        existing = payment_history.find_one({
            "user_id": user_id,
            "date": requested_at
        })
        if not existing:
            payment_history.insert_one({
                "user_id": user_id,
                "amount": amount,
                "membership": plan,
                "date": requested_at,
                "next_due": due_date,
                "status": "active"
            })

        # ✅ Step 5: Send email notification to user
        send_approval_status_email(
            to_email=email,
            name=target_user.get("username", "Member"),
            mobile=target_user.get("mobile", "NA"),
            plan=plan.capitalize(),
            status="approved"
        )


        return JSONResponse(content={"success": True, "message": "Approved successfully"})

    elif action == "reject":
        offline_payments.update_one(
            {"email": email, "status": "pending"},
            {"$set": {"status": "rejected"}}
        )

        # ✅ Send rejection email
        send_approval_status_email(
            to_email=email,
            name=target_user.get("username", "Member"),
            mobile=target_user.get("mobile", "NA"),
            plan=get_membership_plan(offline_request.get("amount", 0)).capitalize(),
            status="rejected"
        )

        return JSONResponse(content={"success": True, "message": "Rejected successfully"})