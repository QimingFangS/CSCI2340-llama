#############################################################################################################################
# Program: app/bug_types.py                                                                                                 #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/28/2024                                                                                                          #
# Version: 1.0.2                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program defines the dictionary of bug types.                                                            #                                                                                                 
#############################################################################################################################
bug_data = {
    "Functional Bugs": {
        "Detailed Explanation": "Functional bugs occur when a feature or functionality of the system does not perform according to the requirements or expected behavior. These bugs can occur in both user-facing features and backend processes.",
        "Examples and Fixes": {
            "Example 1": {
                "Name": "Incorrect Login Validation",
                "Buggy Code": """
                # Buggy Code
                def login(username, password):
                    if username == "admin" and password == "admin123":
                        return "Login Successful"
                    return "Login Failed"

                print(login("Admin", "admin123"))  # Expected: "Login Successful""
                """,
                "Issue": "Case sensitivity in username comparison.",
                "Solution": "Normalize the input for comparison using `.lower()`.",
                "Solution Code": """
                # Fixed Code
                def login(username, password):
                    if username.lower() == "admin" and password == "admin123":
                        return "Login Successful"
                    return "Login Failed"

                print(login("Admin", "admin123"))  # Expected: "Login Successful"
                """
            },
            "Example 2": {
                "Name": "Incorrect Cart Total Calculation",
                "Buggy Code": """
                # Buggy Code
                def calculate_total(prices):
                    total = 0
                    for price in prices:
                        total += price
                    return total + 10  # Adding a fixed shipping fee, ignoring discounts
                """,
                "Issue": "Ignoring discounts and shipping conditions.",
                "Solution": "Include discount logic and conditional shipping fee.",
                "Solution Code": """
                # Fixed Code
                def calculate_total(prices, discount=0, shipping_fee=10):
                    total = sum(prices) * (1 - discount)
                    if total > 50:
                        shipping_fee = 0
                    return total + shipping_fee
                """
            },

            "Example 3": 
            {
                "Name": "Incorrect Sorting",
                "Buggy Code": """
                # Buggy Code
                def sort_numbers(numbers):
                    return sorted(numbers, reverse=True)  # Always sorts in descending order
                """,
                "Issue": "Sorting in descending order by default.",
                "Solution": "Allow dynamic sorting order.",
                "Solution Code": """
                # Fixed Code
                def sort_numbers(numbers, ascending=True):
                    return sorted(numbers, reverse=not ascending)
                """
            },

            "Example 4": {
                "Name": "Incorrect Email Validation",
                "Buggy Code": """
                # Buggy Code
                def validate_email(email):
                    return "@" in email
                """,
                "Issue": "Simplistic validation allowing invalid formats.",
                "Solution": "Use regex for more comprehensive validation.",
                "Solution Code": """
                # Fixed Code
                import re
                def validate_email(email):
                    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                    return re.match(pattern, email) is not None
                """
            },

            "Example 5": {
                "Name": "Incorrect Date Formatting",
                "Buggy Code": """
                # Buggy Code
                def format_date(date):
                    return f"{date.year}/{date.month}/{date.day}"
                """,
                "Issue": "No support for different formats.",
                "Solution": "Add format parameter.",
                "Solution Code": """
                # Fixed Code
                def format_date(date, format="YYYY-MM-DD"):
                    if format == "YYYY-MM-DD":
                        return f"{date.year}-{date.month:02d}-{date.day:02d}"
                    elif format == "DD/MM/YYYY":
                        return f"{date.day:02d}/{date.month:02d}/{date.year}"
                """
            }
        },
        "General Approach to Solving Functional Bugs": [
            "Understand the requirements: Thoroughly review the feature requirements or specifications. Clarify any ambiguities with stakeholders or product managers.",
            "Reproduce the issue: Attempt to recreate the bug by following the steps leading to it. Document all observed behaviors and log files for debugging.",
            "Debugging: Use debugging tools to identify the root cause. Isolate problematic modules and functions.",
            "Fix and refactor: Apply minimal, targeted fixes to ensure stability. Refactor code for clarity and future-proofing where necessary.",
            "Testing: Conduct unit tests for individual components. Perform integration and regression testing to ensure no other functionalities are broken.",
            "Code reviews: Have peers review the fixes for potential edge cases or missed scenarios."
        ]
    },

    "Usability Bugs": {
        "Detailed Explanation": "Usability bugs impact the user experience, making the software difficult or frustrating to use. They usually arise from poor design choices, inconsistent UI elements, or lack of accessibility.",
        "Examples and Fixes": {
            "Example 1": {
                "Name": "Confusing Navigation Menu",
                "Buggy Code": """
                # Buggy Code
                <nav>
                  <a href="/home">Home</a> | <a href="/contact">Contact</a> | <a>Help</a>
                </nav>
                """,
                "Issue": "Missing \"Help\" link URL.",
                "Solution": "Add a valid link and use clearer labels.",
                "Solution Code": """
                # Fixed Code
                <nav>
                  <a href="/home">Home</a> | <a href="/contact">Contact Us</a> | <a href="/help">Help Center</a>
                </nav>
                """
            },

            "Example 2": {
                "Name": "Poor Error Messages",
                "Buggy Code": """
                # Buggy Code
                def login(username, password):
                    if not username or not password:
                        return "Error occurred"
                """,
                "Issue": "Vague error message.",
                "Solution": "Provide specific feedback.",
                "Solution Code": """
                # Fixed Code
                def login(username, password):
                    if not username:
                        return "Username cannot be empty"
                    if not password:
                        return "Password cannot be empty"
                """
            },

            "Example 3": {
                "Name": "Non-Responsive UI Elements",
                "Buggy Code": """
                /* Buggy Code */
                button {
                  width: 200px;
                }
                """,
                "Issue": "Button width is fixed.",
                "Solution": "Use flexible units.",
                "Solution Code": """
                /* Fixed Code */
                button {
                  width: 100%;
                  max-width: 200px;
                }
                """
            },

            "Example 4": {
                "Name": "Missing Keyboard Accessibility",
                "Buggy Code": """
                <!-- Buggy Code -->
                <button onclick="submitForm()">Submit</button>
                """,
                "Issue": "No keyboard support.",
                "Solution": "Add tabindex and event listeners.",
                "Solution Code": """
                <!-- Fixed Code -->
                <button onclick="submitForm()" tabindex="0">Submit</button>
                """
            },

            "Example 5": {
                "Name": "Inconsistent Date Format",
                "Buggy Code": """
                # Buggy Code
                print(f"Date: {day}/{month}/{year}")
                """,
                "Issue": "No consistent formatting.",
                "Solution": "Standardize the format.",
                "Solution Code": """
                # Fixed Code
                print(f"Date: {day:02d}/{month:02d}/{year}")
                """
            },
        },
        "General Approach to Solving Functional Bugs": [
            "Conduct Usability Testing: Perform real-world user testing. Collect feedback on UI/UX pain points.",
            "Adopt UX Guidelines: Follow established design principles (e.g., Material Design).",
            "Perform Accessibility Audits: Check for keyboard navigation, screen reader support, and contrast ratios.",
            "Standardize UI Elements: Ensure consistent labels, formats, and navigation patterns."
        ]
    },
    
    "Security Bugs": {
        "Detailed Explanation": (
            "Security bugs refer to vulnerabilities in the software that can be exploited by attackers to compromise data integrity, confidentiality, or availability. "
            "These issues can include improper input validation, insufficient authentication, or insecure data handling."
        ),
        "Examples and Fixes": {
            "Example 1": {
                "Name": "SQL Injection Vulnerability",
                "Buggy Code": """
                # Buggy Code
                def get_user_info(username):
                    query = f"SELECT * FROM users WHERE username = '{username}'"
                    database.execute(query)
                """,
                "Issue": "Directly using user input in SQL queries allows SQL injection attacks.",
                "Solution": "Use parameterized queries to prevent SQL injection.",
                "Solution Code": """
                # Fixed Code
                def get_user_info(username):
                    query = "SELECT * FROM users WHERE username = %s"
                    database.execute(query, (username,))
                """
            },
            "Example 2": {
                "Name": "Hardcoded Passwords",
                "Buggy Code": """
                # Buggy Code
                def connect_to_db():
                    password = "admin123"  # Hardcoded password
                    return db.connect(password=password)
                """,
                "Issue": "Hardcoded passwords can be easily exposed and compromise security.",
                "Solution": "Use environment variables or secure secret management.",
                "Solution Code": """
                # Fixed Code
                import os
                def connect_to_db():
                    password = os.getenv("DB_PASSWORD")
                    return db.connect(password=password)
                """
            },
            "Example 3": {
                "Name": "Cross-Site Scripting (XSS)",
                "Buggy Code": """
                # Buggy Code
                def render_user_profile(name):
                    return f"<h1>Welcome, {name}</h1>"
                """,
                "Issue": "Directly rendering user input without sanitization makes it vulnerable to XSS attacks.",
                "Solution": "Sanitize input before rendering.",
                "Solution Code": """
                # Fixed Code
                import html
                def render_user_profile(name):
                    safe_name = html.escape(name)
                    return f"<h1>Welcome, {safe_name}</h1>"
                """
            },
            "Example 4": {
                "Name": "Weak Password Policy",
                "Buggy Code": """
                # Buggy Code
                def validate_password(password):
                    return len(password) >= 6
                """,
                "Issue": "Weak password policy with insufficient complexity checks.",
                "Solution": "Implement a stronger password policy.",
                "Solution Code": """
                # Fixed Code
                import re
                def validate_password(password):
                    return len(password) >= 8 and re.search(r'[A-Z]', password) and re.search(r'[0-9]', password)
                """
            },
            "Example 5": {
                "Name": "Insecure File Uploads",
                "Buggy Code": """
                # Buggy Code
                def upload_file(file):
                    file.save(f"/uploads/{file.filename}")
                """,
                "Issue": "No validation on file type or path allows dangerous file uploads.",
                "Solution": "Validate file types and use secure paths.",
                "Solution Code": """
                # Fixed Code
                import os
                def upload_file(file):
                    allowed_extensions = {'.jpg', '.png', '.pdf'}
                    ext = os.path.splitext(file.filename)[1]
                    if ext in allowed_extensions:
                        file.save(f"/secure_uploads/{file.filename}")
                """
            }
        },
        "General Approach to Solving Security Bugs": [
            "Input validation: Always validate and sanitize user inputs to prevent injection attacks.",
            "Authentication and authorization: Implement robust authentication mechanisms and verify user permissions.",
            "Data encryption: Encrypt sensitive data both in transit and at rest.",
            "Regular security audits: Conduct security reviews and penetration testing regularly.",
            "Update dependencies: Keep third-party libraries and frameworks up to date to avoid known vulnerabilities."
        ]
    },

    "Syntax Errors": {
        "Detailed Explanation": (
            "Syntax errors occur when the code violates the language's grammatical rules, leading to a failure in compilation or execution. "
            "These errors are often caused by missing punctuation, incorrect indentation, or incorrect usage of keywords."
        ),
        "Examples and Fixes": {
            "Example 1": {
                "Name": "Missing Colon in Function Definition",
                "Buggy Code": """
                # Buggy Code
                def greet(name)
                    print(f"Hello, {name}")
                """,
                "Issue": "Missing colon after the function definition.",
                "Solution": "Add the colon at the end of the function definition.",
                "Solution Code": """
                # Fixed Code
                def greet(name):
                    print(f"Hello, {name}")
                """
            },
            "Example 2": {
                "Name": "Mismatched Parentheses",
                "Buggy Code": """
                # Buggy Code
                print("Hello, World!"
                """,
                "Issue": "Missing closing parenthesis in the print statement.",
                "Solution": "Ensure parentheses are balanced.",
                "Solution Code": """
                # Fixed Code
                print("Hello, World!")
                """
            },
            "Example 3": {
                "Name": "Incorrect Indentation",
                "Buggy Code": """
                # Buggy Code
                def calculate():
                x = 10
                  y = 20
                return x + y
                """,
                "Issue": "Inconsistent indentation causes a syntax error.",
                "Solution": "Correct the indentation.",
                "Solution Code": """
                # Fixed Code
                def calculate():
                    x = 10
                    y = 20
                    return x + y
                """
            },
            "Example 4": {
                "Name": "Invalid Variable Name",
                "Buggy Code": """
                # Buggy Code
                1st_place = "Gold"
                """,
                "Issue": "Variable names cannot start with a digit.",
                "Solution": "Rename the variable to start with a letter or underscore.",
                "Solution Code": """
                # Fixed Code
                first_place = "Gold"
                """
            },
            "Example 5": {
                "Name": "Unexpected Indent",
                "Buggy Code": """
                # Buggy Code
                    print("Too much indentation")
                """,
                "Issue": "Unexpected indentation causes a syntax error.",
                "Solution": "Remove the extra indentation.",
                "Solution Code": """
                # Fixed Code
                print("Too much indentation")
                """
            }
        },
        "General Approach to Solving Syntax Errors": [
            "Use linters: Employ linters like Pylint or Flake8 to catch syntax errors early.",
            "Code formatting: Use auto-formatting tools like Black to maintain consistent code style.",
            "Error messages: Pay attention to syntax error messages to pinpoint issues.",
            "Code reviews: Conduct regular code reviews to catch syntax errors.",
            "IDE support: Use IDEs with built-in syntax checking and auto-completion features."
        ]
    },

    "Compatibility Bugs": {
        "Detailed Explanation": (
            "Compatibility bugs occur when software does not function correctly across different environments, platforms, browsers, operating systems, or devices. "
            "These bugs can lead to inconsistent user experiences or complete failure in certain configurations."
        ),
        "Examples and Fixes": {
            "Example 1": {
                "Name": "Inconsistent Button Layout on Different Browsers",
                "Buggy Code": """
                <!-- Buggy HTML Code -->
                <style>
                    button {
                        width: 100px;
                        margin: 5px auto;
                    }
                </style>
                <button>Click Me</button>
                """,
                "Issue": "The `margin` property behaves differently across browsers.",
                "Solution": "Use a more consistent layout technique such as flexbox.",
                "Solution Code": """
                <!-- Fixed HTML Code -->
                <style>
                    button {
                        width: 100px;
                        display: flex;
                        justify-content: center;
                        margin: 5px;
                    }
                </style>
                <button>Click Me</button>
                """
            },
            "Example 2": {
                "Name": "API Incompatibility with Different Python Versions",
                "Buggy Code": """
                # Buggy Code
                print(f"Hello, {name}", end='')
                """,
                "Issue": "The `end` parameter is unsupported in older Python 2.x versions.",
                "Solution": "Use a backward-compatible print statement.",
                "Solution Code": """
                # Fixed Code
                import sys
                sys.stdout.write("Hello, {}".format(name))
                """
            },
            "Example 3": {
                "Name": "Unsupported CSS Property",
                "Buggy Code": """
                /* Buggy CSS */
                div {
                    grid-gap: 10px;
                }
                """,
                "Issue": "`grid-gap` property is not supported in older browsers.",
                "Solution": "Provide a fallback using other layout techniques.",
                "Solution Code": """
                /* Fixed CSS */
                div {
                    margin: 10px; /* Fallback */
                }
                @supports (display: grid) {
                    div {
                        display: grid;
                        grid-gap: 10px;
                    }
                }
                """
            },
            "Example 4": {
                "Name": "File Path Incompatibility Across OS",
                "Buggy Code": """
                # Buggy Code
                file_path = "C:\\Users\\Documents\\file.txt"
                """,
                "Issue": "File paths with hardcoded backslashes cause issues on non-Windows systems.",
                "Solution": "Use `os.path.join` for cross-platform compatibility.",
                "Solution Code": """
                # Fixed Code
                import os
                file_path = os.path.join("Users", "Documents", "file.txt")
                """
            },
            "Example 5": {
                "Name": "Date Formatting Issue Across Locales",
                "Buggy Code": """
                # Buggy Code
                print(date.strftime("%x"))  # Locale-dependent formatting
                """,
                "Issue": "Date formatting varies based on the system locale.",
                "Solution": "Use ISO 8601 format for consistency.",
                "Solution Code": """
                # Fixed Code
                print(date.strftime("%Y-%m-%d"))  # Locale-independent
                """
            }
        },
        "General Approach to Solving Compatibility Bugs": [
            "Test across environments: Run tests on multiple platforms, browsers, and devices.",
            "Use polyfills: Implement polyfills for unsupported features.",
            "Check documentation: Verify platform-specific requirements and compatibility notes.",
            "Fallback strategies: Provide fallback mechanisms for unsupported features.",
            "Automation: Use cross-browser testing tools to automate compatibility testing."
        ]
    },

    "Logical Bugs": {
        "Detailed Explanation": (
            "Logical bugs occur when the code executes without syntax errors but produces incorrect or unexpected results due to flaws in the program's logic. "
            "These bugs often stem from incorrect conditionals, loops, or flawed algorithm implementations."
        ),
        "Examples and Fixes": {
            "Example 1": {
                "Name": "Incorrect Loop Condition",
                "Buggy Code": """
                # Buggy Code
                def sum_until_n(n):
                    total = 0
                    i = 1
                    while i < n:
                        total += i
                        i += 1
                    return total
                """,
                "Issue": "The loop does not include `n` in the sum.",
                "Solution": "Change the loop condition to include `n`.",
                "Solution Code": """
                # Fixed Code
                def sum_until_n(n):
                    total = 0
                    i = 1
                    while i <= n:
                        total += i
                        i += 1
                    return total
                """
            },
            "Example 2": {
                "Name": "Incorrect Discount Calculation",
                "Buggy Code": """
                # Buggy Code
                def apply_discount(price, discount):
                    return price - price * discount
                """,
                "Issue": "Misinterpretation of discount percentage calculation.",
                "Solution": "Ensure correct percentage handling.",
                "Solution Code": """
                # Fixed Code
                def apply_discount(price, discount):
                    return price * (1 - discount / 100)
                """
            },
            "Example 3": {
                "Name": "Incorrect Condition Logic",
                "Buggy Code": """
                # Buggy Code
                def is_eligible_for_voting(age):
                    if age > 18:
                        return True
                    else:
                        return False
                """,
                "Issue": "Excludes 18-year-olds from voting.",
                "Solution": "Use `>=` to include 18.",
                "Solution Code": """
                # Fixed Code
                def is_eligible_for_voting(age):
                    return age >= 18
                """
            },
            "Example 4": {
                "Name": "Misplaced Return Statement in Loop",
                "Buggy Code": """
                # Buggy Code
                def find_first_even(numbers):
                    for num in numbers:
                        if num % 2 == 0:
                            return num
                        else:
                            return None
                """,
                "Issue": "Premature return inside the loop.",
                "Solution": "Move return outside the loop.",
                "Solution Code": """
                # Fixed Code
                def find_first_even(numbers):
                    for num in numbers:
                        if num % 2 == 0:
                            return num
                    return None
                """
            },
            "Example 5": {
                "Name": "Infinite Loop Due to Missing Increment",
                "Buggy Code": """
                # Buggy Code
                def print_numbers(n):
                    i = 0
                    while i < n:
                        print(i)
                """,
                "Issue": "The loop never ends due to missing increment.",
                "Solution": "Add an increment statement.",
                "Solution Code": """
                # Fixed Code
                def print_numbers(n):
                    i = 0
                    while i < n:
                        print(i)
                        i += 1
                """
            }
        },
        "General Approach to Solving Logical Bugs": [
            "Trace code execution: Use print statements or a debugger to trace logic flow.",
            "Review conditions: Double-check logical conditions in loops and if-statements.",
            "Algorithm validation: Ensure the chosen algorithm meets problem requirements.",
            "Test edge cases: Test boundary conditions and unusual inputs.",
            "Code reviews: Involve peers to catch logical inconsistencies."
        ]
    },

    "Performance Bugs": {
        "Detailed Explanation": (
            "Performance bugs occur when an application is slower or consumes more resources than expected. "
            "These bugs are often due to inefficient algorithms, excessive memory usage, or improper resource handling."
        ),
        "Examples and Fixes": {
            "Example 1": {
                "Name": "Inefficient Sorting Algorithm",
                "Buggy Code": """
                # Buggy Code
                def sort_numbers(nums):
                    return sorted(sorted(nums))
                """,
                "Issue": "Sorting the list twice unnecessarily.",
                "Solution": "Sort the list only once.",
                "Solution Code": """
                # Fixed Code
                def sort_numbers(nums):
                    return sorted(nums)
                """
            },
            "Example 2": {
                "Name": "Memory Leak in List Appending",
                "Buggy Code": """
                # Buggy Code
                def append_items():
                    items = []
                    for _ in range(1000000):
                        items += [1]
                """,
                "Issue": "Using `+=` creates new lists repeatedly, increasing memory usage.",
                "Solution": "Use `.append()` for efficient list addition.",
                "Solution Code": """
                # Fixed Code
                def append_items():
                    items = []
                    for _ in range(1000000):
                        items.append(1)
                """
            },
            "Example 3": {
                "Name": "Excessive API Calls in Loop",
                "Buggy Code": """
                # Buggy Code
                for item in items:
                    api_call(item)
                """,
                "Issue": "Too many API calls can slow down the system.",
                "Solution": "Batch API calls or use caching.",
                "Solution Code": """
                # Fixed Code
                def batch_api_calls(items):
                    batched_results = []
                    for i in range(0, len(items), 100):
                        batched_results.append(api_call(items[i:i+100]))
                    return batched_results
                """
            },
            "Example 4": {
                "Name": "Excessive Database Queries",
                "Buggy Code": """
                # Buggy Code
                for user in users:
                    user_data = get_user_from_db(user)
                """,
                "Issue": "Multiple queries slow down performance.",
                "Solution": "Use bulk queries or batch processing.",
                "Solution Code": """
                # Fixed Code
                def fetch_all_users(users):
                    return bulk_fetch_from_db(users)
                """
            },
            "Example 5": {
                "Name": "Inefficient Recursive Function",
                "Buggy Code": """
                # Buggy Code
                def fibonacci(n):
                    if n <= 1:
                        return n
                    else:
                        return fibonacci(n - 1) + fibonacci(n - 2)
                """,
                "Issue": "Exponential time complexity due to repeated calculations.",
                "Solution": "Use memoization to store intermediate results.",
                "Solution Code": """
                # Fixed Code
                def fibonacci(n, memo={}):
                    if n in memo:
                        return memo[n]
                    if n <= 1:
                        return n
                    memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
                    return memo[n]
                """
            }
        },
        "General Approach to Solving Performance Bugs": [
            "Optimize algorithms: Use efficient algorithms with lower time complexity.",
            "Minimize resource usage: Identify and eliminate unnecessary resource consumption.",
            "Profile and benchmark: Use performance profiling tools to identify bottlenecks.",
            "Use caching: Store results of expensive computations or queries.",
            "Reduce I/O operations: Minimize file, database, and network I/O."
        ]
    },

    "Unit-Level Bugs": {
        "Detailed Explanation": (
            "Unit-level bugs occur at the smallest testable part of a program, typically in individual functions or methods. "
            "They are usually found during unit testing and can be caused by incorrect logic, data handling, or boundary conditions."
        ),
        "Examples and Fixes": {
            "Example 1": {
                "Name": "Incorrect Function Output",
                "Buggy Code": """
                # Buggy Code
                def add_numbers(a, b):
                    return a - b
                """,
                "Issue": "The function subtracts instead of adding.",
                "Solution": "Use the correct operator.",
                "Solution Code": """
                # Fixed Code
                def add_numbers(a, b):
                    return a + b
                """
            },
            "Example 2": {
                "Name": "Off-by-One Error",
                "Buggy Code": """
                # Buggy Code
                def get_elements(lst):
                    return lst[:len(lst)]
                """,
                "Issue": "This returns the same list but could miss edge cases.",
                "Solution": "Clarify the intent of slicing or use full slicing.",
                "Solution Code": """
                # Fixed Code
                def get_elements(lst):
                    return lst[:]
                """
            },
            "Example 3": {
                "Name": "Incorrect Default Parameter Handling",
                "Buggy Code": """
                # Buggy Code
                def append_item(item, lst=[]):
                    lst.append(item)
                    return lst
                """,
                "Issue": "Using a mutable default argument can lead to unexpected results.",
                "Solution": "Use `None` as the default and initialize inside.",
                "Solution Code": """
                # Fixed Code
                def append_item(item, lst=None):
                    if lst is None:
                        lst = []
                    lst.append(item)
                    return lst
                """
            },
            "Example 4": {
                "Name": "Incorrect Loop Index",
                "Buggy Code": """
                # Buggy Code
                def sum_elements(lst):
                    total = 0
                    for i in range(len(lst)):
                        total += lst[i + 1]
                    return total
                """,
                "Issue": "The loop index goes out of bounds.",
                "Solution": "Fix the index range.",
                "Solution Code": """
                # Fixed Code
                def sum_elements(lst):
                    total = 0
                    for i in range(len(lst)):
                        total += lst[i]
                    return total
                """
            },
            "Example 5": {
                "Name": "Mismatched Data Types",
                "Buggy Code": """
                # Buggy Code
                def concatenate_strings(a, b):
                    return a + b
                """,
                "Issue": "Fails when `a` or `b` is not a string.",
                "Solution": "Convert inputs to strings before concatenating.",
                "Solution Code": """
                # Fixed Code
                def concatenate_strings(a, b):
                    return str(a) + str(b)
                """
            }
        },
        "General Approach to Solving Unit-Level Bugs": [
            "Test individual units: Ensure each function behaves as expected with isolated tests.",
            "Validate inputs: Add input validation to prevent unexpected behavior.",
            "Handle edge cases: Consider boundary conditions and unusual inputs.",
            "Debug outputs: Use assertions and print statements for debugging.",
            "Refactor small units: Keep functions small and focused for easier testing."
        ]
    },

    "Integration Bugs": {
        "Detailed Explanation": (
            "Integration bugs occur when different modules or components of a system fail to work together as expected. "
            "These bugs often emerge from incompatibilities, incorrect assumptions about interfaces, or poor communication between modules."
        ),
        "Examples and Fixes": {
            "Example 1": {
                "Name": "Incorrect Data Mapping Between Modules",
                "Buggy Code": """
                # Buggy Code - Module A sends data
                def send_data():
                    return {"id": 123, "name": "John Doe"}

                # Module B expects different keys
                def process_data(data):
                    return f"User: {data['user_id']} - {data['user_name']}"
                
                data = send_data()
                print(process_data(data))
                """,
                "Issue": "Module B expects different keys ('user_id' and 'user_name') than what Module A provides ('id' and 'name').",
                "Solution": "Ensure consistent key naming across modules.",
                "Solution Code": """
                # Fixed Code
                def send_data():
                    return {"user_id": 123, "user_name": "John Doe"}

                def process_data(data):
                    return f"User: {data['user_id']} - {data['user_name']}"
                
                data = send_data()
                print(process_data(data))
                """
            },
            "Example 2": {
                "Name": "API Endpoint Mismatch",
                "Buggy Code": """
                # Buggy Code
                def get_user():
                    url = "https://api.example.com/user-details"
                    response = requests.get(url)
                    return response.json()
                """,
                "Issue": "Incorrect API endpoint causing a 404 error.",
                "Solution": "Use the correct endpoint as per API documentation.",
                "Solution Code": """
                # Fixed Code
                def get_user():
                    url = "https://api.example.com/users"
                    response = requests.get(url)
                    return response.json()
                """
            },
            "Example 3": {
                "Name": "Inconsistent Data Types Between Modules",
                "Buggy Code": """
                # Buggy Code
                def send_data():
                    return {"id": "123"}  # ID as string

                def process_data(data):
                    return data["id"] + 10  # ID expected as integer
                """,
                "Issue": "Data type mismatch leads to a TypeError.",
                "Solution": "Ensure consistent data types across modules.",
                "Solution Code": """
                # Fixed Code
                def send_data():
                    return {"id": 123}

                def process_data(data):
                    return data["id"] + 10
                """
            }
        },
        "General Approach to Solving Integration Bugs": [
            "Define clear interface contracts: Ensure consistent data structures and interfaces between modules.",
            "Use integration tests: Test interactions between multiple components or systems.",
            "Validate data: Check data types and formats during module communication.",
            "Monitor logs: Review system logs to trace integration issues.",
            "Version control: Maintain compatibility when updating APIs or interfaces."
        ]
    },

    "Out-of-Bound Bugs": {
        "Detailed Explanation": (
            "Out-of-bound bugs occur when an index or pointer exceeds the valid range of an array, list, or buffer. "
            "These bugs can lead to crashes, unexpected behavior, or security vulnerabilities like buffer overflows."
        ),
        "Examples and Fixes": {
            "Example 1": {
                "Name": "Array Index Out of Bound",
                "Buggy Code": """
                # Buggy Code
                def get_element(lst, index):
                    return lst[index]
                
                lst = [1, 2, 3]
                print(get_element(lst, 5))  # Index out of range
                """,
                "Issue": "Accessing an index outside the array's length causes an IndexError.",
                "Solution": "Check index bounds before accessing the array.",
                "Solution Code": """
                # Fixed Code
                def get_element(lst, index):
                    if 0 <= index < len(lst):
                        return lst[index]
                    return "Index out of range"
                
                lst = [1, 2, 3]
                print(get_element(lst, 5))
                """
            },
            "Example 2": {
                "Name": "Buffer Overflow",
                "Buggy Code": """
                # Buggy Code
                buffer = [0] * 10
                for i in range(15):
                    buffer[i] = i
                """,
                "Issue": "Loop exceeds the buffer size, causing potential memory corruption.",
                "Solution": "Restrict loop to valid buffer size.",
                "Solution Code": """
                # Fixed Code
                buffer = [0] * 10
                for i in range(min(15, len(buffer))):
                    buffer[i] = i
                """
            },
            "Example 3": {
                "Name": "String Index Out of Bound",
                "Buggy Code": """
                # Buggy Code
                def get_char(string, index):
                    return string[index]
                
                print(get_char("hello", 10))
                """,
                "Issue": "Accessing a character at an invalid index raises an IndexError.",
                "Solution": "Check index before accessing the string.",
                "Solution Code": """
                # Fixed Code
                def get_char(string, index):
                    if 0 <= index < len(string):
                        return string[index]
                    return "Index out of range"
                
                print(get_char("hello", 10))
                """
            }
        },
        "General Approach to Solving Out-of-Bound Bugs": [
            "Validate indices: Ensure indices are within valid ranges before accessing data.",
            "Use bounds checking: Implement boundary checks in loops and array accesses.",
            "Test edge cases: Include scenarios with the smallest and largest indices in tests.",
            "Avoid hard-coded values: Use dynamic length checks instead of fixed values.",
            "Use safe data structures: Leverage built-in safety mechanisms in higher-level languages."
        ]
    },

    "Functional Errors": {
        "Detailed Explanation": (
            "Functional errors occur when a system feature or functionality fails to operate according to the specified requirements or user expectations. "
            "These errors can be caused by incorrect logic, misinterpretation of requirements, or improper user inputs."
        ),
        "Examples and Fixes": {
            "Example 1": {
                "Name": "Incorrect User Authentication Logic",
                "Buggy Code": """
                # Buggy Code
                def authenticate_user(username, password):
                    if username == "admin" or password == "admin123":
                        return "Access Granted"
                    return "Access Denied"
                """,
                "Issue": "Logical error allows access if either the username or password is correct.",
                "Solution": "Require both username and password to be correct.",
                "Solution Code": """
                # Fixed Code
                def authenticate_user(username, password):
                    if username == "admin" and password == "admin123":
                        return "Access Granted"
                    return "Access Denied"
                """
            },
            "Example 2": {
                "Name": "Incorrect Cart Total Calculation",
                "Buggy Code": """
                # Buggy Code
                def calculate_total(prices):
                    total = sum(prices)
                    return total - 5 if total < 50 else total
                """,
                "Issue": "Incorrect discount application logic.",
                "Solution": "Apply discount only if conditions are met.",
                "Solution Code": """
                # Fixed Code
                def calculate_total(prices):
                    total = sum(prices)
                    if total < 50:
                        total -= 5
                    return total
                """
            },
            "Example 3": {
                "Name": "Incorrect User Role Assignment",
                "Buggy Code": """
                # Buggy Code
                def assign_role(user_type):
                    roles = {"admin": "Admin", "guest": "User"}
                    return roles[user_type]
                """,
                "Issue": "KeyError if an unsupported user type is passed.",
                "Solution": "Provide a default role for unsupported user types.",
                "Solution Code": """
                # Fixed Code
                def assign_role(user_type):
                    roles = {"admin": "Admin", "guest": "User"}
                    return roles.get(user_type, "Guest")
                """
            }
        },
        "General Approach to Solving Functional Errors": [
            "Understand feature requirements: Clarify specifications with stakeholders.",
            "Reproduce the error: Follow steps leading to the error and analyze system behavior.",
            "Debug using logs: Trace the error's origin using logs and breakpoints.",
            "Fix and refactor: Implement targeted corrections and improve code readability.",
            "Test thoroughly: Conduct unit and integration tests to verify fixes.",
            "Review code: Have peers review the code for additional validation."
        ]
    },

    "Security Errors": {
        "Detailed Explanation": (
            "Security errors occur when a system's functionality allows unauthorized access, data leakage, or compromises the system's integrity. "
            "These errors often stem from improper validation, poor encryption practices, or lack of access control."
        ),
        "Examples and Fixes": {
            "Example 1": {
                "Name": "SQL Injection Vulnerability",
                "Buggy Code": """
                # Buggy Code
                def get_user_data(username):
                    query = f"SELECT * FROM users WHERE username = '{username}'"
                    cursor.execute(query)
                """,
                "Issue": "Directly including user input in SQL queries allows injection.",
                "Solution": "Use parameterized queries to prevent SQL injection.",
                "Solution Code": """
                # Fixed Code
                def get_user_data(username):
                    query = "SELECT * FROM users WHERE username = %s"
                    cursor.execute(query, (username,))
                """
            },
            "Example 2": {
                "Name": "Insecure Password Storage",
                "Buggy Code": """
                # Buggy Code
                def store_password(password):
                    database.save(password)  # Storing plain text password
                """,
                "Issue": "Storing passwords in plain text is insecure.",
                "Solution": "Hash passwords using a secure hashing algorithm.",
                "Solution Code": """
                # Fixed Code
                import bcrypt

                def store_password(password):
                    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                    database.save(hashed)
                """
            },
            "Example 3": {
                "Name": "Cross-Site Scripting (XSS)",
                "Buggy Code": """
                # Buggy Code
                def render_page(input_data):
                    return f"<div>{input_data}</div>"
                """,
                "Issue": "Allows malicious scripts to be injected into web pages.",
                "Solution": "Escape user input to prevent script execution.",
                "Solution Code": """
                # Fixed Code
                import html

                def render_page(input_data):
                    safe_input = html.escape(input_data)
                    return f"<div>{safe_input}</div>"
                """
            }
        },
        "General Approach to Solving Security Errors": [
            "Input validation: Sanitize and validate all user inputs.",
            "Use secure practices: Implement secure hashing, encryption, and secure coding guidelines.",
            "Access control: Enforce role-based access and least privilege.",
            "Testing: Perform security testing such as penetration testing.",
            "Monitoring: Implement logging and monitoring for security incidents.",
            "Review policies: Regularly review and update security policies."
        ]
    },

    "Calculation Errors": {
        "Detailed Explanation": (
            "Calculation errors occur when a program produces incorrect numerical results due to issues in arithmetic operations, data type handling, rounding, or incorrect formula implementation. "
            "These errors can severely affect financial, scientific, and statistical applications."
        ),
        "Examples and Fixes": {
            "Example 1": {
                "Name": "Incorrect Rounding Logic",
                "Buggy Code": """
                # Buggy Code
                def calculate_discount(price):
                    return round(price * 0.10, 1)  # Rounding to one decimal place
                """,
                "Issue": "Rounding may lead to incorrect financial values.",
                "Solution": "Use appropriate precision handling or format the output.",
                "Solution Code": """
                # Fixed Code
                def calculate_discount(price):
                    return format(price * 0.10, '.2f')  # Ensures two decimal places
                """
            },
            "Example 2": {
                "Name": "Integer Division Error",
                "Buggy Code": """
                # Buggy Code
                def calculate_average(total, count):
                    return total // count  # Integer division
                """,
                "Issue": "Integer division discards the fractional part.",
                "Solution": "Use floating-point division.",
                "Solution Code": """
                # Fixed Code
                def calculate_average(total, count):
                    return total / count
                """
            },
            "Example 3": {
                "Name": "Overflow Error in Loop",
                "Buggy Code": """
                # Buggy Code
                def factorial(n):
                    result = 1
                    for i in range(1, n + 1):
                        result *= i
                    return result
                print(factorial(10000))  # May cause overflow
                """,
                "Issue": "Large numbers can cause overflow or slow computation.",
                "Solution": "Use specialized libraries for large number handling.",
                "Solution Code": """
                # Fixed Code
                import math
                def factorial(n):
                    return math.factorial(n)
                print(factorial(10000))
                """
            },
            "Example 4": {
                "Name": "Floating-Point Precision Error",
                "Buggy Code": """
                # Buggy Code
                def add_numbers(a, b):
                    return a + b
                print(add_numbers(0.1, 0.2))  # Expected 0.3
                """,
                "Issue": "Floating-point arithmetic leads to precision loss.",
                "Solution": "Use a decimal library for precise arithmetic.",
                "Solution Code": """
                # Fixed Code
                from decimal import Decimal

                def add_numbers(a, b):
                    return Decimal(a) + Decimal(b)
                print(add_numbers(0.1, 0.2))
                """
            },
            "Example 5": {
                "Name": "Wrong Formula Implementation",
                "Buggy Code": """
                # Buggy Code
                def calculate_area(length, width):
                    return length * length * width  # Incorrect multiplication
                """,
                "Issue": "Incorrect formula for area calculation.",
                "Solution": "Use the correct multiplication formula.",
                "Solution Code": """
                # Fixed Code
                def calculate_area(length, width):
                    return length * width
                """
            }
        },
        "General Approach to Solving Calculation Errors": [
            "Understand the expected formula and logic.",
            "Use proper data types (e.g., float vs integer).",
            "Handle rounding and precision carefully.",
            "Test with different inputs to detect inconsistencies.",
            "Use specialized libraries for large or precise calculations.",
            "Conduct peer reviews to verify formulas and calculations."
        ]
    },

    "Communication Errors": {
        "Detailed Explanation": (
            "Communication errors arise when two systems, components, or services fail to exchange data properly. "
            "These errors can be caused by protocol mismatches, incorrect data formats, network failures, or incorrect API usage."
        ),
        "Examples and Fixes": {
            "Example 1": {
                "Name": "API Request Failure",
                "Buggy Code": """
                # Buggy Code
                import requests

                response = requests.get("https://api.example.com/data")
                print(response.json())
                """,
                "Issue": "Fails if the API returns a non-JSON response or an error.",
                "Solution": "Check response status and handle exceptions.",
                "Solution Code": """
                # Fixed Code
                import requests

                response = requests.get("https://api.example.com/data")
                if response.status_code == 200:
                    try:
                        print(response.json())
                    except ValueError:
                        print("Invalid JSON response")
                else:
                    print(f"Error: {response.status_code}")
                """
            },
            "Example 2": {
                "Name": "Socket Timeout Error",
                "Buggy Code": """
                # Buggy Code
                import socket

                s = socket.socket()
                s.connect(("example.com", 80))
                """,
                "Issue": "No timeout set, leading to potential indefinite hang.",
                "Solution": "Set a timeout for the socket connection.",
                "Solution Code": """
                # Fixed Code
                import socket

                s = socket.socket()
                s.settimeout(10)  # 10-second timeout
                s.connect(("example.com", 80))
                """
            },
            "Example 3": {
                "Name": "Data Format Mismatch",
                "Buggy Code": """
                # Buggy Code
                def send_data(data):
                    return str(data)  # Sends data as a string
                """,
                "Issue": "The receiver expects JSON format.",
                "Solution": "Use proper serialization (e.g., JSON).",
                "Solution Code": """
                # Fixed Code
                import json

                def send_data(data):
                    return json.dumps(data)
                """
            },
            "Example 4": {
                "Name": "Protocol Mismatch",
                "Buggy Code": """
                # Buggy Code
                def communicate():
                    return "Message in plain text"
                """,
                "Issue": "Plain text communication in a system requiring secure protocols.",
                "Solution": "Use an encrypted protocol.",
                "Solution Code": """
                # Fixed Code
                import ssl

                def communicate():
                    return ssl.wrap_socket("Encrypted Message")
                """
            },
            "Example 5": {
                "Name": "Incorrect API Endpoint",
                "Buggy Code": """
                # Buggy Code
                response = requests.get("https://api.example.com/wrong-endpoint")
                """,
                "Issue": "API endpoint does not exist.",
                "Solution": "Ensure the correct endpoint is used.",
                "Solution Code": """
                # Fixed Code
                response = requests.get("https://api.example.com/correct-endpoint")
                """
            }
        },
        "General Approach to Solving Communication Errors": [
            "Verify the data format and protocols being used.",
            "Handle network and API exceptions gracefully.",
            "Set timeouts to prevent indefinite hangs.",
            "Ensure endpoints and URLs are correct and reachable.",
            "Test communication in different scenarios and environments.",
            "Log errors for better diagnosis."
        ]
    },

    "Logic Errors": {
        "Detailed Explanation": (
            "Logic errors occur when the program runs without crashing, but it does not produce the correct results due to flaws in the logic of the algorithm or program flow. "
            "These types of errors can be difficult to detect since the code executes without throwing an error, but the output is incorrect or inconsistent."
        ),
        "Examples and Fixes": {
            "Example 1": {
                "Name": "Incorrect Conditional Check",
                "Buggy Code": """
                # Buggy Code
                def is_even(number):
                    if number % 2 == 1:  # Incorrect condition for even check
                        return True
                    return False
                """,
                "Issue": "Incorrect logic for checking even numbers.",
                "Solution": "Fix the condition to check for even numbers correctly.",
                "Solution Code": """
                # Fixed Code
                def is_even(number):
                    if number % 2 == 0:  # Correct condition for even check
                        return True
                    return False
                """
            },
            "Example 2": {
                "Name": "Off-by-One Error in Loop",
                "Buggy Code": """
                # Buggy Code
                def count_elements(arr):
                    count = 0
                    for i in range(len(arr)):  # Incorrect loop range
                        count += 1
                    return count
                """,
                "Issue": "Off-by-one error causes the count to be inaccurate.",
                "Solution": "Adjust loop range or index appropriately.",
                "Solution Code": """
                # Fixed Code
                def count_elements(arr):
                    return len(arr)  # Use built-in length function for accuracy
                """
            },
            "Example 3": {
                "Name": "Incorrect Loop Termination Condition",
                "Buggy Code": """
                # Buggy Code
                def find_max(arr):
                    max_val = arr[0]
                    for i in range(len(arr)):  # Loop runs one extra time, causing index out of range
                        if arr[i] > max_val:
                            max_val = arr[i]
                    return max_val
                """,
                "Issue": "Incorrect loop condition causes an out-of-range error or wrong result.",
                "Solution": "Ensure the loop stops at the correct index.",
                "Solution Code": """
                # Fixed Code
                def find_max(arr):
                    max_val = arr[0]
                    for i in range(1, len(arr)):  # Loop should start from index 1
                        if arr[i] > max_val:
                            max_val = arr[i]
                    return max_val
                """
            },
            "Example 4": {
                "Name": "Incorrect Data Assignment",
                "Buggy Code": """
                # Buggy Code
                def assign_grades(scores):
                    grades = []
                    for score in scores:
                        if score >= 90:
                            grades.append("A")
                        elif score >= 80:
                            grades.append("B")
                        else:
                            grades.append("C")
                    return grades
                """,
                "Issue": "Incorrect grades are assigned because the condition for grade A and B overlap.",
                "Solution": "Fix the grading logic so that ranges don't overlap.",
                "Solution Code": """
                # Fixed Code
                def assign_grades(scores):
                    grades = []
                    for score in scores:
                        if score >= 90:
                            grades.append("A")
                        elif score >= 80:
                            grades.append("B")
                        elif score >= 70:
                            grades.append("C")
                        else:
                            grades.append("D")
                    return grades
                """
            },
            "Example 5": {
                "Name": "Incorrect Function Return",
                "Buggy Code": """
                # Buggy Code
                def calculate_discount(price, discount):
                    if discount == 0:
                        return "No discount applied"
                    return price * discount
                """,
                "Issue": "Logic error in handling the discount of zero.",
                "Solution": "Return the original price when there is no discount.",
                "Solution Code": """
                # Fixed Code
                def calculate_discount(price, discount):
                    if discount == 0:
                        return price  # Return the price unchanged
                    return price * discount
                """
            }
        },
        "General Approach to Solving Logic Errors": [
            "Understand the problem and the expected output.",
            "Carefully analyze the conditions in loops and if statements.",
            "Test edge cases to identify any boundary issues or unexpected behavior.",
            "Consider using print statements or logging to trace variable values during execution.",
            "Refactor complex logic into smaller functions to simplify debugging.",
            "Perform thorough testing, particularly with cases that challenge the boundaries of logic."
        ]
    },

    "Workflow Bugs": {
        "Detailed Explanation": (
            "Workflow bugs occur when the sequence of operations or events in the system does not follow the intended or expected order. "
            "These bugs can be caused by incorrect event handling, improper state transitions, or sequence errors in complex workflows."
        ),
        "Examples and Fixes": {
            "Example 1": {
                "Name": "Incorrect Task Flow",
                "Buggy Code": """
                # Buggy Code
                def process_order(order):
                    if order['payment_status'] == 'Paid':
                        ship_order(order)  # Should not ship if order is not confirmed
                    else:
                        print("Payment not confirmed")
                """,
                "Issue": "The order should be confirmed before shipping, but confirmation is skipped.",
                "Solution": "Ensure order confirmation is checked before shipping.",
                "Solution Code": """
                # Fixed Code
                def process_order(order):
                    if order['payment_status'] == 'Paid' and order['confirmation_status'] == 'Confirmed':
                        ship_order(order)
                    else:
                        print("Payment or confirmation not complete")
                """
            },
            "Example 2": {
                "Name": "Incorrect Event Handling",
                "Buggy Code": """
                # Buggy Code
                def handle_event(event):
                    if event == 'start':
                        start_game()
                    elif event == 'end':
                        end_game()
                    else:
                        print("Unknown event")
                """,
                "Issue": "The workflow logic doesn't allow for intermediate events (e.g., pause).",
                "Solution": "Handle all relevant events in the workflow, including intermediate states.",
                "Solution Code": """
                # Fixed Code
                def handle_event(event):
                    if event == 'start':
                        start_game()
                    elif event == 'pause':
                        pause_game()
                    elif event == 'end':
                        end_game()
                    else:
                        print("Unknown event")
                """
            },
            "Example 3": {
                "Name": "Improper Sequence of Steps",
                "Buggy Code": """
                # Buggy Code
                def deploy_application(version):
                    install_dependencies()
                    run_tests()  # Should run tests before installing dependencies
                    deploy(version)
                """,
                "Issue": "Running tests after dependencies are installed is a wrong sequence.",
                "Solution": "Ensure the correct sequence of operations.",
                "Solution Code": """
                # Fixed Code
                def deploy_application(version):
                    install_dependencies()
                    run_tests()  # Tests should run before deployment
                    deploy(version)
                """
            },
            "Example 4": {
                "Name": "State Transition Error",
                "Buggy Code": """
                # Buggy Code
                def login_user(user):
                    if user['status'] == 'Active':
                        print("Logged in")
                    elif user['status'] == 'Suspended':
                        print("Suspended")
                    else:
                        print("Error: Unknown status")  # Missing status transition
                """,
                "Issue": "Missing handling for transitioning a user from inactive to active status.",
                "Solution": "Handle status transitions explicitly before performing actions.",
                "Solution Code": """
                # Fixed Code
                def login_user(user):
                    if user['status'] == 'Inactive':
                        user['status'] = 'Active'
                    if user['status'] == 'Active':
                        print("Logged in")
                    elif user['status'] == 'Suspended':
                        print("Suspended")
                    else:
                        print("Error: Unknown status")
                """
            },
            "Example 5": {
                "Name": "Inconsistent Workflow in User Registration",
                "Buggy Code": """
                # Buggy Code
                def register_user(user):
                    if user['email_verified']:
                        activate_account(user)
                    if user['payment_verified']:  # Both conditions should be checked together
                        grant_membership(user)
                """,
                "Issue": "Both conditions should be evaluated together to proceed to the next steps.",
                "Solution": "Evaluate both conditions together in one step.",
                "Solution Code": """
                # Fixed Code
                def register_user(user):
                    if user['email_verified'] and user['payment_verified']:
                        activate_account(user)
                        grant_membership(user)
                    else:
                        print("Missing verification")
                """
            }
        },
        "General Approach to Solving Workflow Bugs": [
            "Map out the expected workflow and verify the steps involved.",
            "Ensure that each event is handled in the correct order and the transitions are valid.",
            "Check for missed edge cases, such as intermediate or unhandled states.",
            "Use state machines or flow diagrams to visualize the process.",
            "Test workflows under different conditions to ensure robustness.",
            "Perform code reviews to catch missing or incorrect event handling."
        ]
    },

    "Bohrbugs": {
        "Detailed Explanation": (
            "Bohrbugs are a type of software bug that exhibits consistent, repeatable behavior under specific conditions, similar to the predictable "
            "nature of Bohr's atomic model. These bugs typically manifest in a controlled environment and can be reliably reproduced, often "
            "resulting from specific configurations, inputs, or timing conditions."
        ),
        "Examples and Fixes": {
            "Example 1": {
                "Name": "Race Condition",
                "Buggy Code": """
                # Buggy Code
                import threading
                counter = 0
                
                def increment():
                    global counter
                    counter += 1
                
                def decrement():
                    global counter
                    counter -= 1
                
                threads = []
                for _ in range(1000):
                    t1 = threading.Thread(target=increment)
                    t2 = threading.Thread(target=decrement)
                    threads.append(t1)
                    threads.append(t2)
                    t1.start()
                    t2.start()
                
                for t in threads:
                    t.join()
                
                print(counter)
                """,
                "Issue": "The race condition causes inconsistent results due to concurrent access to the shared counter.",
                "Solution": "Use thread synchronization techniques to ensure that the counter is safely accessed by one thread at a time.",
                "Solution Code": """
                # Fixed Code
                import threading
                counter = 0
                lock = threading.Lock()
                
                def increment():
                    global counter
                    with lock:
                        counter += 1
                
                def decrement():
                    global counter
                    with lock:
                        counter -= 1
                
                threads = []
                for _ in range(1000):
                    t1 = threading.Thread(target=increment)
                    t2 = threading.Thread(target=decrement)
                    threads.append(t1)
                    threads.append(t2)
                    t1.start()
                    t2.start()
                
                for t in threads:
                    t.join()
                
                print(counter)
                """
            },
            "Example 2": {
                "Name": "Memory Leak",
                "Buggy Code": """
                # Buggy Code
                class Resource:
                    def __init__(self):
                        self.data = [0] * 1000000
                
                resources = []
                for _ in range(100):
                    resources.append(Resource())  # Memory keeps increasing but not released
                
                print("Memory leak example")
                """,
                "Issue": "Objects are continuously being added to the list without releasing memory, leading to a memory leak.",
                "Solution": "Ensure proper memory management and clean up resources when they're no longer needed.",
                "Solution Code": """
                # Fixed Code
                class Resource:
                    def __init__(self):
                        self.data = [0] * 1000000
                
                resources = []
                for _ in range(100):
                    resources.append(Resource())
                
                # Explicitly deleting resources after use
                for resource in resources:
                    del resource
                
                print("Memory managed")
                """
            },
            "Example 3": {
                "Name": "Incorrect Output in Multithreading",
                "Buggy Code": """
                # Buggy Code
                def print_numbers():
                    for i in range(5):
                        print(i, end=" ")
                
                thread1 = threading.Thread(target=print_numbers)
                thread2 = threading.Thread(target=print_numbers)
                thread1.start()
                thread2.start()
                thread1.join()
                thread2.join()
                """,
                "Issue": "The output is interleaved and non-deterministic, causing the program to produce incorrect results due to concurrency.",
                "Solution": "Synchronize thread execution to prevent overlap and ensure consistent output.",
                "Solution Code": """
                # Fixed Code
                def print_numbers():
                    for i in range(5):
                        print(i, end=" ")
                
                thread1 = threading.Thread(target=print_numbers)
                thread2 = threading.Thread(target=print_numbers)
                thread1.start()
                thread1.join()  # Ensures thread1 finishes before starting thread2
                thread2.start()
                thread2.join()
                """
            },
            "Example 4": {
                "Name": "Timeout Error in Network Communication",
                "Buggy Code": """
                # Buggy Code
                import socket
                
                def connect_to_server():
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(("localhost", 8080))  # Timeout error might occur if server is down
                    s.send(b"Hello")
                    s.close()
                
                connect_to_server()
                """,
                "Issue": "The program does not handle timeout errors during network communication.",
                "Solution": "Add proper exception handling for network timeouts to prevent crashes.",
                "Solution Code": """
                # Fixed Code
                import socket
                import time
                
                def connect_to_server():
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(5)  # Set timeout
                        s.connect(("localhost", 8080))  # Timeout will now throw an exception if server is unresponsive
                        s.send(b"Hello")
                        s.close()
                    except socket.timeout:
                        print("Connection timed out")
                    except Exception as e:
                        print(f"An error occurred: {e}")
                
                connect_to_server()
                """
            },
            "Example 5": {
                "Name": "Deadlock in Resource Allocation",
                "Buggy Code": """
                # Buggy Code
                import threading
                
                lock1 = threading.Lock()
                lock2 = threading.Lock()
                
                def task1():
                    lock1.acquire()
                    time.sleep(1)  # Simulate work
                    lock2.acquire()
                    print("Task 1 complete")
                    lock1.release()
                    lock2.release()
                
                def task2():
                    lock2.acquire()
                    time.sleep(1)  # Simulate work
                    lock1.acquire()
                    print("Task 2 complete")
                    lock2.release()
                    lock1.release()
                
                thread1 = threading.Thread(target=task1)
                thread2 = threading.Thread(target=task2)
                thread1.start()
                thread2.start()
                thread1.join()
                thread2.join()
                """,
                "Issue": "Deadlock occurs because both threads are waiting for each other to release locks, resulting in a standstill.",
                "Solution": "Ensure locks are acquired in a consistent order to avoid circular wait conditions.",
                "Solution Code": """
                # Fixed Code
                import threading
                
                lock1 = threading.Lock()
                lock2 = threading.Lock()
                
                def task1():
                    lock1.acquire()
                    time.sleep(1)
                    lock2.acquire()
                    print("Task 1 complete")
                    lock1.release()
                    lock2.release()
                
                def task2():
                    lock1.acquire()  # Acquiring lock1 before lock2 to prevent deadlock
                    time.sleep(1)
                    lock2.acquire()
                    print("Task 2 complete")
                    lock1.release()
                    lock2.release()
                
                thread1 = threading.Thread(target=task1)
                thread2 = threading.Thread(target=task2)
                thread1.start()
                thread2.start()
                thread1.join()
                thread2.join()
                """
            }
        },
        "General Approach to Solving Bohrbugs": [
            "Identify the specific conditions under which the bug occurs, such as particular inputs, timings, or configurations.",
            "Replicate the bug consistently in a controlled environment to understand its behavior.",
            "Isolate the components involved, such as multi-threading, network communication, or resource allocation.",
            "Implement proper error handling, synchronization, or resource management to mitigate the issue.",
            "Use debugging tools such as profilers, thread analyzers, or network monitors to help diagnose the problem.",
            "Test thoroughly under various edge cases and conditions to ensure the bug is resolved."
        ]
    },

    "Data Bugs": {
        "Detailed Explanation": (
            "Data bugs occur when the program encounters issues due to incorrect or corrupted data. These bugs can stem from invalid inputs, "
            "improper data formats, or incorrect assumptions about the data, and often result in unexpected behavior, errors, or crashes."
        ),
        "Examples and Fixes": {
            "Example 1": {
                "Name": "Invalid Data Type",
                "Buggy Code": """
                # Buggy Code
                def process_age(age):
                    if age < 18:
                        print("Minor")
                    else:
                        print("Adult")
                
                process_age("twenty")  # Invalid input type
                """,
                "Issue": "Passing a string instead of an integer causes a runtime error.",
                "Solution": "Validate input types before using them.",
                "Solution Code": """
                # Fixed Code
                def process_age(age):
                    if not isinstance(age, int):
                        print("Invalid input type, age should be an integer.")
                        return
                    if age < 18:
                        print("Minor")
                    else:
                        print("Adult")
                
                process_age("twenty")  # Now the program handles the error gracefully
                """
            },
            "Example 2": {
                "Name": "Data Format Inconsistency",
                "Buggy Code": """
                # Buggy Code
                def process_date(date_str):
                    from datetime import datetime
                    date = datetime.strptime(date_str, "%Y/%m/%d")  # Expecting YYYY-MM-DD
                    print(date)
                
                process_date("12/31/2024")  # Wrong format
                """,
                "Issue": "The program expects a specific date format but receives a different format.",
                "Solution": "Ensure proper data format validation and conversion.",
                "Solution Code": """
                # Fixed Code
                def process_date(date_str):
                    from datetime import datetime
                    try:
                        date = datetime.strptime(date_str, "%Y/%m/%d")  # Expecting YYYY-MM-DD
                        print(date)
                    except ValueError:
                        print("Invalid date format, expected YYYY-MM-DD.")
                
                process_date("12/31/2024")  # Program now handles the error
                """
            },
            "Example 3": {
                "Name": "Out-of-Range Data",
                "Buggy Code": """
                # Buggy Code
                def get_value_from_list(data, index):
                    return data[index]  # Index might be out of range
                
                my_list = [1, 2, 3]
                print(get_value_from_list(my_list, 5))  # Index out of range
                """,
                "Issue": "Accessing an index that doesn't exist in the list results in an IndexError.",
                "Solution": "Check if the index is within the bounds of the list.",
                "Solution Code": """
                # Fixed Code
                def get_value_from_list(data, index):
                    if index < 0 or index >= len(data):
                        print("Index out of range")
                        return None
                    return data[index]
                
                my_list = [1, 2, 3]
                print(get_value_from_list(my_list, 5))  # Now safely handled
                """
            },
            "Example 4": {
                "Name": "Missing Required Data",
                "Buggy Code": """
                # Buggy Code
                def process_user_data(user):
                    if 'name' not in user:
                        raise ValueError("Missing required 'name' field")
                    print(f"Processing data for {user['name']}")
                
                user_data = {'age': 30}
                process_user_data(user_data)  # Missing 'name' field
                """,
                "Issue": "Missing required fields in the input data leads to errors.",
                "Solution": "Ensure that all required fields are present and handle missing data gracefully.",
                "Solution Code": """
                # Fixed Code
                def process_user_data(user):
                    if 'name' not in user:
                        print("Error: Missing required 'name' field")
                        return
                    print(f"Processing data for {user['name']}")
                
                user_data = {'age': 30}
                process_user_data(user_data)  # Now handled correctly
                """
            }
        },
        "General Approach to Solving Data Bugs": [
            "Validate all input data to ensure correct types, formats, and ranges.",
            "Handle missing, incomplete, or inconsistent data gracefully.",
            "Implement proper exception handling to prevent program crashes.",
            "Consider using data validation libraries or frameworks for complex data structures.",
            "Ensure data is cleaned and processed consistently throughout the application.",
            "Test with different edge cases and invalid inputs to uncover potential data issues."
        ]
    },

    "Error Handling Defects": {
        "Description": "Error handling defects arise when the program fails to anticipate, catch, or recover from errors.",
        "Examples and Fixes": {
            "Example 1": {
                "Name": "Uncaught Exception",
                "Buggy Code": """
                # Buggy Code
                def divide(a, b):
                    return a / b  # Division by zero may cause an error
                    
                print(divide(5, 0))  # Will raise ZeroDivisionError
                """,
                "Issue": "Attempting to divide by zero leads to an uncaught exception and program crash.",
                "Solution": "Wrap the operation in a try-except block to handle the exception gracefully.",
                "Solution Code": """
                # Fixed Code
                def divide(a, b):
                    try:
                        return a / b
                    except ZeroDivisionError:
                        print("Error: Cannot divide by zero")
                        return None
                    
                print(divide(5, 0))  # Now gracefully handles the error
                """
            },
            "Example 2": {
                "Name": "Incorrect Error Message",
                "Buggy Code": """
                # Buggy Code
                def open_file(filename):
                    with open(filename, 'r') as file:
                        return file.read()
                
                open_file("nonexistent_file.txt")  # Will raise FileNotFoundError
                """,
                "Issue": "Error message is not informative, leading to confusion about the issue.",
                "Solution": "Provide more detailed error messages in the exception handler.",
                "Solution Code": """
                # Fixed Code
                def open_file(filename):
                    try:
                        with open(filename, 'r') as file:
                            return file.read()
                    except FileNotFoundError:
                        print(f"Error: The file '{filename}' does not exist.")
                        return None
                    
                open_file("nonexistent_file.txt")  # Now provides a helpful error message
                """
            },
            "Example 3": {
                "Name": "Failure to Return Proper Error Code",
                "Buggy Code": """
                # Buggy Code
                def get_item_from_dict(data, key):
                    return data[key]  # Might raise KeyError if key doesn't exist
                
                my_dict = {'a': 1}
                print(get_item_from_dict(my_dict, 'b'))  # Will raise KeyError
                """,
                "Issue": "The program fails to handle missing keys, potentially crashing.",
                "Solution": "Ensure a return value or fallback is provided when the error is caught.",
                "Solution Code": """
                # Fixed Code
                def get_item_from_dict(data, key):
                    try:
                        return data[key]
                    except KeyError:
                        print(f"Error: The key '{key}' was not found.")
                        return None
                    
                my_dict = {'a': 1}
                print(get_item_from_dict(my_dict, 'b'))  # Now returns None with error message
                """
            }
        },
        "General Approach to Error Handling Defects": [
            "Always anticipate potential exceptions and handle them gracefully.",
            "Provide meaningful error messages that help developers understand the problem.",
            "Avoid program crashes by using try-except blocks or other error-handling techniques.",
            "Use custom error classes for specific error scenarios to improve code clarity.",
            "Ensure that errors are logged properly to allow tracing issues effectively.",
            "Test error-handling mechanisms with invalid inputs and unexpected conditions."
        ]
    },

    "Performance Faults": {
        "Description": "Performance faults occur when the program does not meet performance expectations, leading to inefficiencies.",
        "Examples and Fixes": {
            "Example 1": {
                "Name": "Inefficient Sorting Algorithm",
                "Buggy Code": """
                # Buggy Code
                def slow_sort(arr):
                    sorted_arr = []
                    while arr:
                        min_val = min(arr)
                        arr.remove(min_val)
                        sorted_arr.append(min_val)
                    return sorted_arr
                    
                print(slow_sort([5, 3, 8, 1, 2]))  # Very slow for large arrays
                """,
                "Issue": "The algorithm uses the min function repeatedly, resulting in O(n^2) time complexity.",
                "Solution": "Use more efficient sorting algorithms like quicksort or mergesort.",
                "Solution Code": """
                # Fixed Code
                def fast_sort(arr):
                    return sorted(arr)  # Built-in optimized sort function
                    
                print(fast_sort([5, 3, 8, 1, 2]))  # Faster for larger arrays
                """
            },
            "Example 2": {
                "Name": "Excessive Memory Usage",
                "Buggy Code": """
                # Buggy Code
                def large_data_handling():
                    data = [i for i in range(10**8)]  # Too much memory usage for large datasets
                    return sum(data)
                
                print(large_data_handling())  # Will consume too much memory
                """,
                "Issue": "The program consumes an excessive amount of memory due to handling large datasets entirely in memory.",
                "Solution": "Use memory-efficient techniques such as generators to process large datasets.",
                "Solution Code": """
                # Fixed Code
                def large_data_handling():
                    data = (i for i in range(10**8))  # Generator uses less memory
                    return sum(data)
                
                print(large_data_handling())  # More memory-efficient
                """
            },
            "Example 3": {
                "Name": "Unnecessary Repeated Calculations",
                "Buggy Code": """
                # Buggy Code
                def fibonacci(n):
                    if n <= 1:
                        return n
                    return fibonacci(n - 1) + fibonacci(n - 2)
                
                print(fibonacci(30))  # Slow for large numbers
                """,
                "Issue": "The recursive Fibonacci function calculates the same values multiple times, leading to exponential time complexity.",
                "Solution": "Use memoization or dynamic programming to optimize repeated calculations.",
                "Solution Code": """
                # Fixed Code
                def fibonacci(n, memo={}):
                    if n <= 1:
                        return n
                    if n not in memo:
                        memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
                    return memo[n]
                
                print(fibonacci(30))  # Now significantly faster
                """
            }
        },
        "General Approach to Addressing Performance Faults": [
            "Analyze the time and space complexity of algorithms to identify inefficiencies.",
            "Profile the code to locate performance bottlenecks and optimize them.",
            "Use memory-efficient data structures to reduce resource consumption.",
            "Optimize code by avoiding unnecessary repeated calculations and redundant operations.",
            "Leverage parallel processing or multi-threading where appropriate to improve speed.",
            "Test with large datasets and real-world conditions to ensure performance meets expectations."
        ]
    },
    
    "No Bugs Found": {
        "Description": "No bugs were found in the code. Great Job!"
    }
}