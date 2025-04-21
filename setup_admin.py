import getpass
from models.db import app_engine
import models
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session

def setup_admin(option: str | None = None, username: str | None = None, password: str | None = None):
    if password:
        if len(password)<3 or len(password)>32:
            print("Password length must be from 3 to 32 characters")
            password = None
    while True:
        session: Session
        match option or input("Type a/r to add/remove an existing username, p to change password of an existing username, c to check all usernames, or x to exit: "):
            case "a":
                username = username or input("Enter Username to add: ")
                if not password:
                    while True:
                        password = getpass.getpass(f"Enter password for username {username}: ")
                        if len(password)<3 or len(password)>32:
                            print("Password length must be from 3 to 32 characters")
                            continue
                        if password == getpass.getpass(f"Confirm password: "):
                            break
                        print("Passwords do not match.")
                user = models.User(username=username, password_hash=generate_password_hash(password))
                with app_engine().Session() as session:
                    try:
                        session.add(user)
                        session.commit()
                        print(f"Added admin user {username}.")
                    except Exception as e:
                        session.rollback()
                        print(f"Error has occured:\n\t{e}")
            case "r":
                username = username or input("Enter Username to remove: ")
                with app_engine().Session() as session:
                    del_user = session.query(models.User).filter_by(username=username).one()
                    if del_user:
                        try:
                            session.delete(del_user)
                            session.commit()
                            print(f"Deleted admin user {username}.")
                        except Exception as e:
                            session.rollback()
                            print(f"Error has occured:\n\t{e}")
                    else:
                        print(f"Admin user {username} not found.")
            case "p":
                username = username or input("Enter Username to change password: ")
                with app_engine().Session() as session:
                    user = session.query(models.User).filter_by(username=username).one()
                    if not user:
                        print(f"Admin user {username} not found.")
                        break
                    if not password:
                        while True:
                            password = getpass.getpass("Enter password: ")
                            if len(password)<3 or len(password)>32:
                                print("Password length must be from 3 to 32 characters")
                                continue
                            if password == getpass.getpass("Confirm password: "):
                                break
                            print("Passwords do not match.")
                    try:
                        user.password_hash = generate_password_hash(password)
                        session.commit()
                        print(f"Changed password of admin user {username}.")
                    except Exception as e:
                        session.rollback()
                        print(f"Error has occured:\n\t{e}")
            case "c":
                session = app_engine().Session()
                all_users = session.query(models.User).all()
                if all_users:
                    print("Registered usernames:")
                    for user in all_users:
                        print(user.username)
                else:
                    print("No admins found in the database.")
            case "x":
                pass
            case _:
                continue
        break

if __name__ == "__main__":
    setup_admin()
    