from flask import Flask, current_app, render_template, request, session, redirect, url_for, jsonify, send_from_directory
from dao import get_all_users,get_user_cv_url,insert_user_cv,get_user_github_link, get_user_linkedin_link,add_user_picture,get_user_picture_url,update_user_github_links,update_user_linkedin_links ,update_user_description,update_user_info ,search_email, search_password,delete_user_skill, insert_users, get_passwd, get_user_info, get_user_description, get_user_education,insert_user_skill, get_user_experience, get_user_skills, get_user_id, get_user_role,get_all_skills,get_user_city,get_user_name, get_users_by_skill, delete_experience, insert_user_experience,insert_user_education,delete_user_education
import bcrypt
from datetime import date
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from werkzeug.utils import secure_filename
import os
import string
app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key_here'

UPLOAD_FOLDER = '/uploads'  # Adjust to your needs
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        uploaded_file = request.files['file']
        if uploaded_file:
            print(uploaded_file)
            upload_directory = 'static'
            if not os.path.exists(upload_directory):
                os.makedirs(upload_directory)

            # Save the uploaded file to the specified directory
            user_id = session.get("user_id")
            uploaded_file.save(os.path.join(upload_directory, uploaded_file.filename))
            profile_picture_url = f'static/{uploaded_file.filename}'
            print(profile_picture_url)
            add_user_picture(user_id, profile_picture_url)
            new_url = get_user_picture_url(user_id)
            print(new_url)
            # You can now handle the uploaded file as needed
            # For example, you can save it to the server
            # uploaded_file.save('path/to/save/' + uploaded_file.filename)

            return jsonify({'success': True, 'message': 'File uploaded successfully', 'url':new_url})
        else:
            return jsonify({'success': False, 'message': 'No file provided'})

    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred while processing the file'})

    # if 'file' not in request.files:
    #     return jsonify({"error": "No file part"}), 400
    # file = request.files['file']
    # if file.filename == '':
    #     return jsonify({"error": "No selected file"}), 400
    # if file and allowed_file(file.filename):
    #     user_id = session.get('user_id')
    #     print(file)
    #     secured_filename = secure_filename(file.filename)
    #     picture_path = os.path.join(app.config['UPLOAD_FOLDER'], secured_filename)
    #     file.save(picture_path)

    #     add_user_picture(user_id, picture_path)#, app.config['UPLOAD_FOLDER'])
    #     # Return the URL of the uploaded file
    #     return jsonify({"success": "File successfully uploaded", "filename": secured_filename}), 200
    # else:
    #     return jsonify({"error": "File type not allowed"}), 400



#backend-predict
# Read the data
predict_info = pd.read_csv("E&EPredict.csv", sep=";")

# Split the data into x/y
x = predict_info.drop("Salariu", axis=1)
y = predict_info["Salariu"]

# Split into training and test set
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Build a column transformer for one-hot encoding
categorical_features = ["Pozitie", "Limbaj", "Tehnologie", "Framework"]
numeric_features = ["Vechime"]
one_hot = OneHotEncoder(handle_unknown='ignore')
transformer = ColumnTransformer([
    ("one_hot", one_hot, categorical_features),
], remainder="passthrough")

# Fit and transform on the training set
x_train_transformed = transformer.fit_transform(x_train)

# Build machine learning model
model = RandomForestRegressor()
model.fit(x_train_transformed, y_train)
#back-predict

#predict endpoints


@app.route("/filter_by_skill", methods = ["POST"])
def filter():

    if request.method == "POST":
        try:
            data = request.get_json()
            skill = data.get("skill")
            user_id = data.get("userIds")
            
            user_names = {}
            users = get_users_by_skill(skill, user_id)
            print(users)
            if users:
                user_names = {user['user_id']: f"{user['first_name']} {user['last_name']}" for user in users}
            print(user_names)

            

            return jsonify(user_names), 200
        except Exception as e:
            print(f"Something is wrong, Data not collected: {e}")
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid request method"}), 400


