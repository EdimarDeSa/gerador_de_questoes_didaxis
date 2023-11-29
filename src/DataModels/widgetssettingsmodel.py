from dataclasses import dataclass, field

from ..Hints import MenuSettingsHint


@dataclass(frozen=True, kw_only=True)
class WidgetsSettingsModel:
    label_settings: MenuSettingsHint = field(default_factory=dict)
    entry_settings: MenuSettingsHint = field(default_factory=dict)
    list_settings: MenuSettingsHint = field(default_factory=dict)
    button_title_settings: MenuSettingsHint = field(default_factory=dict)
    button_default_settings: MenuSettingsHint = field(default_factory=dict)
    text_settings: MenuSettingsHint = field(default_factory=dict)
    scrollable_label_settings: MenuSettingsHint = field(default_factory=dict)
