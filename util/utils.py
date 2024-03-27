from models import db, Profile
def add_user(email_id, first_name, last_name, phone_number, password):
    new_user = Profile(email_id=email_id, first_name=first_name, last_name=last_name,
                       phone_number=phone_number, password=password)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def del_user(user):
        db.session.delete(user)
        db.session.commit() 


def commit_changes():
    db.session.commit()
