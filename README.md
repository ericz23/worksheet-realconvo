# Data Labeling:
Run in order:
- raw_data_loading/load_data.py
- data_extraction/annotate_conv_submit.py
- data_extraction/annotate_retrieve.py

# Generating Agent Rulebook from Conversation Simulation:
## Database Retrieval Method:
Run in order:
- get_policy_db.py
- extend_conv_db.py
Note that if you intend to run it, please ask the authors for database access. The authors will add your local IP to our SQL server and provide ways to connect.

## SFT method:
- get_policy_ft.py

# Consolidating Rulebooks
Run in order:
- get_branching.py
- synthesize_rulebook.py

# Running Evaluations
- policy_eval/eval_pipeline.py
