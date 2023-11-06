from pathlib import Path
from typing import Dict

import pandas as pd
import numpy as np

setting_names = ['6_percent_measurements', '25_percent_measurements']

modality_list = {
        '6_percent_measurements':[
            'lpd_unet_0_1', 'lpd_unet_0_2', 'lpd_unet_0_3',
            'lpd_unet_0_4', 'lpd_unet_0_5', 'lpd_unet_0_6',
            'lpd_unet_0_7', 'lpd_unet_0_8', 'lpd_unet_0_9',
            'lpd_unet_1', 'lpd_unet_sequential'
            ],
        '25_percent_measurements':[
            'lpd_unet_0_1', 'lpd_unet_0_2', 'lpd_unet_0_3',
            'lpd_unet_0_4', 'lpd_unet_0_5', 'lpd_unet_0_6',
            'lpd_unet_0_7', 'lpd_unet_0_8', 'lpd_unet_0_9',
            'lpd_unet_1', 'lpd_unet_sequential'
            ],
        'from_input_images':[
            'unet_shuffle_inception_no_progressive'
            ]
        }


def compute_metric_vs_annotation_size(setting_name:str, metric_name:str, path_to_metric_res:Path):

    result_dict = {
        'Modality':[],
        'Annotation Size':[],
        f'{metric_name}':[]
    }

    path_to_result_folder = Path(f'new_processed_results/{setting_name}')

    for modality in modality_list[setting_name]:
        result = pd.read_csv(path_to_result_folder.joinpath(f'{modality}.csv'))
        result = result[~result['annotation_size_mean'].isna()]
        annotations_sizes = result['annotation_size_mean'].unique()
        for annotation_size in annotations_sizes:
            annotations_subset = result[result['annotation_size_mean'] == annotation_size]
            dice_average = annotations_subset[f'{metric_name}'].mean()
            result_dict['Annotation Size'].append(annotation_size)
            result_dict['Modality'].append(modality)
            result_dict[f'{metric_name}'].append(dice_average)

    result_df = pd.DataFrame.from_dict(result_dict)
    result_df.to_csv(path_to_metric_res, index=False)


def metric_to_hist(mod_df:pd.DataFrame, metric_name:str, bins_dict:Dict):
    if bins_dict[metric_name] is None:
        hist, bin_edges = np.histogram(
                        mod_df[metric_name]
                        )
        bins_dict[metric_name] = list(bin_edges)
    else:
        hist, bin_edges = np.histogram(
                        mod_df[metric_name],
                        bins=bins_dict[metric_name]
                        )

    return hist, bins_dict[metric_name]

if __name__=='__main__':

    bins_dict = {
        'BCE_loss':None,
        'TP':None,
        'FP':None,
        'TN':None,
        'FN':None,
        'Sensitivity':[0.1*i for i in range(11)],
        'DICE':[0.1*i for i in range(11)]
    }

    for setting_name in ['6_percent_measurements', '25_percent_measurements']:
        for metric_name in ['BCE_loss', 'TP', 'FP', 'TN', 'FN', 'Sensitivity', 'DICE']:
            path_to_result_folder = Path(f'new_processed_results/{setting_name}')

            path_to_metric_res = path_to_result_folder.joinpath(f'{metric_name}_against_annotation_size.csv')
            if not path_to_metric_res.is_file():
                compute_metric_vs_annotation_size(setting_name, metric_name, path_to_metric_res)

            result_df = pd.read_csv(path_to_metric_res)

            histogram_path = path_to_result_folder.joinpath(f'{metric_name}_histogram.csv')

            hist_dict = {
                'Modality':[],
                metric_name:[],
                'Count':[]
            }

            for mod in modality_list[setting_name]:
                mod_df = result_df[result_df['Modality'] == mod]
                hist, bin_edges = metric_to_hist(mod_df, metric_name, bins_dict)
                for count, bin_val in zip(hist, bin_edges):
                    hist_dict['Modality'].append(mod)
                    hist_dict[metric_name].append(f'{bin_val:.2f}')
                    hist_dict['Count'].append(count)

            hist_df = pd.DataFrame.from_dict(hist_dict)
            hist_df.to_csv(histogram_path, index=False)

