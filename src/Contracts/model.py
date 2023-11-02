from abc import ABC, abstractmethod
from pathlib import Path

from src.DataModels.imagemodel import ImageModel
from src.DataModels.usermodel import UserModel
from src.Hints.hints import (
    Any,
    GroupedQuestionDBHint,
    ImageModelHint,
    ListDBHint,
    Optional,
    QuestionDataHint,
)


class ModelContract(ABC):
    # Basic questions CRUD methods
    @abstractmethod
    def create_new_question(self, data: QuestionDataHint) -> int:
        pass

    @abstractmethod
    def read_question(self, control: int) -> QuestionDataHint:
        pass

    @abstractmethod
    def update_question(self, data: QuestionDataHint) -> None:
        pass

    @abstractmethod
    def delete_question(self, control: int) -> None:
        pass

    @abstractmethod
    def flush_questions(self) -> None:
        pass

    # End of questions CRUD methods

    # System images CRUD methods
    @abstractmethod
    def read_system_images(self, image_paths: ImageModelHint) -> ImageModel:
        pass

    # End of system images CRUD methods

    # ------ Questions Data Base Handler ------ #
    @abstractmethod
    def get_questions_to_export_xlsx(self) -> ListDBHint:
        pass

    @abstractmethod
    def read_question_xlsx(self, filename: Path) -> GroupedQuestionDBHint:
        pass

    # ------  ------ #

    # User settings CRUD methods
    @abstractmethod
    def create_user_settings(self, configs_dir: Path) -> None:
        pass

    @abstractmethod
    def read_user_settings(self, configs_dir: Path) -> UserModel:
        pass

    @abstractmethod
    def update_user_settings(self, file_path: Path, **new_config) -> UserModel:
        pass

    # End of user settings CRUD methods

    @abstractmethod
    def create_path(self, configs_dir: str) -> Path:
        pass

    @abstractmethod
    def get_base_filename(self) -> Optional[str]:
        ...

    @abstractmethod
    def get_base_dir(self) -> Path:
        ...

    def get_current_file_path(self) -> Path:
        pass

    def register_file_path(self, file_path: Path) -> None:
        pass

    def save_file(self, file_path: Path, data: Any) -> None:
        pass
