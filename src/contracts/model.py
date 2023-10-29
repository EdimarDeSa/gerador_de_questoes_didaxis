from abc import ABC, abstractmethod
from pathlib import Path

from src.Hints.hints import QuestionDataHint, SysImgHint, ImageModelHint, UserSetHint, Optional, Iterable, GroupedQuestionDBHint


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
    def read_system_images(self, image_paths: ImageModelHint) -> SysImgHint:
        pass
    # End of system images CRUD methods

    # ------ Questions Data Base Handler ------ #
    @abstractmethod
    def create_question_data_base(self, questions_data: Iterable[Iterable[QuestionDataHint]]) -> None:
        pass

    @abstractmethod
    def read_question_data_base(self, filename: Path) -> GroupedQuestionDBHint:
        pass
    # ------  ------ #

    # User settings CRUD methods
    @abstractmethod
    def create_user_settings(self, configs_dir: Path) -> UserSetHint:
        pass

    @abstractmethod
    def read_user_settings(self, configs_dir: Path) -> UserSetHint:
        pass

    @abstractmethod
    def update_user_settings(self, param: str, value: any, file_path: Path) -> None:
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
