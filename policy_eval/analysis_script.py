import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Setup and Configuration
RESULTS_DIR = "results"
PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

# File mapping: path -> label
FILES = {
    "evaluation_results_finetuned_model.csv": "Finetuned",
    "evaluation_results_v2.csv": "Policy Probing",
    "evaluation_results_v4.csv": "Policy Probing Extended",
    "evaluation_results_db_branching.csv": "Data Branching",
    "evaluation_results_ft_branching.csv": "Finetuned Branching"
}

def load_data():
    dfs = []
    for filename, label in FILES.items():
        path = os.path.join(RESULTS_DIR, filename)
        if not os.path.exists(path):
            print(f"Warning: File not found: {path}")
            continue
        
        try:
            df = pd.read_csv(path)
            df['Model'] = label
            
            # Ensure numeric columns
            for col in ['intent_match', 'semantic_similarity', 'policy_adherence']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            dfs.append(df)
            print(f"Loaded {label}: {len(df)} rows. Columns: {list(df.columns)}")
        except Exception as e:
            print(f"Error loading {path}: {e}")

    if not dfs:
        raise ValueError("No data loaded.")
    
    return pd.concat(dfs, ignore_index=True)

def generate_visualizations(df):
    sns.set_theme(style="whitegrid", palette="viridis", font_scale=1.1)
    plt.rcParams.update({
        'font.weight': 'bold',
        'axes.labelweight': 'bold',
        'axes.titleweight': 'bold',
        'figure.titleweight': 'bold',
    })
    
    # Create a fixed color mapping for models to ensure consistency across plots
    unique_models = sorted(df['Model'].unique())
    palette = sns.color_palette("viridis", n_colors=len(unique_models))
    model_colors = dict(zip(unique_models, palette))
    
    # Melt for shared metrics comparison
    metrics = ['intent_match', 'semantic_similarity']
    df_melted = df.melt(id_vars=['Model'], value_vars=[m for m in metrics if m in df.columns], 
                        var_name='Metric', value_name='Score')

    # ---------------------------------------------------------
    # Visual A: Performance Overview (Bar Chart of Means)
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_melted, x='Model', y='Score', hue='Metric', ci=95, capsize=.1)
    plt.title('Average Performance by Model (with 95% CI)')
    plt.ylim(0, 1.1)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'performance_overview.png'))
    plt.close()
    print("Generated performance_overview.png")

    # ---------------------------------------------------------
    # Visual B: Semantic Similarity Distribution (Box Plot)
    # ---------------------------------------------------------
    if 'semantic_similarity' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x='Model', y='semantic_similarity', hue='Model', palette=model_colors)
        # Remove the legend manually if desired, or keep it. 
        # sns.boxplot doesn't accept a 'legend' parameter in older seaborn versions or some contexts,
        # but usually hue implies a legend. We can remove it via plt.legend([],[], frameon=False)
        plt.legend([],[], frameon=False)
        plt.title('Distribution of Semantic Similarity Scores')
        plt.ylabel('Semantic Similarity Score')
        plt.ylim(-0.1, 1.1)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, 'semantic_similarity_dist.png'))
        plt.close()
        print("Generated semantic_similarity_dist.png")

    # ---------------------------------------------------------
    # Visual C: Intent Match Distribution (Box Plot) 
    # ---------------------------------------------------------
    if 'intent_match' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x='Model', y='intent_match', hue='Model', palette=model_colors)
        plt.legend([],[], frameon=False)
        plt.title('Distribution of Intent Match Scores')
        plt.ylabel('Intent Match Score')
        plt.ylim(-0.1, 1.1)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, 'intent_match_dist.png'))
        plt.close()
        print("Generated intent_match_dist.png")

    # ---------------------------------------------------------
    # Visual D: Policy Adherence (Histogram + Pass Rate)
    # ---------------------------------------------------------
    if 'policy_adherence' in df.columns:
        df_policy = df.dropna(subset=['policy_adherence'])
        if not df_policy.empty:
            models_with_policy = df_policy['Model'].unique()
            print(f"Models with Policy Adherence data: {models_with_policy}")
            
            # 1. Histogram
            plt.figure(figsize=(10, 6))
            sns.histplot(data=df_policy, x='policy_adherence', hue='Model', 
                         multiple="dodge", bins=20, kde=True, palette=model_colors)
            plt.title('Distribution of Policy Adherence Scores')
            plt.tight_layout()
            plt.savefig(os.path.join(PLOTS_DIR, 'policy_adherence_hist.png'))
            plt.close()
            print("Generated policy_adherence_hist.png")

            # 2. High Score Rate (Bar Chart)
            # Calculate % of responses with score > 0.9
            pass_rates = df_policy.groupby('Model')['policy_adherence'].apply(lambda x: (x > 0.9).mean()).reset_index()
            pass_rates.columns = ['Model', 'Adherence_Rate']

            # Define custom order
            target_order = ["Policy Probing", "Data Branching", "Finetuned Branching"]
            # Ensure we include all models present, but prioritize the target order
            existing_models = set(pass_rates['Model'].unique())
            final_order = [m for m in target_order if m in existing_models]
            # Add any models that are in the data but not in the target order
            final_order.extend([m for m in existing_models if m not in target_order])
            
            plt.figure(figsize=(8, 6))
            sns.barplot(data=pass_rates, x='Model', y='Adherence_Rate', hue='Model', dodge=False, order=final_order, palette=model_colors)
            plt.legend([],[], frameon=False)
            plt.title('Proportion of Policy Adherence Scores > 0.9')
            plt.ylabel('Policy Adherence Rate')
            plt.ylim(0, 1.1)
            
            # Add text labels matching the visual order
            for i, model_name in enumerate(final_order):
                row = pass_rates[pass_rates['Model'] == model_name]
                if not row.empty:
                    rate = row.iloc[0]['Adherence_Rate']
                    plt.text(i, rate + 0.02, f"{rate:.1%}", ha='center')
                    
            plt.tight_layout()
            plt.savefig(os.path.join(PLOTS_DIR, 'policy_adherence_rate.png'))
            plt.close()
            print("Generated policy_adherence_rate.png")
        else:
            print("No policy_adherence data found to plot.")

def print_summary(df):
    print("\n--- Summary Statistics ---")
    
    # Group by Model and calculate mean/std for numeric cols
    numeric_cols = ['intent_match', 'semantic_similarity', 'policy_adherence']
    cols_present = [c for c in numeric_cols if c in df.columns]
    
    summary = df.groupby('Model')[cols_present].agg(['mean', 'median', 'std', 'count'])
    print(summary.round(3))
    
    # Save summary to CSV
    summary.to_csv(os.path.join(RESULTS_DIR, 'analysis_summary.csv'))
    print(f"\nSummary saved to {os.path.join(RESULTS_DIR, 'analysis_summary.csv')}")

if __name__ == "__main__":
    print("Starting analysis...")
    df_all = load_data()
    generate_visualizations(df_all)
    print_summary(df_all)
    print("Analysis complete.")

