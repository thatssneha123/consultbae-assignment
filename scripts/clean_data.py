import re
import pandas as pd


def clean_name(name):
    if pd.isna(name):
        return None
    return " ".join(str(name).strip().title().split())


def clean_email(email):
    if pd.isna(email):
        return None
    return str(email).strip().lower()


def clean_phone(phone):
    if pd.isna(phone):
        return None

    phone = str(phone)

    # Keep digits only
    phone = re.sub(r"\D", "", phone)

    # Remove country code if present
    if phone.startswith("91") and len(phone) > 10:
        phone = phone[-10:]

    return phone


def clean_city(city):
    if pd.isna(city):
        return None
    return str(city).strip().title()


def clean_status(status):
    if pd.isna(status):
        return None
    return str(status).strip().title()


def clean_verified(value):
    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    return value in ["y", "yes", "true", "1"]


def clean_skills(skills):
    if pd.isna(skills):
        return None

    items = [s.strip().title() for s in str(skills).split(",")]

    return ", ".join(sorted(set(items)))