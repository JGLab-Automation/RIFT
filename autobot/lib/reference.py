__author__ = "JG"

"""
This is just a sample file and not used for any execution.
"""



"""
GET a leaf
/api/running/misc/int-leaf

GET a top-level container
/api/running/top-container-deep

GET a top-level container with ?deep
/api/running/top-container-deep?deep

GET a container
/api/running/top-container-deep/inner-container

GET a whole list
/api/running/top-list-shallow

GET a specific list entry
/api/running/top-list-shallow/asdf
"""



"""
POST/PUT a leaf
/api/running/top-container-shallow

POST/PUT a container
/api/config/top-container-deep/inner-container

POST/PUT a list entry
/api/running/top-list-shallow/asdf
"""