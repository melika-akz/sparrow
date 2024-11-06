import abc


class IRepository(abc.ABCMeta):

    @abc.abstractmethod
    def get_list(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, **kwargs):
        raise NotImplementedError

