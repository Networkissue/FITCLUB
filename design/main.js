(async () => {  

  document.addEventListener("DOMContentLoaded", async () => {

    // ✅ SIGNUP handler -------------------------------------------
    const signupBtn = document.getElementById("signupBtn");
    if (!signupBtn) {
        console.error("❌ signupBtn NOT FOUND");
    } else {
        signupBtn.addEventListener("click", async () => {
          const username = document.getElementById("signupUsername")?.value.trim();
          const email = document.getElementById("signupEmail")?.value.trim();
          const mobile = document.getElementById("signupMobile")?.value.trim();
          const gender = document.getElementById("gender")?.value;
          const password = document.getElementById("signupPassword")?.value.trim();  // Ensure password is captured
          const confirm_password = document.getElementById("signupConfirmPassword")?.value.trim();  // Ensure confirm_password is captured

          // Log the values to confirm they're being captured
          console.log("Password:", password);  
          console.log("Confirm Password:", confirm_password);

          const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

          const data = { username, email, mobile, gender, password, confirm_password };


          console.log("Sending signup data:", data);

          console.log({
            username,
            email,
            mobile,
            gender,
            password,
            confirm_password
          });

          try {
              const res = await fetch("/signup", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify(data),
              });

              const result = await res.json();

              if (res.ok) {
                  showSnackbar(result.message, "success", "left");
                  setTimeout(() => {
                      toggle();
                      generateCaptcha();
                  }, 1000);
              } else {
                  showSnackbar(result.detail || result.message || "Signup failed", "error", "left");
              }
          } catch (err) {
              console.error("❌ Signup error:", err);
              showSnackbar("Internal error during signup", "error", "left");
          }
      });
    }


    const container = document.getElementById('container');
    if (!container) {
      console.error("❌ Container element not found.");
      return;
    }

    function toggle() {
      container.classList.toggle('sign-in');
      container.classList.toggle('sign-up');
    }
    window.toggle = toggle;

    setTimeout(() => {
      container.classList.add('sign-in');
    }, 200);

    function generateCaptcha() {
      const symbols = "!@#$%^&*";
      const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789" + symbols;
      let captcha = '';
      for (let i = 0; i < 6; i++) {
        captcha += characters.charAt(Math.floor(Math.random() * characters.length));
      }
      document.getElementById("captchaInput").value = captcha;
    }

    generateCaptcha();
    const generateCaptchaBtn = document.getElementById("generateCaptchaBtn");
    if (generateCaptchaBtn) {
      generateCaptchaBtn.addEventListener("click", generateCaptcha);
    } else {
      console.error("❌ generateCaptchaBtn not found");
    }

    // ✅ SIGNIN handler
    const signinBtn = document.getElementById("signinBtn");
    if (!signinBtn) {
      console.error("❌ signinBtn NOT FOUND");
    }else {
      signinBtn.addEventListener("click", async () => {
        const mobile = document.getElementById("signinMobile")?.value.trim();
        const password = document.getElementById("signinPassword")?.value.trim();
        const enteredCaptcha = document.getElementById("captchaValue")?.value.trim();
        const actualCaptcha = document.getElementById("captchaInput")?.value.trim();
    
        console.log({ mobile, password, enteredCaptcha, actualCaptcha }); // ✅ Debug log
    
        if (!mobile || !password || !enteredCaptcha) {
          showSnackbar("All fields are required", "error", "right");
          return;
        }
    
        if (enteredCaptcha !== actualCaptcha) {
          showSnackbar("CAPTCHA does not match", "error", "right");
          return;
        }
    
        try {
          const res = await fetch("/signin", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mobile, password, actualCaptcha, captcha: enteredCaptcha }),
            credentials: "include"
          });
    
          const result = await res.json();
    
          if (res.ok) {
            const { username, email, role, mobile } = result;

            // Store user info in session storage
            sessionStorage.setItem("Username", username || "");
            sessionStorage.setItem("Email", email || "");
            sessionStorage.setItem("Role", role || "");
            sessionStorage.setItem("Mobile", mobile || "");

            // Show success snackbar
            showSnackbar("✅ Login successful", "success", "right");

            // Redirect based on role after short delay
            setTimeout(() => {
              const userRole = sessionStorage.getItem("Role");
              if (userRole === "user") {
                window.location.href = "/pro";
              } else if (userRole === "admin") {
                window.location.href = "/users";
              } else {
                showSnackbar("Unknown user role", "warning", "right");
              }
            }, 500);

          } else {
            // Show failure snackbar
            showSnackbar(result?.detail || "Signin failed", "error", "right");
          }
        } catch (err) {
          showSnackbar("Internal error", "error", "right");
        }
      });
    }

    
    
    

    // ✅ Snackbar utility
    let snackbarTimeout;
    function showSnackbar(message, type = "success", direction = "left") {
      const snackbar = document.getElementById("snackbar");
      const messageEl = document.getElementById("snackbar-message");
      const icon = document.getElementById("snackbar-icon");

      if (!snackbar || !messageEl || !icon) {
          console.error("Snackbar elements not found.");
          return;
      }

      snackbar.classList.remove("slide-left", "slide-right", "show", "hide");
      icon.classList.remove("error-icon");
      icon.style.display = "flex";

      const dirClass = direction === "right" ? "slide-right" : "slide-left";
      snackbar.classList.add(dirClass);

      if (type !== "success") {
          snackbar.style.backgroundColor = "#d32f2f";
          icon.classList.add("error-icon");
      } else {
          snackbar.style.backgroundColor = "#4caf50";
          icon.style.display = "none";
      }

      message = message.replace(/^[❌✅✖️✔️\u2716\u2714\s]+/, '');
      messageEl.textContent = message;

      requestAnimationFrame(() => {
          snackbar.classList.add("show");
      });

      if (snackbarTimeout) clearTimeout(snackbarTimeout);
      snackbarTimeout = setTimeout(() => {
          snackbar.classList.remove("show");
          snackbar.classList.add("hide");
      }, 2000);
    }

    document.querySelectorAll('.toggle-password').forEach(icon => {
      icon.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation(); // prevent parent click events
    
        const inputSelector = icon.getAttribute('toggle');
        const input = document.querySelector(inputSelector);
    
        if (input) {
          const isPassword = input.type === 'password';
          input.type = isPassword ? 'text' : 'password';
          icon.classList.toggle('bx-show', !isPassword);
          icon.classList.toggle('bx-hide', isPassword);
        }
      });
    });
  });


  sessionStorage.clear();

})(); // End of IIFE
