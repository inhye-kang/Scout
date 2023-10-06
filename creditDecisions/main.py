import sys
sys.path.insert(1, "../")  

import numpy as np
np.random.seed(0)

from aif360.datasets import GermanDataset
from aif360.metrics import BinaryLabelDatasetMetric
from aif360.algorithms.preprocessing import Reweighing

from IPython.display import Markdown, display

#load the initial dataset, set protected attribute to age
dataset_orig = GermanDataset(
    protected_attribute_names=['age'],
    # age >=25 is considered privileged
    privileged_classes=[lambda x: x >= 25],
    # ignore sex-related attributes    
    features_to_drop=['personal_status', 'sex']
)

#split the original dataset into training and testing datasets
dataset_orig_train, dataset_orig_test = dataset_orig.split([0.7], shuffle=True)

#we set two var for the privileged (1) and unprivileged (0) for the age attribute
privileged_groups = [{'age': 1}]
unprivileged_groups = [{'age': 0}]

#compare the percentage of favorable results for the privileged and unprivileged groups thru percentage subtraction
metric_orig_train = BinaryLabelDatasetMetric(dataset_orig_train, unprivileged_groups=unprivileged_groups, privileged_groups=privileged_groups)
display(Markdown("#### Original training dataset"))
print("Difference in mean outcomes between unprivileged and privileged groups = %f" % metric_orig_train.mean_difference())

#use the Reweighing algorithm to transform the dataset to have more equity in positive outcomes on the protected attribute for the privileged and unprivileged groups
RW = Reweighing(unprivileged_groups=unprivileged_groups,
                privileged_groups=privileged_groups)
dataset_transf_train = RW.fit_transform(dataset_orig_train)

#check how effective the transformed dataset was in removing bias by using the same metric we used for the original training dataset
metric_transf_train = BinaryLabelDatasetMetric(dataset_transf_train, 
                                               unprivileged_groups=unprivileged_groups,
                                               privileged_groups=privileged_groups)
display(Markdown("#### Transformed training dataset"))
print("Difference in mean outcomes between unprivileged and privileged groups = %f" % metric_transf_train.mean_difference())