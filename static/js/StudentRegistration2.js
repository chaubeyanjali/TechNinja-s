document.getElementById('slide2Form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const pass = document.querySelectorAll('input[type="password"]')[0].value;
    const confirm = document.querySelectorAll('input[type="password"]')[1].value;

    if (pass !== confirm) {
        alert("Passwords do not match!");
        return;
    }

    alert("Success! Account created for EduSchedule Pro.");
    // Aap yahan login page par redirect kar sakte hain
});