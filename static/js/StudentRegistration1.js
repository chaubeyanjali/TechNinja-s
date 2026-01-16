function nextSlide() {
    // Hide Slide 1, Show Slide 2
    document.getElementById('slide1').style.display = 'none';
    document.getElementById('slide2').style.display = 'block';
    
    // Update Text
    document.getElementById('form-subtitle').innerText = 'Create your login credentials';
    
    // Update Progress Dots
    document.getElementById('step1-dot').classList.remove('active');
    document.getElementById('step2-dot').classList.add('active');
}

function prevSlide() {
    // Hide Slide 2, Show Slide 1
    document.getElementById('slide2').style.display = 'none';
    document.getElementById('slide1').style.display = 'block';
    
    // Reset Text
    document.getElementById('form-subtitle').innerText = 'Fill in your details below';
    
    // Update Progress Dots
    document.getElementById('step2-dot').classList.remove('active');
    document.getElementById('step1-dot').classList.add('active');
}

// Form Submission handling
document.getElementById('multiStepForm').addEventListener('submit', function(e) {
    e.preventDefault();
    alert("Account created successfully!");
});