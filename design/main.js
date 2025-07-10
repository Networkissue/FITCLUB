
// register service worker after load
// window.addEventListener('load', () => {
//   if ('serviceWorker' in navigator) {
//     navigator.serviceWorker.register('/sw.js')
//       .then(reg => console.log('SW registered:', reg))
//       .catch(err => console.error('SW registration failed:', err));
//   }
// });


// static/sw.js
// self.addEventListener('install', (event) => {
//   console.log('Service worker installed');
// });

// // static/sw.js
// self.addEventListener('activate', (event) => {
//   console.log('Service worker activated');
// });

let container = document.getElementById('container')

toggle = () => {
	container.classList.toggle('sign-in')
	container.classList.toggle('sign-up')
}

setTimeout(() => {
	container.classList.add('sign-in')
}, 200)


// signin 

function generateCaptcha() {
  const symbols = "!@#$%^&*";
  const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789" + symbols; 
  let captcha = '';

  for (let i = 0; i < 6; i++) {
    captcha += characters.charAt(Math.floor(Math.random() * characters.length));
  }

  // Instead of showing captcha in a div, put it inside the input
  document.getElementById("captchaInput").value = captcha;
}

// Generate CAPTCHA on page load inside the input
generateCaptcha();

// Generate new CAPTCHA inside input when button clicked
document.getElementById("generateCaptchaBtn").addEventListener("click", function () {
  generateCaptcha();
});



// signup
document.getElementById("signupBtn").addEventListener("click", async () => {
  const data = {
    username: document.getElementById("signupUsername").value,
    email: document.getElementById("signupEmail").value,
    mobile: document.getElementById("signupMobile").value,
    gender: document.getElementById("gender").value,
  };

  try {
    const res = await fetch("http://localhost:8000/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const result = await res.json(); // Always try to parse JSON

    if (res.ok) {
      showSnackbar("Signup successful ✅! Redirecting to Sign In...", "green");
      document.getElementById("container").classList.remove("sign-up");
      document.getElementById("container").classList.add("sign-in");
    } else {
      // Display detailed error message from backend
      showSnackbar(" " + (result.detail || "Unknown error"), "red");
    }

  } catch (err) {
    console.error("Network or unexpected error:", err);
    showSnackbar("❗ An unexpected error occurred. Please try again later.", "red");
  }
});


function showSnackbar(message, type = "success") {
  const snackbar = document.getElementById("snackbar");
  const messageEl = document.getElementById("snackbar-message");
  const iconEl = document.querySelector(".snackbar-icon");

  type = type.toLowerCase(); // normalize

  // Set background color based on type
  if (type === "error" || type === "red") {
    snackbar.style.backgroundColor = "#d32f2f"; // red
  } else {
    snackbar.style.backgroundColor = "#4caf50"; // green
  }

  // Don't set iconEl.textContent since it's now styled via CSS
  messageEl.textContent = message;

  snackbar.classList.remove("hide");
  snackbar.classList.add("show");
  snackbar.style.visibility = "visible";

  // Auto-hide after 3 seconds
  setTimeout(() => {
    snackbar.classList.remove("show");
    snackbar.classList.add("hide");
    setTimeout(() => {
      snackbar.style.visibility = "hidden";
    }, 500); // match transition duration
  }, 3000);
}
