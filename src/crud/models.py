from src.crud.base import CRUDBase
from src.schemas.model import Model, ModelCreateDto, ModelUpdateDto
from src.entities.Model import Model as ModelEntity


class CRUD(CRUDBase[Model, ModelCreateDto, ModelUpdateDto]):
    pass


models = CRUD(ModelEntity)
