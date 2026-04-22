# Applcation name: Mingle
# Creator; Marialda Cabral
# This application helps team members get to know each other and connect.


# ==========================================
# IMPORTS & SETUP
# ==========================================
import streamlit as st
import pandas as pd
import os
import random
import requests 

# Define Excel file path
EXCEL_FILE = 'mingle_users.xlsx'
# Define Excel file columns
EXPECTED_COLUMNS = ["First Name", "Last Name", "Interests","Kudos", "Would You Rather", "Truth 1", "Truth 2", "Lie", "User Manual", "Skill]"]


# ==========================================
# STATE MANAGEMENT
# ==========================================
# Initializing session state variables 
def initializing_session():
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'first_name': '',
            'last_name': '',
            'interests': [],
            'is_setup': False
    }
    
# Updating session state variables when a user is found or new record is created
def update_session(first_name, last_name, interests):
    # Update the session state with the new values
    st.session_state.user_profile['first_name'] = first_name
    st.session_state.user_profile['last_name'] = last_name
    st.session_state.user_profile['interests'] = interests
    st.session_state.user_profile['is_setup'] = True

# ==========================================
# DATA HANDLING 
# ==========================================
# Retriving data from excel file
def load_data():
    # Check if the file exists first
    if os.path.exists(EXCEL_FILE):
        # Load current data
        # Try to read the file
        try:
            df = pd.read_excel(EXCEL_FILE)
        
            # Check if the file exists but has no data rows
            if df.empty:
            # It might be completely blank, or it might just have headers.
            # We return a fresh DataFrame with our specific columns to be safe.
                return pd.DataFrame(columns=EXPECTED_COLUMNS)
            
            return df
        
        # Catch errors that happen if the file is completely blank or unreadable
        except (ValueError, pd.errors.EmptyDataError):
            return pd.DataFrame(columns=EXPECTED_COLUMNS)
    else:
        # If it doesn't exist, return an empty DataFrame with the columns we want
        return pd.DataFrame(columns=EXPECTED_COLUMNS)


# Saving new user to excel spreadsheet
def append_to_excel(df, first_name, last_name, interests):
    # Create a dictionary with the new row of data
    new_user_data = {
        "First Name": first_name.strip().lower(),
        "Last Name": last_name.strip().lower(),
        "Interests": ", ".join(interests).strip(),
        "Kudos": 0,               # Default starting value
        "Would You Rather": "", # Default starting value
        "Truth 1": "",            # Default starting value
        "Truth 2": "",            # Default starting value
        "Lie": "",                # Default starting value
        "User Manual": "",        # Default starting value
        "Skill": ""               # Default starting value
    }

    
    # Convert that single dictionary into a DataFrame
    new_row_df = pd.DataFrame([new_user_data])
    
    # APPEND: Combine the existing DataFrame (df) with the new row (new_row_df)
    # ignore_index=True ensures the row numbers stay in order (0, 1, 2, 3...)
    updated_df = pd.concat([df, new_row_df], ignore_index=True)
    
    # 4. Save the combined data back to the Excel file, overwriting the old one
    updated_df.to_excel('mingle_users.xlsx', index=False)


# Updating an existing user's record in the excel spreadsheet
def update_excel_record(df, first_name, last_name, column_name, new_value):
    # Find the row index for the current user
    user_idx = df[(df['First Name'] == first_name.strip().lower()) & 
                  (df['Last Name'] == last_name.strip().lower())].index
    
    if not user_idx.empty:
        # Update the specific cell with the new value
        df.loc[user_idx[0], column_name] = new_value
        
        # Save back to Excel
        df.to_excel(EXCEL_FILE, index=False)



# ==========================================
# HELPER FUNCTIONS
# ==========================================

