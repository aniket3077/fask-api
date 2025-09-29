#!/usr/bin/env python3
"""
Breed Information Database

This module contains detailed information about different cattle and buffalo breeds
including nutrition planning, disease control, and genetic improvement strategies.
"""

from pathlib import Path

def _list_dataset_breeds():
    """
    Scan the dataset directory and return all breed names (top-level folders).

    Returns:
        list[str]: Breed names derived from folder names in 'Indian_bovine_breeds'.
    """
    base_dir = Path(__file__).resolve().parent
    dataset_dir = base_dir / "Indian_bovine_breeds"
    if not dataset_dir.is_dir():
        return []
    return sorted([p.name for p in dataset_dir.iterdir() if p.is_dir()])

def _default_info_template(breed_name: str):
    """
    Fallback info used when a breed has no curated entry.
    """
    return {
        "origin": "Unknown",
        "type": "Unknown",
        "description": f"Information for {breed_name.replace('_', ' ')} is not yet curated. Showing general guidance.",
        "nutrition_planning": {
            "forage_requirements": "60-70% green fodder, 30-40% dry fodder",
            "concentrate_feed": "Based on production level and body weight",
            "minerals": "Balanced mineral mix with salt licks",
            "water_intake": "Ad libitum access to clean water",
            "feeding_schedule": "2-3 times daily as per local practice"
        },
        "disease_control": {
            "common_diseases": ["Mastitis", "FMD", "Tick-borne diseases"],
            "vaccination_schedule": "Follow local veterinary schedule for bovines",
            "preventive_measures": "Clean housing, regular deworming, routine vet checks",
            "quarantine_period": "21-30 days for new animals"
        },
        "genetic_improvement": {
            "breeding_objectives": "Production, fertility, disease resistance, adaptability",
            "selection_criteria": "Production records, conformation, health",
            "breeding_methods": "Artificial insemination with proven bulls or natural",
            "performance_records": "Maintain production and health records"
        }
    }

