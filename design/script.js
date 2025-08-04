// Razorpay Payment Trigger Function
function payNow(packageName) {
  const packageDisplayNames = {
    BasicPackage: "Basic Plan - ₹900",
    PremiumPackage: "Premium Plan - ₹1500",
    ProPackage: "Pro Plan - ₹3500"
  };

  // Call FastAPI backend to create Razorpay order
  fetch("/create_order", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: `package_name=${encodeURIComponent(packageName)}`
  })
  .then(response => response.json())
  .then(data => {
    if (data.error) {
      alert("Error creating order: " + data.error);
      return;
    }

    const options = {
      key: "rzp_test_3o253LnINUbMOH", // Razorpay test key
      amount: data.amount,
      currency: data.currency,
      name: "FitClub Gym",
      description: packageDisplayNames[packageName] || "Fitness Package",
      order_id: data.id,
      handler: function (response) {
        alert("✅ Payment Successful!\nPayment ID: " + response.razorpay_payment_id);
        // Optional: send this response to your backend to confirm payment
      },
      theme: {
        color: "#000000"
      }
    };

    const rzp = new Razorpay(options);
    rzp.open();
  })
  .catch(error => {
    console.error("Payment error:", error);
    alert("Something went wrong while creating the payment.");
  });
}
