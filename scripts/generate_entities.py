#!/usr/bin/env python3
"""
Generate 120 new entities for the Trace guessing game.
Appends to entities_v1.jsonl and gold_cases_v1.json.

Entities: 24 each in music, acting, sport, politics, internet.
"""

import json
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
ENTITIES_PATH = PROJECT_ROOT / "data" / "seeds" / "entities_v1.jsonl"
GOLD_CASES_PATH = PROJECT_ROOT / "data" / "eval" / "gold_cases_v1.json"

# All 64 attributes in canonical order
ALL_ATTRIBUTES = [
    "is_real_person", "is_alive", "is_female", "is_actor", "is_musician",
    "is_athlete", "is_politician", "is_internet_personality", "age_over_50",
    "age_under_30", "from_north_america", "from_europe", "known_for_movies",
    "known_for_television", "is_singer", "is_rapper", "is_band_member",
    "has_won_grammy", "known_by_single_name", "is_pop_star",
    "known_for_superhero_role", "associated_with_marvel", "has_won_oscar",
    "associated_with_disney", "plays_team_sport", "plays_solo_sport",
    "is_soccer_player", "is_tennis_player", "is_racing_driver",
    "is_basketball_player", "is_wrestler", "has_won_major_championship",
    "is_us_president", "has_won_nobel_prize", "known_for_reality_tv",
    "known_for_social_media", "known_for_streaming", "is_business_person",
    "is_fictional", "is_historical_figure", "is_director", "is_comedian",
    "is_standup_comedian", "is_host", "is_author", "is_scientist",
    "is_royalty", "is_head_of_state", "has_held_elected_office",
    "uses_stage_name", "does_voice_acting", "known_for_comedy",
    "known_for_drama_only", "peak_era_90s", "peak_era_2000s", "is_democrat",
    "is_republican", "held_office_pre_2000", "age_over_75", "is_gaming_creator",
    "is_challenge_creator", "is_american", "is_swedish", "subscriber_count_tier",
]


def _base():
    """Return a dict of all 64 attributes set to 0.0."""
    return {a: 0.0 for a in ALL_ATTRIBUTES}


def _music_base(**overrides):
    d = _base()
    d.update({"is_real_person": 1.0, "is_alive": 1.0, "is_musician": 1.0, "is_fictional": 0.0})
    d.update(overrides)
    return d


def _acting_base(**overrides):
    d = _base()
    d.update({"is_real_person": 1.0, "is_alive": 1.0, "is_actor": 1.0, "is_fictional": 0.0})
    d.update(overrides)
    return d


def _sport_base(**overrides):
    d = _base()
    d.update({"is_real_person": 1.0, "is_alive": 1.0, "is_athlete": 1.0, "is_fictional": 0.0})
    d.update(overrides)
    return d


def _politics_base(**overrides):
    d = _base()
    d.update({"is_real_person": 1.0, "is_alive": 1.0, "is_politician": 1.0, "is_fictional": 0.0})
    d.update(overrides)
    return d


def _internet_base(**overrides):
    d = _base()
    d.update({
        "is_real_person": 1.0, "is_alive": 1.0,
        "is_internet_personality": 1.0, "is_fictional": 0.0,
        "known_for_social_media": 1.0,
    })
    d.update(overrides)
    return d


# ─── MUSIC (24) ────────────────────────────────────────────────────────

