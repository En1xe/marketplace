from utils.text import *


class TestUtilsText:
    
    def test_get_text_by_condition(self):
        main_text = 'main text'
        optional_text = 'optional text'
        
        assert get_text_by_condition(
            main_text,
            optional_text,
            value_condition=True
        ) == f'{main_text} {optional_text}'
        
        assert get_text_by_condition(
            main_text,
            optional_text,
            value_condition=False
        ) == f'{main_text}'