# Helper function to set up a new round of the game Guess Who
def init_guess_who(df):
    # Pick 1 random row to be the mystery coworker
    mystery_row = df.sample(1).iloc[0]
    
    # Format their name nicely (e.g., "marialda cabral" -> "Marialda Cabral")
    correct_name = f"{mystery_row['First Name'].title()} {mystery_row['Last Name'].title()}"
    
    # Find other users to act as wrong answers (distractors)
    # Filter out the mystery person so they aren't in the distractor list
    other_users = df[(df['First Name'] != mystery_row['First Name']) | (df['Last Name'] != mystery_row['Last Name'])]
    
    distractors = []
    if not other_users.empty:
        # Pick up to 3 random wrong answers
        num_distractors = min(3, len(other_users))
        distractor_rows = other_users.sample(num_distractors)
        for _, row in distractor_rows.iterrows():
            distractors.append(f"{row['First Name'].title()} {row['Last Name'].title()}")
            
    # Combine the correct answer with the wrong answers and shuffle them
    options = [correct_name] + distractors
    random.shuffle(options)
    
    # Save this specific game round into session state
    st.session_state.guess_who_state = {
        'correct_name': correct_name,
        'interests': mystery_row['Interests'],
        'options': options,
        'guessed_correctly': False
    }
    
    
# ==========================================
# PAGE VIEWS 
# ==========================================

#Profile Page
def show_Profile_page(df, st_first_name):
    

    #Checking if session state was initicalized. That means we already have user information
    if st.session_state.user_profile['is_setup'] == True:
        st.title(f"We Know You, {st_first_name.capitalize()}")
        
        #Message to user
        st.success("You can start mingling.")

        if st.button("Change User"):
            # Delete everything in the session state
            for key in st.session_state.keys():
                del st.session_state[key]
        
            # Rerun the app to start completely fresh
            st.rerun()

        
    # No user information yet
    else:
        st.title("Tell us Who You Are")
        
        #Gathering information
        first_name_input = st.text_input("What is your first name?", value=st.session_state.user_profile['first_name'])

        # Only show subsequent inputs if te previous ones are filled out
        if first_name_input:
            last_name_input = st.text_input("What is your last name?", value=st.session_state.user_profile['last_name'])

            if last_name_input:
                
                #check to see if the person is already in the excel file
                # Filter the dataframe to find the row where BOTH first and last name match
                user_record = df[(df["First Name"].astype(str).str.strip().str.lower() == first_name_input.strip().lower()) & 
                 (df["Last Name"].astype(str).str.strip().str.lower() == last_name_input.strip().lower())]
                
                # Check if the filtered dataframe is not empty (meaning the user was found)
                if not user_record.empty:
                    st.write(f"Nice to see you, {first_name_input} {last_name_input}! 🎉")
                    # Extract the "Interests" column from the first matching row (index 0)
                    user_interests = user_record.iloc[0]["Interests"]
                    st.write(f"Your interests are: {user_interests}")

                    #Updating session state variables 
                    update_session(user_record.iloc[0]["First Name"], user_record.iloc[0]["Last Name"], user_interests)

                    #Message to user
                    st.success("We know who you are! You can start mingling.")

                    
                else:
                    st.write(f"Nice to meet you, {first_name_input} {last_name_input}! 🎉")
                    # Inquiring interests
                    interests_input = st.multiselect(
                     "Select your interests", 
                    ["Coffee", "Hiking", "Coding", "Board Games", "Running", "Python"],
                    default=st.session_state.user_profile['interests']
                    )

                    if st.button("Save Profile"):
                        # Update the session state with the new values
                        update_session(first_name_input, last_name_input, interests_input)

                        # Save data in excel spreadsheet by calling our updated function
                        append_to_excel(df, first_name_input, last_name_input, interests_input)
                        
                        #Message to user
                        st.success("Now, We are acquainted! You can start mingling.")
                                
                