MUSIC_ENTITIES = [
    {
        "id": "ed_sheeran", "name": "Ed Sheeran",
        "aliases": ["Edward Christopher Sheeran"], "categories": ["musician", "singer"],
        "popularity_score": 95,
        "attributes": _music_base(
            is_female=0.0, is_singer=1.0, is_pop_star=1.0, has_won_grammy=1.0,
            known_by_single_name=0.0, is_rapper=0.1, is_band_member=0.0,
            from_europe=1.0, from_north_america=0.0, is_american=0.0, is_swedish=0.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.4, peak_era_2000s=1.0, uses_stage_name=0.0,
            is_actor=0.1, does_voice_acting=0.1, known_for_movies=0.0,
            known_for_television=0.1, is_business_person=0.1,
        ),
    },
    {
        "id": "billie_eilish", "name": "Billie Eilish",
        "aliases": ["Billie Eilish Pirate Baird O'Connell"], "categories": ["musician", "singer", "pop_star"],
        "popularity_score": 94,
        "attributes": _music_base(
            is_female=1.0, is_singer=1.0, is_pop_star=1.0, has_won_grammy=1.0,
            known_by_single_name=0.0, is_rapper=0.0, is_band_member=0.0,
            from_north_america=1.0, from_europe=0.0, is_american=1.0,
            age_over_50=0.0, age_under_30=1.0, age_over_75=0.0,
            known_for_social_media=0.7, peak_era_2000s=1.0, uses_stage_name=0.0,
            does_voice_acting=0.1, has_won_oscar=1.0,  # Bond theme / Oscar for song
            associated_with_disney=0.1,
        ),
    },
    {
        "id": "kanye_west", "name": "Kanye West",
        "aliases": ["Ye", "Kanye Omari West"], "categories": ["musician", "rapper", "business_person"],
        "popularity_score": 96,
        "attributes": _music_base(
            is_female=0.0, is_singer=0.6, is_rapper=1.0, is_pop_star=0.7,
            has_won_grammy=1.0, known_by_single_name=0.7, is_band_member=0.0,
            from_north_america=1.0, from_europe=0.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.7, peak_era_2000s=1.0,
            uses_stage_name=1.0,  # legally changed to Ye
            is_business_person=0.8, is_politician=0.1,
            known_for_reality_tv=0.3,
        ),
    },
    {
        "id": "justin_bieber", "name": "Justin Bieber",
        "aliases": [], "categories": ["musician", "singer", "pop_star"],
        "popularity_score": 93,
        "attributes": _music_base(
            is_female=0.0, is_singer=1.0, is_pop_star=1.0, has_won_grammy=1.0,
            known_by_single_name=0.0, is_rapper=0.2, is_band_member=0.0,
            from_north_america=1.0, from_europe=0.0, is_american=0.0,  # Canadian
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.6, peak_era_2000s=1.0,
            uses_stage_name=0.0, is_internet_personality=0.3,
        ),
    },
    {
        "id": "ariana_grande", "name": "Ariana Grande",
        "aliases": ["Ariana Grande-Butera"], "categories": ["musician", "singer", "pop_star"],
        "popularity_score": 95,
        "attributes": _music_base(
            is_female=1.0, is_singer=1.0, is_pop_star=1.0, has_won_grammy=1.0,
            known_by_single_name=0.0, is_rapper=0.0, is_band_member=0.0,
            from_north_america=1.0, from_europe=0.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            is_actor=0.6, known_for_television=0.5, known_for_movies=0.3,
            known_for_social_media=0.6, peak_era_2000s=1.0,
            uses_stage_name=0.0, does_voice_acting=0.1,
            known_for_comedy=0.2,
        ),
    },
    {
        "id": "the_weeknd", "name": "The Weeknd",
        "aliases": ["Abel Tesfaye"], "categories": ["musician", "singer"],
        "popularity_score": 94,
        "attributes": _music_base(
            is_female=0.0, is_singer=1.0, is_pop_star=0.8, has_won_grammy=1.0,
            known_by_single_name=1.0, is_rapper=0.2, is_band_member=0.0,
            from_north_america=1.0, from_europe=0.0, is_american=0.0,  # Canadian-Ethiopian
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.4, peak_era_2000s=1.0,
            uses_stage_name=1.0, is_actor=0.2,
            known_for_drama_only=0.1,
        ),
    },
    {
        "id": "lady_gaga", "name": "Lady Gaga",
        "aliases": ["Stefani Joanne Angelina Germanotta"], "categories": ["musician", "singer", "pop_star"],
        "popularity_score": 95,
        "attributes": _music_base(
            is_female=1.0, is_singer=1.0, is_pop_star=1.0, has_won_grammy=1.0,
            known_by_single_name=0.8, is_rapper=0.0, is_band_member=0.0,
            from_north_america=1.0, from_europe=0.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            is_actor=0.7, known_for_movies=0.5, has_won_oscar=1.0,
            known_for_social_media=0.5, peak_era_2000s=1.0,
            uses_stage_name=1.0, known_for_drama_only=0.3,
        ),
    },
    {
        "id": "bruno_mars", "name": "Bruno Mars",
        "aliases": ["Peter Gene Hernandez"], "categories": ["musician", "singer", "pop_star"],
        "popularity_score": 93,
        "attributes": _music_base(
            is_female=0.0, is_singer=1.0, is_pop_star=1.0, has_won_grammy=1.0,
            known_by_single_name=0.0, is_rapper=0.1, is_band_member=0.3,
            from_north_america=1.0, from_europe=0.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.3, peak_era_2000s=1.0,
            uses_stage_name=1.0,
        ),
    },
    {
        "id": "shakira", "name": "Shakira",
        "aliases": ["Shakira Isabel Mebarak Ripoll"], "categories": ["musician", "singer", "pop_star"],
        "popularity_score": 93,
        "attributes": _music_base(
            is_female=1.0, is_singer=1.0, is_pop_star=1.0, has_won_grammy=1.0,
            known_by_single_name=1.0, is_rapper=0.0, is_band_member=0.0,
            from_north_america=0.0, from_europe=0.0, is_american=0.0,  # Colombian
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.4, peak_era_2000s=1.0, peak_era_90s=0.3,
            uses_stage_name=0.0, known_for_television=0.3,  # The Voice judge
            is_host=0.1,
        ),
    },
    {
        "id": "eminem", "name": "Eminem",
        "aliases": ["Marshall Bruce Mathers III", "Slim Shady"], "categories": ["musician", "rapper"],
        "popularity_score": 95,
        "attributes": _music_base(
            is_female=0.0, is_singer=0.3, is_rapper=1.0, is_pop_star=0.5,
            has_won_grammy=1.0, known_by_single_name=1.0, is_band_member=0.0,
            from_north_america=1.0, from_europe=0.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.2, peak_era_2000s=0.8, peak_era_90s=1.0,
            uses_stage_name=1.0, is_actor=0.3, known_for_movies=0.3,
            has_won_oscar=1.0,  # Lose Yourself
        ),
    },
    {
        "id": "jay_z", "name": "Jay-Z",
        "aliases": ["Shawn Corey Carter", "Hov", "Jigga"], "categories": ["musician", "rapper", "business_person"],
        "popularity_score": 94,
        "attributes": _music_base(
            is_female=0.0, is_singer=0.2, is_rapper=1.0, is_pop_star=0.4,
            has_won_grammy=1.0, known_by_single_name=0.8, is_band_member=0.0,
            from_north_america=1.0, from_europe=0.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.2, peak_era_2000s=1.0, peak_era_90s=0.8,
            uses_stage_name=1.0, is_business_person=1.0,
        ),
    },
    {
        "id": "katy_perry", "name": "Katy Perry",
        "aliases": ["Katheryn Elizabeth Hudson"], "categories": ["musician", "singer", "pop_star"],
        "popularity_score": 92,
        "attributes": _music_base(
            is_female=1.0, is_singer=1.0, is_pop_star=1.0, has_won_grammy=0.0,
            known_by_single_name=0.0, is_rapper=0.0, is_band_member=0.0,
            from_north_america=1.0, from_europe=0.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.4, peak_era_2000s=1.0,
            uses_stage_name=1.0, known_for_television=0.4,  # American Idol judge
            is_host=0.2,
        ),
    },
    {
        "id": "dua_lipa", "name": "Dua Lipa",
        "aliases": [], "categories": ["musician", "singer", "pop_star"],
        "popularity_score": 91,
        "attributes": _music_base(
            is_female=1.0, is_singer=1.0, is_pop_star=1.0, has_won_grammy=1.0,
            known_by_single_name=0.0, is_rapper=0.0, is_band_member=0.0,
            from_europe=1.0, from_north_america=0.0, is_american=0.0,  # British-Albanian
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.5, peak_era_2000s=1.0,
            uses_stage_name=0.0,
        ),
    },
    {
        "id": "harry_styles", "name": "Harry Styles",
        "aliases": ["Harry Edward Styles"], "categories": ["musician", "singer", "pop_star"],
        "popularity_score": 93,
        "attributes": _music_base(
            is_female=0.0, is_singer=1.0, is_pop_star=1.0, has_won_grammy=1.0,
            known_by_single_name=0.0, is_rapper=0.0, is_band_member=1.0,  # One Direction
            from_europe=1.0, from_north_america=0.0, is_american=0.0,  # British
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            is_actor=0.5, known_for_movies=0.3, known_for_social_media=0.5,
            peak_era_2000s=1.0, uses_stage_name=0.0,
        ),
    },
    {
        "id": "olivia_rodrigo", "name": "Olivia Rodrigo",
        "aliases": ["Olivia Isabel Rodrigo"], "categories": ["musician", "singer", "pop_star"],
        "popularity_score": 90,
        "attributes": _music_base(
            is_female=1.0, is_singer=1.0, is_pop_star=1.0, has_won_grammy=1.0,
            known_by_single_name=0.0, is_rapper=0.0, is_band_member=0.0,
            from_north_america=1.0, from_europe=0.0, is_american=1.0,
            age_over_50=0.0, age_under_30=1.0, age_over_75=0.0,
            is_actor=0.5, known_for_television=0.4, associated_with_disney=0.7,
            known_for_social_media=0.6, peak_era_2000s=1.0,
            uses_stage_name=0.0,
        ),
    },
    {
        "id": "post_malone", "name": "Post Malone",
        "aliases": ["Austin Richard Post"], "categories": ["musician", "singer", "rapper"],
        "popularity_score": 91,
        "attributes": _music_base(
            is_female=0.0, is_singer=0.8, is_rapper=0.8, is_pop_star=0.6,
            has_won_grammy=1.0, known_by_single_name=0.0, is_band_member=0.0,
            from_north_america=1.0, from_europe=0.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.4, peak_era_2000s=1.0,
            uses_stage_name=1.0,
        ),
    },
    {
        "id": "travis_scott", "name": "Travis Scott",
        "aliases": ["Jacques Bermon Webster II", "La Flame"], "categories": ["musician", "rapper"],
        "popularity_score": 91,
        "attributes": _music_base(
            is_female=0.0, is_singer=0.4, is_rapper=1.0, is_pop_star=0.5,
            has_won_grammy=0.0, known_by_single_name=0.0, is_band_member=0.0,
            from_north_america=1.0, from_europe=0.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.5, peak_era_2000s=1.0,
            uses_stage_name=1.0, is_business_person=0.4,
        ),
    },
    {
        "id": "nicki_minaj", "name": "Nicki Minaj",
        "aliases": ["Onika Tanya Maraj-Petty"], "categories": ["musician", "rapper"],
        "popularity_score": 93,
        "attributes": _music_base(
            is_female=1.0, is_singer=0.6, is_rapper=1.0, is_pop_star=0.7,
            has_won_grammy=0.0, known_by_single_name=0.0, is_band_member=0.0,
            from_north_america=1.0, from_europe=0.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.6, peak_era_2000s=1.0,
            uses_stage_name=1.0, is_actor=0.2, does_voice_acting=0.3,
            known_for_television=0.2,
        ),
    },
    {
        "id": "cardi_b", "name": "Cardi B",
        "aliases": ["Belcalis Marlenis Almanzar"], "categories": ["musician", "rapper"],
        "popularity_score": 91,
        "attributes": _music_base(
            is_female=1.0, is_singer=0.3, is_rapper=1.0, is_pop_star=0.5,
            has_won_grammy=1.0, known_by_single_name=0.8, is_band_member=0.0,
            from_north_america=1.0, from_europe=0.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.8, known_for_reality_tv=0.6,
            peak_era_2000s=1.0, uses_stage_name=1.0,
            is_internet_personality=0.4,
        ),
    },
    {
        "id": "sza", "name": "SZA",
        "aliases": ["Solana Imani Rowe"], "categories": ["musician", "singer"],
        "popularity_score": 90,
        "attributes": _music_base(
            is_female=1.0, is_singer=1.0, is_pop_star=0.6, has_won_grammy=1.0,
            known_by_single_name=1.0, is_rapper=0.1, is_band_member=0.0,
            from_north_america=1.0, from_europe=0.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.4, peak_era_2000s=1.0,
            uses_stage_name=1.0,
        ),
    },
    {
        "id": "bts_group", "name": "BTS",
        "aliases": ["Bangtan Sonyeondan", "Bangtan Boys", "Beyond The Scene"],
        "categories": ["musician", "singer", "pop_star"],
        "popularity_score": 96,
        "attributes": _music_base(
            is_female=0.0, is_singer=1.0, is_pop_star=1.0, has_won_grammy=0.0,
            known_by_single_name=1.0, is_rapper=0.3, is_band_member=1.0,
            from_north_america=0.0, from_europe=0.0, is_american=0.0,  # South Korean
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.9, peak_era_2000s=1.0,
            uses_stage_name=1.0, is_internet_personality=0.3,
        ),
    },
    {
        "id": "elton_john", "name": "Elton John",
        "aliases": ["Reginald Kenneth Dwight", "Sir Elton John"], "categories": ["musician", "singer", "pop_star"],
        "popularity_score": 92,
        "attributes": _music_base(
            is_female=0.0, is_singer=1.0, is_pop_star=1.0, has_won_grammy=1.0,
            known_by_single_name=0.0, is_rapper=0.0, is_band_member=0.0,
            from_europe=1.0, from_north_america=0.0, is_american=0.0,  # British
            age_over_50=1.0, age_under_30=0.0, age_over_75=1.0,
            known_for_social_media=0.1, peak_era_2000s=0.3, peak_era_90s=0.6,
            uses_stage_name=1.0, is_royalty=0.0,
            has_won_oscar=1.0, associated_with_disney=0.6,
            is_author=0.2, is_historical_figure=0.3,
        ),
    },
    {
        "id": "madonna", "name": "Madonna",
        "aliases": ["Madonna Louise Ciccone"], "categories": ["musician", "singer", "pop_star"],
        "popularity_score": 92,
        "attributes": _music_base(
            is_female=1.0, is_singer=1.0, is_pop_star=1.0, has_won_grammy=1.0,
            known_by_single_name=1.0, is_rapper=0.0, is_band_member=0.0,
            from_north_america=1.0, from_europe=0.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.2, peak_era_2000s=0.3, peak_era_90s=0.8,
            uses_stage_name=0.0,  # real first name
            is_actor=0.3, known_for_movies=0.2,
            is_business_person=0.4, is_director=0.1,
            is_historical_figure=0.3,
        ),
    },
    {
        "id": "michael_jackson", "name": "Michael Jackson",
        "aliases": ["King of Pop", "MJ"], "categories": ["musician", "singer", "pop_star"],
        "popularity_score": 97,
        "attributes": _music_base(
            is_alive=0.0,  # deceased 2009
            is_female=0.0, is_singer=1.0, is_pop_star=1.0, has_won_grammy=1.0,
            known_by_single_name=0.0, is_rapper=0.0, is_band_member=1.0,  # Jackson 5
            from_north_america=1.0, from_europe=0.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_social_media=0.0, peak_era_2000s=0.2, peak_era_90s=0.7,
            uses_stage_name=0.0,
            is_historical_figure=1.0, is_business_person=0.3,
            does_voice_acting=0.1,
        ),
    },
]

# ─── ACTING (24) ───────────────────────────────────────────────────────

