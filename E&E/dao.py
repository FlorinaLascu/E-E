import os

from flask import app
from connect import get_sql_conn
import psycopg2
import datetime
from werkzeug.utils import secure_filename






def search_username(username):
    conn = get_sql_conn()
    query = ("select * from users where username = %s")
    cursor = conn.cursor()
   
    cursor.execute(query, (username,))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    if rows:
        for row in rows:
            print(row)
            return True
    else:
        return False 
        



def search_email(email):
    conn = get_sql_conn()
    query = ("select * from users where email = %s")
    cursor = conn.cursor()
    cursor.execute(query, (email,))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    print("Searched for email:", email)
    if rows:
        return True
        
    else:
        return False
    


def search_password(password):
    conn = get_sql_conn()
    query = ("select * from users where password = %s")
    cursor = conn.cursor()
    cursor.execute(query, (password,))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()

    if rows:
        return True
        
    else:
        return False
        

def get_passwd(email):
    conn = get_sql_conn()
    query = ("select password from users where email = %s")
    cursor = conn.cursor()
    cursor.execute(query, (email,))
    row = cursor.fetchone()
    conn.commit()
    conn.close()

    if row:
        hashed_password_with_salt = bytes(row[0]).decode('utf-8')
        print(hashed_password_with_salt)
        return hashed_password_with_salt
        
    else:
        return False

def get_user_id(email):
    conn = get_sql_conn()
    query = ("select user_id from users where email = %s")
    cursor = conn.cursor()
    cursor.execute(query, (email,))
    rows = cursor.fetchone()
    
    conn.close()
    print("Searched for email:", email)
    if rows:
        user_id = { "user_id": rows[0]}
        print(user_id["user_id"])
        return user_id["user_id"]
        
    else:
        return False   
    

def get_user_role(user_id):
    conn = get_sql_conn()
    query = ("select user_role from users where user_id = %s")
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    rows = cursor.fetchone()
    
    conn.close()
    
    if rows:
        user_role= { "user_role": rows[0]}
        print(user_role["user_role"])
        return user_role["user_role"]
        
    else:
        return False   
    

def get_user_github_link(user_id):
    conn = get_sql_conn()
    query = "SELECT link FROM user_github_links WHERE user_id = %s"
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        github_link = row[0]
        return github_link
    else:
        return None

def get_user_linkedin_link(user_id):
    conn = get_sql_conn()
    query = "SELECT link FROM user_linkedin_links WHERE user_id = %s"
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        linkedin_link = row[0]
        return linkedin_link
    else:
        return None


def insert_user_cv(user_id, cv_url):
    conn = get_sql_conn()  # Ensure this function is defined to get your database connection
    cursor = conn.cursor()
    print(cv_url)

    try:
        # Check if the user already has a CV entry
        cursor.execute("SELECT * FROM user_cv WHERE user_id = %s", (user_id,))
        if cursor.fetchone():
            # User already has a CV entry, so update it
            query = "UPDATE user_cv SET url = %s WHERE user_id = %s"
            cursor.execute(query, (cv_url, user_id))
        else:
            # No CV entry exists for the user, so insert a new one
            query = "INSERT INTO user_cv (user_id, url) VALUES (%s, %s)"
            cursor.execute(query, (user_id, cv_url))

        conn.commit()

    except psycopg2.Error as e:
        print(f"Error updating user CV: {e}")
        print('An error occurred while updating the CV.')

    finally:
        cursor.close()
        conn.close()


def get_user_cv_url(user_id):
    """
    Retrieve the URL from the user_cv table by user_id.
    """
    conn = get_sql_conn()  # Ensure this function is defined to get your database connection
    query = "SELECT url FROM user_cv WHERE user_id = %s"
    cursor = conn.cursor()
    try:
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        return row[0] if row else None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()




