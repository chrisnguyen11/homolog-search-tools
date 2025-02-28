from homolog_search_tools.search.search_utils import batch_request

def test_batch_request():
    def example_func(x):
        return [sum(x)]
   
    assert batch_request(example_func, list(range(10)), chunk_size=2) == [1, 5, 9, 13, 17]