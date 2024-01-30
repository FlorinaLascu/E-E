    # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            insert_users(username, email, hashed_password, firstName, lastName, role, current_date, country, city)
            # Process the registration...
            user_id = get_user_id(email)
            response = {'message': 'Registration successful!', 'user_id' : user_id}
            return jsonify(response)