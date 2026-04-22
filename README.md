# 🤝 Mingle

---
    Title : “Mingle App"
    Author: "Marialda Cabral"
---

## Description
Mingle is an interactive Streamlit application designed to help team members break the ice, learn about each other's working styles, and build a stronger team culture.<br />

---

## ✨ Features

Mingle includes several mini-games and directories to help teams connect:

*   👤 **Profile:** Create a new profile and select your interests, or automatically log in if you're a returning user.
*   🕵️‍♀️ **Guess Who:** A mini-game where you guess which coworker matches a set of random interests.
*   🤔 **Would You Rather:** Answer fun dilemmas and see how the rest of your team voted.
*   🎡 **Spin The Wheel:** Generate random icebreaker questions for your next team meeting or coffee chat.
*   🌟 **Kudos:** A Wall of Fame where you can send appreciation and shoutouts to your coworkers.
*   🛠️ **Skill Shop:** A marketplace to offer skills you can teach, and browse what your coworkers are offering.
*   📸 **Caption This:** Take a brain break! Fetch a random dog photo (via the Dog CEO API) and give it your best meme caption.
*   🤥 **Two Truths and a Lie:** Set up your statements and try to guess the lies of your teammates.
*   📖 **User Manual Profile:** A searchable directory where coworkers share the best ways to communicate and give them feedback. <br /> 



---

## 🛠️ Tech Stack

*   **Frontend & Backend:** [Streamlit](https://streamlit.io/) (Python)
*   **Data Manipulation:** Pandas
*   **Data Storage:** Microsoft Excel (`.xlsx`) via `openpyxl`
*   **External APIs:** `requests` (Dog CEO API)

---

## 🚀 How to Run Locally

If you want to run this application on your own computer, follow these steps:

**1. Clone the repository**
```bash
git clone https://github.com/Marialdinha/Mingle-app.git
cd Mingle-app
```

**2. Install the required dependencies**
<br /> Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

**3. Run the Streamlit app**
```bash
streamlit run Mingle.py
```

---

## 🚀 How to Run on the web
To use the application directly in your browser without any installation, visit the live app here: <br /> <br /> 
[Mingle Web App](https://mingle-app-xykjfsuvyvepqjakxcljfd.streamlit.app/)

---

## 🔭 Future Improvements

As Mingle continues to grow, here are a few planned updates and optimizations for the next iteration:

* **Data Storage Optimization:** Transition the database format from an Excel file (`.xlsx`) to a CSV file (`.csv`) for faster read/write speeds and easier version control.
* **Enhanced "Guess Who" Logic:** 
  * Update the game algorithm to account for shared interests. Currently, if multiple coworkers have the exact same interest, the game only accepts the specific person it randomly selected in the background.
  * Add a filter to prevent the game from selecting the active user as the mystery coworker, ensuring no one is prompted to guess their own interests.
* **UI/UX Navigation:** Reorganize the sidebar menu to group the app's features into distinct categories, cleanly separating "Fun & Games" (e.g., Guess Who, Caption This) from "Team/Business Activities" (e.g., User Manual, Skill Shop, Kudos).

---

## 💡 Want to see how this app was built? 
Check out the [Project Development Log ](Project_Development_Log.pdf). <br />
It includes a step by step breakdown of my development methodology, the challenges I overcame (like optimizing Streamlit's UI limitations), and the exact AI prompts I used to generate features, integrate APIs, and set up the CI/CD pipeline."

