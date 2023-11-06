annotations = ['large', 'small']

metrics = ['BCE_loss', 'TP', 'FP', 'TN', 'FN', 'Sensitivity', 'DICE']

metrics_to_display = {
    'BCE_loss': 'Binary Cross-Entropy',
    'TP':'Number of True Positives',
    'FP':'Number of False Positives',
    'TN':'Number of True Negatives',
    'FN':'Number of False Negatives',
    'Sensitivity':'Sensitivity Score',
    'DICE':'Dice Score'
}
display_to_metrics = dict((v, k) for k, v in metrics_to_display.items())

modality_list = [
            'lpd_unet_0_1', 'lpd_unet_0_2', 'lpd_unet_0_3',
            'lpd_unet_0_4', 'lpd_unet_0_5', 'lpd_unet_0_6',
            'lpd_unet_0_7', 'lpd_unet_0_8', 'lpd_unet_0_9',
            'lpd_unet_1', 'lpd_unet_sequential'
            ]

modality_list_display = [
            'sequential',
            '0.1', '0.2', '0.3',
            '0.4', '0.5', '0.6',
            '0.7', '0.8', '0.9',
            'end-to-end',
        ]

modalities_to_display = {
    'lpd_unet_0_1':'C = 0.1',
    'lpd_unet_0_2':'C = 0.2',
    'lpd_unet_0_3':'C = 0.3',
    'lpd_unet_0_4':'C = 0.4',
    'lpd_unet_0_5':'C = 0.5',
    'lpd_unet_0_6':'C = 0.6',
    'lpd_unet_0_7':'C = 0.7',
    'lpd_unet_0_8':'C = 0.8',
    'lpd_unet_0_9':'C = 0.9',
    'lpd_unet_1'  :'C = 1',
    'lpd_unet_sequential':'sequential'
}

displays_to_modality = dict((v, k) for k, v in modalities_to_display.items())