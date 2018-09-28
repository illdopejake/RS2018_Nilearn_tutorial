import warnings
import urllib.parse

import numpy as np
import os.path

from sklearn.datasets.base import Bunch
from nilearn.datasets.utils import _get_dataset_dir, _fetch_files


def fetch_data(n_subjects=30, data_dir=None, url=None, resume=True,
               verbose=1):
    """Download and load the dataset.

    Parameters
    ----------
    n_subjects: int, optional
        The number of subjects to load from maximum of 40 subjects.
        By default, 30 subjects will be loaded. If None is given,
        all 40 subjects will be loaded.

    data_dir: string, optional
        Path of the data directory. Used to force data storage in a specified
        location. Default: None

    url: string, optional
        Override download URL. Used for test only (or if you setup a mirror of
        the data). Default: None

    Returns
    -------
    data: sklearn.datasets.base.Bunch
        Dictionary-like object, the interest attributes are :
         - 'func': Paths to functional resting-state images
         - 'phenotypic': Explanations of preprocessing steps
         - 'confounds': CSV files containing the nuisance variables

    References
    ----------
    :Download:
        https://openneuro.org/datasets/ds000228/versions/00001

    """

    if url is None:
        url = 'https://openneuro.org/crn/datasets/ds000228/snapshots/00001/files/'

    # Preliminary checks and declarations
    dataset_name = 'ds000228'
    data_dir = _get_dataset_dir(dataset_name, data_dir=data_dir,
                                verbose=verbose)
    max_subjects = 155
    if n_subjects is None:
        n_subjects = max_subjects
    if n_subjects > max_subjects:
        warnings.warn('Warning: there are only %d subjects' % max_subjects)
        n_subjects = max_subjects
    ids = range(1, n_subjects + 1)

    # First, get the metadata
    phenotypic = (
            'participants.tsv',
            url + 'participants.tsv', dict())

    phenotypic_file = _fetch_files(data_dir, [phenotypic], resume=resume,
                              verbose=verbose)[0]

    # Load the csv file
    phenotypic = np.genfromtxt(phenotypic_file, names=True, delimiter='\t',
                               dtype=None)

    # Keep phenotypic information for selected subjects
    int_ids = np.asarray(ids, dtype=int)
    phenotypic = phenotypic[[i - 1 for i in int_ids]]

    # Download dataset files

    functionals = [urllib.parse.quote(
        'derivatives:fmriprep:sub-pixar%03i:sub-pixar%03i_task-pixar_run-001_swrf_bold.nii.gz' % (i, i))
        for i in ids]
    urls = [url + name for name in functionals]
    functionals = _fetch_files(
        data_dir, zip(functionals, urls, (dict(),) * n_subjects),
        resume=resume, verbose=verbose)

    confounds = [
        urllib.parse.quote('derivatives:fmriprep:sub-pixar%03i:sub-pixar%03i_task-pixar_run-001_ART_and_CompCor_nuisance_regressors.mat'
        % (i, i))
        for i in ids]
    confound_urls = [url + name for name in confounds]

    confounds = _fetch_files(
        data_dir, zip(confounds, confound_urls, (dict(),) * n_subjects),
        resume=resume, verbose=verbose)

    return Bunch(func=functionals, confounds=confounds,
                 phenotypic=os.path.join(data_dir, phenotypic_file),
                 description='ds000228')


if __name__ == "__main__":
    # Download everything
    fetch_data(n_subjects=None)
