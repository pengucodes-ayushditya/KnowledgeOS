from enum import Enum


# ==========================================================
# Knowledge Graph
# ==========================================================

class AtomType(str, Enum):
    CONCEPT = "concept"
    PERSON = "person"
    EVENT = "event"
    CASE = "case"
    ARTICLE = "article"
    AMENDMENT = "amendment"
    ACT = "act"
    POLICY = "policy"
    SCHEME = "scheme"
    ORGANIZATION = "organization"
    INSTITUTION = "institution"
    COMMITTEE = "committee"
    REPORT = "report"
    LOCATION = "location"


class RelationshipType(str, Enum):
    RELATED_TO = "related_to"
    PREREQUISITE = "prerequisite"
    PART_OF = "part_of"
    REFERENCES = "references"
    CAUSES = "causes"
    CONTRADICTS = "contradicts"
    LEADS_TO = "leads_to"
    IMPLEMENTS = "implements"
    AMENDS = "amends"
    INTERPRETS = "interprets"
    SUPERSEDES = "supersedes"


# ==========================================================
# Academic Domains
# ==========================================================

class Domain(str, Enum):
    POLITY = "polity"
    HISTORY = "history"
    GEOGRAPHY = "geography"
    ECONOMY = "economy"
    ENVIRONMENT = "environment"
    SCIENCE_TECH = "science_tech"
    INTERNATIONAL_RELATIONS = "international_relations"
    ETHICS = "ethics"
    CURRENT_AFFAIRS = "current_affairs"


# ==========================================================
# Ingestion
# ==========================================================

class ResourceType(str, Enum):
    PDF = "pdf"
    YOUTUBE = "youtube"
    WEBSITE = "website"
    NOTES = "notes"
    BOOK = "book"


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"