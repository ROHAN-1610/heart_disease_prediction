// JavaScript for Doctor Dashboard

// Log Out button functionality
document.getElementById("logoutBtn").addEventListener("click", function () {
    // Redirect to the logout URL
    window.location.href = "{% url 'logout' %}";
});
