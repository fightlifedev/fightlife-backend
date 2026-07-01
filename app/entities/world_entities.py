from app.entities.fighters import fighters
from app.entities.fans import fans

# Future imports
# from app.entities.rappers import rappers
# from app.entities.actors import actors
# from app.entities.brands import brands
# from app.entities.media import media
# from app.entities.streamers import streamers
# from app.entities.cities import cities
# from app.entities.states import states
# from app.entities.poi import poi
# from app.entities.civilians import civilians
# from app.entities.sponsors import sponsors
# from app.entities.companies import companies


# ============================
# MASTER WORLD ENTITY REGISTRY
# FightLife Universe Core
# ============================

world_entities = {
    "fighters": fighters,
    "fans": fans,

    # Future social/cultural layers
    "rappers": [],
    "actors": [],
    "brands": [],
    "media": [],
    "streamers": [],
    "athletes": [],

    # Geography layers
    "cities": [],
    "states": [],
    "poi": [],

    # Civilian world
    "civilians": [],

    # Business/economy layers
    "sponsors": [],
    "companies": []
}
