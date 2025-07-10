// register service worker after load
window.addEventListener('load', () => {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
      .then(reg => console.log('SW registered:', reg))
      .catch(err => console.error('SW registration failed:', err));
  }
});


document.addEventListener('DOMContentLoaded', function () {
    // Event listener for the "Join Now" button of the Basic Plan
    document.getElementById('joinbtn16').addEventListener('click', () => {
        const amount = '1370.62';  // Amount for Basic Plan
        const orderId = 'gym16';  // Unique order ID for Basic Plan

        // Send a request to the backend to create the Paytm payment
        fetch('/create-paytm-payment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ amount: amount, orderId: orderId })  // Sending amount and orderId to backend
        })
        .then(response => response.json())
        .then(data => {
            // Ensure the backend returned the necessary parameters
            if (data.orderId && data.amount && data.checksum) {
                const paymentParams = {
                    "MID": "your-merchant-id",  // Replace with your actual Paytm merchant ID
                    "ORDER_ID": data.orderId,    // The order ID generated server-side
                    "CUST_ID": "customer123",    // Unique customer ID
                    "INDUSTRY_TYPE_ID": "Retail", // Industry type
                    "CHANNEL_ID": "WEB",         // Payment channel
                    "TXN_AMOUNT": data.amount,   // Amount to be paid
                    "WEBSITE": "WEBSTAGING",     // Paytm website, use "WEBSTAGING" for sandbox testing
                    "CALLBACK_URL": "http://localhost:8000/payment-callback",  // Callback URL for payment result
                    "EMAIL": "customer@example.com", // Customer email
                    "MOBILE_NO": "9999999999"    // Customer mobile number
                };

                // Initialize Paytm Checkout JS
                Paytm.CheckoutJS.init(paymentParams).then(function onSuccess() {
                    console.log('Payment initiation successful!');
                    Paytm.CheckoutJS.invoke(); // Open Paytm payment interface
                }).catch(function onError(error) {
                    console.log('Payment initiation failed', error);
                });
            } else {
                console.error("Payment data missing or invalid.");
            }
        })
        .catch(error => {
            console.error('Error initiating payment:', error);
        });
    });

    // Event listener for the "Join Now" button of the Weekly Plan
    document.getElementById('joinbtn25').addEventListener('click', () => {
        const amount = '2141.79';  // Amount for Weekly Plan
        const orderId = 'gym25';  // Unique order ID for Weekly Plan

        // Send a request to the backend to create the Paytm payment
        fetch('/create-paytm-payment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ amount: amount, orderId: orderId })  // Sending amount and orderId to backend
        })
        .then(response => response.json())
        .then(data => {
            // Ensure the backend returned the necessary parameters
            if (data.orderId && data.amount && data.checksum) {
                const paymentParams = {
                    "MID": "your-merchant-id",  // Replace with your actual Paytm merchant ID
                    "ORDER_ID": data.orderId,    // The order ID generated server-side
                    "CUST_ID": "customer123",    // Unique customer ID
                    "INDUSTRY_TYPE_ID": "Retail", // Industry type
                    "CHANNEL_ID": "WEB",         // Payment channel
                    "TXN_AMOUNT": data.amount,   // Amount to be paid
                    "WEBSITE": "WEBSTAGING",     // Paytm website, use "WEBSTAGING" for sandbox testing
                    "CALLBACK_URL": "http://localhost:8000/payment-callback",  // Callback URL for payment result
                    "EMAIL": "customer@example.com", // Customer email
                    "MOBILE_NO": "9999999999"    // Customer mobile number
                };

                // Initialize Paytm Checkout JS
                Paytm.CheckoutJS.init(paymentParams).then(function onSuccess() {
                    console.log('Payment initiation successful!');
                    Paytm.CheckoutJS.invoke(); // Open Paytm payment interface
                }).catch(function onError(error) {
                    console.log('Payment initiation failed', error);
                });
            } else {
                console.error("Payment data missing or invalid.");
            }
        })
        .catch(error => {
            console.error('Error initiating payment:', error);
        });
    });

    // Event listener for the "Join Now" button of the Monthly Plan
    document.getElementById('joinbtn45').addEventListener('click', () => {
        const amount = '3855.22';  // Amount for Monthly Plan
        const orderId = 'gym45';  // Unique order ID for Monthly Plan

        // Send a request to the backend to create the Paytm payment
        fetch('/create-paytm-payment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ amount: amount, orderId: orderId })  // Sending amount and orderId to backend
        })
        .then(response => response.json())
        .then(data => {
            // Ensure the backend returned the necessary parameters
            if (data.orderId && data.amount && data.checksum) {
                const paymentParams = {
                    "MID": "your-merchant-id",  // Replace with your actual Paytm merchant ID
                    "ORDER_ID": data.orderId,    // The order ID generated server-side
                    "CUST_ID": "customer123",    // Unique customer ID
                    "INDUSTRY_TYPE_ID": "Retail", // Industry type
                    "CHANNEL_ID": "WEB",         // Payment channel
                    "TXN_AMOUNT": data.amount,   // Amount to be paid
                    "WEBSITE": "WEBSTAGING",     // Paytm website, use "WEBSTAGING" for sandbox testing
                    "CALLBACK_URL": "http://localhost:8000/payment-callback",  // Callback URL for payment result
                    "EMAIL": "customer@example.com", // Customer email
                    "MOBILE_NO": "9999999999"    // Customer mobile number
                };

                // Initialize Paytm Checkout JS
                Paytm.CheckoutJS.init(paymentParams).then(function onSuccess() {
                    console.log('Payment initiation successful!');
                    Paytm.CheckoutJS.invoke(); // Open Paytm payment interface
                }).catch(function onError(error) {
                    console.log('Payment initiation failed', error);
                });
            } else {
                console.error("Payment data missing or invalid.");
            }
        })
        .catch(error => {
            console.error('Error initiating payment:', error);
        });
    });
});
