#!/usr/bin/env python3
"""
Add 20 new attributes to all 150 entities in entities_v1.jsonl,
then enrich gold_cases_v1.json with corresponding yes/no answers.

New attributes:
  is_american_football_player, is_swimmer, is_golfer, is_retired,
  peak_era_2010s, peak_era_2020s, is_european_leader, is_asian_leader,
  lives_in_north_america, is_from_eastern_europe, is_beauty_creator,
  is_tech_reviewer, is_vlog_creator, is_kids_content_creator,
  is_live_streamer, is_activist, has_acting_and_music_career,
  known_for_action_films, known_for_romantic_films, has_most_titles_in_sport
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENTITIES_PATH = ROOT / "data" / "seeds" / "entities_v1.jsonl"
GOLD_PATH = ROOT / "data" / "eval" / "gold_cases_v1.json"

NEW_ATTRS = [
    "is_american_football_player",
    "is_swimmer",
    "is_golfer",
    "is_retired",
    "peak_era_2010s",
    "peak_era_2020s",
    "is_european_leader",
    "is_asian_leader",
    "lives_in_north_america",
    "is_from_eastern_europe",
    "is_beauty_creator",
    "is_tech_reviewer",
    "is_vlog_creator",
    "is_kids_content_creator",
    "is_live_streamer",
    "is_activist",
    "has_acting_and_music_career",
    "known_for_action_films",
    "known_for_romantic_films",
    "has_most_titles_in_sport",
]

# ---------------------------------------------------------------------------
# Per-entity overrides (only non-zero values listed; everything else = 0.0)
# ---------------------------------------------------------------------------
OVERRIDES: dict[str, dict[str, float]] = {
    # ── Musicians ──
    "taylor_swift": {
        "peak_era_2010s": 0.8,
        "peak_era_2020s": 0.9,
        "lives_in_north_america": 1.0,
        "has_acting_and_music_career": 0.1,
    },
    "beyonce": {
        "peak_era_2010s": 0.6,
        "peak_era_2020s": 0.4,
        "lives_in_north_america": 1.0,
        "has_acting_and_music_career": 0.4,
    },
    "drake": {
        "peak_era_2010s": 0.9,
        "peak_era_2020s": 0.5,
        "lives_in_north_america": 1.0,
        "has_acting_and_music_career": 0.4,
    },
    "adele": {
        "peak_era_2010s": 0.8,
        "peak_era_2020s": 0.5,
    },
    "rihanna": {
        "peak_era_2010s": 0.6,
        "peak_era_2020s": 0.2,
        "lives_in_north_america": 1.0,
    },
    "bad_bunny": {
        "peak_era_2010s": 0.3,
        "peak_era_2020s": 1.0,
        "lives_in_north_america": 1.0,
    },
    "ed_sheeran": {
        "peak_era_2010s": 0.9,
        "peak_era_2020s": 0.5,
    },
    "billie_eilish": {
        "peak_era_2020s": 0.9,
        "lives_in_north_america": 1.0,
    },
    "kanye_west": {
        "peak_era_2010s": 0.7,
        "peak_era_2020s": 0.4,
        "lives_in_north_america": 1.0,
    },
    "justin_bieber": {
        "peak_era_2010s": 0.9,
        "peak_era_2020s": 0.4,
        "lives_in_north_america": 1.0,
        "has_acting_and_music_career": 0.2,
    },
    "ariana_grande": {
        "peak_era_2010s": 0.8,
        "peak_era_2020s": 0.5,
        "lives_in_north_america": 1.0,
        "has_acting_and_music_career": 1.0,  # Victorious + music career
    },
    "the_weeknd": {
        "peak_era_2010s": 0.8,
        "peak_era_2020s": 0.6,
        "lives_in_north_america": 1.0,
    },
    "lady_gaga": {
        "peak_era_2010s": 0.7,
        "peak_era_2020s": 0.5,
        "lives_in_north_america": 1.0,
        "has_acting_and_music_career": 0.8,
    },
    "bruno_mars": {
        "peak_era_2010s": 0.8,
        "peak_era_2020s": 0.4,
        "lives_in_north_america": 1.0,
    },
    "shakira": {
        "peak_era_2010s": 0.5,
        "peak_era_2020s": 0.6,
    },
    "eminem": {
        "peak_era_2010s": 0.3,
        "lives_in_north_america": 1.0,
        "is_retired": 0.3,
    },
    "jay_z": {
        "peak_era_2010s": 0.4,
        "lives_in_north_america": 1.0,
    },
    "katy_perry": {
        "peak_era_2010s": 0.7,
        "peak_era_2020s": 0.2,
        "lives_in_north_america": 1.0,
    },
    "dua_lipa": {
        "peak_era_2020s": 0.9,
    },
    "harry_styles": {
        "peak_era_2010s": 0.5,
        "peak_era_2020s": 0.9,
        "has_acting_and_music_career": 0.5,
    },
    "olivia_rodrigo": {
        "peak_era_2010s": 0.1,
        "peak_era_2020s": 1.0,
        "lives_in_north_america": 1.0,
        "has_acting_and_music_career": 0.6,
    },
    "post_malone": {
        "peak_era_2010s": 0.6,
        "peak_era_2020s": 0.5,
        "lives_in_north_america": 1.0,
    },
    "travis_scott": {
        "peak_era_2010s": 0.6,
        "peak_era_2020s": 0.7,
        "lives_in_north_america": 1.0,
    },
    "nicki_minaj": {
        "peak_era_2010s": 0.8,
        "peak_era_2020s": 0.5,
        "lives_in_north_america": 1.0,
        "has_acting_and_music_career": 0.3,
    },
    "cardi_b": {
        "peak_era_2010s": 0.4,
        "peak_era_2020s": 0.6,
        "lives_in_north_america": 1.0,
    },
    "sza": {
        "peak_era_2010s": 0.3,
        "peak_era_2020s": 1.0,
        "lives_in_north_america": 1.0,
    },
    "bts_group": {
        "peak_era_2020s": 0.7,
        "is_asian_leader": 0.0,
    },
    "elton_john": {
        "is_retired": 0.8,
        "peak_era_2010s": 0.2,
        "has_acting_and_music_career": 0.3,
    },
    "madonna": {
        "is_retired": 0.3,
        "peak_era_2010s": 0.2,
        "lives_in_north_america": 1.0,
        "has_acting_and_music_career": 0.5,
    },
    "michael_jackson": {
        "is_retired": 1.0,
        "has_acting_and_music_career": 0.3,
    },

    # ── Actors ──
    "robert_downey_jr": {
        "peak_era_2010s": 0.9,
        "peak_era_2020s": 0.4,
        "lives_in_north_america": 1.0,
        "known_for_action_films": 0.9,
    },
    "zendaya": {
        "peak_era_2010s": 0.4,
        "peak_era_2020s": 0.9,
        "lives_in_north_america": 1.0,
        "has_acting_and_music_career": 0.4,
    },
    "leonardo_dicaprio": {
        "peak_era_2010s": 0.5,
        "peak_era_2020s": 0.3,
        "lives_in_north_america": 1.0,
        "known_for_action_films": 0.3,
        "known_for_romantic_films": 0.5,
    },
    "tom_hanks": {
        "peak_era_2010s": 0.2,
        "lives_in_north_america": 1.0,
        "is_retired": 0.1,
        "known_for_romantic_films": 0.4,
    },
    "scarlett_johansson": {
        "peak_era_2010s": 0.7,
        "peak_era_2020s": 0.4,
        "lives_in_north_america": 1.0,
        "known_for_action_films": 0.8,
        "known_for_romantic_films": 0.3,
    },
    "dwayne_johnson": {
        "peak_era_2010s": 0.9,
        "peak_era_2020s": 0.6,
        "lives_in_north_america": 1.0,
        "known_for_action_films": 1.0,
    },
    "brad_pitt": {
        "peak_era_2010s": 0.5,
        "peak_era_2020s": 0.3,
        "lives_in_north_america": 1.0,
        "known_for_action_films": 0.8,
        "known_for_romantic_films": 0.3,
    },
    "angelina_jolie": {
        "peak_era_2010s": 0.5,
        "lives_in_north_america": 1.0,
        "known_for_action_films": 1.0,
        "known_for_romantic_films": 0.1,
        "is_activist": 0.6,
    },
    "will_smith": {
        "peak_era_2010s": 0.3,
        "lives_in_north_america": 1.0,
        "known_for_action_films": 0.8,
        "has_acting_and_music_career": 0.8,
    },
    "margot_robbie": {
        "peak_era_2010s": 0.7,
        "peak_era_2020s": 0.8,
        "known_for_action_films": 0.4,
        "known_for_romantic_films": 0.4,
    },
    "chris_hemsworth": {
        "peak_era_2010s": 0.9,
        "peak_era_2020s": 0.5,
        "known_for_action_films": 1.0,
    },
    "jennifer_lawrence": {
        "peak_era_2010s": 0.9,
        "peak_era_2020s": 0.3,
        "lives_in_north_america": 1.0,
        "known_for_action_films": 0.2,
        "known_for_romantic_films": 0.3,
    },
    "ryan_reynolds": {
        "peak_era_2010s": 0.6,
        "peak_era_2020s": 0.7,
        "lives_in_north_america": 1.0,
        "known_for_action_films": 0.7,
        "known_for_romantic_films": 0.4,
    },
    "emma_stone": {
        "peak_era_2010s": 0.7,
        "peak_era_2020s": 0.6,
        "lives_in_north_america": 1.0,
        "known_for_romantic_films": 0.9,
    },
    "denzel_washington": {
        "peak_era_2010s": 0.3,
        "lives_in_north_america": 1.0,
        "known_for_action_films": 0.0,
    },
    "meryl_streep": {
        "lives_in_north_america": 1.0,
        "known_for_romantic_films": 0.5,
    },
    "keanu_reeves": {
        "peak_era_2010s": 0.5,
        "peak_era_2020s": 0.4,
        "lives_in_north_america": 1.0,
        "known_for_action_films": 1.0,
    },
    "natalie_portman": {
        "lives_in_north_america": 1.0,
        "known_for_action_films": 0.3,
        "known_for_romantic_films": 0.4,
    },
    "chris_evans": {
        "peak_era_2010s": 0.9,
        "peak_era_2020s": 0.3,
        "lives_in_north_america": 1.0,
        "known_for_action_films": 0.9,
        "known_for_romantic_films": 0.2,
    },
    "gal_gadot": {
        "peak_era_2010s": 0.8,
        "peak_era_2020s": 0.5,
        "known_for_action_films": 1.0,
    },
    "timothee_chalamet": {
        "peak_era_2010s": 0.3,
        "peak_era_2020s": 1.0,
        "lives_in_north_america": 1.0,
        "known_for_romantic_films": 0.6,
    },
    "florence_pugh": {
        "peak_era_2020s": 1.0,
        "known_for_action_films": 0.4,
    },
    "morgan_freeman": {
        "peak_era_2010s": 0.2,
        "lives_in_north_america": 1.0,
        "is_retired": 0.2,
    },
    "cate_blanchett": {
        "known_for_action_films": 0.3,
    },
    "samuel_l_jackson": {
        "peak_era_2010s": 0.5,
        "lives_in_north_america": 1.0,
        "known_for_action_films": 0.9,
    },
    "viola_davis": {
        "lives_in_north_america": 1.0,
        "known_for_action_films": 0.2,
    },
    "jake_gyllenhaal": {
        "lives_in_north_america": 1.0,
        "known_for_action_films": 0.4,
    },
    "anne_hathaway": {
        "lives_in_north_america": 1.0,
        "known_for_romantic_films": 0.9,
        "has_acting_and_music_career": 0.3,
    },
    "benedict_cumberbatch": {
        "peak_era_2010s": 0.8,
        "peak_era_2020s": 0.6,
        "known_for_action_films": 0.5,
    },
    "pedro_pascal": {
        "peak_era_2010s": 0.5,
        "peak_era_2020s": 1.0,
        "lives_in_north_america": 1.0,
        "known_for_action_films": 0.6,
    },

    # ── Athletes ──
    "lionel_messi": {
        "peak_era_2010s": 0.9,
        "peak_era_2020s": 0.6,
        "lives_in_north_america": 1.0,
        "has_most_titles_in_sport": 0.9,
    },
    "serena_williams": {
        "peak_era_2010s": 0.6,
        "is_retired": 1.0,
        "lives_in_north_america": 1.0,
        "has_most_titles_in_sport": 1.0,
        "is_activist": 0.3,
    },
    "lebron_james": {
        "peak_era_2010s": 0.9,
        "peak_era_2020s": 0.5,
        "lives_in_north_america": 1.0,
        "has_most_titles_in_sport": 0.5,
        "is_activist": 0.3,
    },
    "cristiano_ronaldo": {
        "peak_era_2010s": 0.9,
        "peak_era_2020s": 0.4,
        "has_most_titles_in_sport": 0.8,
    },
    "lewis_hamilton": {
        "peak_era_2010s": 0.8,
        "peak_era_2020s": 0.7,
        "has_most_titles_in_sport": 0.9,
        "is_activist": 0.4,
    },
    "roger_federer": {
        "peak_era_2010s": 0.1,
        "is_retired": 1.0,
        "has_most_titles_in_sport": 0.7,
    },
    "novak_djokovic": {
        "peak_era_2010s": 0.9,
        "peak_era_2020s": 0.8,
        "is_from_eastern_europe": 1.0,
        "has_most_titles_in_sport": 1.0,
    },
    "rafael_nadal": {
        "peak_era_2010s": 0.9,
        "is_retired": 1.0,
        "has_most_titles_in_sport": 0.8,
    },
    "naomi_osaka": {
        "peak_era_2010s": 0.5,
        "peak_era_2020s": 0.5,
        "lives_in_north_america": 1.0,
        "is_activist": 0.5,
    },
    "usain_bolt": {
        "peak_era_2010s": 0.8,
        "is_retired": 1.0,
        "has_most_titles_in_sport": 1.0,
    },
    "simone_biles": {
        "peak_era_2010s": 0.6,
        "peak_era_2020s": 0.7,
        "lives_in_north_america": 1.0,
        "has_most_titles_in_sport": 1.0,
    },
    "neymar": {
        "peak_era_2010s": 0.8,
        "peak_era_2020s": 0.3,
    },
    "kylian_mbappe": {
        "peak_era_2010s": 0.4,
        "peak_era_2020s": 1.0,
    },
    "patrick_mahomes": {
        "is_american_football_player": 1.0,
        "peak_era_2020s": 1.0,
        "lives_in_north_america": 1.0,
        "has_most_titles_in_sport": 0.6,
    },
    "stephen_curry": {
        "peak_era_2010s": 0.9,
        "peak_era_2020s": 0.6,
        "lives_in_north_america": 1.0,
        "has_most_titles_in_sport": 0.5,
    },
    "tom_brady": {
        "is_american_football_player": 1.0,
        "is_retired": 1.0,
        "peak_era_2010s": 0.9,
        "lives_in_north_america": 1.0,
        "has_most_titles_in_sport": 1.0,
    },
    "mike_tyson": {
        "is_retired": 0.8,
        "lives_in_north_america": 1.0,
    },
    "tiger_woods": {
        "is_golfer": 1.0,
        "is_retired": 0.7,
        "lives_in_north_america": 1.0,
        "has_most_titles_in_sport": 0.9,
    },
    "michael_phelps": {
        "is_swimmer": 1.0,
        "is_retired": 1.0,
        "lives_in_north_america": 1.0,
        "has_most_titles_in_sport": 1.0,
    },
    "connor_mcgregor": {
        "peak_era_2010s": 0.8,
    },
    "alex_morgan": {
        "is_retired": 1.0,
        "lives_in_north_america": 1.0,
        "is_activist": 0.2,
    },
    "megan_rapinoe": {
        "is_retired": 1.0,
        "lives_in_north_america": 1.0,
        "is_activist": 1.0,
    },
    "shaquille_oneal": {
        "is_retired": 1.0,
        "lives_in_north_america": 1.0,
    },
    "kobe_bryant": {
        "is_retired": 1.0,
        "has_most_titles_in_sport": 0.6,
    },
    "michael_jordan": {
        "is_retired": 1.0,
        "lives_in_north_america": 1.0,
        "has_most_titles_in_sport": 1.0,
    },
    "wayne_gretzky": {
        "is_retired": 1.0,
        "lives_in_north_america": 1.0,
        "has_most_titles_in_sport": 1.0,
    },
    "muhammad_ali": {
        "is_retired": 1.0,
        "is_activist": 0.9,
        "has_most_titles_in_sport": 0.8,
    },
    "venus_williams": {
        "is_retired": 1.0,
        "lives_in_north_america": 1.0,
        "has_most_titles_in_sport": 0.0,
        "is_activist": 0.3,
    },
    "max_verstappen": {
        "peak_era_2010s": 0.5,
        "peak_era_2020s": 1.0,
        "has_most_titles_in_sport": 0.7,
    },
    "luka_modric": {
        "peak_era_2010s": 0.8,
        "peak_era_2020s": 0.3,
        "is_from_eastern_europe": 1.0,
    },

    # ── Politicians / Leaders ──
    "barack_obama": {
        "lives_in_north_america": 1.0,
        "is_retired": 0.6,
        "is_activist": 0.3,
    },
    "donald_trump": {
        "lives_in_north_america": 1.0,
    },
    "joe_biden": {
        "lives_in_north_america": 1.0,
        "is_retired": 0.5,
    },
    "angela_merkel": {
        "is_retired": 1.0,
        "is_european_leader": 1.0,
    },
    "narendra_modi": {
        "is_asian_leader": 1.0,
    },
    "vladimir_putin": {
        "is_european_leader": 0.5,
        "is_from_eastern_europe": 1.0,
        "is_asian_leader": 0.3,
    },
    "hillary_clinton": {
        "lives_in_north_america": 1.0,
        "is_activist": 0.3,
    },
    "bernie_sanders": {
        "lives_in_north_america": 1.0,
        "is_activist": 0.7,
    },
    "kamala_harris": {
        "lives_in_north_america": 1.0,
        "peak_era_2020s": 0.9,
    },
    "emmanuel_macron": {
        "is_european_leader": 1.0,
        "peak_era_2020s": 0.6,
    },
    "justin_trudeau": {
        "lives_in_north_america": 1.0,
        "is_european_leader": 0.0,
    },
    "boris_johnson": {
        "is_european_leader": 1.0,
        "is_from_eastern_europe": 0.0,
    },
    "xi_jinping": {
        "is_asian_leader": 1.0,
    },
    "jacinda_ardern": {
        "is_retired": 0.8,
        "is_activist": 0.3,
    },
    "queen_elizabeth": {
        "is_retired": 1.0,
        "is_european_leader": 0.8,
    },
    "prince_william": {
        "is_european_leader": 0.2,
        "lives_in_north_america": 0.0,
    },
    "prince_harry": {
        "lives_in_north_america": 1.0,
        "is_activist": 0.3,
    },
    "michelle_obama": {
        "lives_in_north_america": 1.0,
        "is_activist": 0.6,
    },
    "alexandria_ocasio_cortez": {
        "lives_in_north_america": 1.0,
        "peak_era_2020s": 0.8,
        "is_activist": 0.8,
    },
    "nelson_mandela": {
        "is_retired": 1.0,
        "is_activist": 1.0,
    },
    "jfk": {
        "is_retired": 1.0,
        "lives_in_north_america": 1.0,
    },
    "abraham_lincoln": {
        "is_retired": 1.0,
        "lives_in_north_america": 1.0,
    },
    "winston_churchill": {
        "is_retired": 1.0,
        "is_european_leader": 1.0,
    },
    "margaret_thatcher": {
        "is_retired": 1.0,
        "is_european_leader": 1.0,
    },
    "george_w_bush": {
        "is_retired": 1.0,
        "lives_in_north_america": 1.0,
    },
    "bill_clinton": {
        "is_retired": 1.0,
        "lives_in_north_america": 1.0,
    },
    "al_gore": {
        "is_retired": 1.0,
        "lives_in_north_america": 1.0,
        "is_activist": 0.7,
    },
    "ruth_bader_ginsburg": {
        "is_retired": 1.0,
        "lives_in_north_america": 1.0,
        "is_activist": 0.8,
    },
    "volodymyr_zelensky": {
        "is_european_leader": 1.0,
        "is_from_eastern_europe": 1.0,
        "peak_era_2020s": 1.0,
        "has_acting_and_music_career": 0.8,
    },
    "pope_francis": {
        "is_european_leader": 0.2,
        "is_activist": 0.4,
    },

    # ── Internet personalities / Creators ──
    "mrbeast": {
        "peak_era_2010s": 0.6,
        "peak_era_2020s": 1.0,
        "lives_in_north_america": 1.0,
        "is_vlog_creator": 0.4,
    },
    "kim_kardashian": {
        "peak_era_2010s": 0.9,
        "peak_era_2020s": 0.5,
        "lives_in_north_america": 1.0,
        "is_beauty_creator": 0.3,
    },
    "kylie_jenner": {
        "peak_era_2010s": 0.7,
        "peak_era_2020s": 0.6,
        "lives_in_north_america": 1.0,
        "is_beauty_creator": 0.5,
    },
    "pewdiepie": {
        "peak_era_2010s": 0.9,
        "peak_era_2020s": 0.3,
        "is_live_streamer": 0.3,
        "is_vlog_creator": 0.4,
    },
    "charli_damelio": {
        "peak_era_2010s": 0.2,
        "peak_era_2020s": 0.9,
        "lives_in_north_america": 1.0,
    },
    "logan_paul": {
        "peak_era_2010s": 0.7,
        "peak_era_2020s": 0.5,
        "lives_in_north_america": 1.0,
        "is_vlog_creator": 0.7,
        "is_live_streamer": 0.3,
    },
    "markiplier": {
        "peak_era_2010s": 0.8,
        "peak_era_2020s": 0.5,
        "lives_in_north_america": 1.0,
        "is_live_streamer": 0.5,
    },
    "ninja_tyler": {
        "peak_era_2010s": 0.9,
        "peak_era_2020s": 0.3,
        "lives_in_north_america": 1.0,
        "is_live_streamer": 1.0,
    },
    "pokimane": {
        "peak_era_2010s": 0.7,
        "peak_era_2020s": 0.5,
        "lives_in_north_america": 1.0,
        "is_live_streamer": 1.0,
    },
    "dream_minecraft": {
        "peak_era_2010s": 0.5,
        "peak_era_2020s": 0.7,
        "lives_in_north_america": 1.0,
        "is_live_streamer": 0.5,
    },
    "addison_rae": {
        "peak_era_2010s": 0.2,
        "peak_era_2020s": 0.7,
        "lives_in_north_america": 1.0,
        "is_vlog_creator": 0.1,
        "has_acting_and_music_career": 0.3,
    },
    "david_dobrik": {
        "peak_era_2010s": 0.5,
        "peak_era_2020s": 0.9,
        "lives_in_north_america": 1.0,
        "is_vlog_creator": 1.0,
        "is_from_eastern_europe": 0.7,
    },
    "emma_chamberlain": {
        "peak_era_2010s": 0.5,
        "peak_era_2020s": 0.6,
        "lives_in_north_america": 1.0,
        "is_vlog_creator": 1.0,
    },
    "james_charles": {
        "peak_era_2010s": 0.7,
        "peak_era_2020s": 0.3,
        "lives_in_north_america": 1.0,
        "is_beauty_creator": 1.0,
    },
    "jeffree_star": {
        "peak_era_2010s": 0.8,
        "peak_era_2020s": 0.3,
        "lives_in_north_america": 1.0,
        "is_beauty_creator": 1.0,
    },
    "lilly_singh": {
        "peak_era_2010s": 0.8,
        "lives_in_north_america": 1.0,
        "is_vlog_creator": 0.5,
    },
    "casey_neistat": {
        "peak_era_2010s": 0.9,
        "peak_era_2020s": 0.2,
        "lives_in_north_america": 1.0,
        "is_vlog_creator": 1.0,
        "is_tech_reviewer": 0.2,
    },
    "marques_brownlee": {
        "peak_era_2010s": 0.7,
        "peak_era_2020s": 0.7,
        "lives_in_north_america": 1.0,
        "is_tech_reviewer": 1.0,
        "is_vlog_creator": 0.2,
    },
    "sssniperwolf": {
        "peak_era_2010s": 0.7,
        "peak_era_2020s": 0.5,
        "lives_in_north_america": 1.0,
    },
    "ryan_kaji": {
        "peak_era_2010s": 0.5,
        "peak_era_2020s": 0.6,
        "lives_in_north_america": 1.0,
        "is_kids_content_creator": 1.0,
    },
    "dude_perfect": {
        "peak_era_2010s": 0.8,
        "peak_era_2020s": 0.5,
        "lives_in_north_america": 1.0,
    },
    "jake_paul": {
        "peak_era_2010s": 0.7,
        "peak_era_2020s": 0.6,
        "lives_in_north_america": 1.0,
        "is_vlog_creator": 0.5,
    },
    "ksi": {
        "peak_era_2010s": 0.7,
        "peak_era_2020s": 0.6,
        "has_acting_and_music_career": 0.4,
    },
    "ishowspeed": {
        "peak_era_2010s": 0.4,
        "peak_era_2020s": 1.0,
        "lives_in_north_america": 1.0,
        "is_live_streamer": 1.0,
    },
    "kai_cenat": {
        "peak_era_2010s": 0.4,
        "peak_era_2020s": 1.0,
        "lives_in_north_america": 1.0,
        "is_live_streamer": 1.0,
        "is_vlog_creator": 0.8,
        "has_most_titles_in_sport": 0.0,
    },
    "adin_ross": {
        "peak_era_2010s": 0.4,
        "peak_era_2020s": 0.9,
        "lives_in_north_america": 1.0,
        "is_live_streamer": 1.0,
        "is_vlog_creator": 0.0,
    },
    "hasan_piker": {
        "peak_era_2010s": 0.6,
        "peak_era_2020s": 0.7,
        "lives_in_north_america": 1.0,
        "is_live_streamer": 1.0,
        "is_activist": 0.8,
    },
    "ludwig_ahgren": {
        "peak_era_2010s": 0.6,
        "peak_era_2020s": 0.7,
        "lives_in_north_america": 1.0,
        "is_live_streamer": 1.0,
        "is_vlog_creator": 0.4,
    },
    "valkyrae": {
        "peak_era_2010s": 0.7,
        "peak_era_2020s": 0.6,
        "lives_in_north_america": 1.0,
        "is_live_streamer": 1.0,
    },
    "corpse_husband": {
        "peak_era_2010s": 0.4,
        "peak_era_2020s": 0.5,
        "lives_in_north_america": 1.0,
        "is_live_streamer": 0.5,
        "has_acting_and_music_career": 0.3,
    },
}


def load_entities() -> list[dict]:
    entities = []
    with open(ENTITIES_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                entities.append(json.loads(line))
    return entities


def save_entities(entities: list[dict]) -> None:
    with open(ENTITIES_PATH, "w") as f:
        for e in entities:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")


def load_gold() -> list[dict]:
    with open(GOLD_PATH) as f:
        return json.load(f)


def save_gold(gold: list[dict]) -> None:
    with open(GOLD_PATH, "w") as f:
        json.dump(gold, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main() -> None:
    # ── Step 1: Load entities ──
    entities = load_entities()
    print(f"Loaded {len(entities)} entities from {ENTITIES_PATH}")

    # ── Step 2: Add new attributes ──
    attrs_added = 0
    for entity in entities:
        eid = entity["id"]
        overrides = OVERRIDES.get(eid, {})
        for attr in NEW_ATTRS:
            value = overrides.get(attr, 0.0)
            entity["attributes"][attr] = value
            attrs_added += 1

    save_entities(entities)
    print(f"Added {len(NEW_ATTRS)} new attributes to each entity ({attrs_added} total values written)")

    # ── Step 3: Enrich gold cases ──
    gold = load_gold()
    print(f"Loaded {len(gold)} gold cases from {GOLD_PATH}")

    # Build a lookup from entity id -> attributes
    entity_lookup: dict[str, dict[str, float]] = {}
    for entity in entities:
        entity_lookup[entity["id"]] = entity["attributes"]

    answers_added = 0
    for case in gold:
        eid = case["target_entity_id"]
        attrs = entity_lookup.get(eid, {})
        for attr in NEW_ATTRS:
            value = attrs.get(attr, 0.0)
            if value >= 0.75:
                case["answers"][attr] = "yes"
                answers_added += 1
            elif value <= 0.25:
                case["answers"][attr] = "no"
                answers_added += 1
            # Values between 0.25 and 0.75 are ambiguous — skip them

    save_gold(gold)
    print(f"Enriched gold cases with {answers_added} new answers")

    # ── Step 4: Print stats ──
    print("\n── Stats ──")
    print(f"  Entities updated:  {len(entities)}")
    print(f"  New attributes:    {len(NEW_ATTRS)}")
    print(f"  Total attr values: {attrs_added}")
    print(f"  Gold answers added: {answers_added}")

    # Show per-attribute coverage
    print("\n── Per-attribute coverage (entities with value > 0) ──")
    for attr in NEW_ATTRS:
        count_nonzero = sum(1 for e in entities if e["attributes"].get(attr, 0.0) > 0.0)
        count_yes = sum(
            1 for c in gold
            if c["answers"].get(attr) == "yes"
        )
        count_no = sum(
            1 for c in gold
            if c["answers"].get(attr) == "no"
        )
        print(f"  {attr:40s}  nonzero={count_nonzero:3d}  gold_yes={count_yes:3d}  gold_no={count_no:3d}")

    # Verify critical pairs
    print("\n── Critical pair diffs (new attrs only) ──")
    critical_pairs = [
        ("ariana_grande", "taylor_swift", "has_acting_and_music_career"),
        ("jennifer_lawrence", "angelina_jolie", "known_for_action_films"),
        ("emma_stone", "angelina_jolie", "known_for_romantic_films"),
        ("anne_hathaway", "angelina_jolie", "known_for_romantic_films"),
        ("denzel_washington", "brad_pitt", "known_for_action_films"),
        ("venus_williams", "serena_williams", "has_most_titles_in_sport"),
        ("rafael_nadal", "roger_federer", "peak_era_2010s"),
        ("novak_djokovic", "roger_federer", "is_retired"),
        ("megan_rapinoe", "alex_morgan", "is_activist"),
        ("tom_brady", "patrick_mahomes", "is_retired"),
        ("michael_phelps", "tiger_woods", "is_swimmer"),
        ("boris_johnson", "vladimir_putin", "is_from_eastern_europe"),
        ("prince_harry", "prince_william", "lives_in_north_america"),
        ("volodymyr_zelensky", "emmanuel_macron", "is_from_eastern_europe"),
        ("addison_rae", "emma_chamberlain", "is_vlog_creator"),
        ("david_dobrik", "casey_neistat", "peak_era_2020s"),
        ("james_charles", "ryan_kaji", "is_beauty_creator"),
        ("marques_brownlee", "casey_neistat", "is_tech_reviewer"),
        ("adin_ross", "kai_cenat", "is_vlog_creator"),
    ]
    for e1, e2, attr in critical_pairs:
        v1 = entity_lookup[e1].get(attr, 0.0)
        v2 = entity_lookup[e2].get(attr, 0.0)
        diff = abs(v1 - v2)
        status = "OK" if diff >= 0.75 else ("CLOSE" if diff >= 0.5 else "WEAK")
        print(f"  {e1:30s} vs {e2:30s}  {attr:40s}  {v1:.1f} vs {v2:.1f}  diff={diff:.1f}  [{status}]")


if __name__ == "__main__":
    main()
