from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import date

from faker import Faker


fake = Faker()


@dataclass(frozen=True)
class ConditionProfile:
    condition: str
    complaints: tuple[str, ...]
    medications: tuple[str, ...]
    advice: tuple[str, ...]


CONDITION_PROFILES = (
    ConditionProfile(
        "Upper respiratory infection",
        ("Fever", "Cough", "Sore throat", "Runny nose", "Fatigue"),
        ("Paracetamol", "Cetirizine", "Cough syrup", "Azithromycin"),
        ("Hydration", "Steam inhalation", "Review if fever persists"),
    ),
    ConditionProfile(
        "Hypertension follow-up",
        ("Headache", "Dizziness", "Fatigue", "Palpitations"),
        ("Amlodipine", "Losartan", "Metoprolol", "Hydrochlorothiazide"),
        ("Low-salt diet", "BP log for 7 days", "Follow up in 2 weeks"),
    ),
    ConditionProfile(
        "Type 2 diabetes review",
        ("Excessive thirst", "Frequent urination", "Tiredness", "Blurred vision"),
        ("Metformin", "Glimepiride", "Insulin", "Vitamin B12"),
        ("Check fasting glucose", "Foot care advice", "Dietician referral"),
    ),
    ConditionProfile(
        "Gastritis",
        ("Acidity", "Heartburn", "Nausea", "Abdominal pain", "Bloating"),
        ("Pantoprazole", "Ondansetron", "Antacid syrup", "Sucralfate"),
        ("Avoid spicy food", "Small frequent meals", "Review in 5 days"),
    ),
    ConditionProfile(
        "Musculoskeletal pain",
        ("Back pain", "Joint pain", "Muscle spasm", "Shoulder pain"),
        ("Ibuprofen", "Diclofenac gel", "Paracetamol", "Calcium carbonate"),
        ("Rest", "Warm compress", "Physiotherapy if persistent"),
    ),
)

ALLERGIES = (
    "No known allergies",
    "Penicillin",
    "Amoxicillin",
    "NSAIDs",
    "Ibuprofen",
    "Aspirin",
    "Sulfa drugs",
    "Latex",
    "Contrast dye",
)

INSURANCE_PROVIDERS = (
    "Blue Insurance",
    "HealthSure",
    "MediCover",
    "CarePlus",
    "SafeLife Health",
    "WellnessCo",
    "MediTrust",
    "PrimeCare",
    "Self pay",
)


def _age_from_dob(dob: date) -> int:
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def _safe_medications(profile: ConditionProfile, allergy: str) -> list[str]:
    choices = list(profile.medications)
    allergy_key = allergy.lower()

    filtered = [med for med in choices if allergy_key not in med.lower()]
    if allergy_key == "penicillin":
        filtered = [med for med in filtered if "amoxicillin" not in med.lower()]
    if allergy_key == "nsaids":
        filtered = [med for med in filtered if med.lower() not in {"ibuprofen", "aspirin"}]

    if not filtered:
        filtered = ["Paracetamol"]

    return random.sample(filtered, k=min(random.randint(1, 3), len(filtered)))


def generate_fake_patient() -> dict[str, str | int]:
    profile = random.choice(CONDITION_PROFILES)
    dob = fake.date_of_birth(minimum_age=18, maximum_age=85)
    allergy = random.choice(ALLERGIES)
    medications = _safe_medications(profile, allergy)
    complaints = random.sample(profile.complaints, k=min(random.randint(1, 3), len(profile.complaints)))

    return {
        "name": fake.name(),
        "date_of_birth": dob.strftime("%Y-%m-%d"),
        "age": _age_from_dob(dob),
        "condition": profile.condition,
        "complaints": ", ".join(complaints),
        "allergies": allergy,
        "medications": ", ".join(medications),
        "insurance": random.choice(INSURANCE_PROVIDERS),
        "doctor": f"Dr. {fake.last_name()}",
        "visit_date": fake.date_between(start_date="-30d", end_date="today").strftime("%Y-%m-%d"),
        "advice": random.choice(profile.advice),
    }


def patient_to_lines(patient: dict[str, str | int], form_type: str = "Prescription Form") -> list[str]:
    if form_type == "Patient Intake Form":
        return [
            f"Name: {patient['name']}",
            f"DOB: {patient['date_of_birth']}   Age: {patient['age']}",
            f"Reason: {patient['complaints']}",
            f"Allergies: {patient['allergies']}",
            f"Insurance: {patient['insurance']}",
            f"Date: {patient['visit_date']}",
        ]

    if form_type == "Lab Request Form":
        return [
            f"Patient: {patient['name']}",
            f"DOB: {patient['date_of_birth']}   Age: {patient['age']}",
            f"Clinical note: {patient['condition']}",
            f"Symptoms: {patient['complaints']}",
            "Tests: CBC, FBS, HbA1c, Urine routine",
            f"Requested by: {patient['doctor']}",
        ]

    return [
        f"Name: {patient['name']}",
        f"DOB: {patient['date_of_birth']}   Age: {patient['age']}",
        f"Complaint: {patient['complaints']}",
        f"Diagnosis: {patient['condition']}",
        f"Rx: {patient['medications']}",
        f"Advice: {patient['advice']}",
    ]
