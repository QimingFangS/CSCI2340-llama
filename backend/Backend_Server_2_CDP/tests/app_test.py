#############################################################################################################################
# Program: tests/app_test.py                                                                                                #
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program contains unit tests for the code extraction and score calculation.                              #    
#############################################################################################################################

from app.get_code import extract_and_select_best_code_block
from app.utils import calculate_scores
from difflib import SequenceMatcher
from pathlib import Path
import json

def normalize_code(code):
    """
    Normalize code by removing extra whitespace and ensuring consistent formatting.

    params:
        code (str): The code to be normalized.

    returns:
        normalized_code (str): The normalized code.
    """
    return "\n".join(line.strip() for line in code.strip().splitlines() if line.strip())

def is_code_similar(code1, code2, threshold=0.99):
    """
    Check if two pieces of code are similar based on a similarity threshold.

    params:
        code1 (str): The first piece of code.
        code2 (str): The second piece of code.
        threshold (float): The similarity threshold (default is 0.99).

    returns:
        is_similar (bool): True if the codes are similar, False otherwise.
    """
    normalized_code1 = normalize_code(code1)
    normalized_code2 = normalize_code(code2)
    similarity_ratio = SequenceMatcher(None, normalized_code1, normalized_code2).ratio()
    return similarity_ratio >= threshold