@app.route('/add-skill', methods=['POST'])
def add_skill():
    if request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "User not logged in"}), 401
        
        data = request.get_json()
        skillName = data.get('skillName')
        skill_level = data.get('skill_level')

        if insert_user_skill(user_id, skillName, skill_level):
            return jsonify({"success": True, "message": "Skill added successfully"}), 200
        else:
            return jsonify({"success": False, "error": "Failed to add skill"}), 500


@app.route('/submit_data', methods=["POST"])  # Changed from UPDATE to POST
def submit_data():
    # Get data from the request
    user_id = session.get('user_id')

    # Retrieve text data from form data
    first_name = request.form.get('first_name', '')
    last_name = request.form.get('last_name', '')
    email = request.form.get('email', '')
    country = request.form.get('country', '')
    city = request.form.get('city', '')
    github = request.form.get('github', '')
    linkedin = request.form.get('linkedin', '')
    description = request.form.get('description', '')
    current_date = date.today()
    
    # Call your update functions here
    update_user_info(user_id, first_name, last_name, country, city)
    update_user_description(user_id, description)
    update_user_linkedin_links(user_id, linkedin)
    update_user_github_links(user_id, github)
    
    directory = 'static'

    # Handle file upload
    if 'cv' in request.files and request.files['cv'].filename != '':
        cv_file = request.files['cv']
    # Proceed with processing the file
    # .
    # Handle the case where no file was uploaded

        cv_file.save(os.path.join(directory, cv_file.filename))
    
        profile_picture_url1 = f'static/{cv_file.filename}'

    
    print("Saving to:", profile_picture_url1)
    insert_user_cv(user_id, profile_picture_url1)  # Replace with your path

    # Send a response back to the client
    return jsonify({"status": "success", "message": "Data received successfully"})




@app.route("/delete-skill", methods=["DELETE"])
def delete_skill():
    try:
        data = request.get_json()
        skill_name = data.get("skillName")
        user_id = session.get("user_id")
        result = delete_user_skill(user_id, skill_name)
        if result:
            return jsonify({"success": "Skill deleted successfully"}), 200
        else:
            return jsonify({"error": "Skill could not be deleted"}), 500
    except Exception as e:
        print(f"Something went wrong: {e}")
    return jsonify({"error": str(e)}), 500









@app.route("/delete-education", methods=["DELETE"])
def delete_education():
    try:
        data = request.get_json()
        school_name = data.get("schoolName")
        degree_name = data.get("degreeName")
        user_id = session.get("user_id")
        result = delete_user_education(user_id, school_name, degree_name)
        if result:
            return jsonify({"success": "Education deleted successfully"}), 200
        else:
            return jsonify({"error": "Education could not be deleted"}), 500
    except Exception as e:
        print(f"Something went wrong: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/delete-experience", methods=["DELETE"])
def deleteExperience():
    # DELETE requests should not use else for invalid method since it's already constrained
    try:
        data = request.get_json()
        company = data.get("company")
        position = data.get("position")
        user_id = session.get("user_id")
        # Assuming delete_experience() is a function that deletes the experience from the DB
        result = delete_experience(user_id, company, position)
        if result:
            return jsonify({"success": "Experience deleted successfully"}), 200
        else:
            return jsonify({"error": "Experience could not be deleted"}), 500
    except Exception as e:
        print(f"Something went wrong, Data not collected: {e}")
        return jsonify({"error": str(e)}), 500

        


@app.route('/add-education', methods=['POST'])
def add_education():
    if request.method == 'POST':
        user_id = session.get('user_id')  
        if not user_id:
            return jsonify({"error": "User not logged in"}), 401
        
        data = request.get_json()
        school_name = data.get('schoolName')
        degree_name = data.get('degreeName')
        year_started = data.get('startYear')
        year_ended = data.get('endYear')

        if insert_user_education(user_id, school_name, degree_name, year_started, year_ended):
            return jsonify({"success": "Education added successfully"}), 200
        else:
            return jsonify({"error": "Failed to add education"}), 500




