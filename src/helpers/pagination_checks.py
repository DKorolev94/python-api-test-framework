from src.models.responses.common import PaginationMeta


def items_fit_limit(items: list, meta: PaginationMeta) -> bool:
    """Возвращает true, если количество элементов не превышает лимит на странице."""
    return len(items) <= meta.limit
