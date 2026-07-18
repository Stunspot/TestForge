from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    user_id: str
    tenant_id: str
    roles: frozenset[str]


@dataclass(frozen=True)
class Document:
    owner_id: str
    tenant_id: str


def can_edit(user: User, document: Document) -> bool:
    """Return whether the user may edit the document."""
    return user.user_id == document.owner_id or "editor" in user.roles