ACTING_ENTITIES = [
    {
        "id": "brad_pitt", "name": "Brad Pitt",
        "aliases": ["William Bradley Pitt"], "categories": ["actor"],
        "popularity_score": 94,
        "attributes": _acting_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.1,
            has_won_oscar=1.0, is_director=0.1, is_business_person=0.3,
            known_for_drama_only=0.4, known_for_comedy=0.3,
            peak_era_90s=0.8, peak_era_2000s=0.8, uses_stage_name=0.0,
            does_voice_acting=0.2,
        ),
    },
    {
        "id": "angelina_jolie", "name": "Angelina Jolie",
        "aliases": ["Angelina Jolie Voight"], "categories": ["actor"],
        "popularity_score": 93,
        "attributes": _acting_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.1,
            has_won_oscar=1.0, is_director=0.6, is_business_person=0.2,
            known_for_drama_only=0.5, known_for_comedy=0.0,
            peak_era_2000s=0.9, peak_era_90s=0.3, uses_stage_name=0.0,
            does_voice_acting=0.5, associated_with_disney=0.2,
        ),
    },
    {
        "id": "will_smith", "name": "Will Smith",
        "aliases": ["Willard Carroll Smith II", "The Fresh Prince"], "categories": ["actor", "musician"],
        "popularity_score": 94,
        "attributes": _acting_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.7,
            has_won_oscar=1.0, is_musician=0.5, is_rapper=0.5, is_singer=0.3,
            known_for_comedy=0.7, known_for_drama_only=0.0,
            peak_era_90s=0.8, peak_era_2000s=0.8, uses_stage_name=0.0,
            known_for_social_media=0.4, is_internet_personality=0.2,
        ),
    },
    {
        "id": "margot_robbie", "name": "Margot Robbie",
        "aliases": ["Margot Elise Robbie"], "categories": ["actor"],
        "popularity_score": 92,
        "attributes": _acting_base(
            is_female=1.0, from_north_america=0.0, from_europe=0.0,  # Australian
            is_american=0.0, age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.2,
            has_won_oscar=0.0, known_for_comedy=0.4, known_for_drama_only=0.2,
            peak_era_2000s=1.0, uses_stage_name=0.0,
            is_business_person=0.3,  # production company
        ),
    },
    {
        "id": "chris_hemsworth", "name": "Chris Hemsworth",
        "aliases": [], "categories": ["actor"],
        "popularity_score": 92,
        "attributes": _acting_base(
            is_female=0.0, from_north_america=0.0, from_europe=0.0,  # Australian
            is_american=0.0, age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.2,
            known_for_superhero_role=1.0, associated_with_marvel=1.0,
            associated_with_disney=0.6, has_won_oscar=0.0,
            known_for_comedy=0.3, known_for_drama_only=0.0,
            peak_era_2000s=1.0, uses_stage_name=0.0,
        ),
    },
    {
        "id": "jennifer_lawrence", "name": "Jennifer Lawrence",
        "aliases": ["J-Law"], "categories": ["actor"],
        "popularity_score": 92,
        "attributes": _acting_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.1,
            has_won_oscar=1.0, known_for_comedy=0.3, known_for_drama_only=0.3,
            peak_era_2000s=1.0, uses_stage_name=0.0,
        ),
    },
    {
        "id": "ryan_reynolds", "name": "Ryan Reynolds",
        "aliases": ["Ryan Rodney Reynolds"], "categories": ["actor", "business_person"],
        "popularity_score": 93,
        "attributes": _acting_base(
            is_female=0.0, from_north_america=1.0, is_american=0.0,  # Canadian
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.2,
            known_for_superhero_role=0.8, associated_with_marvel=0.7,
            associated_with_disney=0.5, has_won_oscar=0.0,
            known_for_comedy=0.9, known_for_drama_only=0.0,
            peak_era_2000s=1.0, uses_stage_name=0.0,
            is_business_person=0.7, known_for_social_media=0.5,
            does_voice_acting=0.4,
        ),
    },
    {
        "id": "emma_stone", "name": "Emma Stone",
        "aliases": ["Emily Jean Stone"], "categories": ["actor"],
        "popularity_score": 92,
        "attributes": _acting_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.1,
            has_won_oscar=1.0, known_for_comedy=0.5, known_for_drama_only=0.2,
            peak_era_2000s=1.0, uses_stage_name=0.0,
            does_voice_acting=0.3,
        ),
    },
    {
        "id": "denzel_washington", "name": "Denzel Washington",
        "aliases": ["Denzel Hayes Washington Jr."], "categories": ["actor", "director"],
        "popularity_score": 93,
        "attributes": _acting_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.1,
            has_won_oscar=1.0, is_director=0.4,
            known_for_comedy=0.0, known_for_drama_only=0.9,
            peak_era_90s=0.8, peak_era_2000s=0.7, uses_stage_name=0.0,
        ),
    },
    {
        "id": "meryl_streep", "name": "Meryl Streep",
        "aliases": ["Mary Louise Streep"], "categories": ["actor"],
        "popularity_score": 93,
        "attributes": _acting_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=1.0,
            known_for_movies=1.0, known_for_television=0.2,
            has_won_oscar=1.0, known_for_comedy=0.3, known_for_drama_only=0.6,
            peak_era_90s=0.7, peak_era_2000s=0.7, uses_stage_name=0.0,
            does_voice_acting=0.3, is_singer=0.2,
        ),
    },
    {
        "id": "keanu_reeves", "name": "Keanu Reeves",
        "aliases": ["Keanu Charles Reeves"], "categories": ["actor"],
        "popularity_score": 93,
        "attributes": _acting_base(
            is_female=0.0, from_north_america=1.0, is_american=0.0,  # Canadian-born
            age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.0,
            has_won_oscar=0.0, known_for_comedy=0.2, known_for_drama_only=0.3,
            peak_era_90s=0.8, peak_era_2000s=0.8, uses_stage_name=0.0,
            known_for_social_media=0.3, does_voice_acting=0.3,
            is_musician=0.1,
        ),
    },
    {
        "id": "natalie_portman", "name": "Natalie Portman",
        "aliases": ["Neta-Lee Hershlag"], "categories": ["actor"],
        "popularity_score": 91,
        "attributes": _acting_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.0,
            has_won_oscar=1.0, associated_with_marvel=0.5, associated_with_disney=0.5,
            known_for_superhero_role=0.4,
            known_for_comedy=0.1, known_for_drama_only=0.7,
            peak_era_2000s=0.8, peak_era_90s=0.3, uses_stage_name=1.0,
        ),
    },
    {
        "id": "chris_evans", "name": "Chris Evans",
        "aliases": ["Christopher Robert Evans"], "categories": ["actor"],
        "popularity_score": 92,
        "attributes": _acting_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.1,
            known_for_superhero_role=1.0, associated_with_marvel=1.0,
            associated_with_disney=0.6, has_won_oscar=0.0,
            known_for_comedy=0.2, known_for_drama_only=0.1,
            peak_era_2000s=1.0, uses_stage_name=0.0,
            is_director=0.2,
        ),
    },
    {
        "id": "gal_gadot", "name": "Gal Gadot",
        "aliases": ["Gal Gadot-Varsano"], "categories": ["actor"],
        "popularity_score": 90,
        "attributes": _acting_base(
            is_female=1.0, from_north_america=0.0, from_europe=0.0,  # Israeli
            is_american=0.0, age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.1,
            known_for_superhero_role=1.0, associated_with_marvel=0.0,  # DC
            associated_with_disney=0.1, has_won_oscar=0.0,
            known_for_comedy=0.1, known_for_drama_only=0.2,
            peak_era_2000s=1.0, uses_stage_name=0.0,
        ),
    },
    {
        "id": "timothee_chalamet", "name": "Timothee Chalamet",
        "aliases": ["Timothee Hal Chalamet"], "categories": ["actor"],
        "popularity_score": 91,
        "attributes": _acting_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.1,
            has_won_oscar=0.0, known_for_comedy=0.1, known_for_drama_only=0.8,
            peak_era_2000s=1.0, uses_stage_name=0.0,
            known_for_social_media=0.3,
        ),
    },
    {
        "id": "florence_pugh", "name": "Florence Pugh",
        "aliases": [], "categories": ["actor"],
        "popularity_score": 89,
        "attributes": _acting_base(
            is_female=1.0, from_europe=1.0, from_north_america=0.0,
            is_american=0.0,  # British
            age_over_50=0.0, age_under_30=1.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.1,
            associated_with_marvel=0.6, associated_with_disney=0.4,
            known_for_superhero_role=0.4, has_won_oscar=0.0,
            known_for_comedy=0.1, known_for_drama_only=0.6,
            peak_era_2000s=1.0, uses_stage_name=0.0,
        ),
    },
    {
        "id": "morgan_freeman", "name": "Morgan Freeman",
        "aliases": [], "categories": ["actor"],
        "popularity_score": 93,
        "attributes": _acting_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=1.0,
            known_for_movies=1.0, known_for_television=0.2,
            has_won_oscar=1.0, known_for_comedy=0.1, known_for_drama_only=0.8,
            peak_era_90s=0.8, peak_era_2000s=0.7, uses_stage_name=0.0,
            does_voice_acting=0.7, is_host=0.2,
            is_historical_figure=0.1,
        ),
    },
    {
        "id": "cate_blanchett", "name": "Cate Blanchett",
        "aliases": ["Catherine Elise Blanchett"], "categories": ["actor"],
        "popularity_score": 91,
        "attributes": _acting_base(
            is_female=1.0, from_north_america=0.0, from_europe=0.0,  # Australian
            is_american=0.0, age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.2,
            has_won_oscar=1.0, associated_with_marvel=0.4, associated_with_disney=0.3,
            known_for_comedy=0.1, known_for_drama_only=0.8,
            peak_era_2000s=0.8, peak_era_90s=0.3, uses_stage_name=0.0,
            does_voice_acting=0.3,
        ),
    },
    {
        "id": "samuel_l_jackson", "name": "Samuel L. Jackson",
        "aliases": ["Samuel Leroy Jackson"], "categories": ["actor"],
        "popularity_score": 94,
        "attributes": _acting_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=1.0,
            known_for_movies=1.0, known_for_television=0.2,
            has_won_oscar=0.0, associated_with_marvel=1.0, associated_with_disney=0.6,
            known_for_superhero_role=0.6,
            known_for_comedy=0.3, known_for_drama_only=0.3,
            peak_era_90s=0.9, peak_era_2000s=0.8, uses_stage_name=0.0,
            does_voice_acting=0.6,
        ),
    },
    {
        "id": "viola_davis", "name": "Viola Davis",
        "aliases": [], "categories": ["actor"],
        "popularity_score": 90,
        "attributes": _acting_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.6,
            has_won_oscar=1.0, known_for_comedy=0.0, known_for_drama_only=0.9,
            peak_era_2000s=1.0, uses_stage_name=0.0,
            is_author=0.2,
        ),
    },
    {
        "id": "jake_gyllenhaal", "name": "Jake Gyllenhaal",
        "aliases": ["Jacob Benjamin Gyllenhaal"], "categories": ["actor"],
        "popularity_score": 90,
        "attributes": _acting_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0, is_swedish=0.2,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.0,
            associated_with_marvel=0.4, known_for_superhero_role=0.3,
            has_won_oscar=0.0, known_for_comedy=0.1, known_for_drama_only=0.7,
            peak_era_2000s=0.9, peak_era_90s=0.1, uses_stage_name=0.0,
        ),
    },
    {
        "id": "anne_hathaway", "name": "Anne Hathaway",
        "aliases": ["Anne Jacqueline Hathaway"], "categories": ["actor"],
        "popularity_score": 91,
        "attributes": _acting_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=1.0, known_for_television=0.1,
            has_won_oscar=1.0, associated_with_disney=0.4,
            known_for_comedy=0.4, known_for_drama_only=0.3,
            peak_era_2000s=0.9, uses_stage_name=0.0,
            is_singer=0.3, does_voice_acting=0.3, is_host=0.1,
        ),
    },
    {
        "id": "benedict_cumberbatch", "name": "Benedict Cumberbatch",
        "aliases": ["Benedict Timothy Carlton Cumberbatch"], "categories": ["actor"],
        "popularity_score": 91,
        "attributes": _acting_base(
            is_female=0.0, from_europe=1.0, from_north_america=0.0,
            is_american=0.0,  # British
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=0.8, known_for_television=0.7,
            known_for_superhero_role=0.8, associated_with_marvel=1.0,
            associated_with_disney=0.5, has_won_oscar=0.0,
            known_for_comedy=0.1, known_for_drama_only=0.7,
            peak_era_2000s=1.0, uses_stage_name=0.0,
            does_voice_acting=0.5,
        ),
    },
    {
        "id": "pedro_pascal", "name": "Pedro Pascal",
        "aliases": ["Jose Pedro Balmaceda Pascal"], "categories": ["actor"],
        "popularity_score": 91,
        "attributes": _acting_base(
            is_female=0.0, from_north_america=0.0, from_europe=0.0,  # Chilean-American
            is_american=0.5,  # dual nationality
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            known_for_movies=0.6, known_for_television=1.0,
            associated_with_disney=0.7,  # The Mandalorian
            has_won_oscar=0.0, known_for_comedy=0.2, known_for_drama_only=0.6,
            peak_era_2000s=1.0, uses_stage_name=0.0,
            does_voice_acting=0.3, known_for_social_media=0.4,
        ),
    },
]

