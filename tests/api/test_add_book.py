

import pytest



class TestBookAdd:

    def test_add_book(self,add_book):

      
      
        assert ["name", "id", "status"] == list(add_book.json().keys())

