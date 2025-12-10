# data labeling:
run in order
- run raw_data_loading/load_data.py
- run data_extraction/annotate_conv_submit.py
- run data_extraction/annotate_retrieve.py to get the results

# generate agent rulebook:
## To run the Database retrieval method: (need to connect to database, please contact authors to add local ip to host)
run those in order:
get_policy_db.py
extend_conv_db.py

## To run the sft method:
get_policy_ft.py

# consolidate rulebooks
run those in order:
get_branching.py
synthesize_rulebook.py

# to run evaluations
run policy_eval/eval_pipeline.py