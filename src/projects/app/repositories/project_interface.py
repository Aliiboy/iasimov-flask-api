from abc import ABC, abstractmethod
from uuid import UUID

from projects.domain.entities.project_entity import (
    ProjectEntity,
    ProjectMemberLinkEntity,
)
from users.domain.entities.user_entity import UserEntity


class ProjectRepositoryInterface(ABC):
    """Interface pour les opérations de base de données sur les projets"""

    # write
    @abstractmethod
    def create_project(self, schema: ProjectEntity) -> ProjectEntity:
        """Crée un nouveau projet

        Args:
            schema (ProjectEntity): Schéma du projet à créer

        Returns:
            ProjectEntity: Projet créé
        """
        pass

    @abstractmethod
    def delete_project_by_id(self, project_id: UUID) -> None:
        """Supprime un projet par son identifiant

        Args:
            project_id (UUID): Identifiant du projet à supprimer
        """
        pass

    @abstractmethod
    def update_project(self, schema: ProjectEntity) -> ProjectEntity:
        """Met à jour un projet

        Args:
            schema (ProjectEntity): Schéma du projet à mettre à jour

        Returns:
            ProjectEntity: Projet mis à jour
        """
        pass

    @abstractmethod
    def add_project_member(
        self, project_id: UUID, user_id: UUID
    ) -> ProjectMemberLinkEntity:
        """Ajoute un membre à un projet

        Args:
            project_id (UUID): Identifiant du projet
            user_id (UUID): Identifiant de l'utilisateur à ajouter

        Returns:
            ProjectMemberLinkEntity: Membre du projet ajouté
        """
        pass

    @abstractmethod
    def remove_project_member(self, project_id: UUID, user_id: UUID) -> None:
        """Supprime un membre d'un projet

        Args:
            project_id (UUID): Identifiant du projet
            user_id (UUID): Identifiant de l'utilisateur à supprimer
        """
        pass

    # read
    @abstractmethod
    def get_project_by_id(self, project_id: UUID) -> ProjectEntity:
        """Récupère un projet par son identifiant

        Args:
            project_id (UUID): Identifiant du projet à récupérer

        Returns:
            ProjectEntity: Projet récupéré
        """
        pass

    @abstractmethod
    def get_all_projects_with_limit(self, limit: int) -> list[ProjectEntity]:
        """Récupère tous les projets avec une limite

        Args:
            limit (int): Limite de récupération

        Returns:
            list[ProjectEntity]: Liste des projets récupérés
        """
        pass

    @abstractmethod
    def get_user_projects(self, user_id: UUID) -> list[ProjectEntity]:
        """Récupère tous les projets d'un utilisateur

        Args:
            user_id (UUID): Identifiant de l'utilisateur

        Returns:
            list[ProjectEntity]: Liste des projets de l'utilisateur
        """
        pass

    @abstractmethod
    def get_project_members(self, project_id: UUID) -> list[UserEntity]:
        """Récupère tous les membres d'un projet

        Args:
            project_id (UUID): Identifiant du projet

        Returns:
            list[UserEntity]: Liste des membres du projet
        """
        pass
