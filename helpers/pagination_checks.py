from models.responses.common import PaginationMeta


def has_multiple_pages(meta: PaginationMeta) -> bool:
    """True if total pages > 1."""
    return meta.pages > 1


def is_page_within_bounds(meta: PaginationMeta) -> bool:
    """True if current page is within valid range [1, pages]."""
    return 1 <= meta.page <= meta.pages


def items_fit_limit(items: list, meta: PaginationMeta) -> bool:
    """True if items count does not exceed per-page limit."""
    return len(items) <= meta.limit