@app.route('/add-experience', methods=['POST'])
def add_experience():
    if request.method == 'POST':
        # Assuming you're using session to store user_id, otherwise, adjust as needed
        user_id = session.get('user_id')  
        if not user_id:
            # Handle not logged in user
            return jsonify({"error": "User not logged in"}), 401
        
        data = request.get_json()
        position_name = data.get('position')
        company_name = data.get('company')
        start_date = data.get('startYear')
        end_date = data.get('endYear')

        # Validate data here as needed before insertion
        if insert_user_experience(user_id, position_name, company_name, start_date, end_date):
            return jsonify({"success": "Experience added successfully"}), 200
        else:
            return jsonify({"error": "Failed to add experience"}), 500


@app.route("/search_by_city", methods=["POST"])
def searchByCity():
    if request.method == "POST":
        try:
            data = request.get_json()
            city = data.get("city")
            
            user_names = {}
            user_name = get_user_name(city)
            print(user_name)
            if user_name:
                user_names = {user['user_id']: f"{user['first_name']} {user['last_name']}" for user in user_name}

            return jsonify(user_names), 200
        except Exception as e:
            print(f"Something is wrong, Data not collected: {e}")
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid request method"}), 400


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            # Collect form data
            data = request.get_json()

            # Extract data fields
            position = data.get("profession")
            language = data.get("language")
            technology = data.get("technology")
            framework = data.get("framework")
            seniority = float(data.get("seniority"))


            # Transform input data
            input_data = pd.DataFrame([[position, language, technology, framework, seniority]],
                                      columns=["Pozitie", "Limbaj", "Tehnologie", "Framework", "Vechime"])
            input_data_transformed = transformer.transform(input_data)

            # Log the transformed input data for debugging
            print("Transformed Input Data:", input_data_transformed)

            # Make the prediction
            predicted_salary = model.predict(input_data_transformed)[0]
            print(predicted_salary)

            # Return the prediction as JSON
            return jsonify({"salary": predicted_salary})

        except Exception as e:
            print(f"Error in /predict route: {e}")

            return jsonify({"error": "Internal Server Error"}), 500

    return render_template("predict.html")
#predict endpoints



@app.route("/edit-profile")
def edit_profile():

    user_id = session.get("user_id")
    
    user_info = get_user_info(user_id)
    print(user_info)
    print(session)
    user_id = session.get("user_id")
    print(user_id)

    user_desc = get_user_description(user_id)
    user_ed = get_user_education(user_id)
    user_ex = get_user_experience(user_id)
    user_skills = get_user_skills(user_id)
    skills = get_all_skills()
    github = get_user_github_link(user_id)
    linkedin = get_user_linkedin_link(user_id)
   
    picture_url = get_user_picture_url(user_id)
    filename = None  # Initialize filename as None
    cv = get_user_cv_url(user_id)



    print(picture_url)
    
    return render_template("edit-profile.html", user_info = user_info, user_desc=user_desc, user_ed = user_ed, user_ex=user_ex, user_skills=user_skills, skills = skills, picture_url = picture_url, github = github, linkedin = linkedin, cv = cv)


@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    # Define the directory where your uploaded files are stored
    uploads_dir = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    
    # Use send_from_directory to send the file to the client
    return send_from_directory(uploads_dir, filename)
   

@app.route("/sign-up") ## this is so that with both notations the same page is accessed
def signup_render_template():
    session["authenticated"] = True
    return render_template("sign-up.html")


@app.route("/sign-up", methods = ["POST"]) ## this is so that with both notations the same page is accessed
def registerUser():
    #ill have to hash and salt here
    #also want to somehow send an email here
    if request.method == "POST" and request.form:
        try:
            email = request.form.get("email")
            password = request.form.get("password")
            firstName = request.form.get("firstName")
            lastName = request.form.get("lastName")
            username = request.form.get("username")
            country = request.form.get("country")
            city = request.form.get("city")
            role = request.form.get("group1")
            # Other form data ...
            print(role)
            current_date = date.today()
            print(type(current_date))
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            insert_users(username, email, hashed_password, firstName, lastName, role, current_date, country, city)
            # Process the registration...
            user_id = get_user_id(email)
            session["authenticated"] = True
            session["user_id"] = user_id
            response = {'message': 'Registration successful!', 'user_id' : user_id}
            return jsonify(response)
            

        except Exception as e:
            response = {'message': f'Error: {str(e)}'}
            return jsonify(response), 400  # Return a 400 status for bad requests

    else:
        response = {'message': 'Invalid request'}
        return jsonify(response), 405  # Return a 405 status for method not allowed
        

        #this isnt gonna work before i change the frontend to multistep


    