# Guess Who Page
def show_Guess_Who_page(df, st_first_name):
    st.title(f"{st_first_name.capitalize()}, Guess Who Your Co-Worker is 🕵️‍♀️")

    # We need at least 2 people in the Excel file to play a guessing game!
    if len(df) < 2:
        st.warning("We need at least 2 people in the database to play! Invite some coworkers to Mingle.")
        return

    # If a game hasn't been started yet, initialize it
    if 'guess_who_state' not in st.session_state:
        init_guess_who(df)

    # Grab the current game state
    state = st.session_state.guess_who_state

    st.write("### Whose interests are these?")
    st.info(f"💡 **{state['interests']}**")

    # Check if the user has already guessed correctly
    if state['guessed_correctly']:
        st.success(f"🎉 Correct! It was **{state['correct_name']}**.")
        
        # Button to start a new round
        if st.button("Play Again"):
            init_guess_who(df) # Generate a new mystery person
            st.rerun()         # Refresh the page
    else:
        # Show the multiple choice options
        guess = st.radio("Select the coworker:", state['options'], index=0)
        
        if st.button("Submit Guess"):
            if guess == state['correct_name']:
                # They got it right! Update state and show balloons
                st.session_state.guess_who_state['guessed_correctly'] = True
                st.balloons()
                st.rerun()
            else:
                # They got it wrong
                st.error("Oops! That's not correct. Try again!")
                

#Would You Rather Page
def show_Would_You_Rather_page(df, st_first_name, st_last_name):
    st.title(f"Would You Rather, {st_first_name.title()}? 🤔")
    
    question = "Would you rather work from a beach 🏖️ or a mountain cabin 🏔️?"
    st.write(f"### {question}")
    
    # 1. Find the current user's record to see if they already answered
    user_record = df[(df['First Name'] == st_first_name.lower()) & (df['Last Name'] == st_last_name.lower())]
    
    if user_record.empty:
        st.error("Could not find your profile. Please go back to the Profile page.")
        return
        
    current_answer = user_record.iloc[0]['Would You Rather']
    
    # 2. Check if the answer is empty (meaning they haven't played yet)
    # pd.notna() checks for pandas 'NaN' (empty excel cells)
    has_answered = pd.notna(current_answer) and str(current_answer).strip().lower() not in ["", "nan"]
    
    if not has_answered:
        # --- VIEW 1: USER HAS NOT ANSWERED YET ---
        st.info("Answer the question to see what your coworkers said!")
        
        choice = st.radio("Choose one:", ["Beach 🏖️", "Mountain Cabin 🏔️"], index=None)
        
        if st.button("Submit Answer"):
            if choice:
                # Save their answer to Excel
                update_excel_record(df, st_first_name, st_last_name, "Would You Rather", choice)
                st.balloons()
                st.rerun() # Refresh to show the results!
            else:
                st.warning("Please select an option before submitting.")
                
    else:
        # --- VIEW 2: USER HAS ANSWERED (SHOW RESULTS) ---
        st.success(f"You answered: **{current_answer}**")
        
        if st.button("Change My Answer"):
            # Erase their answer and refresh
            update_excel_record(df, st_first_name, st_last_name, "Would You Rather", "")
            st.rerun()
            
        st.divider()
        st.write("### 📊 What your co-workers said:")
        
        # Get everyone who has answered the question
        answered_df = df[df['Would You Rather'].notna() & (df['Would You Rather'] != "")]
        
        # Split them into two groups based on their answer
        beach_lovers = answered_df[answered_df['Would You Rather'] == "Beach 🏖️"]
        mountain_lovers = answered_df[answered_df['Would You Rather'] == "Mountain Cabin 🏔️"]
        
        # Display the results side-by-side using Streamlit Columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"Beach 🏖️ ({len(beach_lovers)})")
            for _, row in beach_lovers.iterrows():
                st.write(f"• {row['First Name'].title()} {row['Last Name'].title()}")
                
        with col2:
            st.subheader(f"Mountain Cabin 🏔️ ({len(mountain_lovers)})")
            for _, row in mountain_lovers.iterrows():
                st.write(f"• {row['First Name'].title()} {row['Last Name'].title()}")