BREED_INFO_OVERRIDES = {
    "Amritmahal": {
        "origin": "Karnataka, India",
        "type": "Draft",
        "description": "A majestic and powerful draft breed, renowned for its endurance and speed. They have a compact frame, long horns, and are typically grey in color. Historically used for transporting army supplies.",
        "nutrition_planning": {
            "forage_requirements": "Primarily dry fodder and grazing on sparse vegetation",
            "concentrate_feed": "1-2 kg per day during heavy work seasons",
            "minerals": "Salt licks and area-specific mineral mixtures are crucial for bone strength",
            "water_intake": "40-60 liters per day, increased during work",
            "feeding_schedule": "2 times daily with ample rest"
        },
        "disease_control": {
            "common_diseases": ["Foot and Mouth Disease (FMD)", "Tick-borne illnesses"],
            "vaccination_schedule": "Annual FMD vaccination is critical",
            "preventive_measures": "Regular deworming, tick control, and hoof care",
            "quarantine_period": "21 days for new animals"
        },
        "genetic_improvement": {
            "breeding_objectives": "Enhancing draft capacity, endurance, and breed purity",
            "selection_criteria": "Selection based on conformation, leg strength, and stamina",
            "breeding_methods": "Primarily natural service with government-approved bulls",
            "performance_records": "Tracking work output and endurance"
        }
    },
    "Ayrshire": {
        "origin": "County of Ayr, Scotland",
        "type": "Dairy",
        "description": "A hardy and efficient dairy breed, known for its excellent grazing ability and high-quality milk with ideal fat and protein content. Typically reddish-brown and white.",
        "nutrition_planning": {
            "forage_requirements": "High-quality pasture and silage",
            "concentrate_feed": "3-5 kg per day, balanced for protein and energy based on milk yield",
            "minerals": "Balanced dairy mineral mix with high calcium and phosphorus",
            "water_intake": "100-140 liters per day",
            "feeding_schedule": "Total Mixed Ration (TMR) or concentrate feeding during milking"
        },
        "disease_control": {
            "common_diseases": ["Mastitis", "Lameness", "Metabolic disorders (milk fever, ketosis)"],
            "vaccination_schedule": "Comprehensive schedule for clostridial diseases, IBR, BVD",
            "preventive_measures": "Good udder hygiene, comfortable housing, and nutritional management",
            "quarantine_period": "30 days for new animals"
        },
        "genetic_improvement": {
            "breeding_objectives": "High milk yield, udder health, longevity, and feed efficiency",
            "selection_criteria": "Genomic testing, milk production records, and conformation traits",
            "breeding_methods": "Widespread use of artificial insemination with globally proven sires",
            "performance_records": "Detailed milk recording and health event logging"
        }
    },
    "Banni": {
        "origin": "Kutch, Gujarat, India",
        "type": "Buffalo - Dairy",
        "description": "A hardy buffalo breed adapted to the arid, saline environment of the Kutch region. Known for its good milk production even under harsh climatic conditions.",
        "nutrition_planning": {
            "forage_requirements": "Thrives on local saline grasses and agricultural by-products",
            "concentrate_feed": "1-2 kg per day, supplemented during lactation",
            "minerals": "Mineral mixtures adapted for saline environments",
            "water_intake": "80-100 liters per day; can tolerate moderate salinity",
            "feeding_schedule": "Primarily night-time grazing and twice-daily feeding"
        },
        "disease_control": {
            "common_diseases": ["Parasitic infections", "FMD"],
            "vaccination_schedule": "Standard FMD and HS-BQ vaccinations",
            "preventive_measures": "Regular deworming and providing wallowing facilities",
            "quarantine_period": "21 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Improving milk yield, fat content, and adaptability to salinity",
            "selection_criteria": "Milk yield under stress, calving interval, and heat tolerance",
            "breeding_methods": "Selective breeding using community bulls and AI",
            "performance_records": "Milk recording by local dairy cooperatives"
        }
    },
    "Bargur": {
        "origin": "Tamil Nadu, India",
        "type": "Draft",
        "description": "A small, fiery, and aggressive draft breed found in the hilly regions of Bargur. Known for their speed and endurance on rough terrain. Brown coat with white markings.",
        "nutrition_planning": {
            "forage_requirements": "Primarily thrives on forest grazing and browsing",
            "concentrate_feed": "Minimal concentrate feed required, given only during heavy work",
            "minerals": "Natural salt licks in the forest terrain",
            "water_intake": "30-50 liters per day",
            "feeding_schedule": "Extensive grazing"
        },
        "disease_control": {
            "common_diseases": ["Very high resistance to local diseases due to minimal human intervention"],
            "vaccination_schedule": "Generally not vaccinated unless there is a major outbreak",
            "preventive_measures": "Natural immunity is very strong",
            "quarantine_period": "Not applicable in the traditional rearing system"
        },
        "genetic_improvement": {
            "breeding_objectives": "Conservation of the breed and maintaining its hardiness and draft ability",
            "selection_criteria": "Based on agility, temperament, and conformity to breed standards",
            "breeding_methods": "Natural selection within semi-wild herds",
            "performance_records": "Not systematically recorded"
        }
    },
    "Bhadawari": {
        "origin": "Uttar Pradesh & Madhya Pradesh, India",
        "type": "Buffalo - Dairy",
        "description": "Famous for having an exceptionally high butterfat content in its milk, ranging from 8% to over 13%. Copper-colored coat and arrow-head shaped horns.",
        "nutrition_planning": {
            "forage_requirements": "Efficient converter of coarse forages and agricultural by-products",
            "concentrate_feed": "2-3 kg/day for lactating animals",
            "minerals": "High calcium and energy supplements to support high-fat milk production",
            "water_intake": "90-120 liters per day, plus access to wallowing",
            "feeding_schedule": "Stall-fed with locally available greens and dry fodder"
        },
        "disease_control": {
            "common_diseases": ["Mastitis", "Parasitic infections"],
            "vaccination_schedule": "Regular FMD and HS-BQ vaccination",
            "preventive_measures": "Clean housing, regular health checks, and wallowing",
            "quarantine_period": "21-30 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "To increase milk yield while maintaining the ultra-high fat percentage",
            "selection_criteria": "Milk fat percentage, milk yield, and reproductive efficiency",
            "breeding_methods": "AI with progeny-tested bulls",
            "performance_records": "Milk and fat percentage recording"
        }
    },
    "Brown_Swiss": {
        "origin": "Switzerland",
        "type": "Dairy",
        "description": "A hardy, long-living dairy breed known for its excellent feet and legs, strong udder, and high-protein milk ideal for cheese making. Docile temperament.",
        "nutrition_planning": {
            "forage_requirements": "High intake capacity for quality forages like alfalfa and silage",
            "concentrate_feed": "4-6 kg/day for high-yielding cows",
            "minerals": "Balanced mix, with attention to protein-to-energy ratio",
            "water_intake": "100-150 liters per day",
            "feeding_schedule": "Total Mixed Ration (TMR) system is ideal"
        },
        "disease_control": {
            "common_diseases": ["Mastitis", "Lameness"],
            "vaccination_schedule": "Standard dairy vaccination protocols",
            "preventive_measures": "Hoof care, comfortable stalls, and good milking hygiene",
            "quarantine_period": "30 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Milk protein content, longevity, foot and leg strength",
            "selection_criteria": "Genomic selection for health traits and milk components",
            "breeding_methods": "Artificial insemination with internationally ranked sires",
            "performance_records": "Detailed recording of milk components, health, and fertility"
        }
    },
    "Gir": {
        "origin": "Gujarat, India",
        "type": "Dairy",
        "description": "One of the principal Zebu dairy breeds of India, known for its high milk production and disease resistance.",
        "nutrition_planning": {
            "forage_requirements": "60-70% green fodder, 30-40% dry fodder",
            "concentrate_feed": "2-3 kg per day for lactating cows",
            "minerals": "Calcium, Phosphorus, Salt, and trace minerals",
            "water_intake": "80-120 liters per day",
            "feeding_schedule": "3-4 times daily with fresh water always available"
        },
        "disease_control": {
            "common_diseases": ["Mastitis", "Foot and Mouth Disease", "Tick-borne diseases"],
            "vaccination_schedule": "Annual FMD vaccination, regular deworming",
            "preventive_measures": "Regular health checkups, clean housing, proper sanitation",
            "quarantine_period": "21 days for new animals"
        },
        "genetic_improvement": {
            "breeding_objectives": "High milk yield, disease resistance, heat tolerance",
            "selection_criteria": "Milk production records, conformation, health status",
            "breeding_methods": "Artificial insemination with proven bulls",
            "performance_records": "Maintain detailed milk yield and health records"
        }
    },
    "Dangi": {
        "origin": "Maharashtra & Gujarat, India",
        "type": "Draft",
        "description": "A distinct draft breed well-adapted to heavy rainfall and hilly rice paddy regions. Secretes an oily substance that protects it from rain and insects.",
        "nutrition_planning": {
            "forage_requirements": "Thrives on low-quality grazing and paddy straw",
            "concentrate_feed": "1-1.5 kg/day during peak working season",
            "minerals": "Salt and mineral blocks",
            "water_intake": "40-60 liters per day",
            "feeding_schedule": "Grazing supplemented with stall feeding"
        },
        "disease_control": {
            "common_diseases": ["Highly resistant to diseases in high-rainfall areas, including foot rot"],
            "vaccination_schedule": "FMD vaccination",
            "preventive_measures": "Natural resistance is high",
            "quarantine_period": "21 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Maintaining draft power for paddy cultivation and disease resistance",
            "selection_criteria": "Work capacity in wet conditions, conformation",
            "breeding_methods": "Natural service with selected local bulls",
            "performance_records": "Not systematically recorded"
        }
    },
    "Deoni": {
        "origin": "Maharashtra & Karnataka, India",
        "type": "Dual Purpose",
        "description": "A popular dual-purpose breed, resembling the Gir. Known for its good milk production and excellent draft capacity. Docile temperament makes them easy to handle.",
        "nutrition_planning": {
            "forage_requirements": "60-70% green fodder, 30-40% dry fodder",
            "concentrate_feed": "2-3 kg/day for lactating or working animals",
            "minerals": "Balanced mineral mixture",
            "water_intake": "70-100 liters per day",
            "feeding_schedule": "Twice or thrice daily feeding"
        },
        "disease_control": {
            "common_diseases": ["Mastitis", "Tick-borne diseases"],
            "vaccination_schedule": "Regular FMD vaccination and deworming",
            "preventive_measures": "Clean housing, tick control",
            "quarantine_period": "21 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "To balance both milk yield and draft power",
            "selection_criteria": "Milk production, bullock work capacity, and conformation",
            "breeding_methods": "Artificial insemination with dual-purpose bulls",
            "performance_records": "Milk and work performance recording"
        }
    },
    "Guernsey": {
        "origin": "Isle of Guernsey, Channel Islands",
        "type": "Dairy",
        "description": "Famous for its rich, golden-colored milk, which is high in butterfat, protein, and Beta-carotene. Known as the 'Golden Guernsey.' Very docile.",
        "nutrition_planning": {
            "forage_requirements": "High-efficiency grazer, requires less feed than larger dairy breeds",
            "concentrate_feed": "3-4 kg/day, balanced for high component milk",
            "minerals": "Standard dairy mix",
            "water_intake": "80-120 liters per day",
            "feeding_schedule": "Pasture-based system with supplemental feeding"
        },
        "disease_control": {
            "common_diseases": ["Mastitis", "Milk fever"],
            "vaccination_schedule": "Standard dairy vaccination program",
            "preventive_measures": "Nutritional management to prevent metabolic issues",
            "quarantine_period": "30 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "High milk components (butterfat and protein), feed efficiency",
            "selection_criteria": "Milk component percentages, health traits",
            "breeding_methods": "Artificial insemination",
            "performance_records": "Milk component testing and recording"
        }
    },
    "Hallikar": {
        "origin": "Karnataka, India",
        "type": "Draft",
        "description": "A classic and powerful draft breed, known for its long, vertical horns and trotting ability. Famous for its use in the traditional sport of 'Hori Habba' (bull catching).",
        "nutrition_planning": {
            "forage_requirements": "Thrives on dry fodder and grazing",
            "concentrate_feed": "1.5-2.5 kg/day for working bullocks",
            "minerals": "Mineral licks",
            "water_intake": "50-80 liters per day",
            "feeding_schedule": "Twice daily feeding"
        },
        "disease_control": {
            "common_diseases": ["Very hardy and disease resistant", "FMD"],
            "vaccination_schedule": "Annual FMD vaccination",
            "preventive_measures": "Hoof care and regular deworming",
            "quarantine_period": "21 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Draft capacity, speed, and breed purity",
            "selection_criteria": "Conformation, horn shape, and performance in draft work/sports",
            "breeding_methods": "Natural service with champion bulls",
            "performance_records": "Performance in traditional sports is a key indicator"
        }
    },
    "Jaffrabadi": {
        "origin": "Gujarat, India",
        "type": "Buffalo - Dairy",
        "description": "One of the heaviest buffalo breeds, known for its massive build and high milk yield with good fat content. It has distinctive, drooping horns that curl at the tip.",
        "nutrition_planning": {
            "forage_requirements": "High intake of green fodder, legumes, and dry roughage",
            "concentrate_feed": "3-4 kg per day for lactating animals, rich in protein and energy",
            "minerals": "High requirement for calcium and phosphorus",
            "water_intake": "120-160 liters per day, with essential access to wallowing",
            "feeding_schedule": "Stall-fed with a focus on high-energy rations"
        },
        "disease_control": {
            "common_diseases": ["Metabolic disorders", "Mastitis", "FMD"],
            "vaccination_schedule": "Regular FMD and HS-BQ vaccinations",
            "preventive_measures": "Proper nutritional management, clean and spacious housing",
            "quarantine_period": "30 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Improving milk yield, fat content, and maintaining body size",
            "selection_criteria": "305-day milk yield, fat percentage, and body conformation",
            "breeding_methods": "Artificial insemination with progeny-tested superior bulls",
            "performance_records": "Maintained by dairy cooperatives and breeding farms"
        }
    },
    "Kangayam": {
        "origin": "Tamil Nadu, India",
        "type": "Draft",
        "description": "A strong and active draft breed known for its endurance and ability to thrive on minimal feeding. Bullocks are prized for their work capacity in dry agricultural lands.",
        "nutrition_planning": {
            "forage_requirements": "Thrives on sparse grazing and dry fodder like sorghum straw",
            "concentrate_feed": "Minimal concentrate (1-1.5 kg) required, only during heavy work",
            "minerals": "Salt licks are generally sufficient",
            "water_intake": "40-70 liters per day",
            "feeding_schedule": "Primarily grazing with supplemental feeding"
        },
        "disease_control": {
            "common_diseases": ["Extremely hardy with high tolerance to heat and drought-related stress"],
            "vaccination_schedule": "FMD vaccination in endemic areas",
            "preventive_measures": "Hoof care is important for working animals",
            "quarantine_period": "21 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Preservation of draft quality, endurance, and breed purity",
            "selection_criteria": "Work capacity, leg strength, and conformation",
            "breeding_methods": "Natural mating with bulls selected for their work performance",
            "performance_records": "Owners track work ability"
        }
    },
    "Kasargod": {
        "origin": "Kerala, India",
        "type": "Dual Purpose",
        "description": "A dwarf cattle breed, known for its small size and adaptability to the hot and humid climate of Kerala. Requires minimal feed and housing.",
        "nutrition_planning": {
            "forage_requirements": "Thrives on local grasses and kitchen waste. Very low feed requirement",
            "concentrate_feed": "Rarely given, except for lactating cows (0.5 kg/day)",
            "minerals": "Can subsist on available forage",
            "water_intake": "15-25 liters per day",
            "feeding_schedule": "Free-ranging or tethered grazing"
        },
        "disease_control": {
            "common_diseases": ["High resistance to local diseases"],
            "vaccination_schedule": "As per local veterinary advice, often minimal",
            "preventive_measures": "Natural hardiness is its main protection",
            "quarantine_period": "14 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Conservation of this unique dwarf genetic resource",
            "selection_criteria": "Size, adaptability, and milk yield relative to body size",
            "breeding_methods": "Community-based conservation efforts",
            "performance_records": "Maintained by conservation societies and universities"
        }
    },
    "Kenkatha": {
        "origin": "Uttar Pradesh & Madhya Pradesh, India",
        "type": "Draft",
        "description": "A small, sturdy draft breed adapted to the Bundelkhand region. Known for its agility and endurance in agricultural operations on small landholdings.",
        "nutrition_planning": {
            "forage_requirements": "Survives on grazing and dry fodder",
            "concentrate_feed": "Minimal, supplemented during the work season",
            "minerals": "Salt licks",
            "water_intake": "30-50 liters per day",
            "feeding_schedule": "Grazing with supplemental feeding"
        },
        "disease_control": {
            "common_diseases": ["Hardy and resistant to local ailments"],
            "vaccination_schedule": "FMD vaccination",
            "preventive_measures": "Basic deworming and care",
            "quarantine_period": "21 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Draft power and hardiness",
            "selection_criteria": "Work efficiency and conformation",
            "breeding_methods": "Natural service",
            "performance_records": "Not systematically maintained"
        }
    },
    "Kherigarh": {
        "origin": "Uttar Pradesh, India",
        "type": "Draft",
        "description": "A medium-sized, active, and swift draft breed. Known for its white coat and alert temperament. Bullocks are used for light plowing and transportation.",
        "nutrition_planning": {
            "forage_requirements": "Primarily grazing and agricultural by-products",
            "concentrate_feed": "1-2 kg/day for working bullocks",
            "minerals": "Area-specific mineral mixture",
            "water_intake": "40-60 liters per day",
            "feeding_schedule": "Grazing based"
        },
        "disease_control": {
            "common_diseases": ["Good resistance to tropical diseases"],
            "vaccination_schedule": "Regular FMD vaccination",
            "preventive_measures": "Regular health check-ups",
            "quarantine_period": "21 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Swiftness, draft ability, and breed conformation",
            "selection_criteria": "Speed, work endurance, and body structure",
            "breeding_methods": "Natural mating with selected bulls",
            "performance_records": "Not systematically recorded"
        }
    },
    "Khillari": {
        "origin": "Maharashtra & Karnataka, India",
        "type": "Draft",
        "description": "A powerful and spirited draft breed, closely resembling the Hallikar. Known for its speed, strength, and endurance, making it popular for farm work and bullock cart racing.",
        "nutrition_planning": {
            "forage_requirements": "Adapted to thrive on dry fodder and sparse grazing in drought-prone areas",
            "concentrate_feed": "1.5-2.5 kg/day for animals engaged in heavy work",
            "minerals": "Salt and mineral supplements",
            "water_intake": "50-80 liters per day",
            "feeding_schedule": "Twice daily stall feeding and grazing"
        },
        "disease_control": {
            "common_diseases": ["Very hardy and disease-resistant", "Hoof issues"],
            "vaccination_schedule": "Annual FMD vaccination is recommended",
            "preventive_measures": "Proper shoeing and hoof trimming for working bullocks",
            "quarantine_period": "21 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "To enhance draft power, speed, and endurance",
            "selection_criteria": "Performance in farm work and carting, conformation, and temperament",
            "breeding_methods": "Selection of bulls based on their performance and physical traits",
            "performance_records": "Performance in races and work is a key informal record"
        }
    },
    "Krishna_Valley": {
        "origin": "Karnataka & Maharashtra, India",
        "type": "Dual Purpose",
        "description": "A large and heavy draft breed, valued for its immense strength for plowing in black cotton soils. Cows are fair milkers.",
        "nutrition_planning": {
            "forage_requirements": "High intake of quality green and dry fodder, especially sorghum straw",
            "concentrate_feed": "2-3 kg/day for working animals",
            "minerals": "Supplementation is required to maintain large body size",
            "water_intake": "80-110 liters per day",
            "feeding_schedule": "Stall feeding is common"
        },
        "disease_control": {
            "common_diseases": ["FMD", "Respiratory infections"],
            "vaccination_schedule": "Comprehensive vaccination program",
            "preventive_measures": "Good housing and nutrition to maintain health",
            "quarantine_period": "30 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "To improve draft capacity and maintain milk yield",
            "selection_criteria": "Body size, draft power, and milk production",
            "breeding_methods": "AI and natural service with superior bulls",
            "performance_records": "Maintained by government farms"
        }
    },
    "Malnad_gidda": {
        "origin": "Karnataka, India",
        "type": "Dual Purpose",
        "description": "A dwarf cattle breed from the hilly, high-rainfall Malenadu region. It is known for its exceptional hardiness, disease resistance, and ability to thrive on forest grazing.",
        "nutrition_planning": {
            "forage_requirements": "Subsists almost entirely on natural grazing and browsing in forests",
            "concentrate_feed": "Not traditionally given",
            "minerals": "Obtained from natural vegetation",
            "water_intake": "15-25 liters per day",
            "feeding_schedule": "Free-ranging"
        },
        "disease_control": {
            "common_diseases": ["Extremely high immunity to local diseases, including tick-borne illnesses"],
            "vaccination_schedule": "Rarely practiced by traditional rearers",
            "preventive_measures": "Natural hardiness",
            "quarantine_period": "Not applicable in the traditional system"
        },
        "genetic_improvement": {
            "breeding_objectives": "Conservation and promoting its use in low-input organic farming",
            "selection_criteria": "Adaptability, reproductive efficiency, and milk quality (A2 milk)",
            "breeding_methods": "Community-led conservation programs",
            "performance_records": "Maintained by conservation organizations"
        }
    },
    "Mehsana": {
        "origin": "Gujarat, India",
        "type": "Buffalo - Dairy",
        "description": "A dairy buffalo breed developed from a cross between Murrah and Surti breeds. Known for good milk production, regularity in breeding, and a docile nature.",
        "nutrition_planning": {
            "forage_requirements": "Balanced mix of green and dry fodder",
            "concentrate_feed": "2.5-3.5 kg/day for lactating buffaloes",
            "minerals": "Balanced mineral mixture for dairy animals",
            "water_intake": "100-140 liters per day with access to wallowing",
            "feeding_schedule": "Stall-fed system is common in dairy cooperatives"
        },
        "disease_control": {
            "common_diseases": ["Mastitis", "Reproductive issues", "FMD"],
            "vaccination_schedule": "Regular vaccination for FMD, HS-BQ",
            "preventive_measures": "Clean milking practices, regular vet check-ups",
            "quarantine_period": "21-30 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "High milk yield, longer lactation period, and better reproductive efficiency",
            "selection_criteria": "Milk yield, calving interval, and fat content",
            "breeding_methods": "Extensive use of Artificial Insemination",
            "performance_records": "Detailed records maintained by Mehsana Dairy Union"
        }
    },
    "Nagori": {
        "origin": "Rajasthan, India",
        "type": "Draft",
        "description": "A famous draft breed from the Nagaur district, known for its large, powerful bullocks which are prized for their speed and endurance in agricultural work and transport.",
        "nutrition_planning": {
            "forage_requirements": "Thrives on dry fodder and desert grasses",
            "concentrate_feed": "1.5-2.5 kg/day for working animals",
            "minerals": "Salt licks and locally available mineral-rich soil",
            "water_intake": "40-70 liters per day",
            "feeding_schedule": "Twice daily feeding supplemented with grazing"
        },
        "disease_control": {
            "common_diseases": ["Highly resistant to drought and heat stress"],
            "vaccination_schedule": "Annual FMD vaccination",
            "preventive_measures": "Hoof care and deworming",
            "quarantine_period": "21 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Superior draft quality, speed, and endurance",
            "selection_criteria": "Performance in plowing and carting, conformation",
            "breeding_methods": "Selective breeding by farmers and at cattle fairs",
            "performance_records": "Informal records of work capacity"
        }
    },
    "Nagpuri": {
        "origin": "Maharashtra, India",
        "type": "Buffalo - Dual Purpose",
        "description": "A versatile buffalo breed from the Vidarbha region, also known as 'Berari'. Valued for both its milk and the strength of its bullocks for heavy draft work.",
        "nutrition_planning": {
            "forage_requirements": "Adapted to a wide variety of forages including coarse straws",
            "concentrate_feed": "1.5-2.5 kg/day depending on work/lactation status",
            "minerals": "Standard mineral supplements",
            "water_intake": "80-120 liters per day, with need for wallowing",
            "feeding_schedule": "Stall feeding combined with grazing"
        },
        "disease_control": {
            "common_diseases": ["Hardy and well-adapted to the local climate"],
            "vaccination_schedule": "Regular FMD and HS-BQ vaccinations",
            "preventive_measures": "Wallowing facilities to prevent heat stress",
            "quarantine_period": "21 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "To balance draft ability with milk production",
            "selection_criteria": "Work capacity of males and milk yield of females",
            "breeding_methods": "AI is being promoted, but natural service is common",
            "performance_records": "Maintained at government breeding farms"
        }
    },
    "Nili_Ravi": {
        "origin": "Punjab, Pakistan & India",
        "type": "Buffalo - Dairy",
        "description": "A high-yielding dairy buffalo breed, easily identified by its walled (blue) eyes and white markings on the face and legs. Known for its deep, massive frame.",
        "nutrition_planning": {
            "forage_requirements": "High intake of quality green fodder like berseem and lucerne",
            "concentrate_feed": "3-5 kg/day for high-yielding animals",
            "minerals": "High calcium and phosphorus for heavy milk production",
            "water_intake": "100-150 liters per day, with essential wallowing",
            "feeding_schedule": "Intensive stall-feeding systems"
        },
        "disease_control": {
            "common_diseases": ["Mastitis", "Metabolic disorders", "FMD"],
            "vaccination_schedule": "Comprehensive vaccination program",
            "preventive_measures": "Good hygiene, nutritional management, and comfortable housing",
            "quarantine_period": "30 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Maximizing milk yield and fat content",
            "selection_criteria": "305-day milk yield, fat percentage, and age at first calving",
            "breeding_methods": "Progeny testing and extensive use of AI with proven bulls",
            "performance_records": "Systematic recording by breeding associations"
        }
    },
    "Nimari": {
        "origin": "Madhya Pradesh, India",
        "type": "Draft",
        "description": "A hardy draft breed from the Nimar region, resulting from a mix of Gir and Khillari. Known for its agility and endurance, with a reddish coat and Gir-like forehead.",
        "nutrition_planning": {
            "forage_requirements": "Survives well on grazing and dry fodder",
            "concentrate_feed": "1-2 kg/day for working animals",
            "minerals": "Salt licks",
            "water_intake": "40-60 liters per day",
            "feeding_schedule": "Grazing with supplemental feeding"
        },
        "disease_control": {
            "common_diseases": ["Good disease resistance"],
            "vaccination_schedule": "FMD vaccination",
            "preventive_measures": "Basic animal husbandry practices",
            "quarantine_period": "21 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Draft power and hardiness",
            "selection_criteria": "Work capacity and conformation",
            "breeding_methods": "Natural service with selected bulls",
            "performance_records": "Not systematically recorded"
        }
    },
    "Pulikulam": {
        "origin": "Tamil Nadu, India",
        "type": "Draft / Sport",
        "description": "A strong, aggressive, and agile breed primarily used for the traditional sport of Jallikattu. Also used for draft purposes. Known for its fighting spirit.",
        "nutrition_planning": {
            "forage_requirements": "Grazing and dry fodder",
            "concentrate_feed": "Special high-energy feeds for bulls used in sport",
            "minerals": "Specific supplements to build muscle and strength",
            "water_intake": "50-80 liters per day",
            "feeding_schedule": "Specialized feeding schedule for sporting bulls"
        },
        "disease_control": {
            "common_diseases": ["Very hardy; prone to injury during sport"],
            "vaccination_schedule": "FMD and other essential vaccinations",
            "preventive_measures": "Proper training and care to prevent injuries",
            "quarantine_period": "21 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Agility, strength, and temperament for Jallikattu",
            "selection_criteria": "Performance in Jallikattu, conformation, and lineage",
            "breeding_methods": "Natural mating with champion Jallikattu bulls",
            "performance_records": "Performance in the sport is the primary record"
        }
    },
    "Rathi": {
        "origin": "Rajasthan, India",
        "type": "Dual Purpose",
        "description": "A milch breed from the arid regions of Rajasthan, known for its good milk production on low-input systems. Thrives in the desert environment.",
        "nutrition_planning": {
            "forage_requirements": "Efficiently utilizes desert grasses and shrubs",
            "concentrate_feed": "1.5-2.5 kg/day for lactating cows",
            "minerals": "Area-specific mineral mixture",
            "water_intake": "40-70 liters per day, adapted to water scarcity",
            "feeding_schedule": "Extensive grazing supplemented with stall feeding"
        },
        "disease_control": {
            "common_diseases": ["High tolerance to heat and drought stress"],
            "vaccination_schedule": "FMD vaccination",
            "preventive_measures": "Management practices to conserve water and feed",
            "quarantine_period": "21 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Improving milk yield while retaining hardiness",
            "selection_criteria": "Milk yield, calving interval, and drought resistance",
            "breeding_methods": "AI is being introduced to improve genetics",
            "performance_records": "Maintained by livestock development boards"
        }
    },
    "Red_Dane": {
        "origin": "Denmark",
        "type": "Dairy",
        "description": "A major dairy breed from Denmark, known for its high milk yield with good fat and protein content. Valued for its longevity and strong constitution.",
        "nutrition_planning": {
            "forage_requirements": "High-quality silage, hay, and pasture",
            "concentrate_feed": "4-6 kg/day for high producers",
            "minerals": "Balanced dairy mineral supplement",
            "water_intake": "100-150 liters per day",
            "feeding_schedule": "TMR system is common for this breed"
        },
        "disease_control": {
            "common_diseases": ["Mastitis", "Lameness", "Metabolic disorders"],
            "vaccination_schedule": "Comprehensive vaccination schedule for dairy cattle",
            "preventive_measures": "Excellent housing, nutrition, and hygiene management",
            "quarantine_period": "30-45 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "High lifetime milk production, fertility, and health",
            "selection_criteria": "Genomic testing, production records, health traits",
            "breeding_methods": "AI with internationally proven sires",
            "performance_records": "Detailed national database for all performance traits"
        }
    },
    "Sahiwal": {
        "origin": "Punjab, Pakistan & India",
        "type": "Dairy",
        "description": "Excellent tropical dairy breed known for high milk production and heat tolerance.",
        "nutrition_planning": {
            "forage_requirements": "65-75% green fodder, 25-35% dry fodder",
            "concentrate_feed": "2.5-3.5 kg per day for lactating cows",
            "minerals": "High calcium and phosphorus for milk production",
            "water_intake": "90-130 liters per day",
            "feeding_schedule": "4 times daily with mineral supplements"
        },
        "disease_control": {
            "common_diseases": ["Mastitis", "Brucellosis", "Tuberculosis"],
            "vaccination_schedule": "Regular vaccination against FMD, Brucellosis",
            "preventive_measures": "Milk testing, regular veterinary checkups",
            "quarantine_period": "30 days for new animals"
        },
        "genetic_improvement": {
            "breeding_objectives": "Milk yield, fat content, reproductive efficiency",
            "selection_criteria": "305-day milk yield, calving interval, conformation",
            "breeding_methods": "Proven bull semen, embryo transfer",
            "performance_records": "Detailed production and reproduction records"
        }
    },
    "Surti": {
        "origin": "Gujarat, India",
        "type": "Buffalo - Dairy",
        "description": "A medium-sized dairy buffalo breed known for its sickle-shaped horns and docile temperament. It is an efficient milk producer with good fat content.",
        "nutrition_planning": {
            "forage_requirements": "Efficient converter of fodder to milk",
            "concentrate_feed": "2-3 kg/day for lactating animals",
            "minerals": "Standard dairy mineral mix",
            "water_intake": "80-120 liters per day, with wallowing",
            "feeding_schedule": "Commonly managed by small and marginal farmers"
        },
        "disease_control": {
            "common_diseases": ["Good resistance to local diseases"],
            "vaccination_schedule": "Regular FMD and HS-BQ vaccination",
            "preventive_measures": "Cleanliness and regular health checks",
            "quarantine_period": "21 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Improving milk yield, fat percentage, and reproductive regularity",
            "selection_criteria": "Milk yield, age at first calving, fat content",
            "breeding_methods": "AI with proven bulls is actively promoted",
            "performance_records": "Maintained by dairy co-operatives"
        }
    },
    "Holstein_Friesian": {
        "origin": "Netherlands",
        "type": "Dairy",
        "description": "World's highest milk-producing dairy breed, widely used for commercial dairy farming.",
        "nutrition_planning": {
            "forage_requirements": "50-60% high-quality forage, 40-50% concentrates",
            "concentrate_feed": "4-6 kg per day for high-producing cows",
            "minerals": "Balanced mineral mix with emphasis on calcium",
            "water_intake": "100-150 liters per day",
            "feeding_schedule": "Total mixed ration (TMR) feeding system"
        },
        "disease_control": {
            "common_diseases": ["Mastitis", "Lameness", "Metabolic disorders"],
            "vaccination_schedule": "Comprehensive vaccination program",
            "preventive_measures": "Regular health monitoring, proper nutrition management",
            "quarantine_period": "45 days for new animals"
        },
        "genetic_improvement": {
            "breeding_objectives": "Maximum milk production, feed efficiency, longevity",
            "selection_criteria": "Milk yield, protein content, health traits",
            "breeding_methods": "Genomic selection, artificial insemination",
            "performance_records": "Comprehensive performance recording system"
        }
    },
    "Toda": {
        "origin": "Tamil Nadu, India",
        "type": "Buffalo - Dual Purpose",
        "description": "A semi-wild buffalo breed reared by the Toda tribal community in the Nilgiris. Known for its aggressive nature, hardiness, and rich milk.",
        "nutrition_planning": {
            "forage_requirements": "Exclusively thrives on natural grazing in the high-altitude grasslands",
            "concentrate_feed": "Not given",
            "minerals": "Obtained from natural vegetation",
            "water_intake": "Sourced from natural streams",
            "feeding_schedule": "Free-ranging"
        },
        "disease_control": {
            "common_diseases": ["Extremely high disease resistance"],
            "vaccination_schedule": "Not practiced",
            "preventive_measures": "Lives in a natural, isolated environment",
            "quarantine_period": "Not applicable"
        },
        "genetic_improvement": {
            "breeding_objectives": "Conservation of this unique and culturally significant breed",
            "selection_criteria": "Hardiness and conformity to breed traits",
            "breeding_methods": "Natural selection within the herd",
            "performance_records": "Not applicable"
        }
    },
    "Murrah": {
        "origin": "Haryana, India",
        "type": "Buffalo - Dairy",
        "description": "Premium dairy buffalo breed known for high milk fat content and adaptability.",
        "nutrition_planning": {
            "forage_requirements": "70-80% green fodder, 20-30% dry fodder",
            "concentrate_feed": "2-3 kg per day for lactating buffaloes",
            "minerals": "High calcium for milk production, salt licks",
            "water_intake": "100-140 liters per day",
            "feeding_schedule": "3-4 times daily with wallowing facilities"
        },
        "disease_control": {
            "common_diseases": ["Mastitis", "Foot rot", "Parasitic infections"],
            "vaccination_schedule": "Regular FMD vaccination, deworming program",
            "preventive_measures": "Wallowing facilities, clean water, proper housing",
            "quarantine_period": "21 days for new animals"
        },
        "genetic_improvement": {
            "breeding_objectives": "High milk yield, fat content, disease resistance",
            "selection_criteria": "Milk production, fat percentage, reproductive performance",
            "breeding_methods": "Artificial insemination with proven bulls",
            "performance_records": "Milk recording, progeny testing"
        }
    },
    "Jersey": {
        "origin": "Jersey Island, UK",
        "type": "Dairy",
        "description": "Small, efficient dairy breed known for high butterfat content in milk.",
        "nutrition_planning": {
            "forage_requirements": "55-65% quality forage, 35-45% concentrates",
            "concentrate_feed": "3-4 kg per day for lactating cows",
            "minerals": "Balanced mineral mix, especially calcium and phosphorus",
            "water_intake": "70-100 liters per day",
            "feeding_schedule": "3 times daily with free access to water"
        },
        "disease_control": {
            "common_diseases": ["Mastitis", "Metabolic disorders", "Lameness"],
            "vaccination_schedule": "Standard dairy vaccination program",
            "preventive_measures": "Regular health monitoring, proper nutrition",
            "quarantine_period": "30 days for new animals"
        },
        "genetic_improvement": {
            "breeding_objectives": "High butterfat content, feed efficiency, fertility",
            "selection_criteria": "Milk components, feed conversion, health traits",
            "breeding_methods": "Genomic selection, artificial insemination",
            "performance_records": "Component testing, health monitoring"
        }
    },
    "Umblachery": {
        "origin": "Tamil Nadu, India",
        "type": "Draft",
        "description": "A small draft breed suitable for work in the marshy paddy fields of the Cauvery delta. Calves are born red and turn grey as they mature.",
        "nutrition_planning": {
            "forage_requirements": "Thrives on paddy straw and grazing on fallow fields",
            "concentrate_feed": "Minimal, supplemented only during heavy work",
            "minerals": "Salt licks",
            "water_intake": "30-50 liters per day",
            "feeding_schedule": "Grazing and supplemental stall feeding"
        },
        "disease_control": {
            "common_diseases": ["Resistant to diseases prevalent in damp, marshy conditions"],
            "vaccination_schedule": "FMD vaccination",
            "preventive_measures": "Hoof care is important",
            "quarantine_period": "21 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Draft capacity in wet agricultural lands",
            "selection_criteria": "Work performance in paddy fields, conformation",
            "breeding_methods": "Natural mating with selected local bulls",
            "performance_records": "Informally maintained by farmers"
        }
    },
    "Kankrej": {
        "origin": "Gujarat, India",
        "type": "Dual Purpose",
        "description": "Strong, hardy breed used for both milk and draft purposes, known for drought tolerance.",
        "nutrition_planning": {
            "forage_requirements": "60-70% green fodder, 30-40% dry fodder",
            "concentrate_feed": "1.5-2.5 kg per day for working animals",
            "minerals": "Salt licks, mineral supplements for working animals",
            "water_intake": "60-90 liters per day",
            "feeding_schedule": "2-3 times daily with adequate rest periods"
        },
        "disease_control": {
            "common_diseases": ["Tick-borne diseases", "Foot problems", "Parasitic infections"],
            "vaccination_schedule": "Annual FMD vaccination, regular deworming",
            "preventive_measures": "Regular grooming, proper hoof care, clean housing",
            "quarantine_period": "21 days for new animals"
        },
        "genetic_improvement": {
            "breeding_objectives": "Draft power, milk production, disease resistance",
            "selection_criteria": "Work capacity, milk yield, conformation",
            "breeding_methods": "Natural breeding, artificial insemination",
            "performance_records": "Work performance, milk production records"
        }
    },
    "Vechur": {
        "origin": "Kerala, India",
        "type": "Dual Purpose",
        "description": "Recognized as the world's smallest cattle breed. Known for its extreme hardiness and the purported medicinal properties of its high-fat, A2 milk.",
        "nutrition_planning": {
            "forage_requirements": "Extremely low feed requirement; can survive on kitchen scraps and sparse grazing",
            "concentrate_feed": "Rarely required",
            "minerals": "Obtained from local vegetation",
            "water_intake": "10-20 liters per day",
            "feeding_schedule": "Free-ranging or tethered grazing"
        },
        "disease_control": {
            "common_diseases": ["Extraordinary resistance to almost all common cattle diseases, including FMD"],
            "vaccination_schedule": "Generally not required",
            "preventive_measures": "Natural hardiness",
            "quarantine_period": "14 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Conservation of this unique genetic resource",
            "selection_criteria": "Purity of breed, small size, and milk quality",
            "breeding_methods": "Carefully managed conservation programs by veterinary universities",
            "performance_records": "Maintained by the Vechur Conservation Trust"
        }
    },
    "Tharparkar": {
        "origin": "Rajasthan, India",
        "type": "Dual Purpose",
        "description": "Desert-adapted breed known for heat tolerance and ability to survive in harsh conditions.",
        "nutrition_planning": {
            "forage_requirements": "50-60% green fodder, 40-50% dry fodder",
            "concentrate_feed": "1-2 kg per day during drought periods",
            "minerals": "Salt blocks, mineral supplements for desert conditions",
            "water_intake": "40-80 liters per day (varies with season)",
            "feeding_schedule": "Adapted to seasonal availability of feed"
        },
        "disease_control": {
            "common_diseases": ["Heat stress", "Dehydration", "Parasitic infections"],
            "vaccination_schedule": "Essential vaccinations only, adapted to local conditions",
            "preventive_measures": "Shade provision, water management, regular health checks",
            "quarantine_period": "14 days for new animals"
        },
        "genetic_improvement": {
            "breeding_objectives": "Heat tolerance, drought resistance, milk production",
            "selection_criteria": "Survival rate, milk yield under stress, conformation",
            "breeding_methods": "Natural breeding, community-based selection",
            "performance_records": "Survival and production under harsh conditions"
        }
    },
    "Malnad_gidda": {
        "origin": "Karnataka, India",
        "type": "Dual Purpose",
        "description": "A dwarf cattle breed from the hilly, high-rainfall Malenadu region. It is known for its exceptional hardiness, disease resistance, and ability to thrive on forest grazing.",
        "nutrition_planning": {
            "forage_requirements": "Subsists almost entirely on natural grazing and browsing in forests",
            "concentrate_feed": "Not traditionally given",
            "minerals": "Obtained from natural vegetation",
            "water_intake": "15-25 liters per day",
            "feeding_schedule": "Free-ranging"
        },
        "disease_control": {
            "common_diseases": ["Extremely high immunity to local diseases, including tick-borne illnesses"],
            "vaccination_schedule": "Rarely practiced by traditional rearers",
            "preventive_measures": "Natural hardiness",
            "quarantine_period": "Not applicable in the traditional system"
        },
        "genetic_improvement": {
            "breeding_objectives": "Conservation and promoting its use in low-input organic farming",
            "selection_criteria": "Adaptability, reproductive efficiency, and milk quality (A2 milk)",
            "breeding_methods": "Community-led conservation programs",
            "performance_records": "Maintained by conservation organizations"
        }
    },
    "Red_Sindhi": {
        "origin": "Sindh, Pakistan",
        "type": "Dairy",
        "description": "Tropical dairy breed known for heat tolerance and good milk production in hot climates.",
        "nutrition_planning": {
            "forage_requirements": "65-75% green fodder, 25-35% dry fodder",
            "concentrate_feed": "2-3 kg per day for lactating cows",
            "minerals": "Balanced mineral mix for tropical conditions",
            "water_intake": "80-120 liters per day",
            "feeding_schedule": "3-4 times daily with cooling measures"
        },
        "disease_control": {
            "common_diseases": ["Heat stress", "Mastitis", "Tick-borne diseases"],
            "vaccination_schedule": "Regular FMD vaccination, heat stress management",
            "preventive_measures": "Cooling systems, regular health monitoring",
            "quarantine_period": "21 days for new animals"
        },
        "genetic_improvement": {
            "breeding_objectives": "Heat tolerance, milk production, disease resistance",
            "selection_criteria": "Milk yield in hot conditions, heat tolerance",
            "breeding_methods": "Artificial insemination, natural breeding",
            "performance_records": "Production records under heat stress"
        }
    },
    "Jaffrabadi": {
        "origin": "Gujarat, India",
        "type": "Buffalo - Dairy",
        "description": "One of the heaviest buffalo breeds, known for its massive build and high milk yield with good fat content. It has distinctive, drooping horns that curl at the tip.",
        "nutrition_planning": {
            "forage_requirements": "High intake of green fodder, legumes, and dry roughage",
            "concentrate_feed": "3-4 kg per day for lactating animals, rich in protein and energy",
            "minerals": "High requirement for calcium and phosphorus",
            "water_intake": "120-160 liters per day, with essential access to wallowing",
            "feeding_schedule": "Stall-fed with a focus on high-energy rations"
        },
        "disease_control": {
            "common_diseases": ["Metabolic disorders", "Mastitis", "FMD"],
            "vaccination_schedule": "Regular FMD and HS-BQ vaccinations",
            "preventive_measures": "Proper nutritional management, clean and spacious housing",
            "quarantine_period": "30 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Improving milk yield, fat content, and maintaining body size",
            "selection_criteria": "305-day milk yield, fat percentage, and body conformation",
            "breeding_methods": "Artificial insemination with progeny-tested superior bulls",
            "performance_records": "Maintained by dairy cooperatives and breeding farms"
        }
    },
    "Rathi": {
        "origin": "Rajasthan, India",
        "type": "Dual Purpose",
        "description": "A milch breed from the arid regions of Rajasthan, known for its good milk production on low-input systems. Thrives in the desert environment.",
        "nutrition_planning": {
            "forage_requirements": "Efficiently utilizes desert grasses and shrubs",
            "concentrate_feed": "1.5-2.5 kg/day for lactating cows",
            "minerals": "Area-specific mineral mixture",
            "water_intake": "40-70 liters per day, adapted to water scarcity",
            "feeding_schedule": "Extensive grazing supplemented with stall feeding"
        },
        "disease_control": {
            "common_diseases": ["High tolerance to heat and drought stress"],
            "vaccination_schedule": "FMD vaccination",
            "preventive_measures": "Management practices to conserve water and feed",
            "quarantine_period": "21 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Improving milk yield while retaining hardiness",
            "selection_criteria": "Milk yield, calving interval, and drought resistance",
            "breeding_methods": "AI is being introduced to improve genetics",
            "performance_records": "Maintained by livestock development boards"
        }
    },
    "Ongole": {
        "origin": "Andhra Pradesh, India",
        "type": "Dual Purpose",
        "description": "Large, powerful breed used for both milk and draft, known for strength and endurance.",
        "nutrition_planning": {
            "forage_requirements": "60-70% green fodder, 30-40% dry fodder",
            "concentrate_feed": "2-3 kg per day for working animals",
            "minerals": "High energy feeds for working animals, mineral supplements",
            "water_intake": "80-120 liters per day",
            "feeding_schedule": "3 times daily with adequate rest for working animals"
        },
        "disease_control": {
            "common_diseases": ["Foot problems", "Parasitic infections", "Respiratory diseases"],
            "vaccination_schedule": "Annual vaccination program, regular deworming",
            "preventive_measures": "Proper hoof care, regular health checks, clean housing",
            "quarantine_period": "30 days for new animals"
        },
        "genetic_improvement": {
            "breeding_objectives": "Draft power, milk production, disease resistance",
            "selection_criteria": "Work performance, milk yield, health status",
            "breeding_methods": "Proven bull selection, artificial insemination",
            "performance_records": "Work capacity and milk production records"
        }
    },
    "Nili_Ravi": {
        "origin": "Punjab, Pakistan & India",
        "type": "Buffalo - Dairy",
        "description": "A high-yielding dairy buffalo breed, easily identified by its walled (blue) eyes and white markings on the face and legs. Known for its deep, massive frame.",
        "nutrition_planning": {
            "forage_requirements": "High intake of quality green fodder like berseem and lucerne",
            "concentrate_feed": "3-5 kg/day for high-yielding animals",
            "minerals": "High calcium and phosphorus for heavy milk production",
            "water_intake": "100-150 liters per day, with essential wallowing",
            "feeding_schedule": "Intensive stall-feeding systems"
        },
        "disease_control": {
            "common_diseases": ["Mastitis", "Metabolic disorders", "FMD"],
            "vaccination_schedule": "Comprehensive vaccination program",
            "preventive_measures": "Good hygiene, nutritional management, and comfortable housing",
            "quarantine_period": "30 days"
        },
        "genetic_improvement": {
            "breeding_objectives": "Maximizing milk yield and fat content",
            "selection_criteria": "305-day milk yield, fat percentage, and age at first calving",
            "breeding_methods": "Progeny testing and extensive use of AI with proven bulls",
            "performance_records": "Systematic recording by breeding associations"
        }
    },
    "Hariana": {
        "origin": "Haryana, India",
        "type": "Dual Purpose",
        "description": "Versatile breed used for both milk and draft, known for adaptability to different climates.",
        "nutrition_planning": {
            "forage_requirements": "60-70% green fodder, 30-40% dry fodder",
            "concentrate_feed": "2-3 kg per day for lactating cows",
            "minerals": "Balanced mineral mix, salt licks",
            "water_intake": "70-110 liters per day",
            "feeding_schedule": "3 times daily with seasonal adjustments"
        },
        "disease_control": {
            "common_diseases": ["Mastitis", "Foot and Mouth Disease", "Parasitic infections"],
            "vaccination_schedule": "Regular FMD vaccination, deworming program",
            "preventive_measures": "Regular health monitoring, proper nutrition management",
            "quarantine_period": "21 days for new animals"
        },
        "genetic_improvement": {
            "breeding_objectives": "Milk production, draft power, adaptability",
            "selection_criteria": "Milk yield, work capacity, health traits",
            "breeding_methods": "Artificial insemination, natural breeding",
            "performance_records": "Comprehensive production and health records"
        }
    }
}