# ─── SPORT (24) ────────────────────────────────────────────────────────

SPORT_ENTITIES = [
    {
        "id": "novak_djokovic", "name": "Novak Djokovic",
        "aliases": ["Nole"], "categories": ["athlete", "tennis_player"],
        "popularity_score": 93,
        "attributes": _sport_base(
            is_female=0.0, from_europe=1.0, from_north_america=0.0,
            is_american=0.0,  # Serbian
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            plays_solo_sport=1.0, plays_team_sport=0.0,
            is_tennis_player=1.0, has_won_major_championship=1.0,
            peak_era_2000s=1.0,
        ),
    },
    {
        "id": "naomi_osaka", "name": "Naomi Osaka",
        "aliases": [], "categories": ["athlete", "tennis_player"],
        "popularity_score": 88,
        "attributes": _sport_base(
            is_female=1.0, from_north_america=0.0, from_europe=0.0,  # Japanese
            is_american=0.0,
            age_over_50=0.0, age_under_30=1.0, age_over_75=0.0,
            plays_solo_sport=1.0, plays_team_sport=0.0,
            is_tennis_player=1.0, has_won_major_championship=1.0,
            peak_era_2000s=1.0, known_for_social_media=0.5,
            is_business_person=0.3,
        ),
    },
    {
        "id": "usain_bolt", "name": "Usain Bolt",
        "aliases": ["Lightning Bolt"], "categories": ["athlete"],
        "popularity_score": 92,
        "attributes": _sport_base(
            is_female=0.0, from_north_america=0.0, from_europe=0.0,  # Jamaican
            is_american=0.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            plays_solo_sport=1.0, plays_team_sport=0.0,
            has_won_major_championship=1.0,
            peak_era_2000s=1.0, known_by_single_name=0.0,
            is_historical_figure=0.2,
        ),
    },
    {
        "id": "simone_biles", "name": "Simone Biles",
        "aliases": ["Simone Arianne Biles"], "categories": ["athlete"],
        "popularity_score": 91,
        "attributes": _sport_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=1.0, age_over_75=0.0,
            plays_solo_sport=1.0, plays_team_sport=0.2,
            has_won_major_championship=1.0,
            peak_era_2000s=1.0, known_for_social_media=0.4,
        ),
    },
    {
        "id": "neymar", "name": "Neymar",
        "aliases": ["Neymar da Silva Santos Junior", "Neymar Jr"], "categories": ["athlete", "soccer_player"],
        "popularity_score": 93,
        "attributes": _sport_base(
            is_female=0.0, from_north_america=0.0, from_europe=0.0,  # Brazilian
            is_american=0.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            plays_team_sport=1.0, plays_solo_sport=0.0,
            is_soccer_player=1.0, has_won_major_championship=0.6,
            peak_era_2000s=1.0, known_by_single_name=1.0,
            known_for_social_media=0.6,
        ),
    },
    {
        "id": "kylian_mbappe", "name": "Kylian Mbappe",
        "aliases": ["Kylian Mbappe Lottin"], "categories": ["athlete", "soccer_player"],
        "popularity_score": 93,
        "attributes": _sport_base(
            is_female=0.0, from_europe=1.0, from_north_america=0.0,
            is_american=0.0,  # French
            age_over_50=0.0, age_under_30=1.0, age_over_75=0.0,
            plays_team_sport=1.0, plays_solo_sport=0.0,
            is_soccer_player=1.0, has_won_major_championship=1.0,  # World Cup 2018
            peak_era_2000s=1.0, known_for_social_media=0.4,
        ),
    },
    {
        "id": "patrick_mahomes", "name": "Patrick Mahomes",
        "aliases": ["Patrick Lavon Mahomes II"], "categories": ["athlete"],
        "popularity_score": 91,
        "attributes": _sport_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            plays_team_sport=1.0, plays_solo_sport=0.0,
            has_won_major_championship=1.0,
            peak_era_2000s=1.0,
        ),
    },
    {
        "id": "stephen_curry", "name": "Stephen Curry",
        "aliases": ["Wardell Stephen Curry II", "Steph Curry"], "categories": ["athlete", "basketball_player"],
        "popularity_score": 93,
        "attributes": _sport_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            plays_team_sport=1.0, plays_solo_sport=0.0,
            is_basketball_player=1.0, has_won_major_championship=1.0,
            peak_era_2000s=1.0,
        ),
    },
    {
        "id": "tom_brady", "name": "Tom Brady",
        "aliases": ["Thomas Edward Patrick Brady Jr."], "categories": ["athlete"],
        "popularity_score": 94,
        "attributes": _sport_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            plays_team_sport=1.0, plays_solo_sport=0.0,
            has_won_major_championship=1.0,
            peak_era_2000s=1.0, peak_era_90s=0.0,
            is_business_person=0.4, known_for_social_media=0.3,
            is_host=0.1,
        ),
    },
    {
        "id": "mike_tyson", "name": "Mike Tyson",
        "aliases": ["Michael Gerard Tyson", "Iron Mike"], "categories": ["athlete"],
        "popularity_score": 91,
        "attributes": _sport_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            plays_solo_sport=1.0, plays_team_sport=0.0,
            has_won_major_championship=1.0,
            peak_era_90s=1.0, peak_era_2000s=0.1,
            is_actor=0.2, known_for_movies=0.2, known_for_television=0.2,
            is_internet_personality=0.2, known_for_social_media=0.3,
            is_historical_figure=0.3,
        ),
    },
    {
        "id": "tiger_woods", "name": "Tiger Woods",
        "aliases": ["Eldrick Tont Woods"], "categories": ["athlete"],
        "popularity_score": 93,
        "attributes": _sport_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            plays_solo_sport=1.0, plays_team_sport=0.0,
            has_won_major_championship=1.0,
            peak_era_2000s=0.8, peak_era_90s=0.7,
            is_business_person=0.3, is_historical_figure=0.2,
        ),
    },
    {
        "id": "michael_phelps", "name": "Michael Phelps",
        "aliases": ["Michael Fred Phelps II"], "categories": ["athlete"],
        "popularity_score": 91,
        "attributes": _sport_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            plays_solo_sport=1.0, plays_team_sport=0.1,
            has_won_major_championship=1.0,
            peak_era_2000s=1.0, peak_era_90s=0.0,
            is_historical_figure=0.2,
        ),
    },
    {
        "id": "connor_mcgregor", "name": "Conor McGregor",
        "aliases": ["The Notorious"], "categories": ["athlete"],
        "popularity_score": 91,
        "attributes": _sport_base(
            is_female=0.0, from_europe=1.0, from_north_america=0.0,
            is_american=0.0,  # Irish
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            plays_solo_sport=1.0, plays_team_sport=0.0,
            has_won_major_championship=1.0,
            peak_era_2000s=1.0,
            is_business_person=0.6, known_for_social_media=0.6,
            is_internet_personality=0.2, is_actor=0.1,
        ),
    },
    {
        "id": "alex_morgan", "name": "Alex Morgan",
        "aliases": ["Alexandra Patricia Morgan Carrasco"], "categories": ["athlete", "soccer_player"],
        "popularity_score": 87,
        "attributes": _sport_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            plays_team_sport=1.0, plays_solo_sport=0.0,
            is_soccer_player=1.0, has_won_major_championship=1.0,
            peak_era_2000s=1.0,
            is_author=0.2, known_for_social_media=0.3,
        ),
    },
    {
        "id": "megan_rapinoe", "name": "Megan Rapinoe",
        "aliases": [], "categories": ["athlete", "soccer_player"],
        "popularity_score": 87,
        "attributes": _sport_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            plays_team_sport=1.0, plays_solo_sport=0.0,
            is_soccer_player=1.0, has_won_major_championship=1.0,
            peak_era_2000s=1.0,
            is_politician=0.1, known_for_social_media=0.4,
        ),
    },
    {
        "id": "shaquille_oneal", "name": "Shaquille O'Neal",
        "aliases": ["Shaq"], "categories": ["athlete", "basketball_player"],
        "popularity_score": 92,
        "attributes": _sport_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            plays_team_sport=1.0, plays_solo_sport=0.0,
            is_basketball_player=1.0, has_won_major_championship=1.0,
            peak_era_90s=0.7, peak_era_2000s=0.8,
            known_by_single_name=0.8,
            is_actor=0.3, known_for_movies=0.2, known_for_television=0.4,
            is_host=0.3, is_comedian=0.2, is_business_person=0.6,
            is_rapper=0.2, is_musician=0.1,
            known_for_social_media=0.3, is_internet_personality=0.2,
        ),
    },
    {
        "id": "kobe_bryant", "name": "Kobe Bryant",
        "aliases": ["Black Mamba", "Kobe Bean Bryant"], "categories": ["athlete", "basketball_player"],
        "popularity_score": 95,
        "attributes": _sport_base(
            is_alive=0.0,  # deceased 2020
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            plays_team_sport=1.0, plays_solo_sport=0.0,
            is_basketball_player=1.0, has_won_major_championship=1.0,
            peak_era_90s=0.4, peak_era_2000s=1.0,
            is_business_person=0.3, is_author=0.2,
            has_won_oscar=1.0,  # animated short "Dear Basketball"
            is_historical_figure=0.6,
        ),
    },
    {
        "id": "michael_jordan", "name": "Michael Jordan",
        "aliases": ["MJ", "Air Jordan", "His Airness"], "categories": ["athlete", "basketball_player"],
        "popularity_score": 96,
        "attributes": _sport_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            plays_team_sport=1.0, plays_solo_sport=0.0,
            is_basketball_player=1.0, has_won_major_championship=1.0,
            peak_era_90s=1.0, peak_era_2000s=0.1,
            is_business_person=1.0, is_actor=0.2, known_for_movies=0.3,
            is_historical_figure=0.7,
        ),
    },
    {
        "id": "wayne_gretzky", "name": "Wayne Gretzky",
        "aliases": ["The Great One"], "categories": ["athlete"],
        "popularity_score": 89,
        "attributes": _sport_base(
            is_female=0.0, from_north_america=1.0, is_american=0.0,  # Canadian
            age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            plays_team_sport=1.0, plays_solo_sport=0.0,
            has_won_major_championship=1.0,
            peak_era_90s=0.6, peak_era_2000s=0.0,
            is_historical_figure=0.6,
        ),
    },
    {
        "id": "muhammad_ali", "name": "Muhammad Ali",
        "aliases": ["Cassius Marcellus Clay Jr.", "The Greatest"], "categories": ["athlete"],
        "popularity_score": 95,
        "attributes": _sport_base(
            is_alive=0.0,  # deceased 2016
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            plays_solo_sport=1.0, plays_team_sport=0.0,
            has_won_major_championship=1.0,
            peak_era_90s=0.0, peak_era_2000s=0.0,
            uses_stage_name=1.0,
            is_historical_figure=1.0, is_politician=0.2,
            is_author=0.2,
        ),
    },
    {
        "id": "venus_williams", "name": "Venus Williams",
        "aliases": ["Venus Ebony Starr Williams"], "categories": ["athlete", "tennis_player"],
        "popularity_score": 89,
        "attributes": _sport_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            plays_solo_sport=1.0, plays_team_sport=0.1,
            is_tennis_player=1.0, has_won_major_championship=1.0,
            peak_era_2000s=0.7, peak_era_90s=0.4,
            is_business_person=0.4,
        ),
    },
    {
        "id": "rafael_nadal", "name": "Rafael Nadal",
        "aliases": ["Rafa", "Rafael Nadal Parera"], "categories": ["athlete", "tennis_player"],
        "popularity_score": 93,
        "attributes": _sport_base(
            is_female=0.0, from_europe=1.0, from_north_america=0.0,
            is_american=0.0,  # Spanish
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            plays_solo_sport=1.0, plays_team_sport=0.0,
            is_tennis_player=1.0, has_won_major_championship=1.0,
            peak_era_2000s=1.0,
            is_historical_figure=0.1,
        ),
    },
    {
        "id": "max_verstappen", "name": "Max Verstappen",
        "aliases": ["Max Emilian Verstappen"], "categories": ["athlete", "racing_driver"],
        "popularity_score": 90,
        "attributes": _sport_base(
            is_female=0.0, from_europe=1.0, from_north_america=0.0,
            is_american=0.0,  # Dutch-Belgian
            age_over_50=0.0, age_under_30=1.0, age_over_75=0.0,
            plays_solo_sport=1.0, plays_team_sport=0.0,
            is_racing_driver=1.0, has_won_major_championship=1.0,
            peak_era_2000s=1.0,
            known_for_social_media=0.3, is_gaming_creator=0.2,
        ),
    },
    {
        "id": "luka_modric", "name": "Luka Modric",
        "aliases": [], "categories": ["athlete", "soccer_player"],
        "popularity_score": 89,
        "attributes": _sport_base(
            is_female=0.0, from_europe=1.0, from_north_america=0.0,
            is_american=0.0,  # Croatian
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            plays_team_sport=1.0, plays_solo_sport=0.0,
            is_soccer_player=1.0, has_won_major_championship=1.0,
            peak_era_2000s=1.0,
        ),
    },
]