def test_extract_and_select_best_code_block():
    """
    Test the extract_and_select_best_code_block function.
    """
    # Test cases
    sample_text1 = "```python\ndef add(a, b):\n    return a + b\n```"
    expected_result1 = "def add(a, b):\n    return a + b"

    sample_text2 = """
    def twosum(nums, target):    
        nums.sort()    
        left, right = 0, len(nums) - 1    
        while left < right:        
            current_sum = nums[left] + nums[right]        
            if current_sum == target:            
                return [left, right]        
            elif current_sum < target:            
                left += 1        
            else:            
                right -= 1    
        return []
    """

    expected_result2 = """
    def twosum(nums, target):
        nums.sort()
        left, right = 0, len(nums) - 1
        while left < right:
            current_sum = nums[left] + nums[right]
            if current_sum == target:
                return [left, right]
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        return []
    """

    sample_text3 = """
    ```python
    def flatten_list_recursive(input_list):
        result = []
        for i in input_list:
            if isinstance(i, list):
                result.extend(flatten_list_recursive(i))
            else:
                result.append(i)
        return result
    ```
    """
    expected_result3 = """
    def flatten_list_recursive(input_list):
    result = []
    for i in input_list:
        if isinstance(i, list):
            result.extend(flatten_list_recursive(i))
        else:
            result.append(i)
    return result
    """

    sample_text4 = """
    def add(a, b):    
        return a + b
    ```python
    def multiply(a, b):    
        return a * b
    ```
    This is some text.
    ```python
    def divide(a, b):    
        if b == 0:       
            raise ValueError(\"Cannot divide by zero\")  
        return a / b
    ```
    """
    expected_result4 = """
    def multiply(a, b):
        return a * b
    """

    sample_text5 = """
    ```python
    def flatten_list(input_list):    
        if not isinstance(input_list, list):        
            return [input_list]    
        if input_list == []:        
            return []    
        return input_list + flatten_list([item for sublist in input_list for item in sublist])\n
    ```
    The provided code attempts to flatten a list that may contain nested lists. However, it does 
    not correctly handle the nesting because it only attempts to flatten the first element. 
    A correct flattening approach would involve recursion or using a library function designed 
    for this purpose, like `itertools.chain.from_iterable`. Here is a revised version using 
    recursion:
    ```python
    def flatten_list_recursive(input_list):    
        result = []    
        for i in input_list:        
            if isinstance(i, list):            
                result.extend(flatten_list_recursive(i))        
            else:            
                result.append(i)    
        return result
    ```
    This recursive solution checks each item in the input list. If the item is an instance of a 
    list, it recursively flattens that sublist and extends the result list with the flattened 
    sublist. If the item is not a list, it appends the item directly to the result list. This 
    method will correctly handle lists of arbitrary nesting."""

    expected_result5 = """
    def flatten_list_recursive(input_list):
    result = []
    for i in input_list:
        if isinstance(i, list):
            result.extend(flatten_list_recursive(i))
        else:
            result.append(i)
    return result
    """

    sample_text6 = """
    def twosum(nums, target):    
        nums.sort()    
        left, right = 0, len(nums) - 1    
        while left < right:        
            current_sum = nums[left] + nums[right]        
            if current_sum == target:            
                return [left, right]        
            elif current_sum < target:            
                left += 1        
            else:            
                right -= 1    
        return [] 
        
    def twosum(nums, target):    
        nums.sort()    
        left, right = 0, len(nums) - 1    
        while left < right:        
            current_sum = nums[left] + nums[right]        
            if current_sum == target:            
                return [left, right]        
            elif current_sum < target:            
                left += 1        
            else:          
                right -= 1    
        return [] 
        
    def twosum(nums, target):    
        nums.sort()    
        left, right = 0, len(nums) - 1   
          result = []    
          while left < right:        
            current_sum = nums[left] + nums[right]        
            if current_sum == target:            
                result = [left, right]            
                break        
            elif current_sum < target:            
                left += 1        
            else:            
                right -= 1    
        return result 
        
    def twosum_efficient(nums, target):    
        num_indices = {num: index for index, num in enumerate(nums)}    
        for num in nums:        
            complement = target - num        
            if complement in num_indices and num_indices[complement] != num_indices[num]:            
                return [num_indices[num], num_indices[complement]]    
        return []
    """
    
    expected_result6 = """
    def twosum(nums, target):
    nums.sort()
    left, right = 0, len(nums) - 1
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []
 def twosum(nums, target):
    nums.sort()
    left, right = 0, len(nums) - 1
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []
 def twosum(nums, target):
    nums.sort()
    left, right = 0, len(nums) - 1
    result = []
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            result = [left, right]
            break
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return result
 def twosum_efficient(nums, target):
    num_indices = {num: index for index, num in enumerate(nums)}
    for num in nums:
        complement = target - num
        if complement in num_indices and num_indices[complement] != num_indices[num]:
            return [num_indices[num], num_indices[complement]]
    return []
    """

    sample_text7 = """
    The updated code is below:
    ```java
    import java.util.*;

    public class Main {
        public static void main(String[] args) {
            ArrayList<String> list = new ArrayList<>(Arrays.asList("A", "B", "C"));
            Hashtable<Integer, String> hashtable = new Hashtable<>();
            for (int i = 0; i < list.size(); i++) {
                hashtable.put(i, list.get(i));
            }
            System.out.println(hashtable);
        }
    }
    ```
    """

    expected_result7 = """
    import java.util.*;

    public class Main {
        public static void main(String[] args) {
            ArrayList<String> list = new ArrayList<>(Arrays.asList("A", "B", "C"));
            Hashtable<Integer, String> hashtable = new Hashtable<>();
            for (int i = 0; i < list.size(); i++) {
                hashtable.put(i, list.get(i));
            }
            System.out.println(hashtable);
        }
    }
    """

    sample_text8 = """
    The revised implementation is shown below:
    Template class T is used to create a LinkedList.

    class Node {
    public:
        T data;
        Node* next;
        Node(T value) : data(value), next(nullptr) {}
    };

    class LinkedList {
    public:
        Node* head;
        LinkedList() : head(nullptr) {}

        void add(T value) {
            if (!head) {
                head = new Node(value);
            } else {
                Node* temp = head;
                while (temp->next) {
                    temp = temp->next;
                }
                temp->next = new Node(value);
            }
        }
    };
    """
    expected_result8 = """
    class Node {
    public:
        T data;
        Node* next;
        Node(T value) : data(value), next(nullptr) {}
    };

    class LinkedList {
    public:
        Node* head;
        LinkedList() : head(nullptr) {}

        void add(T value) {
            if (!head) {
                head = new Node(value);
            } else {
                Node* temp = head;
                while (temp->next) {
                    temp = temp->next;
                }
                temp->next = new Node(value);
            }
        }
    };
    """
    
    code_1_passed = is_code_similar(extract_and_select_best_code_block(sample_text1), expected_result1)
    code_2_passed = is_code_similar(extract_and_select_best_code_block(sample_text2), expected_result2)
    code_3_passed = is_code_similar(extract_and_select_best_code_block(sample_text3), expected_result3)
    code_4_passed = is_code_similar(extract_and_select_best_code_block(sample_text4), expected_result4)
    code_5_passed = is_code_similar(extract_and_select_best_code_block(sample_text5), expected_result5)
    code_6_passed = is_code_similar(extract_and_select_best_code_block(sample_text6), expected_result6)
    code_7_passed = is_code_similar(extract_and_select_best_code_block(sample_text7), expected_result7)
    code_8_passed = is_code_similar(extract_and_select_best_code_block(sample_text8), expected_result8)
    if code_1_passed and code_2_passed and code_3_passed and code_4_passed and code_5_passed and code_6_passed and code_7_passed and code_8_passed:
        print("Code extraction and valadation tests passed!")

def utility_tests():
    """
    Utility tests.
    """
    data = Path(__file__).parent.parent / 'Results' / 'combined_results.json'
    with open(data, 'r') as f:
        data = json.load(f)
    scores = calculate_scores(data=data, mode="mode_2")
    assert 0 <= scores["final_score"] <= 10
    print("Utility tests passed!")


# Run the tests
if __name__ == "__main__":
    test_extract_and_select_best_code_block()
    utility_tests()