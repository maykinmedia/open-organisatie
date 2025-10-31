from .attr_mapping_config import AttribuutMappingConfigAdmin
from .functie import FunctieAdmin
from .functietype import FunctieTypeAdmin
from .group import GroupAdmin
from .medewerker import MedewerkerAdmin
from .organisatorische_eenheid import OrganisatorischeEenheidAdmin
from .team import TeamAdmin
from .user import UserAdmin
from .vestiging import VestigingAdmin

__all__ = [
    "MedewerkerAdmin",
    "OrganisatorischeEenheidAdmin",
    "VestigingAdmin",
    "TeamAdmin",
    "UserAdmin",
    "GroupAdmin",
    "FunctieAdmin",
    "FunctieTypeAdmin",
    "AttribuutMappingConfigAdmin",
]