#Spin The Wheel Page
def show_Spin_The_Wheel_page(st_first_name):
    st.title(f"Spin The Wheel, {st_first_name.title()}! 🎡")
    st.write("Need an icebreaker? Spin the wheel to get a random conversation topic for your next team meeting or coffee chat.")

    # 1. Create a list of fun conversation topics
    topics = [
        "If you could have any superpower, what would it be and why? 🦸",
        "What is your favorite travel destination and why? ✈️",
        "What is the best book or movie you've consumed recently? 🍿",
        "If you had to eat one meal for the rest of your life, what would it be? 🍕",
        "What's a hidden talent you have that most people don't know about? 🤹",
        "What was your first job? 💼",
        "If you could instantly become an expert in something, what would it be? 🧠",
        "What's the best piece of advice you've ever received? 💡",
        "Are you an early bird or a night owl? 🦉",
        "What is your favorite way to unwind after a busy day? 🧘"
    ]

    # 2. Initialize a session state variable to hold the current topic
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = None

    # 3. Create a big, fun button to spin the wheel
    if st.button("🎡 Spin the Wheel!", type="primary"):
        # Pick a random topic from the list
        st.session_state.current_topic = random.choice(topics)
        
        # Add a fun visual effect! (st.snow() is great for a "spinning/falling" effect)
        st.snow()

    # 4. Display the topic if one has been selected
    if st.session_state.current_topic:
        st.divider()
        st.write("### Your Conversation Topic:")
        # st.info creates a nice highlighted blue box
        st.info(f"#### {st.session_state.current_topic}")

# Kudos page
def show_Kudos_page(df, st_first_name, st_last_name):
    st.title("Wall of Fame: Give Kudos! 🌟")
    st.write("Show some appreciation! Send a Kudo to a coworker who helped you out or did an awesome job.")

    # 1. Clean up the Kudos column so we can do math on it
    # (Converts blanks/NaNs to 0, and ensures they are numbers)
    df['Kudos'] = pd.to_numeric(df['Kudos'], errors='coerce').fillna(0).astype(int)

    # 2. Filter out the current user (you can't give yourself a Kudo!)
    other_users = df[(df['First Name'] != st_first_name.lower()) | (df['Last Name'] != st_last_name.lower())]

    if other_users.empty:
        st.info("You are the only one here! Invite some coworkers to give them Kudos.")
        return

    # Create a dictionary mapping the display name to the exact Excel row index
    # (This prevents bugs if someone has a two-word first name like "Mary Jane")
    coworker_dict = {}
    for idx, row in other_users.iterrows():
        display_name = f"{row['First Name'].title()} {row['Last Name'].title()}"
        coworker_dict[display_name] = idx

    st.write("### Send a Kudo 💌")
    
    # Use columns to put the dropdown and button side-by-side
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_coworker = st.selectbox("Who deserves a shoutout today?", ["-- Select a Coworker --"] + list(coworker_dict.keys()))
    
    with col2:
        st.write("") # Spacing to push the button down to align with the box
        st.write("")
        if st.button("Send Kudo! 🚀", type="primary"):
            if selected_coworker != "-- Select a Coworker --":
                # Find the exact person they selected using our dictionary
                target_idx = coworker_dict[selected_coworker]
                target_first = df.loc[target_idx, 'First Name']
                target_last = df.loc[target_idx, 'Last Name']
                current_kudos = df.loc[target_idx, 'Kudos']
                
                # Update the Excel file by adding 1 to their current score
                update_excel_record(df, target_first, target_last, "Kudos", current_kudos + 1)
                
                # Fun interactive feedback!
                st.success(f"Yay! You sent a Kudo to {selected_coworker}! 🎉")
                st.balloons()
                st.rerun()
            else:
                st.warning("Please select a coworker first.")

    st.divider()

    # 3. Leaderboard / Wall of Fame
    st.write("### 🏆 Kudos Leaderboard")
    
    # Sort dataframe by Kudos from highest to lowest
    leaderboard = df.sort_values(by="Kudos", ascending=False)
    
    # Grab only the people who have at least 1 Kudo, and take the top 3
    top_users = leaderboard[leaderboard['Kudos'] > 0].head(3)
    
    if top_users.empty:
        st.info("No Kudos have been given yet. Be the first to spread some joy!")
    else:
        # Create dynamic columns based on how many top users there are (up to 3)
        cols = st.columns(len(top_users))
        medals = ["🥇", "🥈", "🥉"]
        
        # Display the leaderboard using Streamlit's built-in Metric UI
        for i, (index, row) in enumerate(top_users.iterrows()):
            with cols[i]:
                st.metric(
                    label=f"{medals[i]} {row['First Name'].title()} {row['Last Name'].title()}",
                    value=f"{row['Kudos']} 🌟"
                )


