# ai-trust-testbed
A program designed for a study involving participants' trust in an artificial intelligence.  This is tested by asking the participant to "bet" on horse races where an AI has predicted the outcome.  Researchers will then observe the participant's actions while choosing their bet, as an indication of trust, (i.e. choosing the AI's suggestion, amount of time taken, etc).

Data used for the AI will be located in `../data`, which allows read access to everyone (`774`).  On gemini, this directory is `~amcarthu/summer-research-2017/data`.
This will contain data from the forumlator website, as it was downloaded.  A user can run `compile_data.py` (after configuring the compilation in `config.py`), which scrapes the data found in `../data` to generate a single (large) data file for use for a given AI, depending on the settings found in the config file.  This file can be found at `data.csv` by default.
