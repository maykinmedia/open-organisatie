from .attr_mapping_config import AttribuutMappingConfigAdmin
from .functie import FunctieAdmin
from .functietype import FunctieTypeAdmin
from .medewerker import MedewerkerAdmin
from .organisatorische_eenheid import OrganisatorischeEenheidAdmin
from .team import TeamAdmin
from .vestiging import VestigingAdmin

__all__ = [
    "MedewerkerAdmin",
    "OrganisatorischeEenheidAdmin",
    "VestigingAdmin",
    "TeamAdmin",
    "FunctieAdmin",
    "FunctieTypeAdmin",
    "AttribuutMappingConfigAdmin",
]
