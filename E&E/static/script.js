const passwordInput = document.getElementById("password");
const eyeIcon = document.getElementById("eyeIcon");



const multiStepForm = document.querySelector("[data-multi-step]")
//selecteaza tot din multistepform care are atributul data-step
//rezultatul este convertit intr-un array folosind operatorul spread [...], si apoi asignat variabilei

const formSteps = [...multiStepForm.querySelectorAll("[data-step]")]

//gaseste primul element din array ul form steps care are o clasa care contine "active"
//daca un element este gasit, ii ia atributul dataset.step, il transforma in int si asigneaza
let currentStep = formSteps.findIndex(step => {
  return step.classList.contains("active")
})



if (currentStep < 0) {
  currentStep = 0
  formSteps[currentStep].classList.add("active")
  showCurrentStep()
}


//dont forget to set required on all inputs
//adauga un click event listener la multistep , event object e ca parametru 
multiStepForm.addEventListener("click", e => {
  let incrementor
  if (e.target.matches("[data-next]")) {
    incrementor = 1
  }
  else if (e.target.matches("[data-previous]")) {
    incrementor = -1
  } if (incrementor == null) {return}

  const inputs = [...formSteps[currentStep].querySelectorAll("input")]
  const allValid = inputs.every(input => input.reportValidity())
  if (allValid){
    currentStep += incrementor
  showCurrentStep()
  }
})

formSteps.forEach(step => {
  step.addEventListener("animationend", e => {
    formSteps[currentStep].classList.remove("hide")
    console.log("here")
  e.target.classList.toggle("hide", !e.target.classList.contains("active"))
  })
})

//iterates over formsteps array, step is content and index is index of content in array
//toggles the css class active on the condition that index is equal to currentstep
function showCurrentStep() {
  formSteps.forEach((step, index) => {
    step.classList.toggle('active', index === currentStep)
    
  })
}


eyeIcon.addEventListener("click", togglePassword);


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


//validators
function check() {

  var input = document.getElementById("password").value
  input=input.trim(); //to remove all whitespace
  var hasUppercase = /[A-Z]/.test(input);
  var specialCharRegex = /[^a-zA-Z0-9]/;
  if (input.length >= 8){
    document.getElementById("req1").style.color = "green"
  }
  else{
    document.getElementById("req1").style.color = "red"
  }


  if (hasUppercase){
    document.getElementById("req2").style.color = "green"
  
  }

  else {
    document.getElementById("req2").style.color = "red"
  }

if (specialCharRegex.test(input)) {
  document.getElementById("req3").style.color = "green";

}
else{
  document.getElementById("req3").style.color = "red"
}

}

//my backend

function register() {
  var form = document.getElementById('registerForm');
  var formData = new FormData(form);

  fetch("/sign-up", {
    method: "POST",
    body: formData,
  })
  .then(response => {
    console.log("Full Response:", response);
    return response.json();
  })
  .then(data => {
    console.log("Data:", data);
    // Check for 'user_id' in the response JSON to determine if registration was successful
    if (data.user_id) {
      console.log("Registration successful, user_id:", data.user_id);
      // Redirect to the predict page
      window.location.href = 'http://127.0.0.1:5000/predict';
    } else {
      console.log("Registration failed:", data.message);
      // Handle registration failure
    }
  })
  .catch(error => {
    console.error("Error", error);
  });
};
