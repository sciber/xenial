"""
UI translator
=============
Provides single instance of UITranslator class which translates keys in TRANSLATIONS dictionary into corresponding
value according to the instance's `ui_lang_code` value.
"""

AVAILABLE_LANGUAGES = [('English', 'en'),
                       ('Slovenčina', 'sk')]

TRANSLATIONS = {
    'Prompt': {
        'en': 'Prompt',
        'sk': 'Otázka'
    },
    'Warning': {
        'en': 'Warning',
        'sk': 'Upozornenie'
    },
    'Error': {
        'en': 'Error',
        'sk': 'Chyba'
    },
    'OK': {
        'en': 'OK',
        'sk': 'OK'
    },
    'Load': {
        'en': 'Load',
        'sk': 'Načítať'
    },
    'Switch': {
        'en': 'Switch',
        'sk': 'Prepnúť'
    },
    'Cancel': {
        'en': 'Cancel',
        'sk': 'Zrušiť'
    },
    'Quit': {
        'en': 'Quit',
        'sk': 'Ukončiť'
    },
    'Delete': {
        'en': 'Delete',
        'sk': 'Zmazať'
    },
    'Language': {
        'en': 'Language',
        'sk': 'Jazyk'
    },
    'From': {
        'en': 'From',
        'sk': 'Z'
    },
    'To': {
        'en': 'To',
        'sk': 'Do'
    },
    'Guide': {
        'en': 'Guide',
        'sk': 'Sprievodca'
    },
    'Delete guide': {
        'en': 'Delete guide',
        'sk': 'Zmazať sprievodcu'
    },
    'Guides': {
        'en': 'Guides',
        'sk': 'Sprievodcovia'
    },
    'Import guide': {
        'en': 'Import guide',
        'sk': 'Importovať sprievodcu'
    },
    'Select guide (zip) archive file': {
        'en': 'Select guide (zip) archive file',
        'sk': 'Zvoľ súbor so zip-archivovaným sprievodcom'
    },
    '"[b]{}[/b]"\n guide load failed!': {
        'en': '"[b]{}[/b]"\n guide load failed!',
        'sk': 'Zlyhalo načítanie sprievodcu\n"[b]{}[/b]"!'
    },
    'Tag': {
        'en': 'Tag',
        'sk': 'Nálepka'
    },
    'Tagged categories': {
        'en': 'Tagged categories',
        'sk': 'Onálepkované kategórie'
    },
    'Tagged articles': {
        'en': 'Tagged articles',
        'sk': 'Onálepkované články'
    },
    'Tags': {
        'en': 'Tags',
        'sk': 'Nálepky'
    },
    'Category': {
        'en': 'Category',
        'sk': 'Kategória'
    },
    'Categories': {
        'en': 'Categories',
        'sk': 'Kategórie'
    },
    'Related categories': {
        'en': 'Related categories',
        'sk': 'Súvisiace kategórie'
    },
    'Article': {
        'en': 'Article',
        'sk': 'Článok'
    },
    'Articles': {
        'en': 'Articles',
        'sk': 'Články'
    },
    'Related articles': {
        'en': 'Related articles',
        'sk': 'Súvisiace články'
    },
    'Bookmarks': {
        'en': 'Bookmarks',
        'sk': 'Záložky'
    },
    'Settings': {
        'en': 'Settings',
        'sk': 'Nastavenia'
    },
    'Application language': {
        'en': 'Application language',
        'sk': 'Jazyk aplikácie'
    },
    'Search': {
        'en': 'Search',
        'sk': 'Vyhľadávanie'
    },
    'Search active guide articles': {
        'en': 'Search active guide articles',
        'sk': 'Hľadaj v článkoch aktuálneho sprievodcu'
    },
    'Your search did not match any articles': {
        'en': 'Your search did not match any articles',
        'sk': 'Nenašli sa žiadne články s vyhľadávaným výrazom'
    },
    'Switch to\n"[b]{}[/b]"\n guide to get previous screen?': {
        'en': 'Switch to\n"[b]{}[/b]"\nguide to get previous screen?',
        'sk': 'Prepnúť na sprievodcu \n"[b]{}[/b]"\npre prechod na predchádzajúcu obrazovku?'
    },
    'Do you want to leave the app?': {
        'en': 'Do you want to leave the app?',
        'sk': 'Chceš ukončiť aplikáciur?'
    }
}


class UITranslator:
    """
    Provides functionality for translation of the application's UI to `AVAILABLE LANGUAGES`.
    """

    ui_lang_code = 'en'

    def translate(self, phrase):
        """ Translates `phrase` into language defined by `ui_lang_code` attribute. """

        if phrase not in TRANSLATIONS or self.ui_lang_code not in TRANSLATIONS[phrase]:
            return phrase
        return TRANSLATIONS[phrase][self.ui_lang_code]


transl = UITranslator()
