from app.entities.fighters import fighters
from app.entities.fans import fans

try:
    from app.entities.promoters import promoters
except ImportError:
    promoters = []

try:
    from app.entities.media import media
except ImportError:
    media = []


world_entities = (
    fighters +
    fans +
    promoters +
    media
)
