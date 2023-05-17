import pickle
from pathlib import Path
import streamlit_authenticator as stauth

names = ["Przemysław Zych", "Szymon Wiśniewski"]
usernames = ["pzych", "swisniewski"]
passwords = ["lab1916", "lab1916"]

hashed_passwords = stauth.Hasher (passwords).generate()
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)

    