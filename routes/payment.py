from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import razorpay
import uuid

payment = APIRouter()

payment.mount("/staticfile", StaticFiles(directory="staticfile"), name="staticfile")
templates = Jinja2Templates(directory="template")

client = razorpay.Client(auth=("rzp_test_3o253LnINUbMOH", "nzEjD1hevJTvRenH2oJzz1Gn"))

packages = {
    "BasicPackage": 900,
    "PremiumPackage": 1500,
    "ProPackage": 3500
}

@payment.get("/{package_name}", response_class=HTMLResponse)
def package_page(request: Request, package_name: str):
    if package_name not in packages:
        return HTMLResponse(content="<h2>Package Not Found</h2>", status_code=404)
    return templates.TemplateResponse("payment.html", {"request": request, "package_name": package_name, "amount": packages[package_name]})

# @payment.post("/create_order")
# def create_order(package_name: str = Form(...)):
#     amount = packages.get(package_name)
#     if not amount:
#         return {"error": "Invalid package"}
#     order = client.order.create({
#         "amount": amount * 100,
#         "currency": "INR",
#         "receipt": str(uuid.uuid4()),
#         "payment_capture": 1
#     })
#     return order