# Skill Shop page        
def show_Skill_Shop_page(df, st_first_name, st_last_name):
    st.title("Skill Shop 🛠️")
    st.write("Welcome to the Skill Shop! Share a skill you can teach others, or browse what your coworkers are offering.")
    
    # 1. Find the current user's record
    user_record = df[(df['First Name'] == st_first_name.lower()) & (df['Last Name'] == st_last_name.lower())]
    
    if user_record.empty:
        st.error("Could not find your profile. Please go back to the Profile page.")
        return
        
    current_skill = user_record.iloc[0]['Skill']
    
    # 2. Check if the user has already added a skill
    has_skill = pd.notna(current_skill) and str(current_skill).strip().lower() not in ["", "nan"]
    
    st.divider()
    
    # --- SECTION 1: ADD / UPDATE YOUR SKILL ---
    st.subheader("Your Offered Skill")
    
    if not has_skill:
        st.info("You haven't listed a skill yet. What's something you're good at that you could teach a coworker?")
        
        # Form to submit a new skill
        with st.form("skill_form"):
            new_skill = st.text_input("I can teach someone how to...", placeholder="e.g., Use Pivot Tables, Bake sourdough, Write Python scripts")
            submit_skill = st.form_submit_button("Add to Skill Shop")
            
            if submit_skill:
                if new_skill.strip():
                    # Save to Excel
                    update_excel_record(df, st_first_name, st_last_name, "Skill", new_skill.strip())
                    st.success("Skill added! 🌟")
                    st.rerun()
                else:
                    st.warning("Please enter a skill before submitting.")
    else:
        st.success(f"**You are currently offering to teach:** {current_skill}")
        
        # Allow them to change their skill
        with st.expander("Update your skill"):
            with st.form("update_skill_form"):
                updated_skill = st.text_input("Change your skill to:", value=current_skill)
                update_btn = st.form_submit_button("Update Skill")
                
                if update_btn:
                    if updated_skill.strip():
                        update_excel_record(df, st_first_name, st_last_name, "Skill", updated_skill.strip())
                        st.success("Skill updated! 🌟")
                        st.rerun()
                    else:
                        # If they leave it blank, we can clear it
                        update_excel_record(df, st_first_name, st_last_name, "Skill", "")
                        st.rerun()

    st.divider()

    # --- SECTION 2: BROWSE COWORKERS' SKILLS ---
    st.subheader("Browse the Shop 🛒")
    
    # Filter the dataframe to only include people who have listed a skill
    # We use a lambda function to check that the skill is not empty and not "nan"
    shop_df = df[df['Skill'].apply(lambda x: pd.notna(x) and str(x).strip().lower() not in ["", "nan"])]
    
    # Filter out the current user so they don't see their own skill in the shop
    shop_df = shop_df[(shop_df['First Name'] != st_first_name.lower()) | (shop_df['Last Name'] != st_last_name.lower())]
    
    if shop_df.empty:
        st.info("The shop is currently empty. Be the first to offer a skill, or invite your coworkers to add theirs!")
    else:
        # Display skills in a nice grid format using Streamlit columns
        # We'll create rows of 2 columns
        for i in range(0, len(shop_df), 2):
            cols = st.columns(2)
            
            # First column
            with cols[0]:
                row1 = shop_df.iloc[i]
                name1 = f"{row1['First Name'].title()} {row1['Last Name'].title()}"
                skill1 = row1['Skill']
                
                # Using a container with a border to make it look like a "card"
                with st.container(border=True):
                    st.markdown(f"**{name1}**")
                    st.write(f"🧠 Can teach: *{skill1}*")
                    
            # Second column (if there is a second item in this row)
            if i + 1 < len(shop_df):
                with cols[1]:
                    row2 = shop_df.iloc[i+1]
                    name2 = f"{row2['First Name'].title()} {row2['Last Name'].title()}"
                    skill2 = row2['Skill']
                    
                    with st.container(border=True):
                        st.markdown(f"**{name2}**")
                        st.write(f"🧠 Can teach: *{skill2}*")

   
