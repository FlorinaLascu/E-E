const passwordInput = document.getElementById("pass");
const eyeIcon = document.getElementById("eyeIcon");

// Function to toggle password visibility
function togglePassword() {
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    eyeIcon.classList.remove("fa-eye");
    eyeIcon.classList.add("fa-eye-slash");
  } else {
    passwordInput.type = "password";
    eyeIcon.classList.remove("fa-eye-slash");
    eyeIcon.classList.add("fa-eye");
  }
}

// Attach the togglePassword function to the click event of the eye icon
eyeIcon.addEventListener("click", togglePassword);


function check() {

  var input = document.getElementById("pass").value
  input=input.trim(); //to remove all whitespace
  var hasUppercase = /[A-Z]/.test(input);
  var specialCharRegex = /[^a-zA-Z0-9]/;
  if (input.length >= 8){
    document.getElementById("req1").style.color = "green"
  }
  if (hasUppercase){
    document.getElementById("req2").style.color = "green"
  
  }

if (specialCharRegex.test(input)) {
  document.getElementById("req3").style.color = "green";

}
}