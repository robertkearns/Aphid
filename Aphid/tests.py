from Aphid import *
import unittest
import re


class NestedClass:
    def __init__(self, value1, cls_value):
        self.first = [{1:2, 3:2, value1:cls_value}, {1:{2:'not the key'}},{1:2, 3:2, value1:cls_value}, {1:{2:'not the key'}}]
        

class UnitTests(unittest.TestCase):
    """All regression tests for the Aphid package. Please test before making comits to prevent regression"""
    
    def test_attribute_path(self):
        """Tests the find_attribute_path. Tests normal, regex, iterable searchtypes, and value searchtypes.
         Also checks the max_ attribute."""
        cls1 = NestedClass('key', 4)
        cls3 = NestedClass('not the key', cls1)
        cls4 = NestedClass('not key', cls3)

        to_test = []
        regex = re.compile('^key')
        regex1 = re.compile('4')

        to_test.append(find_attribute_path(cls4, 'key'))
        to_test.append(find_attribute_path(cls4, 4, searchtype='value'))
        to_test.append(find_attribute_path(cls4, regex))
        to_test.append(find_attribute_path(cls4, regex1, searchtype='value'))
        to_test.append(find_attribute_path(cls4, ('mock', 'key')))
        to_test.append(find_attribute_path(cls4, ['mock', 'key']))
        stop_test = find_attribute_path(cls4, 'key', max_=2)
        self.assertEqual(len(stop_test), 2)
        
        last = cls4

        #Ensuring the paths found lineup with the searched for item
        for results in to_test:
            for index in results:
                last = cls4
                for item in results[results.index(index)]:
                
                    if hasattr(last, '__dict__') and not isinstance(last, (list, tuple)):
                        last = last.__dict__[item]
                        
                    else:
                        last = last[item]
                        
                    last_item = item
                    last_value = last
                    
                self.assertEqual(last_item, 'key')
                self.assertEqual(last_value, 4)
            self.assertEqual(len(results), 8)

    def test_findpaths(self):
        """Tests the find_paths function with normal, regex, iterable, and value searchtypes."""
        test_nest = [{1: 2, 3: 4, 'key': 'value'}, {1: {2: 'not the key'}},
                     [{1: 2, 3: 4, 'key': 'value'}, {1: {2: 'not the key'}}]]
        
        to_test = []
        regex = re.compile('^key')
        regex1 = re.compile('value')
        
        to_test.append(find_paths(test_nest, 'key'))
        to_test.append(find_paths(test_nest, 'value', searchtype='value'))
        to_test.append(find_paths(test_nest, regex))
        to_test.append(find_paths(test_nest, regex1, searchtype='value'))
        to_test.append(find_paths(test_nest, ['mock', 'key']))
        to_test.append(find_paths(test_nest, ('mock', 'key')))
        stop_test = find_paths(test_nest, 'key', max_=1)
        self.assertEqual(len(stop_test), 1)

        #Ensuring the paths found lineup with the searched for item
        for results in to_test:
            for index in results:
                last = test_nest
                for item in results[results.index(index)]:
                
                    if hasattr(last, '__dict__') and not isinstance(last, (list, tuple)):
                        last = last.__dict__[item]
                        
                    else:
                        last = last[item]
                        
                    last_item = item
                    last_value = last
                    
                self.assertEqual(last_item, 'key')
                self.assertEqual(last_value, 'value')
            self.assertEqual(len(results), 2)

    def test_findall(self):
        """Tests the findall function with normal, regex, iterable, and value searchtypes."""
        test_nest = [{1: 2, 3: 4, 'key': 'value'}, {1: {2: 'not the key'}},
                     [{1: 2, 3: 4, 'key': 'value'}, {1 :{2: 'not the key'}}]]

        to_test = []
        regex = re.compile('^key')
        regex1 = re.compile('value')

        to_test.append(findall(test_nest, 'key'))
        to_test.append(findall(test_nest, 'value', searchtype='value'))
        to_test.append(findall(test_nest, regex))
        to_test.append(findall(test_nest, regex1, searchtype='value'))
        to_test.append(findall(test_nest, ['mock', 'key']))
        to_test.append(findall(test_nest, ('mock', 'key')))
        stop_test = findall(test_nest, 'key', max_=1)
        self.assertEqual(len(stop_test), 1)

        for results in to_test:
            self.assertEqual(len(results), 2)
            for keyset in results:
                self.assertEqual((keyset[0], keyset[1]), ('key', 'value'))

    def test_search(self):
        """Tests the search function with normal, regex, iterable, and value searchtypes."""
        test_nest = [{1: 2, 3: 4, 'key': 'value'}, {1: {2: 'not the key'}},
                     [{1: 2, 3: 4, 'key': 'value'}, {1: {2: 'not the key'}}]]

        to_test = []
        regex = re.compile('^key')
        regex1 = re.compile('value')

        to_test.append(search(test_nest, 'key'))
        to_test.append(search(test_nest, 'value', searchtype='value'))
        to_test.append(search(test_nest, regex))
        to_test.append(search(test_nest, regex1, searchtype='value'))
        to_test.append(search(test_nest, ['mock', 'key']))
        to_test.append(search(test_nest, ('mock', 'key')))

        for results in to_test:
            self.assertEqual((results[0], results[1]), ('key', 'value'))

    def test_sub(self):
        """Tests the sub function to ensure its reaching all values and subbing them out"""
        test_nest = [{1: 2, 3: 4, 'key': 'value'}, {1: {2: 'not the key'}},
                     [{1: 2, 3: 4, 'key': 'value'}, {1: {2: 'not the key'}}]]

        sub(test_nest, 'key', 'it works')
        self.assertEqual(test_nest[0]['key'], 'it works')
        self.assertEqual(test_nest[2][0]['key'], 'it works')

    def test_max_recursion(self):
        """Tests the max_depth function to ensure the recursion limiter is working properly"""

        deep_nest = {1: {2: {'key': 1}, 3: {4: {'key': 1},5: {6: {'key': 1}}}}}
        results = findall(deep_nest, 'key', max_depth=4)
        self.assertEqual(len(results), 2)
                    
        
            


                
            
                
                
if __name__ == '__main__':
    unittest.main()

    