@app.route("/profile", methods = ["GET"])
def profile():
    user_id = request.args.get('user_id')

    print(user_id)
    user_info = get_user_info(user_id)
    user_desc = get_user_description(user_id)
    user_ed = get_user_education(user_id)
    user_ex = get_user_experience(user_id)
    user_skills = get_user_skills(user_id)
    picture = get_user_picture_url(user_id)
    cv = get_user_cv_url(user_id)
    linkedin = get_user_linkedin_link(user_id)
    github = get_user_github_link(user_id)
    print(user_ex)

    if user_info is None:
        # You can redirect to an error page or handle it in another way
        print("user_info  is none")
    
    if session.get("authenticated"):
        return render_template('profile.html', user_id = user_id, user_info = user_info, user_desc=user_desc, user_ed = user_ed, user_ex=user_ex, user_skills=user_skills, picture=picture, cv = cv, linkedin = linkedin, github = github)
    elif session.get("authenticated") and session.permanent:
        return render_template('profile.html', user_id = user_id, user_info = user_info, user_desc=user_desc, user_ed = user_ed, user_ex=user_ex, user_skills=user_skills, picture=picture, cv = cv, linkedin = linkedin, github = github)
    else:
        return jsonify({"success": False, "message": "user not logged in!" })


  

@app.route("/your_profile", methods = ["GET"])
def your_profile():
    user_id = session.get('user_id')
    print(user_id)
    
    
    if session.get("authenticated") and session.permanent:
        return jsonify({"authenticated": True, "message": "user logged in!", "user_id":user_id })
    if session.get("authenticated"):
        return jsonify({"authenticated": True, "message": "user logged in!", "user_id":user_id })
    
    return jsonify({"authenticated": False, "message": "user not logged in!" })



@app.route("/redirect_to_profile/<int:user_id>", methods=["GET"])
def redirect_to_profile(user_id):

    if session.get("authenticated") and session.permanent:

    # Redirect to the /profile route with the user_id as a query parameter
        return redirect(url_for('profile', user_id=user_id))
    
    else:
        return jsonify({"success": False, "message": "user not logged in!" })

@app.route('/some_route', methods=['GET'])
def some_route():
    user_id = session.get("user_id")
    # Logic to get the user's role
    user_role = get_user_role(user_id)  # Replace this with your actual function to get the user's role

    return jsonify({"user_role": user_role})


@app.route("/recruit")
def recruit():
    users = get_all_users()
    skills = get_all_skills()

    return render_template('recruit.html', users=users, skills = skills)




@app.route("/login", methods =["POST"]) ## this is so that with both notations the same page is accessed
def home():
    
    email = request.form.get("email")
    password = request.form.get("password")
    remember = request.form.get("remember")
    print(remember)
    if search_email(email):
        hashed_password_with_salt = get_passwd(email)
        
           
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password_with_salt.encode('utf-8')):
            session["authenticated"] = True
            session["email"] = email
            if remember:
                session.permanent = True
            user_id = get_user_id(email)
            session['user_id'] = user_id
            user_role = get_user_role(user_id)
            return jsonify({"success": True, "user_id": user_id, "user_role": user_role })
            

        else: 
            return jsonify({"success": False, "message": "Wrong password!"}), 200, {"Content-Type": "application/json"}
    else:
        return jsonify({"success": False, "message": "Wrong email"}), 200, {"Content-Type": "application/json"}




@app.route("/login", methods = ["GET"])
def render_login_template():
    if session.get("authenticated") and session.permanent:
        print("ceva ")
        return redirect(url_for("profile"))
    return render_template("home.html")

    
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("render_login_template"))






if __name__ == "__main__":
    app.run(debug=True)