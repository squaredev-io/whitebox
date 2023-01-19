from whitebox.crud.base import CRUDBase
from whitebox.schemas.model import Model, ModelCreateDto, ModelUpdateDto
from whitebox.entities.Model import Model as ModelEntity


class CRUD(CRUDBase[Model, ModelCreateDto, ModelUpdateDto]):
    pass


models = CRUD(ModelEntity)
