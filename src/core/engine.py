from py2neo import Graph
from .settings import get_settings

settings = get_settings()
graph = Graph(settings.NEO4J_URI, auth=(
    settings.NEO4J_USER, settings.NEO4J_PASS))
