"""Batch 2: Add 123 more entities to reach 500 total."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTITIES_PATH = ROOT / "data" / "seeds" / "entities_v1.jsonl"
GOLD_CASES_PATH = ROOT / "data" / "eval" / "gold_cases_v1.json"

ALL_ATTRS = [
    "is_real_person", "is_alive", "is_female", "is_actor", "is_musician",
    "is_athlete", "is_politician", "is_internet_personality", "from_north_america",
    "from_europe", "is_historical_figure", "age_over_50", "age_under_30",
    "is_fictional", "known_for_movies", "known_for_television", "is_singer",
    "is_rapper", "is_band_member", "is_pop_star", "has_won_grammy",
    "known_by_single_name", "known_for_reality_tv", "is_us_president",
    "has_won_nobel_prize", "known_for_social_media", "known_for_streaming",
    "is_business_person", "plays_team_sport", "plays_solo_sport",
    "is_soccer_player", "is_basketball_player", "is_tennis_player",
    "is_racing_driver", "is_wrestler", "has_won_major_championship",
    "has_won_oscar", "known_for_superhero_role", "associated_with_marvel",
    "associated_with_disney", "is_director", "is_comedian", "is_standup_comedian",
    "is_host", "is_author", "is_scientist", "is_royalty", "is_head_of_state",
    "has_held_elected_office", "uses_stage_name", "does_voice_acting",
    "is_american", "known_for_drama_only", "is_republican", "age_over_75",
    "is_democrat", "is_swedish", "peak_era_2000s", "is_challenge_creator",
    "is_gaming_creator", "subscriber_count_tier", "peak_era_90s",
    "held_office_pre_2000", "known_for_comedy", "is_american_football_player",
    "is_swimmer", "is_golfer", "is_retired", "peak_era_2010s", "peak_era_2020s",
    "is_european_leader", "is_asian_leader", "lives_in_north_america",
    "is_from_eastern_europe", "is_beauty_creator", "is_tech_reviewer",
    "is_vlog_creator", "is_kids_content_creator", "is_live_streamer",
    "is_activist", "has_acting_and_music_career", "known_for_action_films",
    "known_for_romantic_films", "has_most_titles_in_sport",
]

def base_attrs():
    return {k: 0.0 for k in ALL_ATTRS}

def make_entity(id_, name, aliases, categories, popularity, overrides):
    attrs = base_attrs()
    attrs["is_real_person"] = 1.0
    attrs["is_fictional"] = 0.0
    for k, v in overrides.items():
        attrs[k] = v
    return {
        "id": id_, "name": name, "aliases": aliases,
        "categories": categories, "popularity_score": popularity,
        "attributes": attrs,
    }

def confidence_to_answer(v):
    if v >= 0.8: return "yes"
    elif v >= 0.5: return "probably_yes"
    elif v >= 0.3: return "i_dont_know"
    elif v >= 0.1: return "probably_no"
    else: return "no"

def entity_to_gold(entity):
    answers = {}
    for k in ALL_ATTRS:
        answers[k] = confidence_to_answer(entity["attributes"][k])
    return {"target_entity_id": entity["id"], "answers": answers}

# More politicians/public figures (~30)
BATCH2_POLITICIANS = [
    ("mitch_mcconnell", "Mitch McConnell", [], ["politician"], 88,
     {"is_alive": 1.0, "is_female": 0.0, "is_politician": 1.0, "is_american": 1.0,
      "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "age_over_50": 1.0, "age_over_75": 1.0,
      "has_held_elected_office": 1.0, "is_republican": 1.0,
      "held_office_pre_2000": 1.0,
      "peak_era_2010s": 0.6, "peak_era_2020s": 0.7}),
    ("tim_walz", "Tim Walz", [], ["politician"], 86,
     {"is_alive": 1.0, "is_female": 0.0, "is_politician": 1.0, "is_american": 1.0,
      "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "age_over_50": 1.0, "has_held_elected_office": 1.0, "is_democrat": 1.0,
      "peak_era_2020s": 1.0}),
    ("vivek_ramaswamy", "Vivek Ramaswamy", [], ["politician", "business_person"], 86,
     {"is_alive": 1.0, "is_female": 0.0, "is_politician": 0.8, "is_american": 1.0,
      "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "is_business_person": 0.8, "is_republican": 0.8, "is_author": 0.4,
      "peak_era_2020s": 1.0}),
    ("pedro_sanchez", "Pedro Sanchez", [], ["politician"], 86,
     {"is_alive": 1.0, "is_female": 0.0, "is_politician": 1.0, "is_american": 0.0,
      "from_europe": 1.0, "age_over_50": 1.0, "is_head_of_state": 1.0,
      "has_held_elected_office": 1.0, "is_european_leader": 1.0,
      "peak_era_2020s": 0.9}),
    ("yoon_suk_yeol", "Yoon Suk Yeol", [], ["politician"], 85,
     {"is_alive": 1.0, "is_female": 0.0, "is_politician": 1.0, "is_american": 0.0,
      "age_over_50": 1.0, "is_head_of_state": 1.0,
      "has_held_elected_office": 1.0, "is_asian_leader": 1.0,
      "peak_era_2020s": 1.0}),
    ("lula_da_silva", "Lula da Silva", ["Luiz Inacio Lula da Silva"], ["politician"], 87,
     {"is_alive": 1.0, "is_female": 0.0, "is_politician": 1.0, "is_american": 0.0,
      "age_over_50": 1.0, "age_over_75": 1.0,
      "is_head_of_state": 1.0, "has_held_elected_office": 1.0,
      "is_activist": 0.5, "peak_era_2000s": 0.7, "peak_era_2020s": 0.8}),
    ("javier_milei", "Javier Milei", [], ["politician"], 86,
     {"is_alive": 1.0, "is_female": 0.0, "is_politician": 1.0, "is_american": 0.0,
      "age_over_50": 1.0, "is_head_of_state": 1.0,
      "has_held_elected_office": 1.0, "is_author": 0.3,
      "known_for_social_media": 0.6, "is_internet_personality": 0.3,
      "peak_era_2020s": 1.0}),
    ("recep_erdogan", "Recep Tayyip Erdogan", [], ["politician"], 87,
     {"is_alive": 1.0, "is_female": 0.0, "is_politician": 1.0, "is_american": 0.0,
      "from_europe": 0.5, "age_over_50": 1.0, "is_head_of_state": 1.0,
      "has_held_elected_office": 1.0,
      "peak_era_2000s": 0.5, "peak_era_2010s": 0.7, "peak_era_2020s": 0.8}),
    ("fidel_castro", "Fidel Castro", [], ["politician"], 90,
     {"is_alive": 0.0, "is_female": 0.0, "is_politician": 1.0, "is_american": 0.0,
      "from_north_america": 1.0, "age_over_50": 1.0, "age_over_75": 1.0,
      "is_historical_figure": 1.0, "is_head_of_state": 1.0, "is_author": 0.3}),
    ("che_guevara", "Che Guevara", ["Ernesto Guevara"], ["activist"], 90,
     {"is_alive": 0.0, "is_female": 0.0, "is_politician": 0.6, "is_american": 0.0,
      "is_historical_figure": 1.0, "is_activist": 1.0, "is_author": 0.4,
      "uses_stage_name": 0.5}),
    ("warren_buffett", "Warren Buffett", [], ["business_person"], 91,
     {"is_alive": 1.0, "is_female": 0.0, "is_business_person": 1.0,
      "is_american": 1.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "age_over_50": 1.0, "age_over_75": 1.0,
      "peak_era_2000s": 0.6, "peak_era_2010s": 0.5}),
    ("tim_cook", "Tim Cook", [], ["business_person"], 88,
     {"is_alive": 1.0, "is_female": 0.0, "is_business_person": 1.0,
      "is_american": 1.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "age_over_50": 1.0, "is_activist": 0.3,
      "peak_era_2010s": 0.7, "peak_era_2020s": 0.7}),
    ("fumio_kishida", "Fumio Kishida", [], ["politician"], 84,
     {"is_alive": 1.0, "is_female": 0.0, "is_politician": 1.0, "is_american": 0.0,
      "age_over_50": 1.0, "is_head_of_state": 1.0,
      "has_held_elected_office": 1.0, "is_asian_leader": 1.0,
      "peak_era_2020s": 0.9}),
]

# More internet creators (~30)
BATCH2_INTERNET = [
    ("iman_gadzhi", "Iman Gadzhi", [], ["internet_personality", "business_person"], 86,
     {"is_alive": 1.0, "is_female": 0.0, "is_internet_personality": 1.0,
      "is_american": 0.0, "from_europe": 1.0,
      "age_under_30": 1.0, "is_business_person": 0.8,
      "known_for_social_media": 0.9, "is_vlog_creator": 0.6,
      "subscriber_count_tier": 0.7, "peak_era_2020s": 1.0}),
    ("alex_hormozi", "Alex Hormozi", [], ["internet_personality", "business_person"], 86,
     {"is_alive": 1.0, "is_female": 0.0, "is_internet_personality": 1.0,
      "is_american": 1.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "is_business_person": 1.0, "is_author": 0.6,
      "known_for_social_media": 0.9, "subscriber_count_tier": 0.7,
      "peak_era_2020s": 1.0}),
    ("danny_gonzalez", "Danny Gonzalez", [], ["internet_personality"], 85,
     {"is_alive": 1.0, "is_female": 0.0, "is_internet_personality": 1.0,
      "is_american": 1.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "age_under_30": 1.0, "is_comedian": 0.5, "is_musician": 0.3,
      "known_for_social_media": 0.7, "is_vlog_creator": 0.5,
      "subscriber_count_tier": 0.6, "peak_era_2020s": 0.9}),
    ("drew_gooden", "Drew Gooden", [], ["internet_personality"], 85,
     {"is_alive": 1.0, "is_female": 0.0, "is_internet_personality": 1.0,
      "is_american": 1.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "age_under_30": 1.0, "is_comedian": 0.5,
      "known_for_social_media": 0.7, "is_vlog_creator": 0.5,
      "subscriber_count_tier": 0.6, "peak_era_2020s": 0.9}),
    ("sneako", "Sneako", ["Nico Kenn De Balinthazy"], ["internet_personality"], 85,
     {"is_alive": 1.0, "is_female": 0.0, "is_internet_personality": 1.0,
      "is_american": 1.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "age_under_30": 1.0, "known_for_social_media": 0.8,
      "known_for_streaming": 0.6, "is_live_streamer": 0.5,
      "uses_stage_name": 1.0, "known_by_single_name": 1.0,
      "subscriber_count_tier": 0.5, "peak_era_2020s": 1.0}),
    ("yes_theory", "Yes Theory", ["Thomas Brag"], ["internet_personality"], 85,
     {"is_alive": 1.0, "is_female": 0.0, "is_internet_personality": 1.0,
      "is_american": 0.0, "lives_in_north_america": 1.0,
      "is_challenge_creator": 0.8, "is_vlog_creator": 0.8,
      "known_for_social_media": 0.7, "subscriber_count_tier": 0.7,
      "peak_era_2010s": 0.5, "peak_era_2020s": 0.8}),
    ("ijustine", "iJustine", ["Justine Ezarik"], ["internet_personality"], 85,
     {"is_alive": 1.0, "is_female": 1.0, "is_internet_personality": 1.0,
      "is_american": 1.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "is_tech_reviewer": 0.8, "is_vlog_creator": 0.6,
      "known_for_social_media": 0.7, "uses_stage_name": 1.0,
      "subscriber_count_tier": 0.6, "peak_era_2010s": 0.7, "peak_era_2020s": 0.4}),
    ("unbox_therapy", "Lewis Hilsenteger", ["Unbox Therapy"], ["internet_personality"], 86,
     {"is_alive": 1.0, "is_female": 0.0, "is_internet_personality": 1.0,
      "is_american": 0.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "is_tech_reviewer": 1.0, "known_for_social_media": 0.6,
      "subscriber_count_tier": 0.8, "peak_era_2010s": 0.8, "peak_era_2020s": 0.5}),
    ("asmr_gibi", "Gibi ASMR", ["Gibi Klein"], ["internet_personality"], 84,
     {"is_alive": 1.0, "is_female": 1.0, "is_internet_personality": 1.0,
      "is_american": 1.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "known_for_social_media": 0.7, "known_for_streaming": 0.5,
      "subscriber_count_tier": 0.6, "is_live_streamer": 0.3,
      "peak_era_2020s": 0.8}),
    ("mizkif", "Mizkif", ["Matthew Rinaudo"], ["internet_personality"], 85,
     {"is_alive": 1.0, "is_female": 0.0, "is_internet_personality": 1.0,
      "is_american": 1.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "age_under_30": 1.0, "is_gaming_creator": 0.5,
      "known_for_streaming": 0.9, "is_live_streamer": 0.9,
      "known_for_social_media": 0.6, "uses_stage_name": 1.0,
      "known_by_single_name": 1.0, "subscriber_count_tier": 0.5,
      "peak_era_2020s": 0.9}),
    ("jerma985", "Jerma985", ["Jeremy Elbertson"], ["internet_personality"], 86,
     {"is_alive": 1.0, "is_female": 0.0, "is_internet_personality": 1.0,
      "is_american": 1.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "is_gaming_creator": 0.7, "is_comedian": 0.5,
      "known_for_streaming": 0.9, "is_live_streamer": 0.9,
      "known_for_social_media": 0.6, "uses_stage_name": 1.0,
      "subscriber_count_tier": 0.5, "peak_era_2020s": 0.8}),
    ("ricegum", "RiceGum", ["Bryan Quang Le"], ["internet_personality"], 85,
     {"is_alive": 1.0, "is_female": 0.0, "is_internet_personality": 1.0,
      "is_american": 1.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "age_under_30": 1.0, "is_rapper": 0.2, "known_for_social_media": 0.8,
      "is_vlog_creator": 0.6, "uses_stage_name": 1.0, "known_by_single_name": 1.0,
      "subscriber_count_tier": 0.6, "peak_era_2010s": 0.8, "peak_era_2020s": 0.3}),
    ("lachlan", "Lachlan", ["Lachlan Ross Power"], ["internet_personality"], 85,
     {"is_alive": 1.0, "is_female": 0.0, "is_internet_personality": 1.0,
      "is_american": 0.0, "is_gaming_creator": 1.0, "known_for_streaming": 0.5,
      "known_for_social_media": 0.6, "known_by_single_name": 1.0,
      "subscriber_count_tier": 0.7, "peak_era_2010s": 0.7, "peak_era_2020s": 0.6}),
    ("stampy_cat", "Stampylonghead", ["Joseph Garrett"], ["internet_personality"], 84,
     {"is_alive": 1.0, "is_female": 0.0, "is_internet_personality": 1.0,
      "is_american": 0.0, "from_europe": 1.0,
      "is_gaming_creator": 1.0, "is_kids_content_creator": 0.8,
      "known_for_social_media": 0.5, "uses_stage_name": 1.0,
      "subscriber_count_tier": 0.6, "peak_era_2010s": 0.9, "peak_era_2020s": 0.2}),
]

# More athletes (~40)
BATCH2_ATHLETES = [
    ("jordan_spieth", "Jordan Spieth", [], ["athlete", "golf"], 88,
     {"is_alive": 1.0, "is_female": 0.0, "is_athlete": 1.0, "is_american": 1.0,
      "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "plays_solo_sport": 1.0, "is_golfer": 1.0,
      "has_won_major_championship": 1.0,
      "peak_era_2010s": 0.8, "peak_era_2020s": 0.5}),
    ("leon_draisaitl", "Leon Draisaitl", [], ["athlete", "hockey"], 87,
     {"is_alive": 1.0, "is_female": 0.0, "is_athlete": 1.0, "is_american": 0.0,
      "from_europe": 1.0, "lives_in_north_america": 1.0,
      "age_under_30": 1.0, "plays_team_sport": 1.0,
      "peak_era_2020s": 1.0}),
    ("mookie_betts", "Mookie Betts", [], ["athlete", "baseball"], 88,
     {"is_alive": 1.0, "is_female": 0.0, "is_athlete": 1.0, "is_american": 1.0,
      "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "plays_team_sport": 1.0, "has_won_major_championship": 1.0,
      "peak_era_2020s": 0.9}),
    ("sydney_mclaughlin", "Sydney McLaughlin-Levrone", [], ["athlete", "track"], 87,
     {"is_alive": 1.0, "is_female": 1.0, "is_athlete": 1.0, "is_american": 1.0,
      "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "age_under_30": 1.0, "plays_solo_sport": 1.0,
      "has_won_major_championship": 1.0, "has_most_titles_in_sport": 0.5,
      "peak_era_2020s": 1.0}),
    ("pedri", "Pedri", ["Pedro Gonzalez Lopez"], ["athlete", "soccer"], 87,
     {"is_alive": 1.0, "is_female": 0.0, "is_athlete": 1.0, "is_american": 0.0,
      "from_europe": 1.0, "age_under_30": 1.0, "plays_team_sport": 1.0,
      "is_soccer_player": 1.0, "known_by_single_name": 1.0,
      "peak_era_2020s": 1.0}),
    ("virgil_van_dijk", "Virgil van Dijk", [], ["athlete", "soccer"], 89,
     {"is_alive": 1.0, "is_female": 0.0, "is_athlete": 1.0, "is_american": 0.0,
      "from_europe": 1.0, "plays_team_sport": 1.0, "is_soccer_player": 1.0,
      "has_won_major_championship": 1.0, "peak_era_2020s": 0.9}),
    ("phil_foden", "Phil Foden", [], ["athlete", "soccer"], 87,
     {"is_alive": 1.0, "is_female": 0.0, "is_athlete": 1.0, "is_american": 0.0,
      "from_europe": 1.0, "age_under_30": 1.0, "plays_team_sport": 1.0,
      "is_soccer_player": 1.0, "has_won_major_championship": 1.0,
      "peak_era_2020s": 1.0}),
    # More diverse athletes
    ("alexander_zverev", "Alexander Zverev", [], ["athlete", "tennis"], 87,
     {"is_alive": 1.0, "is_female": 0.0, "is_athlete": 1.0, "is_american": 0.0,
      "from_europe": 1.0, "age_under_30": 1.0, "plays_solo_sport": 1.0,
      "is_tennis_player": 1.0, "has_won_major_championship": 0.5,
      "peak_era_2020s": 0.9}),
    ("daniil_medvedev", "Daniil Medvedev", [], ["athlete", "tennis"], 87,
     {"is_alive": 1.0, "is_female": 0.0, "is_athlete": 1.0, "is_american": 0.0,
      "from_europe": 1.0, "is_from_eastern_europe": 1.0,
      "age_under_30": 1.0, "plays_solo_sport": 1.0, "is_tennis_player": 1.0,
      "has_won_major_championship": 1.0, "peak_era_2020s": 0.9}),
    ("ruud_gullit", "SKIP", [], [], 0, {}),
    ("son_heung_min", "Son Heung-min", [], ["athlete", "soccer"], 89,
     {"is_alive": 1.0, "is_female": 0.0, "is_athlete": 1.0, "is_american": 0.0,
      "from_europe": 0.0, "is_asian_leader": 0.0,
      "lives_in_north_america": 0.0,
      "plays_team_sport": 1.0, "is_soccer_player": 1.0,
      "has_won_major_championship": 0.5,
      "peak_era_2010s": 0.5, "peak_era_2020s": 0.9}),
    ("mbappe_check", "SKIP", [], [], 0, {}),
    ("thibaut_courtois", "Thibaut Courtois", [], ["athlete", "soccer"], 87,
     {"is_alive": 1.0, "is_female": 0.0, "is_athlete": 1.0, "is_american": 0.0,
      "from_europe": 1.0, "plays_team_sport": 1.0, "is_soccer_player": 1.0,
      "has_won_major_championship": 1.0, "peak_era_2020s": 0.9}),
    ("derrick_henry", "Derrick Henry", [], ["athlete", "american_football"], 88,
     {"is_alive": 1.0, "is_female": 0.0, "is_athlete": 1.0, "is_american": 1.0,
      "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "plays_team_sport": 1.0, "is_american_football_player": 1.0,
      "has_won_major_championship": 0.0, "peak_era_2020s": 0.9}),
    ("dak_prescott", "Dak Prescott", [], ["athlete", "american_football"], 87,
     {"is_alive": 1.0, "is_female": 0.0, "is_athlete": 1.0, "is_american": 1.0,
      "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "plays_team_sport": 1.0, "is_american_football_player": 1.0,
      "peak_era_2020s": 0.9}),
    ("tyreek_hill", "Tyreek Hill", [], ["athlete", "american_football"], 87,
     {"is_alive": 1.0, "is_female": 0.0, "is_athlete": 1.0, "is_american": 1.0,
      "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "plays_team_sport": 1.0, "is_american_football_player": 1.0,
      "has_won_major_championship": 1.0, "known_for_social_media": 0.5,
      "peak_era_2020s": 1.0}),
    ("breanna_stewart", "Breanna Stewart", [], ["athlete", "basketball"], 87,
     {"is_alive": 1.0, "is_female": 1.0, "is_athlete": 1.0, "is_american": 1.0,
      "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "plays_team_sport": 1.0, "is_basketball_player": 1.0,
      "has_won_major_championship": 1.0, "peak_era_2020s": 0.9}),
    ("auston_matthews", "Auston Matthews", [], ["athlete", "hockey"], 87,
     {"is_alive": 1.0, "is_female": 0.0, "is_athlete": 1.0, "is_american": 1.0,
      "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "age_under_30": 1.0, "plays_team_sport": 1.0,
      "peak_era_2020s": 1.0}),
    ("florian_wirtz", "Florian Wirtz", [], ["athlete", "soccer"], 86,
     {"is_alive": 1.0, "is_female": 0.0, "is_athlete": 1.0, "is_american": 0.0,
      "from_europe": 1.0, "age_under_30": 1.0,
      "plays_team_sport": 1.0, "is_soccer_player": 1.0,
      "peak_era_2020s": 1.0}),
    ("jamal_musiala", "Jamal Musiala", [], ["athlete", "soccer"], 86,
     {"is_alive": 1.0, "is_female": 0.0, "is_athlete": 1.0, "is_american": 0.0,
      "from_europe": 1.0, "age_under_30": 1.0,
      "plays_team_sport": 1.0, "is_soccer_player": 1.0,
      "peak_era_2020s": 1.0}),
]

# More musicians (~20)
BATCH2_MUSICIANS = [
    ("nle_choppa", "NLE Choppa", ["Bryson Lashun Potts"], ["musician", "rapper"], 86,
     {"is_alive": 1.0, "is_female": 0.0, "is_musician": 1.0, "is_rapper": 1.0,
      "is_american": 1.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "age_under_30": 1.0, "uses_stage_name": 1.0,
      "known_for_social_media": 0.6, "is_internet_personality": 0.4,
      "peak_era_2020s": 0.9}),
    ("olivia_dean", "Olivia Dean", [], ["musician", "singer"], 85,
     {"is_alive": 1.0, "is_female": 1.0, "is_musician": 1.0, "is_singer": 1.0,
      "is_american": 0.0, "from_europe": 1.0, "age_under_30": 1.0,
      "peak_era_2020s": 1.0}),
    ("raye_singer", "Raye", ["Rachel Agatha Keen"], ["musician", "singer"], 86,
     {"is_alive": 1.0, "is_female": 1.0, "is_musician": 1.0, "is_singer": 1.0,
      "is_american": 0.0, "from_europe": 1.0, "age_under_30": 1.0,
      "has_won_grammy": 0.0, "known_by_single_name": 1.0, "uses_stage_name": 1.0,
      "peak_era_2020s": 1.0}),
    ("doechii", "Doechii", ["Jaylah Ji'mya Hickmon"], ["musician", "rapper"], 86,
     {"is_alive": 1.0, "is_female": 1.0, "is_musician": 1.0, "is_rapper": 1.0,
      "is_singer": 0.5, "is_american": 1.0, "from_north_america": 1.0,
      "lives_in_north_america": 1.0, "age_under_30": 1.0,
      "uses_stage_name": 1.0, "known_by_single_name": 1.0,
      "known_for_social_media": 0.5, "peak_era_2020s": 1.0}),
    ("rod_wave", "Rod Wave", ["Rodarius Marcell Green"], ["musician", "rapper"], 87,
     {"is_alive": 1.0, "is_female": 0.0, "is_musician": 1.0, "is_rapper": 1.0,
      "is_singer": 0.6, "is_american": 1.0, "from_north_america": 1.0,
      "lives_in_north_america": 1.0, "age_under_30": 1.0,
      "uses_stage_name": 1.0, "peak_era_2020s": 1.0}),
    ("sexyy_red", "Sexyy Red", ["Janae Wherry"], ["musician", "rapper"], 86,
     {"is_alive": 1.0, "is_female": 1.0, "is_musician": 1.0, "is_rapper": 1.0,
      "is_american": 1.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "age_under_30": 1.0, "uses_stage_name": 1.0,
      "known_for_social_media": 0.7, "peak_era_2020s": 1.0}),
    ("ed_sheeran_check", "SKIP", [], [], 0, {}),
    ("glass_animals", "Glass Animals", ["Dave Bayley"], ["musician", "band"], 86,
     {"is_alive": 1.0, "is_female": 0.0, "is_musician": 1.0, "is_singer": 0.7,
      "is_band_member": 1.0, "is_american": 0.0, "from_europe": 1.0,
      "is_pop_star": 0.5, "peak_era_2020s": 0.9}),
    ("sza_check", "SKIP", [], [], 0, {}),
    ("mitski", "Mitski", ["Mitsuki Laycock"], ["musician", "singer"], 86,
     {"is_alive": 1.0, "is_female": 1.0, "is_musician": 1.0, "is_singer": 1.0,
      "is_american": 1.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "known_by_single_name": 1.0, "uses_stage_name": 0.0,
      "peak_era_2020s": 0.9}),
    ("lil_baby", "Lil Baby", ["Dominique Armani Jones"], ["musician", "rapper"], 88,
     {"is_alive": 1.0, "is_female": 0.0, "is_musician": 1.0, "is_rapper": 1.0,
      "is_american": 1.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "uses_stage_name": 1.0, "peak_era_2020s": 1.0}),
    ("morgan_wallen", "Morgan Wallen", [], ["musician", "singer"], 88,
     {"is_alive": 1.0, "is_female": 0.0, "is_musician": 1.0, "is_singer": 1.0,
      "is_american": 1.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "known_for_social_media": 0.5, "peak_era_2020s": 1.0}),
    ("luke_combs", "Luke Combs", [], ["musician", "singer"], 87,
     {"is_alive": 1.0, "is_female": 0.0, "is_musician": 1.0, "is_singer": 1.0,
      "is_american": 1.0, "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "has_won_grammy": 0.0, "peak_era_2020s": 1.0}),
    ("billie_joe_armstrong", "Billie Joe Armstrong", [], ["musician", "singer"], 88,
     {"is_alive": 1.0, "is_female": 0.0, "is_musician": 1.0, "is_singer": 1.0,
      "is_band_member": 1.0, "is_american": 1.0, "from_north_america": 1.0,
      "lives_in_north_america": 1.0, "age_over_50": 1.0,
      "has_won_grammy": 1.0, "is_activist": 0.4,
      "peak_era_2000s": 0.8, "peak_era_2010s": 0.4}),
]

# More actors (~20)
BATCH2_ACTORS = [
    ("jeff_bridges", "Jeff Bridges", [], ["actor"], 90,
     {"is_alive": 1.0, "is_female": 0.0, "is_actor": 1.0, "is_american": 1.0,
      "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "age_over_50": 1.0, "age_over_75": 1.0, "known_for_movies": 1.0,
      "has_won_oscar": 1.0, "known_for_drama_only": 0.6, "known_for_comedy": 0.4,
      "peak_era_90s": 0.5, "peak_era_2000s": 0.7, "peak_era_2010s": 0.5}),
    ("rachel_zegler", "Rachel Zegler", [], ["actor", "singer"], 86,
     {"is_alive": 1.0, "is_female": 1.0, "is_actor": 1.0, "is_singer": 0.5,
      "is_musician": 0.3, "is_american": 1.0, "from_north_america": 1.0,
      "lives_in_north_america": 1.0, "age_under_30": 1.0,
      "known_for_movies": 0.8, "associated_with_disney": 0.5,
      "has_acting_and_music_career": 0.4, "peak_era_2020s": 1.0}),
    ("florence_welch", "SKIP", [], [], 0, {}),
    ("timothee_check2", "SKIP", [], [], 0, {}),
    ("benedict_check2", "SKIP", [], [], 0, {}),
    ("pedro_pascal_check", "SKIP", [], [], 0, {}),
    ("john_boyega", "John Boyega", [], ["actor"], 88,
     {"is_alive": 1.0, "is_female": 0.0, "is_actor": 1.0, "is_american": 0.0,
      "from_europe": 1.0, "lives_in_north_america": 0.5,
      "known_for_movies": 1.0, "known_for_action_films": 0.6,
      "associated_with_disney": 0.5, "is_activist": 0.4,
      "peak_era_2010s": 0.7, "peak_era_2020s": 0.6}),
    ("sofia_vergara", "Sofia Vergara", [], ["actor", "business_person"], 90,
     {"is_alive": 1.0, "is_female": 1.0, "is_actor": 1.0, "is_american": 0.0,
      "from_north_america": 0.0, "lives_in_north_america": 1.0,
      "age_over_50": 1.0, "known_for_television": 1.0,
      "known_for_comedy": 0.8, "is_business_person": 0.5,
      "peak_era_2010s": 0.9, "peak_era_2020s": 0.5}),
    ("pedro_alonso", "SKIP", [], [], 0, {}),
    ("florence_pugh_check", "SKIP", [], [], 0, {}),
    ("sydney_sweeney_check", "SKIP", [], [], 0, {}),
    ("zoe_saldana", "Zoe Saldana", [], ["actor"], 90,
     {"is_alive": 1.0, "is_female": 1.0, "is_actor": 1.0, "is_american": 1.0,
      "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "age_over_50": 1.0, "known_for_movies": 1.0,
      "known_for_action_films": 0.7, "known_for_superhero_role": 0.5,
      "associated_with_marvel": 0.8, "associated_with_disney": 0.5,
      "peak_era_2010s": 0.8, "peak_era_2020s": 0.7}),
    ("pedro_pascal_actor_check", "SKIP", [], [], 0, {}),
    ("dev_patel", "Dev Patel", [], ["actor"], 88,
     {"is_alive": 1.0, "is_female": 0.0, "is_actor": 1.0, "is_american": 0.0,
      "from_europe": 1.0, "lives_in_north_america": 1.0,
      "known_for_movies": 1.0, "known_for_drama_only": 0.6,
      "known_for_action_films": 0.4, "is_director": 0.3,
      "peak_era_2010s": 0.6, "peak_era_2020s": 0.8}),
    ("elizabeth_olsen", "Elizabeth Olsen", [], ["actor"], 89,
     {"is_alive": 1.0, "is_female": 1.0, "is_actor": 1.0, "is_american": 1.0,
      "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "known_for_movies": 0.8, "known_for_television": 0.7,
      "known_for_superhero_role": 0.9, "associated_with_marvel": 1.0,
      "associated_with_disney": 0.5,
      "peak_era_2010s": 0.6, "peak_era_2020s": 0.9}),
    ("timothee_check3", "SKIP", [], [], 0, {}),
    ("chris_pine", "Chris Pine", [], ["actor"], 89,
     {"is_alive": 1.0, "is_female": 0.0, "is_actor": 1.0, "is_american": 1.0,
      "from_north_america": 1.0, "lives_in_north_america": 1.0,
      "known_for_movies": 1.0, "known_for_action_films": 0.7,
      "known_for_superhero_role": 0.4, "associated_with_disney": 0.4,
      "peak_era_2010s": 0.7, "peak_era_2020s": 0.6}),
    ("tilda_swinton", "Tilda Swinton", [], ["actor"], 89,
     {"is_alive": 1.0, "is_female": 1.0, "is_actor": 1.0, "is_american": 0.0,
      "from_europe": 1.0, "age_over_50": 1.0,
      "known_for_movies": 1.0, "has_won_oscar": 1.0,
      "known_for_drama_only": 0.7, "associated_with_marvel": 0.3,
      "peak_era_2000s": 0.6, "peak_era_2010s": 0.7, "peak_era_2020s": 0.5}),
]

def main():
    all_new = []
    for source in [BATCH2_POLITICIANS, BATCH2_INTERNET, BATCH2_ATHLETES, BATCH2_MUSICIANS, BATCH2_ACTORS]:
        for item in source:
            if item[1] == "SKIP":
                continue
            all_new.append(make_entity(*item))

    existing_ids = set()
    existing_lines = []
    with ENTITIES_PATH.open("r") as f:
        for line in f:
            if line.strip():
                e = json.loads(line)
                existing_ids.add(e["id"])
                existing_lines.append(line.rstrip())

    new_entities = [e for e in all_new if e["id"] not in existing_ids]
    print(f"Existing entities: {len(existing_ids)}")
    print(f"New entities to add: {len(new_entities)}")
    print(f"Total will be: {len(existing_ids) + len(new_entities)}")

    for e in new_entities:
        missing = set(ALL_ATTRS) - set(e["attributes"].keys())
        if missing:
            print(f"WARNING: {e['id']} missing: {missing}")

    with ENTITIES_PATH.open("w") as f:
        for line in existing_lines:
            f.write(line + "\n")
        for e in new_entities:
            f.write(json.dumps(e, separators=(",", ":")) + "\n")

    with GOLD_CASES_PATH.open("r") as f:
        existing_gold = json.load(f)
    existing_gold_ids = {g["target_entity_id"] for g in existing_gold}
    new_gold = [entity_to_gold(e) for e in new_entities if e["id"] not in existing_gold_ids]
    all_gold = existing_gold + new_gold
    with GOLD_CASES_PATH.open("w") as f:
        json.dump(all_gold, f, indent=2)

    print(f"Gold cases: {len(existing_gold)} existing + {len(new_gold)} new = {len(all_gold)} total")

if __name__ == "__main__":
    main()
