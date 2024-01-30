
function delete_ex_db(deleteButtonElement, companyName, position) {
    // Prepare the payload with the company name and position
    var payload = {
        company: companyName,
        position: position,
        // Add user_id from the session if needed
        // user_id: userSessionId
    };

    // Send the DELETE request to the server
    fetch('/delete-experience', {  // Ensure this endpoint matches your server's API
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
        // Include credentials if your endpoint requires authentication
        credentials: 'same-origin'
    })
    .then(response => {
        // Check if the response was ok
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        // Optionally, remove the experience item from the DOM
        deleteItem(deleteButtonElement, 'experience-item', 'experience-list', 'title-experience');
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}








//array with skillz
//let skills = ["Python", "Java", "C++", "Javascript", "HTML & CSS", "Typescript", "Flask", "React"]

// function addSkill(){
//     options.innerHTML = ""
//     skills.forEach(skill => {
//         console.log(skill)
//         //this adds each skill inside li and inserts all li inside options tag
//         let li = <li onclick="updateName(this)">${skill}</li>;
//         options.insertAdjacentHTML("beforeend", li)
// });
// }

//addSkill()








function handleSquareClick(click_square, level) {
    // Add your logic here
    console.log('Square clicked!');
    document.querySelectorAll('.square').forEach(function(square){
        square.classList.remove('active');
    })
    click_square.classList.add('active');
    document.querySelector('.square-title').textContent = 'Level: ' + level;
    console.log('Square clicked:', level);
  }

  document.querySelectorAll('.square').forEach(function(square) {
    const level = square.getAttribute('data-level');
      square.addEventListener('click',function(){
        handleSquareClick(this, level)
      });
    });





function addWork(){

    var info = document.getElementById("add-experience-container")
    var button = document.getElementsByClassName("add-experience-button")

    for (var i = 0; i < button.length; i++) {
        var button = button[i];
        button.style.display = 'none'; // Add your CSS here
        // For example, to change the display property
    }

    info.style.display = 'inline-block'
    console.log(info)
}


function areAllFieldsCompleted() {
    // Get the form element by its ID
    var info = document.getElementById('add-experience-container');

    // Find all input elements within the form
    var inputs = info.getElementsByTagName('input');

    // Loop through the inputs and check if any are empty
    for (var i = 0; i < inputs.length; i++) {
        // If the input is empty, return false
        if (inputs[i].value.trim() === '') {
            return false;
        }
    }

    // If none of the inputs are empty, return true
    return true;
}



function areAllFieldsCompleted2() {
    // Get the form element by its ID
    var info = document.getElementById('add-education-form');

    // Find all input elements within the form
    var inputs = info.getElementsByTagName('input');

    // Loop through the inputs and check if any are empty
    for (var i = 0; i < inputs.length; i++) {
        // If the input is empty, return false
        if (inputs[i].value.trim() === '') {
            return false;
        }
    }

    // If none of the inputs are empty, return true
    return true;
}
function addExperienceItem() {
    var jobTitle = document.getElementById('jobTitle').value;
    var companyName = document.getElementById('companyName').value;
    var startYear = document.getElementById('startYear').value;
    var endYear = document.getElementById('endYear').value || 'Present';  // Default to 'Present' if endYear is empty

    // Create the new experience item
    var experienceItem = document.createElement('div');
    experienceItem.className = 'experience-item';
    var expDetails = `
        <div class="exp-details">
            <h4>${jobTitle} at ${companyName}</h4>
            <p>${startYear} - ${endYear}</p>
            <img src="./static/delete.png" class="delete" alt="Delete Icon">
        </div>
    `;
    experienceItem.innerHTML = expDetails;

    // Get the .experience-list container
    var experienceList = document.querySelector('.experience-list');

    // Assuming the .experience-list is always in the DOM, as per the new structure
    if (experienceList) {
        // Insert the new experience item at the top of the experience list
        experienceList.insertBefore(experienceItem, experienceList.firstChild);
    } else {
        console.error('The experience list does not exist in the DOM.');
        return;
    }

    // Clear the form fields
    document.getElementById('jobTitle').value = '';
    document.getElementById('companyName').value = '';
    document.getElementById('startYear').value = '';
    document.getElementById('endYear').value = '';
}



function addWorkExperience() {

    
    if (areAllFieldsCompleted()) {
        addExperienceItem()
        // ...
    } else {
        // Not all fields are completed, handle accordingly
        // Perhaps alert the user or highlight the empty fields
        alert('Please complete all fields before saving.');
    }
}
 
function showEducationForm(){
    var button = document.getElementsByClassName("add-education-button")
    var container = document.getElementById("add-education-form")

    for (var i = 0; i < button.length; i++) {
        var button = button[i];
        button.style.display = 'none'; // Add your CSS here
        // For example, to change the display property

    }

    container.style.display="inline-block"
}



function addEducationItem() {


    // Get values from the inputs within the add-education-form container
    var container = document.getElementById('add-education-form');
    var institutionName = container.querySelector('#institutionName').value;
    var degree = container.querySelector('#degree').value;
    var startYear = container.querySelector('#startYear').value;
    var endYear = container.querySelector('#endYear').value;

    // Default to 'Present' if endYear is empty
    

    // Create a new div element for the education item
    var educationItem = document.createElement('div');
    educationItem.className = 'education-items';

    // Create the HTML content for the new education item
    var eduDetails = `
        <p class="education-item">${institutionName}</p>
        <p class="education-item">${degree}</p>
        <p class="education-item">${startYear} - ${endYear}</p>
        <img src="./static/delete.png" class="delete" alt="Delete Icon">
    `;

    // Set the innerHTML of the educationItem div
    educationItem.innerHTML = eduDetails;

    // Append the new education item to the education-list
    var educationList = document.querySelector('.education-list');
    educationList.appendChild(educationItem);

}





function saveEducationInfo(){

    
    if (areAllFieldsCompleted2()) {
        addEducationItem()
        
        // ...
    } else {
        // Not all fields are completed, handle accordingly
        // Perhaps alert the user or highlight the empty fields
        alert('Please complete all fields before saving.');
    }
}