# ─── POLITICS (24) ─────────────────────────────────────────────────────

POLITICS_ENTITIES = [
    {
        "id": "hillary_clinton", "name": "Hillary Clinton",
        "aliases": ["Hillary Rodham Clinton", "Hillary Diane Rodham Clinton"],
        "categories": ["politician", "author"],
        "popularity_score": 92,
        "attributes": _politics_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=1.0,
            is_democrat=1.0, is_republican=0.0,
            is_head_of_state=0.0, has_held_elected_office=1.0,
            held_office_pre_2000=0.0,
            is_us_president=0.0, has_won_nobel_prize=0.0,
            is_author=0.6, is_historical_figure=0.4,
        ),
    },
    {
        "id": "bernie_sanders", "name": "Bernie Sanders",
        "aliases": ["Bernard Sanders"], "categories": ["politician"],
        "popularity_score": 89,
        "attributes": _politics_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=1.0,
            is_democrat=0.7,  # Independent, caucuses with Democrats
            is_republican=0.0,
            is_head_of_state=0.0, has_held_elected_office=1.0,
            held_office_pre_2000=1.0,
            is_us_president=0.0, has_won_nobel_prize=0.0,
            is_author=0.4, is_internet_personality=0.2,
            known_for_social_media=0.4,
        ),
    },
    {
        "id": "kamala_harris", "name": "Kamala Harris",
        "aliases": ["Kamala Devi Harris"], "categories": ["politician"],
        "popularity_score": 93,
        "attributes": _politics_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=1.0, is_republican=0.0,
            is_head_of_state=0.0,  # VP not head of state
            has_held_elected_office=1.0,
            held_office_pre_2000=0.0,
            is_us_president=0.0, has_won_nobel_prize=0.0,
            is_author=0.3,
        ),
    },
    {
        "id": "emmanuel_macron", "name": "Emmanuel Macron",
        "aliases": [], "categories": ["politician"],
        "popularity_score": 90,
        "attributes": _politics_base(
            is_female=0.0, from_europe=1.0, from_north_america=0.0,
            is_american=0.0,  # French
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=0.0, is_republican=0.0,
            is_head_of_state=1.0, has_held_elected_office=1.0,
            held_office_pre_2000=0.0,
            is_us_president=0.0, has_won_nobel_prize=0.0,
        ),
    },
    {
        "id": "justin_trudeau", "name": "Justin Trudeau",
        "aliases": ["Justin Pierre James Trudeau"], "categories": ["politician"],
        "popularity_score": 89,
        "attributes": _politics_base(
            is_female=0.0, from_north_america=1.0, is_american=0.0,  # Canadian
            age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=0.0, is_republican=0.0,
            is_head_of_state=1.0, has_held_elected_office=1.0,
            held_office_pre_2000=0.0,
            is_us_president=0.0, has_won_nobel_prize=0.0,
            known_for_social_media=0.4,
        ),
    },
    {
        "id": "boris_johnson", "name": "Boris Johnson",
        "aliases": ["Alexander Boris de Pfeffel Johnson"], "categories": ["politician", "author"],
        "popularity_score": 88,
        "attributes": _politics_base(
            is_female=0.0, from_europe=1.0, from_north_america=0.0,
            is_american=0.0,  # British (born in US but British politician)
            age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=0.0, is_republican=0.0,
            is_head_of_state=0.8,  # was PM
            has_held_elected_office=1.0,
            held_office_pre_2000=0.0,
            is_us_president=0.0, has_won_nobel_prize=0.0,
            is_author=0.5, is_comedian=0.2,
        ),
    },
    {
        "id": "xi_jinping", "name": "Xi Jinping",
        "aliases": [], "categories": ["politician"],
        "popularity_score": 92,
        "attributes": _politics_base(
            is_female=0.0, from_north_america=0.0, from_europe=0.0,  # Chinese
            is_american=0.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=0.0, is_republican=0.0,
            is_head_of_state=1.0, has_held_elected_office=0.3,  # not elected in Western sense
            held_office_pre_2000=0.0,
            is_us_president=0.0, has_won_nobel_prize=0.0,
        ),
    },
    {
        "id": "jacinda_ardern", "name": "Jacinda Ardern",
        "aliases": ["Dame Jacinda Kate Laurell Ardern"], "categories": ["politician"],
        "popularity_score": 87,
        "attributes": _politics_base(
            is_female=1.0, from_north_america=0.0, from_europe=0.0,  # New Zealand
            is_american=0.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=0.0, is_republican=0.0,
            is_head_of_state=0.8,  # was PM
            has_held_elected_office=1.0,
            held_office_pre_2000=0.0,
            is_us_president=0.0, has_won_nobel_prize=0.0,
            known_for_social_media=0.3,
        ),
    },
    {
        "id": "queen_elizabeth", "name": "Queen Elizabeth II",
        "aliases": ["Elizabeth Alexandra Mary Windsor"], "categories": ["royalty", "head_of_state"],
        "popularity_score": 95,
        "attributes": _politics_base(
            is_alive=0.0,  # deceased 2022
            is_female=1.0, from_europe=1.0, from_north_america=0.0,
            is_american=0.0,  # British
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=0.0, is_republican=0.0,
            is_royalty=1.0, is_head_of_state=1.0,
            has_held_elected_office=0.0,
            held_office_pre_2000=0.0,  # not elected office
            is_us_president=0.0, has_won_nobel_prize=0.0,
            is_historical_figure=1.0, is_politician=0.3,  # monarch, not politician per se
        ),
    },
    {
        "id": "prince_william", "name": "Prince William",
        "aliases": ["William Arthur Philip Louis", "Prince of Wales"],
        "categories": ["royalty"],
        "popularity_score": 89,
        "attributes": _politics_base(
            is_female=0.0, from_europe=1.0, from_north_america=0.0,
            is_american=0.0,  # British
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=0.0, is_republican=0.0,
            is_royalty=1.0, is_head_of_state=0.0,
            has_held_elected_office=0.0,
            held_office_pre_2000=0.0,
            is_us_president=0.0, has_won_nobel_prize=0.0,
            is_politician=0.1,
            known_by_single_name=0.0,
        ),
    },
    {
        "id": "prince_harry", "name": "Prince Harry",
        "aliases": ["Henry Charles Albert David", "Duke of Sussex"],
        "categories": ["royalty"],
        "popularity_score": 89,
        "attributes": _politics_base(
            is_female=0.0, from_europe=1.0, from_north_america=0.0,
            is_american=0.0,  # British
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=0.0, is_republican=0.0,
            is_royalty=1.0, is_head_of_state=0.0,
            has_held_elected_office=0.0,
            held_office_pre_2000=0.0,
            is_us_president=0.0, has_won_nobel_prize=0.0,
            is_politician=0.1,
            is_author=0.5, known_for_social_media=0.3,
            known_for_reality_tv=0.3, is_internet_personality=0.2,
        ),
    },
    {
        "id": "michelle_obama", "name": "Michelle Obama",
        "aliases": ["Michelle LaVaughn Robinson Obama"], "categories": ["politician", "author"],
        "popularity_score": 92,
        "attributes": _politics_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=1.0, is_republican=0.0,
            is_head_of_state=0.0, has_held_elected_office=0.0,
            held_office_pre_2000=0.0,
            is_us_president=0.0, has_won_nobel_prize=0.0,
            is_politician=0.4,  # First Lady, not really a politician
            is_author=0.8, known_for_social_media=0.4,
        ),
    },
    {
        "id": "alexandria_ocasio_cortez", "name": "Alexandria Ocasio-Cortez",
        "aliases": ["AOC"], "categories": ["politician"],
        "popularity_score": 88,
        "attributes": _politics_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=1.0, is_republican=0.0,
            is_head_of_state=0.0, has_held_elected_office=1.0,
            held_office_pre_2000=0.0,
            is_us_president=0.0, has_won_nobel_prize=0.0,
            known_for_social_media=0.8, is_internet_personality=0.3,
            known_for_streaming=0.2,
            uses_stage_name=0.0, known_by_single_name=0.0,
        ),
    },
    {
        "id": "nelson_mandela", "name": "Nelson Mandela",
        "aliases": ["Madiba", "Nelson Rolihlahla Mandela"], "categories": ["politician"],
        "popularity_score": 95,
        "attributes": _politics_base(
            is_alive=0.0,  # deceased 2013
            is_female=0.0, from_north_america=0.0, from_europe=0.0,  # South African
            is_american=0.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=0.0, is_republican=0.0,
            is_head_of_state=1.0, has_held_elected_office=1.0,
            held_office_pre_2000=1.0,
            is_us_president=0.0, has_won_nobel_prize=1.0,
            is_historical_figure=1.0, is_author=0.5,
        ),
    },
    {
        "id": "jfk", "name": "John F. Kennedy",
        "aliases": ["JFK", "John Fitzgerald Kennedy", "Jack Kennedy"], "categories": ["politician"],
        "popularity_score": 93,
        "attributes": _politics_base(
            is_alive=0.0,  # deceased 1963
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=1.0, is_republican=0.0,
            is_head_of_state=1.0, has_held_elected_office=1.0,
            held_office_pre_2000=1.0,
            is_us_president=1.0, has_won_nobel_prize=0.0,
            is_historical_figure=1.0, is_author=0.4,
            known_by_single_name=0.0,
        ),
    },
    {
        "id": "abraham_lincoln", "name": "Abraham Lincoln",
        "aliases": ["Honest Abe"], "categories": ["politician"],
        "popularity_score": 93,
        "attributes": _politics_base(
            is_alive=0.0,  # deceased 1865
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=0.0, is_republican=1.0,
            is_head_of_state=1.0, has_held_elected_office=1.0,
            held_office_pre_2000=1.0,
            is_us_president=1.0, has_won_nobel_prize=0.0,
            is_historical_figure=1.0, is_author=0.3,
        ),
    },
    {
        "id": "winston_churchill", "name": "Winston Churchill",
        "aliases": ["Sir Winston Leonard Spencer Churchill"], "categories": ["politician", "author"],
        "popularity_score": 92,
        "attributes": _politics_base(
            is_alive=0.0,  # deceased 1965
            is_female=0.0, from_europe=1.0, from_north_america=0.0,
            is_american=0.0,  # British
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=0.0, is_republican=0.0,
            is_head_of_state=0.8,  # PM
            has_held_elected_office=1.0,
            held_office_pre_2000=1.0,
            is_us_president=0.0, has_won_nobel_prize=1.0,  # Literature
            is_historical_figure=1.0, is_author=0.8,
        ),
    },
    {
        "id": "margaret_thatcher", "name": "Margaret Thatcher",
        "aliases": ["The Iron Lady", "Margaret Hilda Thatcher"], "categories": ["politician"],
        "popularity_score": 90,
        "attributes": _politics_base(
            is_alive=0.0,  # deceased 2013
            is_female=1.0, from_europe=1.0, from_north_america=0.0,
            is_american=0.0,  # British
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=0.0, is_republican=0.0,
            is_head_of_state=0.8,  # PM
            has_held_elected_office=1.0,
            held_office_pre_2000=1.0,
            is_us_president=0.0, has_won_nobel_prize=0.0,
            is_historical_figure=1.0, is_author=0.3,
        ),
    },
    {
        "id": "george_w_bush", "name": "George W. Bush",
        "aliases": ["George Walker Bush", "Dubya"], "categories": ["politician"],
        "popularity_score": 90,
        "attributes": _politics_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=1.0,
            is_democrat=0.0, is_republican=1.0,
            is_head_of_state=1.0, has_held_elected_office=1.0,
            held_office_pre_2000=0.3,  # Governor before 2000
            is_us_president=1.0, has_won_nobel_prize=0.0,
            is_historical_figure=0.6, is_author=0.3,
        ),
    },
    {
        "id": "bill_clinton", "name": "Bill Clinton",
        "aliases": ["William Jefferson Clinton"], "categories": ["politician", "author"],
        "popularity_score": 91,
        "attributes": _politics_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=1.0,
            is_democrat=1.0, is_republican=0.0,
            is_head_of_state=1.0, has_held_elected_office=1.0,
            held_office_pre_2000=1.0,
            is_us_president=1.0, has_won_nobel_prize=0.0,
            is_historical_figure=0.5, is_author=0.5,
            is_musician=0.1,  # plays saxophone
        ),
    },
    {
        "id": "al_gore", "name": "Al Gore",
        "aliases": ["Albert Arnold Gore Jr."], "categories": ["politician", "author"],
        "popularity_score": 86,
        "attributes": _politics_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=1.0,
            is_democrat=1.0, is_republican=0.0,
            is_head_of_state=0.0, has_held_elected_office=1.0,
            held_office_pre_2000=1.0,
            is_us_president=0.0, has_won_nobel_prize=1.0,  # Peace Prize 2007
            is_historical_figure=0.3, is_author=0.6,
            is_business_person=0.4,
        ),
    },
    {
        "id": "ruth_bader_ginsburg", "name": "Ruth Bader Ginsburg",
        "aliases": ["RBG", "The Notorious RBG"], "categories": ["politician"],
        "popularity_score": 88,
        "attributes": _politics_base(
            is_alive=0.0,  # deceased 2020
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=0.6,  # appointed by Clinton, liberal but judges aren't party members
            is_republican=0.0,
            is_head_of_state=0.0, has_held_elected_office=0.0,
            held_office_pre_2000=0.0,
            is_us_president=0.0, has_won_nobel_prize=0.0,
            is_politician=0.3,  # judge, not politician
            is_historical_figure=0.7, is_author=0.4,
            known_for_social_media=0.3,  # became internet icon
            is_internet_personality=0.1,
        ),
    },
    {
        "id": "volodymyr_zelensky", "name": "Volodymyr Zelensky",
        "aliases": ["Volodymyr Oleksandrovych Zelenskyy"], "categories": ["politician", "actor"],
        "popularity_score": 91,
        "attributes": _politics_base(
            is_female=0.0, from_europe=1.0, from_north_america=0.0,
            is_american=0.0,  # Ukrainian
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            is_democrat=0.0, is_republican=0.0,
            is_head_of_state=1.0, has_held_elected_office=1.0,
            held_office_pre_2000=0.0,
            is_us_president=0.0, has_won_nobel_prize=0.0,
            is_actor=0.6, is_comedian=0.5, known_for_television=0.5,
            known_for_comedy=0.4, known_for_social_media=0.5,
        ),
    },
    {
        "id": "pope_francis", "name": "Pope Francis",
        "aliases": ["Jorge Mario Bergoglio"], "categories": ["head_of_state", "religious_leader"],
        "popularity_score": 92,
        "attributes": _politics_base(
            is_female=0.0, from_north_america=0.0, from_europe=0.0,  # Argentine
            is_american=0.0,
            age_over_50=1.0, age_under_30=0.0, age_over_75=1.0,
            is_democrat=0.0, is_republican=0.0,
            is_head_of_state=1.0,  # head of Vatican City
            has_held_elected_office=0.0,  # elected by conclave but not public office
            held_office_pre_2000=0.0,
            is_us_president=0.0, has_won_nobel_prize=0.0,
            is_politician=0.3,  # religious leader more than politician
            is_author=0.6, is_historical_figure=0.5,
            known_by_single_name=0.0,
            uses_stage_name=1.0,  # papal name
            known_for_social_media=0.4,
        ),
    },
]

