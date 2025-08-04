async function loadUsers() {
    try {
      const res = await fetch("/list/users", {
        credentials: "include" // Needed if you use cookies for auth
      });

      const data = await res.json();

      if (data.status === "success") {
        const users = data.users;
        const tbody = document.getElementById("userTableBody");
        tbody.innerHTML = ""; // Clear old rows

        users.forEach(user => {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td data-label="ID">${user.id}</td>
            <td data-label="Username">${user.username}</td>
            <td data-label="Mobile">${user.mobile}</td>
            <td data-label="Gender">${user.gender}</td>
            <td data-label="Joining Date">${user.joining_date}</td>
            <td data-label="Last Payment">${user.last_payment_date}</td>
            <td data-label="Next Due">${user.next_due_date}</td>
          `;
          tbody.appendChild(row);
        });
      } else {
        alert("❌ Failed to load users: " + data.message);
      }
    } catch (err) {
      console.error("Error loading users", err);
      alert("Server error while loading user list.");
    }
  }

  // Load users on page load if admin
  if (sessionStorage.getItem("Role") === "admin") {
    loadUsers();
  }