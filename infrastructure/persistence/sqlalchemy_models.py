from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from infrastructure.database.session import Base


class ClientModel(Base):
    """Modèle SQLAlchemy pour la table clients."""

    __tablename__ = "clients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    contact_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(50), nullable=False)

    # Adresse (dénormalisée)
    address_street = Column(String(255), nullable=False)
    address_city = Column(String(100), nullable=False)
    address_zip_code = Column(String(20), nullable=False)
    address_country = Column(String(100), nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<ClientModel(id={self.id}, name='{self.name}', email='{self.email}')>"