def insert_user_education(user_id, school_name, degree_name, year_started, year_ended):
    conn = get_sql_conn()
    query = ("INSERT INTO user_education (user_id, school_name, degree_name, year_started, year_ended) "
             "VALUES (%s, %s, %s, %s, %s)")
    cursor = conn.cursor()
    data = (user_id, school_name, degree_name, year_started, year_ended)
    
    try:
        cursor.execute(query, data)
        conn.commit()
        print("User education added successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
        return True



def insert_user_skill(user_id, skill_name, skill_level):
    conn = get_sql_conn()
    cursor = conn.cursor()
    query1 = ("SELECT skill_id FROM skills WHERE skill_name = %s")
    cursor.execute(query1, (skill_name,))
    row = cursor.fetchone()
    skill_id = row[0]
    query = ("INSERT INTO user_skills (user_id, skill_id, skill_level) "
             "VALUES (%s, %s, %s)")
    
    
    try:
        cursor.execute(query, (user_id, skill_id, skill_level))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        cursor.close()
        conn.close()




def insert_user_experience(user_id, position_name, company_name, start_date, end_date):
    conn = get_sql_conn()
    query = ("INSERT INTO user_experience (user_id, position_name, company_name, start_date, end_date) "
             "VALUES (%s, %s, %s, %s, %s)")
    cursor = conn.cursor()
    data = (user_id, position_name, company_name, start_date, end_date)
    
    try:
        cursor.execute(query, data)
        conn.commit()
        print("User experience added successfully.")

    except psycopg2.Error as e:
        print(f"An error occurred: {e}")

    finally:
        cursor.close()
        conn.close()




def insert_users(username, email, password, first_name, last_name, user_role, date_created, country, city):
    conn = get_sql_conn()
    query = ("insert into users (username, email, password, first_name, last_name, user_role, date_created, country, city) "
             "values(%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    cursor = conn.cursor()
    data =(username, email, password, first_name, last_name, user_role, date_created, country, city)
    
    if not search_email(email):
        if not search_username(username):
    
            try:
                cursor.execute(query, data)
                conn.commit()
    
            except psycopg2.Error as e: 
                if 'user_role' in str(e):
                    print (F"error invalid user_role - {user_role}")

                else:
                    print(f"error: {e}")
    
            finally:
                cursor.close()
                conn.close()
        else:
            print("error - username already exist")
    else:
        print("error - email already exists")


def update_user_info(user_id, new_first_name, new_last_name, new_country, new_city):
    conn = get_sql_conn()
    query = ("UPDATE users SET first_name = %s, last_name = %s, country = %s, city = %s "
             "WHERE user_id = %s")
    cursor = conn.cursor()
    data = (new_first_name, new_last_name, new_country, new_city, user_id)
    
    try:
        cursor.execute(query, data)
        conn.commit()

    except psycopg2.Error as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        conn.close()


def update_user_description(user_id, new_description):
    conn = get_sql_conn()
    
    cursor = conn.cursor()
    print(type(user_id))

    cursor.execute("SELECT * FROM user_description WHERE user_id = %s", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
    # If a row is found, print the user's information
        query = ("UPDATE user_description SET description = %s "
         "WHERE user_id = %s")
        data =  (new_description,user_id)

   
    else:
        query = ("INSERT INTO user_description  (user_id, description) "
         "VALUES (%s, %s)")
        data = (user_id,new_description)

    try:
        cursor.execute(query, data)
        conn.commit()

    except psycopg2.Error as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        conn.close()


def add_user_picture(user_id, picturePath):
    conn = get_sql_conn()
    cursor = conn.cursor()
    print(picturePath)
    try:
        cursor.execute("SELECT * FROM user_picture WHERE user_id = %s", (user_id,))
        if cursor.fetchone():
            query = "UPDATE user_picture SET picture_url = %s WHERE user_id = %s"
            cursor.execute(query, (picturePath, user_id))
            conn.commit()
        else:
            query = "INSERT INTO user_picture (user_id, picture_url) VALUES (%s, %s)"
            cursor.execute(query, (user_id, picturePath))
            conn.commit()
    except psycopg2.Error as e:
            print(f"Error updating user picture: {e}")
            print('An error occurred while updating the profile picture.')
    finally:
        cursor.close()
        conn.close()





def get_user_picture_url(user_id):
    conn = get_sql_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT picture_url FROM user_picture WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    person_img = '/static/person.png'
    
    return result[0] if result else person_img


def update_user_linkedin_links(user_id, new_linkedin_link):
    conn = get_sql_conn()
    cursor = conn.cursor()

    # Check if the user already has a LinkedIn link
    cursor.execute("SELECT * FROM user_linkedin_links WHERE user_id = %s", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        # Update the existing link
        query = "UPDATE user_linkedin_links SET link = %s WHERE user_id = %s"
        data = (new_linkedin_link, user_id)
    else:
        # Insert a new link
        query = "INSERT INTO user_linkedin_links (user_id, link) VALUES (%s, %s)"
        data = (user_id, new_linkedin_link)

    try:
        cursor.execute(query, data)
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def update_user_github_links(user_id, new_github_link):
    conn = get_sql_conn()
    cursor = conn.cursor()

    # Check if the user already has a GitHub link
    cursor.execute("SELECT * FROM user_github_links WHERE user_id = %s", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        # Update the existing link
        query = "UPDATE user_github_links SET link = %s WHERE user_id = %s"
        data = (new_github_link, user_id)
    else:
        # Insert a new link
        query = "INSERT INTO user_github_links (user_id, link) VALUES (%s, %s)"
        data = (user_id, new_github_link)

    try:
        cursor.execute(query, data)
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Example usage:
# update_user_linkedin_links(1, 'https://www.linkedin.com/in/username/')
# update_user_g










def delete_user_education(user_id, school_name, degree_name):
    try:
        conn = get_sql_conn()
        cursor = conn.cursor()
        query = """
        DELETE FROM user_education 
        WHERE user_id = %s AND school_name = %s AND degree_name = %s
        """
        cursor.execute(query, (user_id, school_name, degree_name))
        conn.commit()
        deleted_rows = cursor.rowcount  # returns the number of rows deleted
        cursor.close()
        conn.close()
        return deleted_rows > 0
    except Exception as e:
        print(f"Error deleting education: {e}")
        return False


def delete_user_skill(user_id, skill_name):
    try:
        conn = get_sql_conn()
        cursor = conn.cursor()
            # First query: get the skill_id from the skills table
        cursor.execute("SELECT skill_id FROM skills WHERE skill_name = %s", (skill_name,))
        skill = cursor.fetchone()
        if skill is None:
            print(f"Skill with name {skill_name} does not exist.")
            return None

        skill_id = skill[0]

        # Second query: use the skill_id to delete the user's skill
        delete_query = """
            DELETE FROM user_skills
            WHERE user_id = %s AND skill_id = %s
        """
        cursor.execute(delete_query, (user_id, skill_id))
        conn.commit()
        deleted_rows = cursor.rowcount

        print("Number of skills deleted:", deleted_rows)
        return deleted_rows > 0

    except Exception as e:
        print(f"Error deleting user's skill: {e}")
        return False
    finally:
        cursor.close()
        conn.close()



       






def delete_experience( user_id, company_name, position_name):
        try:
            conn = get_sql_conn()
            cursor = conn.cursor()
            query = """
            DELETE FROM user_experience 
            WHERE user_id = %s AND company_name = %s AND position_name = %s
            """
            cursor.execute(query, (user_id, company_name, position_name))
            conn.commit()
            print("success")
            return cursor.rowcount  # returns the number of rows deleted
        except Exception as e:
            print(f"Error deleting experience: {e}")
            return None


def get_all_users():
    conn = get_sql_conn()
    query = ("select user_id, first_name, last_name from users where user_role = 'normal'")
    cursor =  conn.cursor()

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()


    users = []
    for row in rows:
        user = {
            "user_id": row[0],
            'first_name': row[1],
            'last_name': row[2],
            # Add more keys as needed
        }
        users.append(user)
    return users if users else None



def get_user_image(user_id):
    conn = get_sql_conn()
    query = ("select picture_url from user_picture where user_id = %s ")
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()

    conn.commit()
    conn.close()


    if not rows:
        False #i waant to set static images on the server if there s no pic in the dbh
    else:
        return rows
    
def get_user_name(city):
    try:
        with get_sql_conn() as conn:
            query = "SELECT user_id, first_name, last_name FROM users WHERE city = %s"
            with conn.cursor() as cursor:
                cursor.execute(query, (city,))
                rows = cursor.fetchall()  # Fetch all rows

        users = []
        for row in rows:
            user_id, first_name, last_name = row
            users.append({'user_id': user_id, 'first_name': first_name, 'last_name': last_name})
            print(row)

        return users

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def get_users_by_skill(skill_name, user_ids):
    try:
        with get_sql_conn() as conn:
            # Use a parameterized query to prevent SQL injection
            query = """
            SELECT u.user_id, u.first_name, u.last_name
            FROM users u
            JOIN user_skills us ON u.user_id = us.user_id
            JOIN skills s ON us.skill_id = s.skill_id
            WHERE s.skill_name = %s AND u.user_id = ANY(%s)
            """
            with conn.cursor() as cursor:
                cursor.execute(query, (skill_name, user_ids))
                rows = cursor.fetchall()

        # Create a dictionary with the user_id as the key and the first_name and last_name as values
        users = [{'user_id': row[0], 'first_name': row[1], 'last_name': row[2]} for row in rows]
        return users

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def get_user_info(user_id):
    
    try:
        conn = get_sql_conn()
        query = ("select first_name, last_name, email, country, city from users where user_id = %s")
        cursor =  conn.cursor()

        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
 
        if row:
            user_info = {
                
                'first_name': row[0],
                'last_name': row[1],
                "email": row[2],
                "country": row[3],
                "city": row[4],
                # Add more keys as needed
            }
            print(user_info)
            return user_info
        
        else:
            return None
    except Exception as e:
        print(f"Error in get_user_info; {e}")
        return None

    finally:
        if conn:
            conn.commit()
            conn.close()


def get_user_description(user_id):
    
    try:
        conn = get_sql_conn()
        query = ("select description from user_description where user_id = %s")
        cursor =  conn.cursor()

        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
 
        if row:
            description = {
                
                'description': row[0],
                
                # Add more keys as needed
            }
            print(description)
            return description
        
        else:
            return None
    except Exception as e:
        print(f"Error in get_user_info; {e}")
        return None

    finally:
        if conn:
            
            conn.close()



def get_user_education(user_id):
    conn = get_sql_conn()
    query = ("select school_name, degree_name, year_started, year_ended from user_education where user_id = %s")
    cursor =  conn.cursor()

    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()


    education = []
    for row in rows:
        user_education = {
            "school_name": row[0],
            'degree_name': row[1],
            'start': row[2],
            'end': row[3]
            # Add more keys as needed
        }
        education.append(user_education)
    print(education)
    return education if education else None


    
def get_user_experience(user_id):
    conn = get_sql_conn()
    query = ("select position_name, company_name, start_date, end_date from user_experience where user_id = %s")
    cursor =  conn.cursor()

    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()


    experience = []
    for row in rows:
        user_experience = {
            "position": row[0],
            'company': row[1],
            'start': row[2],
            'end': row[3]
            # Add more keys as needed
        }
        experience.append(user_experience)
    print(experience)
    return experience if experience else None


   
def get_user_skills(user_id):
    conn = get_sql_conn()
    query = """SELECT skills.skill_name, user_skills.skill_level 
    FROM user_skills
    JOIN skills ON user_skills.skill_id = skills.skill_id
    WHERE user_skills.user_id = %s;"""

    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    conn.commit()
    conn.close()


    skills = []
    for row in rows:
        user_skills = {
            "skill_name": row[0],
            'skill_level': row[1],
            
            # Add more keys as needed
        }
        skills.append(user_skills)
    print(skills)
    return skills if skills else None


def get_user_city(user_id):
    try:
        with get_sql_conn() as conn:
            query = "SELECT user_id, city FROM users WHERE user_id = %s"
            print(f"Executing query: {query} with user_id = {user_id}")
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id,))
                row = cursor.fetchone()
                print(f"Fetched row: {row}")

        if row:
            return {row[0]: row[1]}
        else:
            print("No data found for the given user_id.")
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}






def get_all_skills():
    conn = get_sql_conn()
    query = "select * from skills"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    
    skills = []
    for row in rows:
        user_skills = {
            "skill_id": row[0],
            "skill_name": row[1],
            
            # Add more keys as needed
        }
        skills.append(user_skills)
    print(skills)
    return skills if skills else None

#insert_users("florina1", "florina1@example.com", "password1234", "florina", "lascu", "administrator", "2023-11-30")
#search_username("john_doe")
#print(search_email("john@example.com"))


#get_all_users()
#get_passwd("carinafurmanek@gmail.com")
#get_all_users()
#get_user_info(10)
#get_user_description(11)
#get_user_experience(11)
#get_user_skills(11)
#get_user_id("florina.lascu@yahoo.com")
#get_user_role(11)
#get_passwd("harry.styles@yahoo.com")
#get_user_city(4)
get_user_name("Bucuresti")
