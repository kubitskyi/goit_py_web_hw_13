from datetime import date, timedelta

from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import extract

from src.database.models import Contact, User
from src.schemas import ContactSchema, ContactBirthday


async def create_contact(body: ContactSchema, db: Session, user: User):
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_contacts(limit: int, offset: int, db: Session, user: User):
    contacts = db.query(Contact).filter(and_(Contact.user_id == user.id)).limit(limit).offset(offset).all()
    return contacts


async def get_contact(contact_id: int, db: Session, user: User):
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    return contact


async def update_contact(body: ContactSchema, contact_id: int, db: Session, user: User):
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional_info = body.additional_info
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session, user: User):
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(query: str, db: Session, user: User):
    contacts = db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            (
                (Contact.first_name.contains(query)) |
                (Contact.last_name.contains(query)) |
                (Contact.email.contains(query))
            )
        )
    ).all()
    return contacts


async def get_birthdays_week(db: Session, user: User):
    today = date.today()
    end_date = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
        (Contact.user_id == user.id) &
        (extract('month', Contact.birthday) == today.month) & (extract('day', Contact.birthday) >= today.day)
        & (extract('month', Contact.birthday) == end_date.month) & (extract('day', Contact.birthday) <= end_date.day)
    ).all()
    return [
        ContactBirthday(
            id=contact.id,
            first_name=contact.first_name,
            last_name=contact.last_name,
            birthday=contact.birthday
        )
        for contact in contacts
    ]