# Caption This Page (Using an API!)
def show_Caption_This_page(st_first_name):
    st.title("Caption This! 📸")
    st.write(f"Hey {st_first_name.title()}, take a quick brain break! Fetch a random photo and give it your best meme caption.")

    # 1. Initialize session state to remember the image so it doesn't disappear
    if 'meme_image_url' not in st.session_state:
        st.session_state.meme_image_url = None
        st.session_state.current_caption = ""

    # 2. Button to call the API
    if st.button("🐶 Fetch a Random Photo", type="primary"):
        try:
            # CALLING THE API!
            response = requests.get("https://dog.ceo/api/breeds/image/random")
            data = response.json() # Convert the response to a dictionary
            
            # Save the image URL to session state
            st.session_state.meme_image_url = data['message']
            st.session_state.current_caption = "" # Reset the caption for the new image
        except:
            st.error("Oops! The API is taking a nap. Try again later.")

    # 3. If we successfully fetched an image, display it!
    if st.session_state.meme_image_url:
        st.divider()
        
        # Display the image
        st.image(st.session_state.meme_image_url, use_container_width=True)
        
        # 4. Input for the user to write a caption
        caption_input = st.text_input("Write your funny caption here:")
        
        if st.button("Submit Caption"):
            st.session_state.current_caption = caption_input
            
        # 5. Display the caption in big text like a meme!
        if st.session_state.current_caption:
            # Using HTML/Markdown to make the text big, centered, and colorful
            st.markdown(
                f"<h2 style='text-align: center; color: #FF4B4B; font-style: italic;'>&quot;{st.session_state.current_caption}&quot;</h2>", 
                unsafe_allow_html=True
            )
            st.balloons()

            
