import logging
import os
from typing import Optional, Union

from typing_extensions import Literal

from knot_resolver_manager.compat.dataclasses import dataclass
from knot_resolver_manager.datamodel.errors import DataValidationError
from knot_resolver_manager.utils.dataclasses_parservalidator import DataclassParserValidatorMixin

logger = logging.getLogger(__name__)


def _cpu_count() -> int:
    try:
        return len(os.sched_getaffinity(0))
    except (NotImplementedError, AttributeError):
        logger.warning(
            "The number of usable CPUs could not be determined using 'os.sched_getaffinity()'."
            "Attempting to get the number of system CPUs using 'os.cpu_count()'"
        )
        cpus = os.cpu_count()
        if cpus is None:
            raise DataValidationError(
                "The number of available CPUs to automatically set the number of running"
                "'kresd' workers could not be determined."
                "The number can be specified manually in 'server:instances' configuration option."
            )
        return cpus


@dataclass
class ServerConfig(DataclassParserValidatorMixin):
    hostname: Optional[str] = None
    instances: Union[Literal["auto"], int, None] = None
    _instances: int = 1
    use_cache_gc: bool = True

    def __post_init__(self):
        if isinstance(self.instances, int):
            self._instances = self.instances
        elif self.instances == "auto":
            self._instances = _cpu_count()

    def get_instances(self) -> int:
        return self._instances

    def _validate(self):
        if not 0 < self._instances <= 256:
            raise DataValidationError("number of kresd instances must be in range 1..256")
