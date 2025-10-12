from faker import Faker
import random

fake = Faker()

# List of possible complaints
complaints_list = [
    "Fever", "Headache", "Cold", "Cough", "Sore Throat",
    "Body Pain", "Fatigue", "Nausea", "Vomiting", "Abdominal Pain",
    "Breathing Difficulty", "Joint Pain", "Swelling", "Skin Rash",
    "Itching", "Dizziness", "Weakness", "Chest Pain", "Palpitations",
    "Loss of Appetite", "Back Pain", "Neck Pain", "Ear Pain",
    "Toothache", "Runny Nose", "Sneezing", "Eye Irritation",
    "Blurred Vision", "Burning Sensation", "Constipation",
    "Diarrhea", "Acidity", "Heartburn", "Gas", "Bloating",
    "Urinary Pain", "Frequent Urination", "Loss of Consciousness",
    "Anxiety", "Depression", "Insomnia", "Weight Loss",
    "Weight Gain", "Tremors", "Bleeding", "Cramps",
    "Numbness", "Tingling Sensation", "Loss of Balance",
    "Memory Loss", "Confusion", "Dry Mouth", "Hoarseness",
    "Mouth Ulcers", "Nose Bleed", "Back Stiffness", "Shoulder Pain",
    "Muscle Spasm", "Pain While Walking", "Swollen Glands",
    "Difficulty Swallowing", "Change in Voice", "Excessive Sweating",
    "Cold Hands or Feet", "Yellowing of Eyes", "Dark Urine",
    "Loss of Taste", "Loss of Smell", "Chills", "Night Sweats",
    "Hair Loss", "Acne", "Dry Skin", "Sun Sensitivity",
    "Wound Not Healing", "Irregular Heartbeat", "Shortness of Breath",
    "Fainting", "Restlessness", "Irritability", "Decreased Urine Output",
    "Swelling of Legs", "Painful Menstruation", "Irregular Periods",
    "Excessive Thirst", "Blurred Speech", "Tiredness",
    "General Weakness", "Malaise", ""
]


# List of possible medications
medications_list = [
    # 🔹 Analgesics / Antipyretics
    "Paracetamol", "Ibuprofen", "Diclofenac", "Naproxen", "Aspirin",
    "Aceclofenac", "Tramadol", "Mefenamic Acid", "Ketorolac",

    # 🔹 Antibiotics
    "Amoxicillin", "Ciprofloxacin", "Azithromycin", "Doxycycline",
    "Cephalexin", "Cefixime", "Metronidazole", "Clarithromycin",
    "Amoxicillin-Clavulanate", "Levofloxacin",

    # 🔹 Antihistamines / Anti-allergic
    "Cetirizine", "Loratadine", "Fexofenadine", "Chlorpheniramine",
    "Levocetirizine", "Diphenhydramine", "Montelukast", "Desloratadine",

    # 🔹 Gastrointestinal
    "Ranitidine", "Omeprazole", "Pantoprazole", "Esomeprazole",
    "Rabeprazole", "Domperidone", "Ondansetron", "Metoclopramide",
    "Sucralfate", "Antacid Syrup",

    # 🔹 Respiratory
    "Salbutamol", "Budesonide Inhaler", "Levosalbutamol", "Theophylline",
    "Formoterol", "Ipratropium Bromide", "Cough Syrup", "Ambroxol",

    # 🔹 Cardiovascular
    "Nitroglycerin", "Amlodipine", "Losartan", "Metoprolol",
    "Atenolol", "Enalapril", "Clopidogrel", "Atorvastatin",
    "Furosemide", "Hydrochlorothiazide",

    # 🔹 Endocrine / Metabolic
    "Insulin", "Metformin", "Glimepiride", "Thyroxine", "Prednisolone",
    "Hydrocortisone", "Dexamethasone", "Methylprednisolone",

    # 🔹 Vitamins / Supplements
    "Iron Supplements", "Vitamin D", "Vitamin B12", "Folic Acid",
    "Calcium Carbonate", "Multivitamin", "Zinc Sulphate",

    # 🔹 Dermatological
    "Hydrocortisone Cream", "Clotrimazole Cream", "Miconazole",
    "Betamethasone Cream", "Neomycin Ointment", "Calamine Lotion",

    # 🔹 Neurological / Psychiatric
    "Diazepam", "Alprazolam", "Sertraline", "Fluoxetine",
    "Amitriptyline", "Gabapentin", "Pregabalin",

    # 🔹 Miscellaneous
    "ORS Solution", "Loperamide", "Paracetamol Syrup",
    "Eye Drops (Lubricant)", "Nasal Spray", "Pain Relief Gel", ""
]


