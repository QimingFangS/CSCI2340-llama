Title: 
Code Debugging Project -- Backend Server 2

Link to the overall backends workflow pipeline:
https://docs.google.com/drawings/d/1_L3x8BSyXFxRXm1XaalxutYp5_VynZwe3JpWyMylrLg/edit?usp=sharing

Structure: 
Here is the structure of current evaluation backend 2:

project_postgeneation_root/
├── main.py                             # The main entry point to run the server and initialize endpoints
├── requirements.txt                    # All library dependencies required by the backend              
├── tools.txt                           # All tools dependencies required by the backend
├── app/                                # Directory for the server application 
│   ├── routes.py                       # Defines API endpoint to communicate with other backends/frontends
│   └── utils.py                        # Utility functions for formatting, logging, etc.
│   └── get_code.py                     # Extract and validate code block from the LLM's output
├── Checks/                             # Directory for different checks
│   ├── static_analysis/                # Static analysis checking
│   │   ├── __init__.py
│   │   ├── run_py_check.py             # Run Bandit, mypy, an pylint for Python
│   │   ├── run_clangtidy_check.py      # Run clang-tidy for C/C++
│   │   └── run_sonarqube_check.py      # Run SonarQube for other languages
│   ├── dynamic_analysis/               # Dynamic analysis checking
│   │   ├── __init__.py
│   │   └── run_valgrind_check.py       # Run Valgrind for memory checking
│   ├── formal_verification/            # Formal verification checking
│   │   ├── __init__.py
│   │   └── run_dafny_check.py          # Run Dafny for formal verification
│   └── rankme/                         # Ranking mechanism based on embeddings
│       ├── __init__.py
│       └── rankme_computation.py       # Compute RankMe score based on the output's text embeddings
└── Results/                            # Directory to save combined results (JSON)
│   └── combined_results.json           # Final output file with all results
└── temp/                               # Temporary files directory
│   └── code_files/                     # Subdirectory for temporary code files
└── logs/                               # Directory to record loggings
│   └── app.log                         # File to record local loggings
│   └── logs.txt                        # File to record global loggings
└── tests/                              # Directory for unit tests
    └── app_test.py                     # Test on app
    └── checks_test.py                  # Test on Checks