import argparse
import pandas as pd

class DatasetFormatter:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)

    def format_to_competition(self, text_col, ai_text_col=None, prompt_col=None, generated_col=None):
        formatted_df = pd.DataFrame(columns=['text', 'prompt', 'generated'])
        if generated_col:
            self.df['text'] = self.df[text_col]
            self.df['prompt'] = self.df[prompt_col]
            self.df['generated'] = self.df[generated_col]
            formatted_df = self.df[['text', 'prompt', 'generated']]
        else:
            ai_texts = self.df[ai_text_col].dropna().tolist()
            ai_prompts = self.df[prompt_col].dropna().tolist()[:len(ai_texts)]
            
            student_texts = self.df[text_col].dropna().tolist()
            student_prompts = self.df[prompt_col].dropna().tolist()[:len(student_texts)]
            
            # Ensure consistent lengths
            min_length = min(len(ai_texts), len(ai_prompts))
            ai_texts, ai_prompts = ai_texts[:min_length], ai_prompts[:min_length]
            
            min_length = min(len(student_texts), len(student_prompts))
            student_texts, student_prompts = student_texts[:min_length], student_prompts[:min_length]
            
            ai_df = pd.DataFrame({
                'text': ai_texts,
                'prompt': ai_prompts,
                'generated': [1] * len(ai_texts)
            })

            student_df = pd.DataFrame({
                'text': student_texts,
                'prompt': student_prompts,
                'generated': [0] * len(student_texts)
            })

            formatted_df = pd.concat([ai_df, student_df], ignore_index=True)

        formatted_df = formatted_df.sample(frac=1).reset_index(drop=True)
        return formatted_df

    def save_to_csv(self, dataframe, save_path):
        dataframe.to_csv(save_path, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Format external dataset to competition's format.")
    parser.add_argument('--file', required=True, help='Path to the external dataset.')
    parser.add_argument('--text_col', required=True, help='Column name for student texts.')
    parser.add_argument('--ai_text_col', default=None, help='Column name for AI texts.')
    parser.add_argument('--prompt_col', required=True, help='Column name for prompts.')
    parser.add_argument('--generated_col', default=None, help='Column name for generated flag.')
    parser.add_argument('--output', default='formatted_dataset.csv', help='Path to save the formatted dataset.')

    args = parser.parse_args()

    formatter = DatasetFormatter(args.file)
    formatted_df = formatter.format_to_competition(args.text_col, args.ai_text_col, args.prompt_col, args.generated_col)
    formatter.save_to_csv(formatted_df, args.output)
