from homolog_search_tools.search._search_utils import batch_request

def peudo_request_func(array):
    """
    Given an array of integers, 
    Throw an error if array contains any integers divisible by 9 and
    Return an array of integers not divisible by 9.
    """
    output = []
    for x in array:
        if x % 10 == 0:
            raise Exception()
        output.append(x)
    return output

def test_batch_request():
    output = [x for x in range(100) if x % 10 != 0]
    assert batch_request(peudo_request_func, list(range(100))) == output