# Allergies
allergies_list = [
    # 🔹 Common Responses
    "None", "Unknown", "No Known Allergies", "NKA",

    # 🔹 Drug Allergies
    "Penicillin", "Amoxicillin", "Cephalosporins", "Sulfa Drugs",
    "Aspirin", "NSAIDs", "Ibuprofen", "Codeine", "Morphine",
    "Paracetamol", "Erythromycin", "Tetracycline", "Insulin",
    "Local Anesthetics", "Lidocaine", "Carbamazepine",
    "Phenytoin", "Vancomycin",

    # 🔹 Food Allergies
    "Peanuts", "Tree Nuts", "Milk", "Eggs", "Soy", "Wheat",
    "Gluten", "Shellfish", "Seafood", "Fish", "Sesame",
    "Corn", "Strawberries", "Kiwi", "Banana",

    # 🔹 Environmental Allergies
    "Dust", "Pollen", "Mold", "Grass", "Animal Dander",
    "Cat Dander", "Dog Dander", "House Dust Mites",
    "Insect Stings", "Bee Venom", "Cockroach Allergen",

    # 🔹 Material / Contact Allergies
    "Latex", "Nickel", "Fragrance", "Detergents", "Dyes",
    "Formaldehyde", "Cosmetics", "Adhesive Tape",
    "Sunscreen", "Rubber",

    # 🔹 Others / Rare
    "Iodine", "Contrast Dye", "Acrylic", "Alcohol",
    "Preservatives", "Caffeine", "Vaccine Components", ""
]


# Insurance
insurance_list = [
    "Blue Insurance", "HealthSure", "MediCover", "CarePlus",
    "SafeLife Health", "WellnessCo", "MediTrust", "PrimeCare",
    "HealthGuard", "CureShield", "LifeSecure", "VitalOne",
    "NovaHealth", "Apex Insurance", "TruHealth", "ProCare",
    "AssureLife", "Guardian Health", "OptiCare", "Medisure",
    "Pioneer Health", "Harbor Health", "SummitCare", "Everwell Insurance",
    "BrightPath Health", "CrestaCare", "Horizon Health", "Zenith Health Plans",
    "Silverline Insurance", "Rosewood Health", "Pillar Health", "Nimbus Care",
    "Cobalt Health", "SageWell Insurance", "MapleCare", "Orchid Health",
    "Beacon Health", "Meridian Insurance", "Willow Health", "Cascade Care",
    ""
]

def generate_fake_patient():
    # Random number of complaints (1–3), join as string
    complaints = ", ".join(random.sample(complaints_list, k=random.randint(1,3)))
    # Random number of medications (1–3), join as string
    medications = ", ".join(random.sample(medications_list, k=random.randint(1,3)))
    
    return [
        fake.name(),
        fake.date_of_birth(minimum_age=18, maximum_age=85).strftime("%Y-%m-%d"),
        complaints,       # comma-separated string
        random.choice(allergies_list),
        medications,      # comma-separated string
        random.choice(insurance_list)
    ]

# Generate multiple patients
# n = 10000
# patients_list_of_lists = [generate_fake_patient() for _ in range(n)]

# # Display
# for patient in patients_list_of_lists:
#     print(patient)