# Merge dataset-derived breeds with curated overrides so that every model class
# has at least a default information block available to the app.
_dataset_breeds = _list_dataset_breeds()
_all_breeds = sorted(set(list(BREED_INFO_OVERRIDES.keys()) + _dataset_breeds))

BREED_INFO = {}
for _breed in _all_breeds:
    if _breed in BREED_INFO_OVERRIDES:
        BREED_INFO[_breed] = BREED_INFO_OVERRIDES[_breed]
    else:
        BREED_INFO[_breed] = _default_info_template(_breed)

def get_breed_info(breed_name):
    """
    Get detailed information about a specific breed.
    
    Args:
        breed_name (str): Name of the breed
        
    Returns:
        dict: Breed information including nutrition, disease control, and genetic improvement
    """
    return BREED_INFO.get(breed_name, {
        "origin": "Unknown",
        "type": "Unknown",
        "description": "Breed information not available in database.",
        "nutrition_planning": {
            "forage_requirements": "Consult local veterinarian for specific requirements",
            "concentrate_feed": "Based on production level and body weight",
            "minerals": "Balanced mineral mix as per local conditions",
            "water_intake": "Ad libitum access to clean water",
            "feeding_schedule": "Regular feeding schedule as per local practices"
        },
        "disease_control": {
            "common_diseases": ["Consult local veterinarian for breed-specific diseases"],
            "vaccination_schedule": "Follow local vaccination program",
            "preventive_measures": "Regular health monitoring and proper management",
            "quarantine_period": "As per local regulations"
        },
        "genetic_improvement": {
            "breeding_objectives": "Consult breed association for specific objectives",
            "selection_criteria": "Based on breed standards and local requirements",
            "breeding_methods": "Artificial insemination or natural breeding",
            "performance_records": "Maintain detailed production and health records"
        }
    })

def get_all_breeds():
    """
    Get list of all available breeds in the database.
    
    Returns:
        list: List of breed names
    """
    return sorted(list(BREED_INFO.keys()))
