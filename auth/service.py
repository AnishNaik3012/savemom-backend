from sqlalchemy.orm import Session
from model import User, Role
from db import SessionLocal
import uuid

def get_user_roles(identifier: str):
    db = SessionLocal()
    try:
        users = db.query(User).filter(
            ((User.email == identifier) | (User.phone == identifier)),
            (User.isDeleted == False) | (User.isDeleted == None)
        ).all()
        
        # Return list of roles with their names and IDs
        roles = []
        for u in users:
            if u.role:
                roles.append({"role_id": str(u.role.id), "role_name": u.role.name})
            else:
                roles.append({"role_id": None, "role_name": "User"})
        return roles
    finally:
        db.close()

def is_new_user(identifier: str) -> bool:
    db = SessionLocal()
    try:
        user = db.query(User).filter(
            ((User.email == identifier) | (User.phone == identifier)),
            (User.isDeleted == False) | (User.isDeleted == None)
        ).first()
        return user is None
    finally:
        db.close()

def get_all_roles():
    db = SessionLocal()
    try:
        roles = db.query(Role).all()
        # Seed if empty for demo
        if not roles:
            default_roles = ["Mother", "Father", "Doctor", "Lab"]
            for name in default_roles:
                new_role = Role(name=name, permissions=[])
                db.add(new_role)
            db.commit()
            roles = db.query(Role).all()
        
        return [{"role_id": str(r.id), "role_name": r.name} for r in roles]
    finally:
        db.close()

def register_user(identifier: str, role_id: str, name: str = None):
    db = SessionLocal()
    try:
        # Check if this email+role already exists (even if deleted)
        existing = db.query(User).filter(
            ((User.email == identifier) | (User.phone == identifier)),
            User.roleId == uuid.UUID(role_id)
        ).first()
        
        if existing:
            # If it was deleted, "undelete" it
            if existing.isDeleted:
                existing.isDeleted = False
                db.commit()
                db.refresh(existing)
            return existing

        new_user = User(
            id=uuid.uuid4(),
            email=identifier if "@" in identifier else None,
            phone=identifier if "@" not in identifier else None,
            roleId=uuid.UUID(role_id),
            name=name or identifier.split('@')[0],
            isDeleted=False
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    finally:
        db.close()

def unsubscribe_user_db(email: str):
    db = SessionLocal()
    try:
        # Sanitize just in case
        email = email.strip().lower()
        users = db.query(User).filter(User.email == email).all()
        for user in users:
            user.isUnsubscribed = True
        db.commit()
    finally:
        db.close()

def is_user_unsubscribed(email: str) -> bool:
    db = SessionLocal()
    try:
        # Sanitize just in case
        email = email.strip().lower()
        # Use a more robust check for boolean in SQLite (1 or True)
        user = db.query(User).filter(
            User.email == email, 
            (User.isUnsubscribed == True) | (User.isUnsubscribed == 1)
        ).first()
        return user is not None
    finally:
        db.close()

