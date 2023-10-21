from customtkinter import CTkFrame, CTk, CTkLabel, CTkOptionMenu, CTkEntry

from ..Hints import (
    LabelConfigs, ListConfigs, CategoryVar, CategoryList, EntryConfigs, SubcategoryVar, TimeVar,
    TypeList, TypeVar, TypeChangeHandler, DifficultiesList, DifficultVar, WeightVar
)


class JanelaParametrosDaQuestao(CTkFrame):
    def __init__(
            self, master: CTk, entry_configs: EntryConfigs, label_configs: LabelConfigs, list_configs: ListConfigs,
            category_var: CategoryVar, category_list: CategoryList, subcategory_var: SubcategoryVar, time_var: TimeVar,
            type_list: TypeList, type_var: TypeVar, type_change_handler: TypeChangeHandler,
            difficulties_list: DifficultiesList, difficult_var: DifficultVar, weight_var: WeightVar,
            **kwargs
    ):
        super().__init__(master, **kwargs)
        for i in range(3): self.grid_columnconfigure(i, weight=1)

        list_configs = list_configs.copy()
        list_configs.update({'width': 180})

        CTkLabel(self, **label_configs, text='Unidade').grid(column=0, row=0)
        CTkOptionMenu(self, values=category_list, variable=category_var, **list_configs).grid(column=0, row=1)

        CTkLabel(self, text='Código do curso', **label_configs).grid(column=1, row=0)
        CTkEntry(self, textvariable=subcategory_var, **entry_configs).grid(column=1, row=1)

        CTkLabel(self, text='Tempo de resposta', **label_configs).grid(column=2, row=0)
        CTkEntry(self, textvariable=time_var, **entry_configs).grid(column=2, row=1)

        CTkLabel(self, text='Tipo da questão', **label_configs).grid(column=0, row=2, pady=(10, 0))
        CTkOptionMenu(
            self, values=type_list, variable=type_var, command=type_change_handler, **list_configs
        ).grid(column=0, row=3)

        CTkLabel(self, text='Dificuldade', **label_configs).grid(column=1, row=2, pady=(10, 0))
        CTkOptionMenu(self, values=difficulties_list, variable=difficult_var, **list_configs).grid(column=1, row=3)

        CTkLabel(self, text='Peso da questão', **label_configs).grid(column=2, row=2, pady=(10, 0))
        CTkEntry(self, textvariable=weight_var, **entry_configs).grid(column=2, row=3)