# Two truths and a lie page
def show_Two_truths_and_a_lie_page(df, st_first_name, st_last_name):
    st.title("Two Truths and a Lie 🤥")
    st.write("Can you spot the fake? Set up your own statements, then try to guess the lies of your coworkers!")

    # 1. Find the current user's record
    user_record = df[(df['First Name'] == st_first_name.lower()) & (df['Last Name'] == st_last_name.lower())]
    
    if user_record.empty:
        st.error("Could not find your profile. Please go back to the Profile page.")
        return
        
    current_truth_1 = user_record.iloc[0]['Truth 1']
    current_truth_2 = user_record.iloc[0]['Truth 2']
    current_lie = user_record.iloc[0]['Lie']
    
    # Check if the user has already set up their game
    has_setup_game = (pd.notna(current_truth_1) and str(current_truth_1).strip().lower() not in ["", "nan"] and
                      pd.notna(current_truth_2) and str(current_truth_2).strip().lower() not in ["", "nan"] and
                      pd.notna(current_lie) and str(current_lie).strip().lower() not in ["", "nan"])

    # --- SECTION 1: SET UP YOUR STATEMENTS ---
    with st.expander("📝 Set Up / Edit Your Statements", expanded=not has_setup_game):
        if has_setup_game:
            st.success("Your statements are set! Your coworkers can now try to guess your lie.")
            
        with st.form("truths_and_lie_form"):
            st.write("Enter two true statements about yourself, and one believable lie.")
            t1 = st.text_input("Truth 1:", value=current_truth_1 if pd.notna(current_truth_1) else "")
            t2 = st.text_input("Truth 2:", value=current_truth_2 if pd.notna(current_truth_2) else "")
            l1 = st.text_input("The Lie:", value=current_lie if pd.notna(current_lie) else "")
            
            submit_statements = st.form_submit_button("Save Statements")
            
            if submit_statements:
                if t1.strip() and t2.strip() and l1.strip():
                    update_excel_record(df, st_first_name, st_last_name, "Truth 1", t1.strip())
                    update_excel_record(df, st_first_name, st_last_name, "Truth 2", t2.strip())
                    update_excel_record(df, st_first_name, st_last_name, "Lie", l1.strip())
                    st.success("Statements saved! 🌟")
                    st.rerun()
                else:
                    st.warning("Please fill out all three fields before saving.")

    st.divider()

    # --- SECTION 2: PLAY THE GAME ---
    st.subheader("Play the Game 🎮")
    
    # Filter for users who have set up their game (all 3 fields are filled)
    playable_df = df[
        df['Truth 1'].apply(lambda x: pd.notna(x) and str(x).strip().lower() not in ["", "nan"]) &
        df['Truth 2'].apply(lambda x: pd.notna(x) and str(x).strip().lower() not in ["", "nan"]) &
        df['Lie'].apply(lambda x: pd.notna(x) and str(x).strip().lower() not in ["", "nan"])
    ]
    
    # Filter out the current user (you can't guess your own lie)
    playable_df = playable_df[(playable_df['First Name'] != st_first_name.lower()) | (playable_df['Last Name'] != st_last_name.lower())]
    
    if playable_df.empty:
        st.info("No coworkers have set up their statements yet. Remind them to fill out their profile!")
        return

    # Create a dictionary mapping display names to their row data
    coworker_dict = {}
    for _, row in playable_df.iterrows():
        display_name = f"{row['First Name'].title()} {row['Last Name'].title()}"
        coworker_dict[display_name] = row

    # Dropdown to select a coworker
    selected_coworker = st.selectbox("Select a coworker to play:", ["-- Select a Coworker --"] + list(coworker_dict.keys()))

    if selected_coworker != "-- Select a Coworker --":
        target_data = coworker_dict[selected_coworker]
        
        # Gather the statements
        statements = [
            {"text": target_data['Truth 1'], "is_lie": False},
            {"text": target_data['Truth 2'], "is_lie": False},
            {"text": target_data['Lie'], "is_lie": True}
        ]
        
        # We need to shuffle the statements so the lie isn't always last!
        # We use session state to keep the shuffle order consistent while the user is guessing
        session_key = f"ttl_order_{selected_coworker}"
        
        if session_key not in st.session_state:
            random.shuffle(statements)
            st.session_state[session_key] = statements
            # Keep track of if they guessed correctly for this specific coworker
            st.session_state[f"ttl_guessed_{selected_coworker}"] = False
            
        current_statements = st.session_state[session_key]
        has_guessed_correctly = st.session_state[f"ttl_guessed_{selected_coworker}"]

        st.write(f"### Which of these is {selected_coworker.split()[0]}'s lie?")
        
        if has_guessed_correctly:
            st.success(f"🎉 You got it! The lie was: **{target_data['Lie']}**")
            if st.button("Pick someone else"):
                st.rerun()
        else:
            # Display the statements as buttons
            for i, stmt in enumerate(current_statements):
                # We use a unique key for each button
                if st.button(stmt["text"], key=f"btn_{selected_coworker}_{i}", use_container_width=True):
                    if stmt["is_lie"]:
                        st.session_state[f"ttl_guessed_{selected_coworker}"] = True
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Nope, that one is true! Try again.")