# ─── INTERNET (24) ─────────────────────────────────────────────────────

INTERNET_ENTITIES = [
    {
        "id": "markiplier", "name": "Markiplier",
        "aliases": ["Mark Edward Fischbach"], "categories": ["internet_personality", "streamer"],
        "popularity_score": 89,
        "attributes": _internet_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            uses_stage_name=1.0, known_for_streaming=0.8,
            is_gaming_creator=1.0, is_challenge_creator=0.2,
            subscriber_count_tier=0.8,  # ~36M subs
            known_for_comedy=0.6, is_comedian=0.3,
            is_actor=0.2, is_business_person=0.3,
            peak_era_2000s=1.0,
        ),
    },
    {
        "id": "ninja_tyler", "name": "Ninja",
        "aliases": ["Tyler Blevins", "Richard Tyler Blevins"],
        "categories": ["internet_personality", "streamer"],
        "popularity_score": 88,
        "attributes": _internet_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            uses_stage_name=1.0, known_for_streaming=1.0,
            is_gaming_creator=1.0, is_challenge_creator=0.1,
            subscriber_count_tier=0.6,  # ~24M subs
            known_by_single_name=1.0,
            peak_era_2000s=1.0,
            is_athlete=0.1,
        ),
    },
    {
        "id": "pokimane", "name": "Pokimane",
        "aliases": ["Imane Anys"], "categories": ["internet_personality", "streamer"],
        "popularity_score": 87,
        "attributes": _internet_base(
            is_female=1.0, from_north_america=1.0, is_american=0.0,  # Moroccan-Canadian
            age_over_50=0.0, age_under_30=1.0, age_over_75=0.0,
            uses_stage_name=1.0, known_for_streaming=1.0,
            is_gaming_creator=0.8, is_challenge_creator=0.1,
            subscriber_count_tier=0.5,  # ~9M subs
            known_by_single_name=1.0,
            peak_era_2000s=1.0,
            is_business_person=0.4,
        ),
    },
    {
        "id": "dream_minecraft", "name": "Dream",
        "aliases": ["Clay"], "categories": ["internet_personality", "streamer"],
        "popularity_score": 86,
        "attributes": _internet_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=1.0, age_over_75=0.0,
            uses_stage_name=1.0, known_for_streaming=0.7,
            is_gaming_creator=1.0, is_challenge_creator=0.6,
            subscriber_count_tier=0.7,  # ~32M subs
            known_by_single_name=1.0,
            peak_era_2000s=1.0,
        ),
    },
    {
        "id": "addison_rae", "name": "Addison Rae",
        "aliases": ["Addison Rae Easterling"], "categories": ["internet_personality", "social_media"],
        "popularity_score": 86,
        "attributes": _internet_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=1.0, age_over_75=0.0,
            uses_stage_name=0.0, known_for_streaming=0.2,
            is_gaming_creator=0.0, is_challenge_creator=0.7,
            subscriber_count_tier=0.1,
            peak_era_2000s=1.0,
            is_actor=0.2, is_singer=0.2, is_musician=0.2,
            known_for_reality_tv=0.2,
        ),
    },
    {
        "id": "david_dobrik", "name": "David Dobrik",
        "aliases": [], "categories": ["internet_personality"],
        "popularity_score": 86,
        "attributes": _internet_base(
            is_female=0.0, from_north_america=1.0, is_american=0.5,  # Slovak-born, US-raised
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            uses_stage_name=0.0, known_for_streaming=0.2,
            is_gaming_creator=0.0, is_challenge_creator=0.7,
            subscriber_count_tier=0.6,  # ~18M subs
            peak_era_2000s=1.0,
            known_for_comedy=0.6, is_comedian=0.3,
            is_business_person=0.3,
        ),
    },
    {
        "id": "emma_chamberlain", "name": "Emma Chamberlain",
        "aliases": [], "categories": ["internet_personality", "social_media"],
        "popularity_score": 86,
        "attributes": _internet_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=1.0, age_over_75=0.0,
            uses_stage_name=0.0, known_for_streaming=0.1,
            is_gaming_creator=0.0, is_challenge_creator=0.2,
            subscriber_count_tier=0.6,  # ~12M subs
            peak_era_2000s=1.0,
            is_business_person=0.5,  # Chamberlain Coffee
            is_host=0.2,
        ),
    },
    {
        "id": "james_charles", "name": "James Charles",
        "aliases": ["James Charles Dickinson"], "categories": ["internet_personality", "social_media"],
        "popularity_score": 85,
        "attributes": _internet_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=1.0, age_over_75=0.0,
            uses_stage_name=0.0, known_for_streaming=0.2,
            is_gaming_creator=0.0, is_challenge_creator=0.3,
            subscriber_count_tier=0.6,  # ~24M subs
            peak_era_2000s=1.0,
            is_business_person=0.3,
        ),
    },
    {
        "id": "jeffree_star", "name": "Jeffree Star",
        "aliases": ["Jeffrey Lynn Steininger Jr."], "categories": ["internet_personality", "business_person"],
        "popularity_score": 85,
        "attributes": _internet_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            uses_stage_name=1.0, known_for_streaming=0.2,
            is_gaming_creator=0.0, is_challenge_creator=0.1,
            subscriber_count_tier=0.6,  # ~16M subs
            peak_era_2000s=1.0,
            is_business_person=0.9, is_musician=0.2,
            known_for_reality_tv=0.2,
        ),
    },
    {
        "id": "lilly_singh", "name": "Lilly Singh",
        "aliases": ["Superwoman", "IISuperwomanII"], "categories": ["internet_personality", "comedian"],
        "popularity_score": 85,
        "attributes": _internet_base(
            is_female=1.0, from_north_america=1.0, is_american=0.0,  # Canadian
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            uses_stage_name=1.0, known_for_streaming=0.1,
            is_gaming_creator=0.0, is_challenge_creator=0.2,
            subscriber_count_tier=0.6,  # ~15M subs
            peak_era_2000s=1.0,
            is_comedian=0.7, is_standup_comedian=0.3, known_for_comedy=0.8,
            is_host=0.6, known_for_television=0.4,
            is_author=0.3, is_actor=0.3,
        ),
    },
    {
        "id": "casey_neistat", "name": "Casey Neistat",
        "aliases": [], "categories": ["internet_personality"],
        "popularity_score": 85,
        "attributes": _internet_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            uses_stage_name=0.0, known_for_streaming=0.1,
            is_gaming_creator=0.0, is_challenge_creator=0.2,
            subscriber_count_tier=0.6,  # ~12M subs
            peak_era_2000s=1.0,
            is_director=0.5, is_business_person=0.6,
        ),
    },
    {
        "id": "marques_brownlee", "name": "Marques Brownlee",
        "aliases": ["MKBHD"], "categories": ["internet_personality"],
        "popularity_score": 87,
        "attributes": _internet_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            uses_stage_name=0.0, known_for_streaming=0.2,
            is_gaming_creator=0.0, is_challenge_creator=0.0,
            subscriber_count_tier=0.6,  # ~19M subs
            peak_era_2000s=1.0,
            is_business_person=0.4, is_athlete=0.2,  # ultimate frisbee
        ),
    },
    {
        "id": "sssniperwolf", "name": "SSSniperwolf",
        "aliases": ["Alia Marie Shelesh", "Lia"], "categories": ["internet_personality"],
        "popularity_score": 86,
        "attributes": _internet_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            uses_stage_name=1.0, known_for_streaming=0.3,
            is_gaming_creator=0.6, is_challenge_creator=0.4,
            subscriber_count_tier=0.8,  # ~34M subs
            peak_era_2000s=1.0,
            known_for_comedy=0.3,
        ),
    },
    {
        "id": "ryan_kaji", "name": "Ryan Kaji",
        "aliases": ["Ryan's World"], "categories": ["internet_personality"],
        "popularity_score": 86,
        "attributes": _internet_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=1.0, age_over_75=0.0,
            uses_stage_name=0.0, known_for_streaming=0.1,
            is_gaming_creator=0.2, is_challenge_creator=0.5,
            subscriber_count_tier=0.8,  # ~36M subs
            peak_era_2000s=1.0,
            known_for_television=0.3, is_business_person=0.3,
        ),
    },
    {
        "id": "dude_perfect", "name": "Dude Perfect",
        "aliases": ["DP"], "categories": ["internet_personality"],
        "popularity_score": 87,
        "attributes": _internet_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            uses_stage_name=1.0, known_for_streaming=0.1,
            is_gaming_creator=0.0, is_challenge_creator=1.0,
            subscriber_count_tier=0.9,  # ~60M subs
            peak_era_2000s=1.0,
            is_athlete=0.3, known_for_comedy=0.4,
            known_for_television=0.2,
        ),
    },
    {
        "id": "jake_paul", "name": "Jake Paul",
        "aliases": ["Jake Joseph Paul"], "categories": ["internet_personality", "athlete"],
        "popularity_score": 88,
        "attributes": _internet_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            uses_stage_name=0.0, known_for_streaming=0.3,
            is_gaming_creator=0.1, is_challenge_creator=0.5,
            subscriber_count_tier=0.6,  # ~20M subs
            peak_era_2000s=1.0,
            is_athlete=0.5, is_wrestler=0.3,
            known_for_comedy=0.3, is_actor=0.2,
            known_for_television=0.2, is_business_person=0.5,
            is_musician=0.1,
        ),
    },
    {
        "id": "ksi", "name": "KSI",
        "aliases": ["Olajide Olayinka Williams Olatunji", "JJ Olatunji"],
        "categories": ["internet_personality", "musician", "athlete"],
        "popularity_score": 88,
        "attributes": _internet_base(
            is_female=0.0, from_europe=1.0, from_north_america=0.0,
            is_american=0.0,  # British
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            uses_stage_name=1.0, known_for_streaming=0.5,
            is_gaming_creator=0.7, is_challenge_creator=0.5,
            subscriber_count_tier=0.6,  # ~24M subs (main + second)
            known_by_single_name=1.0,
            peak_era_2000s=1.0,
            is_athlete=0.4, is_wrestler=0.2,
            is_musician=0.6, is_rapper=0.6, is_singer=0.3,
            is_business_person=0.6, is_actor=0.1,
            known_for_comedy=0.4,
        ),
    },
    {
        "id": "ishowspeed", "name": "IShowSpeed",
        "aliases": ["Darren Watkins Jr.", "Speed"], "categories": ["internet_personality", "streamer"],
        "popularity_score": 87,
        "attributes": _internet_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=1.0, age_over_75=0.0,
            uses_stage_name=1.0, known_for_streaming=1.0,
            is_gaming_creator=0.8, is_challenge_creator=0.4,
            subscriber_count_tier=0.7,  # ~27M subs
            peak_era_2000s=1.0,
            is_musician=0.2, is_singer=0.2,
            known_for_comedy=0.4,
        ),
    },
    {
        "id": "kai_cenat", "name": "Kai Cenat",
        "aliases": [], "categories": ["internet_personality", "streamer"],
        "popularity_score": 88,
        "attributes": _internet_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=1.0, age_over_75=0.0,
            uses_stage_name=0.0, known_for_streaming=1.0,
            is_gaming_creator=0.5, is_challenge_creator=0.5,
            subscriber_count_tier=0.4,  # ~7M YouTube subs (bigger on Twitch)
            peak_era_2000s=1.0,
            known_for_comedy=0.6, is_comedian=0.3,
        ),
    },
    {
        "id": "adin_ross", "name": "Adin Ross",
        "aliases": [], "categories": ["internet_personality", "streamer"],
        "popularity_score": 86,
        "attributes": _internet_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=1.0, age_over_75=0.0,
            uses_stage_name=0.0, known_for_streaming=1.0,
            is_gaming_creator=0.6, is_challenge_creator=0.3,
            subscriber_count_tier=0.3,  # ~5M YouTube subs
            peak_era_2000s=1.0,
            known_for_comedy=0.3,
            is_politician=0.0,  # political controversies but not a politician
        ),
    },
    {
        "id": "hasan_piker", "name": "Hasan Piker",
        "aliases": ["HasanAbi"], "categories": ["internet_personality", "streamer"],
        "popularity_score": 85,
        "attributes": _internet_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            uses_stage_name=0.0, known_for_streaming=1.0,
            is_gaming_creator=0.3, is_challenge_creator=0.0,
            subscriber_count_tier=0.3,  # ~2M YouTube
            peak_era_2000s=1.0,
            is_politician=0.2,  # political commentator
            is_comedian=0.2, known_for_comedy=0.3,
            is_host=0.3,
        ),
    },
    {
        "id": "ludwig_ahgren", "name": "Ludwig",
        "aliases": ["Ludwig Anders Ahgren"], "categories": ["internet_personality", "streamer"],
        "popularity_score": 85,
        "attributes": _internet_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            is_swedish=0.2,  # Swedish-American heritage
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            uses_stage_name=0.0, known_for_streaming=1.0,
            is_gaming_creator=0.6, is_challenge_creator=0.4,
            subscriber_count_tier=0.4,  # ~6M YouTube subs
            known_by_single_name=0.8,
            peak_era_2000s=1.0,
            known_for_comedy=0.5, is_comedian=0.2,
            is_host=0.5, is_business_person=0.3,
        ),
    },
    {
        "id": "valkyrae", "name": "Valkyrae",
        "aliases": ["Rachell Hofstetter"], "categories": ["internet_personality", "streamer"],
        "popularity_score": 85,
        "attributes": _internet_base(
            is_female=1.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=0.0, age_over_75=0.0,
            uses_stage_name=1.0, known_for_streaming=1.0,
            is_gaming_creator=1.0, is_challenge_creator=0.1,
            subscriber_count_tier=0.3,  # ~4M YouTube subs
            known_by_single_name=1.0,
            peak_era_2000s=1.0,
            is_business_person=0.3,
        ),
    },
    {
        "id": "corpse_husband", "name": "Corpse Husband",
        "aliases": ["Corpse"], "categories": ["internet_personality", "musician"],
        "popularity_score": 84,
        "attributes": _internet_base(
            is_female=0.0, from_north_america=1.0, is_american=1.0,
            age_over_50=0.0, age_under_30=1.0, age_over_75=0.0,
            uses_stage_name=1.0, known_for_streaming=0.5,
            is_gaming_creator=0.6, is_challenge_creator=0.0,
            subscriber_count_tier=0.4,  # ~8M YouTube subs
            peak_era_2000s=1.0,
            is_musician=0.5, is_singer=0.4,
            known_by_single_name=0.0,
        ),
    },
]


