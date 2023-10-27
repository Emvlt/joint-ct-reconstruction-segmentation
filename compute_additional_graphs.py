from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

setting_names = ['6_percent_measurements', '25_percent_measurements']

modality_list = [
        '0_1', '0_2', '0_3',
        '0_4', '0_5', '0_6',
        '0_7', '0_8', '0_9',
        '1', 'sequential'
        ]


def compute_metric_vs_annotation_size(metric_name:str):
    for setting in setting_names:
        result_dict = {
        'Modality':[],
        'Annotation Size':[],
        f'{metric_name}':[]
    }

        path_to_result_folder = Path(f'new_processed_results/{setting}')

        for modality in modality_list:
            result = pd.read_csv(f'./new_processed_results/{setting}/lpd_unet_{modality}.csv')
            result = result[~result['annotation_size_mean'].isna()]
            annotations_sizes = result['annotation_size_mean'].unique()
            for annotation_size in annotations_sizes:
                annotations_subset = result[result['annotation_size_mean'] == annotation_size]
                dice_average = annotations_subset[f'{metric_name}'].mean()
                result_dict['Annotation Size'].append(annotation_size)
                result_dict['Modality'].append(modality)
                result_dict[f'{metric_name}'].append(dice_average)

        result_df = pd.DataFrame.from_dict(result_dict)
        result_df.to_csv(path_to_result_folder.joinpath(f'{metric_name}_against_annotation_size.csv'), index=False)


if __name__=='__main__':
    for setting in ['6_percent_measurements', '25_percent_measurements']:
        metric_name = 'DICE'
        path_to_result_folder = Path(f'new_processed_results/{setting}')

        #compute_metric_vs_annotation_size(metric_name)

        result_df = pd.read_csv( path_to_result_folder.joinpath(f'{metric_name}_against_annotation_size.csv'))

        histogram_path = path_to_result_folder.joinpath(f'{metric_name}_histogram.csv')

        hist_dict = {
            'Modality':[],
            'DICE':[],
            'Count':[]
        }

        for mod in modality_list:
            mod_df = result_df[result_df['Modality'] == mod]
            hist, bin_edges = np.histogram(
                mod_df['DICE'],
                bins=[0.1*i for i in range(10)]
                )
            for count, dice in zip(hist, [0.1*i for i in range(10)]):
                hist_dict['Modality'].append(mod)
                hist_dict['DICE'].append(f'{dice:.2f}')
                hist_dict['Count'].append(count)

        hist_df = pd.DataFrame.from_dict(hist_dict)
        hist_df.to_csv(histogram_path, index=False)

