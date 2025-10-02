from sqlalchemy import Column, String, DateTime, Date, Enum, ForeignKey, func, DECIMAL, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from infrastructure.database.session import Base
from domain.projects.value_objects.project_status import ProjectStatus
from domain.projects.value_objects.complexity import Complexity
from domain.quotes.value_objects.quote_status import QuoteStatus


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


class ProjectModel(Base):
    """Modèle SQLAlchemy pour la table projects."""

    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(1000), nullable=False)
    status = Column(Enum(ProjectStatus), nullable=False, default=ProjectStatus.PLANNED, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # Relation one-to-many avec Module
    modules = relationship("ModuleModel", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ProjectModel(id={self.id}, name='{self.name}', status='{self.status}')>"


class ModuleModel(Base):
    """Modèle SQLAlchemy pour la table modules."""

    __tablename__ = "modules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)

    # Relation many-to-one avec Project
    project = relationship("ProjectModel", back_populates="modules")

    # Relation one-to-many avec Feature
    features = relationship("FeatureModel", back_populates="module", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ModuleModel(id={self.id}, name='{self.name}')>"


class FeatureModel(Base):
    """Modèle SQLAlchemy pour la table features."""

    __tablename__ = "features"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    module_id = Column(UUID(as_uuid=True), ForeignKey("modules.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(1000), nullable=False)
    complexity = Column(Enum(Complexity), nullable=False, index=True)
    profile_allocation = Column(JSON, nullable=False)  # Stocke le dict de ratios
    extra_hours = Column(Integer, nullable=False, default=0)

    # Relation many-to-one avec Module
    module = relationship("ModuleModel", back_populates="features")

    def __repr__(self):
        return f"<FeatureModel(id={self.id}, name='{self.name}', complexity='{self.complexity}')>"


class QuoteModel(Base):
    """Modèle SQLAlchemy pour la table quotes."""

    __tablename__ = "quotes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False, index=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    status = Column(Enum(QuoteStatus), nullable=False, default=QuoteStatus.DRAFT, index=True)
    currency = Column(String(3), nullable=False, default="EUR")
    total_ht = Column(DECIMAL(10, 2), nullable=False, default=0)
    total_ttc = Column(DECIMAL(10, 2), nullable=False, default=0)
    tax_rate = Column(DECIMAL(5, 4), nullable=False, default=0.20)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    valid_until = Column(Date, nullable=False)

    # Relation one-to-many avec QuoteItem
    items = relationship("QuoteItemModel", back_populates="quote", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<QuoteModel(id={self.id}, title='{self.title}', status='{self.status}')>"


class QuoteItemModel(Base):
    """Modèle SQLAlchemy pour la table quote_items."""

    __tablename__ = "quote_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quote_id = Column(UUID(as_uuid=True), ForeignKey("quotes.id"), nullable=False, index=True)
    description = Column(String(500), nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(DECIMAL(10, 2), nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="EUR")

    # Relation many-to-one avec Quote
    quote = relationship("QuoteModel", back_populates="items")

    def __repr__(self):
        return f"<QuoteItemModel(id={self.id}, description='{self.description}', total={self.total})>"