ALL_NEW_ENTITIES = MUSIC_ENTITIES + ACTING_ENTITIES + SPORT_ENTITIES + POLITICS_ENTITIES + INTERNET_ENTITIES


def validate_entities(entities):
    """Validate that all entities have all 64 attributes."""
    errors = []
    for e in entities:
        attrs = e["attributes"]
        missing = set(ALL_ATTRIBUTES) - set(attrs.keys())
        extra = set(attrs.keys()) - set(ALL_ATTRIBUTES)
        if missing:
            errors.append(f"{e['id']}: missing attributes: {missing}")
        if extra:
            errors.append(f"{e['id']}: extra attributes: {extra}")
        for k, v in attrs.items():
            if not isinstance(v, (int, float)):
                errors.append(f"{e['id']}.{k}: value {v!r} is not a number")
            elif v < 0.0 or v > 1.0:
                errors.append(f"{e['id']}.{k}: value {v} out of range [0,1]")
    if errors:
        for err in errors:
            print(f"  ERROR: {err}")
        raise ValueError(f"{len(errors)} validation error(s)")
    print(f"  All {len(entities)} entities validated OK ({len(ALL_ATTRIBUTES)} attributes each)")


def generate_gold_answers(attrs):
    """
    Generate gold case answers from attribute values.
    >= 0.75 -> "yes"
    <= 0.25 -> "no"
    Between 0.25 and 0.75 -> omitted (ambiguous)
    """
    answers = {}
    for attr, val in attrs.items():
        if val >= 0.75:
            answers[attr] = "yes"
        elif val <= 0.25:
            answers[attr] = "no"
        # else: ambiguous, omit from gold answers
    return answers


