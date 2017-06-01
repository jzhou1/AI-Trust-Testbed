"""
 * Drew McArthur, Geo Engel, Risa Ulinski, Judy Zhou
 * 6/1/17
 * This file is used to configure the project.  Initially, it will contain 
   variables used in the compilation script, however it can and likely will 
   expand to be used within other files.
"""

"""     Compilation Configuration       """
# Filename to save final data to
final_data_filename = "~amcarthu/summer-research-2017/ai-trust-testbed/data.csv"

# The AI that the data is being compiled for.
# This can be one of three options, which can be seen in the variables below.
# The problems are described in more depth within README.MD
PREDICT_TIME_AI = 1
PREDICT_BSF_AI = 2
PREDICT_WINNER_AI = 3
target_ai = PREDICT_TIME_AI
