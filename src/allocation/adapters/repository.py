import abc
from allocation.domain import model


class AbstractRepository(abc.ABC):

    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError



class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, sku):
        return self.session.query(model.Product).filter_by(sku=sku).first()

    def list(self):
        return self.session.query(model.Batch).all()
