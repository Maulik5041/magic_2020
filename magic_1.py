"""Flatten the arbitrarily nested arrays

**************************************************************
First thought:

  - Looping over the list and checking if it is a list
    YES --> Loop over it again and check the same
              and recursively keep on doing till
              it is no more a list. After that, append
              it to the new list generated

    NO --> Append it in a new list

  ----Decision:

  - Did not continue with the solution as it demanded
    a lot of loops. I considered this as a bit of 
    complicated and non-memory friendly approach

Second thought:

  - Creating a helper function that strips out all
    the outer lists by just returning the elements
    of this nested list

  - The main function will loop over the original list
    and would store each element/list in a stack.

  - Then the helper function would be called to each
    of these elements which would return ONLY the
    elements of the lists

  - These elements would be appended to the new list
  - Thus, the flattened list.

  ----Decision:

  - Did not pursue this approach as well as I felt this
    might cause a lot of overhead and speed might not be
    achieved. But this, in my opinion, felt like a better
    approach than the first solution.


My Approach:

  - Initially I was solving the problem with not expecting
    any other data types. But then I figured that as long as
    I can get access of the elements from the nested lists it
    should not matter

  - I started thinking in terms of using 'yield' operator which
    solves the concern of overhead

  - With the help of this operator, even while choosing the
    recursive approach it will not access a lot of stack memory
    as it would generate only one item at a time

  - Although this does not help completely as recursion in itself
    would use stack memory

  - I did consider iteration approach as well but while solving
    I had to use multiple slicing operations which seemed tedious
    and memory heavy if the list were to expand
*******************************************************************
"""


def flatten_it(nested_arr):
    """Function to flatten the arbitrarily nested arrays:
       :param type : list of arbitrarily nested lists
       :rtype      : list
    """

    # check if the input is valid or empty
    if not nested_arr or not isinstance(nested_arr, list):
        return

    # looping over all the elements --> O(N)
    for inner_arr in nested_arr:

        # check if the given element is list --> O(1)
        if isinstance(inner_arr, list):

            # recursively call the function again --> O(k), k = no of elements
            flat_it_out = flatten_it(inner_arr)
            for an_elem in flat_it_out:

                # ignore if there is a nested empty list
                if an_elem:
                    yield an_elem

        # if it is not a list --> O(1)
        else:
            yield inner_arr


def test_flatten_it():

    assert list(flatten_it([[1, 2, [3]], 4])) == [1, 2, 3, 4]
    assert list(flatten_it(None)) == []
    assert list(flatten_it([])) == []
    assert list(flatten_it([[[[[]]]]])) == []
    assert list(flatten_it([-1, -2, -3, -4])) == [-1, -2, -3, -4]
    assert list(flatten_it([["this", ["should"]], [[["solve"]]], ["this"], "problem"])) == ["this", "should", "solve", "this", "problem"]
    assert list(flatten_it([["Approach"], 3, [[["is"], ["better"]], "than"], "Approach", 2, ["and", [[[1]]]]])) == ["Approach", 3, "is", "better", "than", "Approach", 2, "and", 1]
    assert list(flatten_it([1])) == [1]
    assert list(flatten_it([0, [[]], "apple"])) == [0, "apple"]
    assert list(flatten_it(True)) == []
    print("All test cases passed")


if __name__ == '__main__':
    test_flatten_it()


"""
******************************************************************
The time complexity here would be quadratic in the worst case:

  - The main loop would be O(N)
  - If there is another list inside the list:
      - Again, loop would be O(k), k = no. of elements
  - There could be p amount of nesting and thus the function
    would require to loop that many times

  - Space complexity would be to hold the list of N final elements

  - In my opinion, there is no way around accessing the elements
    by traveling through all the lists. 

    Time = O(N**p)
    Space = O(N)


P.S. We can solve by using regular 'return' as well but I felt the
      need of using yield as it seems memory efficient in theory
********************************************************************
"""