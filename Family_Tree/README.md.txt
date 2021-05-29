# Meet_The_Family
## GEEKTRUST MEET THE FAMILY

### INSTRUCTIONS TO RUN:
pip install -r requirements.txt
python -m geektrust <absolute_path_to_filename>

### INSTRUCTIONS TO UNIT TEST:
python -m unittest discover ./tests/unit && flake8

### INSTRUCTIONS TO INTEGRATION TEST:
python -m unittest discover ./tests/integration && flake8

### INPUT FORMATS:
* ADD_CHILD (MOTHER_NAME) (CHILD_NAME) (CHILD_GENDER)
* GET_RELATIONSHIP (PERSON_NAME) (RELATIONSHIP)
* Relationships :
	* Paternal-Uncle
	* Maternal-Uncle
	* Paternal-Aunt
	* Maternal-Aunt
	* Sister-In-Law
	* Brother-In-Law
	* Son
	* Daughter
	* Siblings
* Genders :
	* Male
	* Female
* **All inputs are case-sensitive**