def main():
    print("=== Trace Entity Generator ===\n")

    # Validate
    print("Validating entities...")
    validate_entities(ALL_NEW_ENTITIES)

    # Check for duplicate IDs
    ids = [e["id"] for e in ALL_NEW_ENTITIES]
    if len(ids) != len(set(ids)):
        dupes = [x for x in ids if ids.count(x) > 1]
        raise ValueError(f"Duplicate entity IDs: {set(dupes)}")
    print(f"  No duplicate IDs found\n")

    # Read existing entities to check for ID collisions
    print("Reading existing data...")
    existing_ids = set()
    if ENTITIES_PATH.exists():
        with open(ENTITIES_PATH, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    existing_ids.add(json.loads(line)["id"])
    print(f"  Found {len(existing_ids)} existing entities")

    collisions = existing_ids & set(ids)
    if collisions:
        raise ValueError(f"ID collisions with existing entities: {collisions}")
    print(f"  No ID collisions\n")

    # Read existing gold cases
    existing_gold = []
    if GOLD_CASES_PATH.exists():
        with open(GOLD_CASES_PATH, "r") as f:
            existing_gold = json.load(f)
    print(f"  Found {len(existing_gold)} existing gold cases\n")

    # Generate gold cases for new entities
    print("Generating gold cases...")
    new_gold_cases = []
    for e in ALL_NEW_ENTITIES:
        answers = generate_gold_answers(e["attributes"])
        new_gold_cases.append({
            "target_entity_id": e["id"],
            "answers": answers,
        })

    # Summary stats
    total_answers = sum(len(gc["answers"]) for gc in new_gold_cases)
    avg_answers = total_answers / len(new_gold_cases)
    print(f"  Generated {len(new_gold_cases)} gold cases")
    print(f"  Average {avg_answers:.1f} definitive answers per entity (out of {len(ALL_ATTRIBUTES)})\n")

    # Append to entities JSONL
    print("Writing entities...")
    with open(ENTITIES_PATH, "a") as f:
        for e in ALL_NEW_ENTITIES:
            entity_line = {
                "id": e["id"],
                "name": e["name"],
                "aliases": e.get("aliases", []),
                "categories": e.get("categories", []),
                "popularity_score": e.get("popularity_score", 85),
                "attributes": e["attributes"],
            }
            f.write(json.dumps(entity_line) + "\n")
    print(f"  Appended {len(ALL_NEW_ENTITIES)} entities to {ENTITIES_PATH}\n")

    # Merge and write gold cases
    print("Writing gold cases...")
    merged_gold = existing_gold + new_gold_cases
    with open(GOLD_CASES_PATH, "w") as f:
        json.dump(merged_gold, f, indent=2)
    print(f"  Wrote {len(merged_gold)} total gold cases to {GOLD_CASES_PATH}\n")

    # Domain breakdown
    print("=== Summary ===")
    print(f"  New entities added:     {len(ALL_NEW_ENTITIES)}")
    print(f"  Total entities now:     {len(existing_ids) + len(ALL_NEW_ENTITIES)}")
    print(f"  Total gold cases now:   {len(merged_gold)}")
    print()
    domains = {
        "Music": MUSIC_ENTITIES,
        "Acting": ACTING_ENTITIES,
        "Sport": SPORT_ENTITIES,
        "Politics": POLITICS_ENTITIES,
        "Internet": INTERNET_ENTITIES,
    }
    for domain, entities in domains.items():
        print(f"  {domain:12s}: {len(entities)} entities")
    print()
    print("Done!")


if __name__ == "__main__":
    main()
