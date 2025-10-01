from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.session import get_db
from infrastructure.persistence.sqlalchemy_client_repository import SQLAlchemyClientRepository
from domain.clients.use_cases.create_client import CreateClientUseCase
from domain.clients.use_cases.get_client import GetClientUseCase
from domain.clients.use_cases.list_clients import ListClientsUseCase
from domain.clients.use_cases.update_client import UpdateClientUseCase
from domain.clients.use_cases.delete_client import DeleteClientUseCase
from domain.clients.dto.client_dto import CreateClientDTO, UpdateClientDTO, ClientResponseDTO

router = APIRouter(prefix="/api/clients", tags=["clients"])


# Dependency pour obtenir le repository
def get_client_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyClientRepository:
    return SQLAlchemyClientRepository(db)


@router.post(
    "/",
    response_model=ClientResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new client",
    description="Creates a new client with the provided information",
)
async def create_client(
    dto: CreateClientDTO,
    repository: SQLAlchemyClientRepository = Depends(get_client_repository),
):
    """Crée un nouveau client."""
    try:
        use_case = CreateClientUseCase(repository)
        return await use_case.execute(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "/{client_id}",
    response_model=ClientResponseDTO,
    summary="Get a client by ID",
    description="Retrieves a client by their unique identifier",
)
async def get_client(
    client_id: UUID,
    repository: SQLAlchemyClientRepository = Depends(get_client_repository),
):
    """Récupère un client par son ID."""
    try:
        use_case = GetClientUseCase(repository)
        return await use_case.execute(client_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "/",
    response_model=List[ClientResponseDTO],
    summary="List all clients",
    description="Retrieves a paginated list of all clients",
)
async def list_clients(
    skip: int = 0,
    limit: int = 100,
    repository: SQLAlchemyClientRepository = Depends(get_client_repository),
):
    """Liste tous les clients."""
    try:
        use_case = ListClientsUseCase(repository)
        return await use_case.execute(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put(
    "/{client_id}",
    response_model=ClientResponseDTO,
    summary="Update a client",
    description="Updates an existing client with the provided information",
)
async def update_client(
    client_id: UUID,
    dto: UpdateClientDTO,
    repository: SQLAlchemyClientRepository = Depends(get_client_repository),
):
    """Met à jour un client."""
    try:
        use_case = UpdateClientUseCase(repository)
        return await use_case.execute(client_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a client",
    description="Deletes a client by their unique identifier",
)
async def delete_client(
    client_id: UUID,
    repository: SQLAlchemyClientRepository = Depends(get_client_repository),
):
    """Supprime un client."""
    try:
        use_case = DeleteClientUseCase(repository)
        await use_case.execute(client_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