# User Manual Profile Page
def show_User_Manual_Profile_page(df, st_first_name, st_last_name):
    st.title("User Manual 📖")
    st.write("A 'User Manual' helps coworkers understand how best to work with you. Fill out your manual and search for others to learn their working styles!")

    # 1. Find the current user's record
    user_record = df[(df['First Name'] == st_first_name.lower()) & (df['Last Name'] == st_last_name.lower())]
    
    if user_record.empty:
        st.error("Could not find your profile. Please go back to the Profile page.")
        return
        
    current_manual = user_record.iloc[0]['User Manual']
    
    # Check if the user has already filled out their manual
    has_manual = pd.notna(current_manual) and str(current_manual).strip().lower() not in ["", "nan"]

    # --- SECTION 1: YOUR USER MANUAL ---
    with st.expander("📝 Edit Your User Manual", expanded=not has_manual):
        if has_manual:
            st.success("Your User Manual is saved! Coworkers can now search for it.")
            
        with st.form("user_manual_form"):
            st.write("Complete the following sentence to help your team work better with you:")
            
            # The prompt for the user manual
            manual_input = st.text_area(
                "The best way to give me feedback is...", 
                value=current_manual if has_manual else "",
                placeholder="e.g., ...in writing first so I can process it, then scheduling a 1-on-1 to discuss.",
                height=150
            )
            
            submit_manual = st.form_submit_button("Save User Manual")
            
            if submit_manual:
                if manual_input.strip():
                    update_excel_record(df, st_first_name, st_last_name, "User Manual", manual_input.strip())
                    st.success("User Manual saved! 🌟")
                    st.rerun()
                else:
                    st.warning("Please enter your feedback preferences before saving.")

    st.divider()

    # --- SECTION 2: SEARCH COWORKERS' MANUALS ---
    st.subheader("Search Directory 🔍")
    
    # Filter the dataframe to only include people who have filled out their manual
    manual_df = df[df['User Manual'].apply(lambda x: pd.notna(x) and str(x).strip().lower() not in ["", "nan"])]
    
    # Filter out the current user (you don't need to search for your own manual)
    manual_df = manual_df[(manual_df['First Name'] != st_first_name.lower()) | (manual_df['Last Name'] != st_last_name.lower())]
    
    if manual_df.empty:
        st.info("No coworkers have filled out their User Manual yet. Be the first to set the trend!")
        return

    # Create a dictionary mapping display names to their manual text
    coworker_dict = {}
    for _, row in manual_df.iterrows():
        display_name = f"{row['First Name'].title()} {row['Last Name'].title()}"
        coworker_dict[display_name] = row['User Manual']

    # Searchable dropdown (selectbox in Streamlit is searchable by default!)
    selected_coworker = st.selectbox("Search for a coworker:", ["-- Select a Coworker --"] + sorted(list(coworker_dict.keys())))

    if selected_coworker != "-- Select a Coworker --":
        target_manual = coworker_dict[selected_coworker]
        
        # Display the selected coworker's manual in a nice card format
        st.write(f"### How to work with {selected_coworker.split()[0]}")
        
        with st.container(border=True):
            st.markdown(f"**The best way to give me feedback is...**")
            st.info(f"*{target_manual}*")

    
            
# ==========================================
# MAIN APP EXECUTION
# ==========================================

#initializing session state variables 
initializing_session()

# Loading data from excel file
df = load_data()

#Create the Sidebar
with st.sidebar:
    st.header("Navigation")
    # Create a radio button menu for the user to choose a page
    selected_page = st.radio("Go to:", ["Profile", "Guess Who", "Would You Rather", "Spin The Wheel", "Kudos", "Skill Shop", "Caption This", "Two truths and a lie", "User Manual Profile"], index=0)

    
# Initial View
st.title("Welcome to Mingle! 👋")
st.write("Turn coworkers into connections.")
st.image("team_banner.png", use_container_width=True
)

# Retrieving first name from session state
st_first_name = st.session_state.user_profile['first_name']
st_last_name = st.session_state.user_profile['last_name']

# Render Selected Page View
# Select Profile Page
if selected_page == "Profile":
    show_Profile_page(df, st_first_name)

# Ony show other pages when the person provides their name.
if st.session_state.user_profile['is_setup'] == False and  selected_page != "Profile":
    st.warning("🕵️‍♂️ We need to know who you are before we can unlock the rest of the app. Head over to the **Profile Page** first.")

# Select Guess Who Page
elif selected_page == "Guess Who":
    show_Guess_Who_page(df, st_first_name)

# Select Would You Rather Page
elif selected_page == "Would You Rather":
    show_Would_You_Rather_page(df, st_first_name, st_last_name )

# Select Spin The Wheel Page
elif selected_page == "Spin The Wheel":
    show_Spin_The_Wheel_page(st_first_name)

# Select Kudos Page
elif selected_page == "Kudos":
    show_Kudos_page(df, st_first_name, st_last_name)

# Select Skill Shop Page
elif selected_page == "Skill Shop":
    show_Skill_Shop_page(df, st_first_name, st_last_name)

# Select Caption This Page
elif selected_page == "Caption This":
    show_Caption_This_page(st_first_name)

# Select Two truths and a lie Page
elif selected_page == "Two truths and a lie":
    show_Two_truths_and_a_lie_page(df, st_first_name, st_last_name)

# Select User Manual Profile Page
elif selected_page == "User Manual Profile":
    show_User_Manual_Profile_page(df, st_first_name, st_last_name)


















    
