"""
clustering-benchmarks Package
"""


# ############################################################################ #
#                                                                              #
#   Copyleft (C) 2020-2022, Marek Gagolewski <https://www.gagolewski.com>      #
#                                                                              #
#                                                                              #
#   This program is free software: you can redistribute it and/or modify       #
#   it under the terms of the GNU Affero General Public License                #
#   Version 3, 19 November 2007, published by the Free Software Foundation.    #
#   This program is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the               #
#   GNU Affero General Public License Version 3 for more details.              #
#   You should have received a copy of the License along with this program.    #
#   If this is not the case, refer to <https://www.gnu.org/licenses/>.         #
#                                                                              #
# ############################################################################ #


import os.path
import numpy as np
from collections import namedtuple
from .preprocess_data import preprocess_data


def load_dataset(
    battery, dataset, path=None,
    url=None, expanduser=True, expandvars=True,
    preprocess=True, random_state=None
):
    """
    Load a benchmark dataset

    Reads a dataset named `battery/dataset.data.gz`
    (relative to `url` or the directory `path`)
    as well as all the corresponding labels
    (`battery/dataset.labels0.gz`, `battery/dataset.labels1.gz`, ...).

    Parameters
    ----------

    battery
        Name of the battery, e.g., ``"wut"`` or ``"other"``.

    dataset
        Dataset name, e.g., ``"x2"`` or ``"iris"``.

    path
        Mutually exclusive with `url`.
        Path to the directory containing the downloaded benchmark datasets
        suite. Defaults to the current working directory.

    url
        Mutually exclusive with `path`. For example,
        ``"https://github.com/gagolews/clustering-data-v1/raw/v1.0.1"``
        to get access to <https://github.com/gagolews/clustering-data-v1>,

    expanduser
        Whether to call ``os.path.expanduser`` on the file path.

    expandvars
        Whether to call ``os.path.expandvars`` on the file path.

    preprocess
        Whether to call :any:`preprocess_data` on the data matrix.

    random_state
        Seed of the random number generator; passed to :any:`preprocess_data`.


    Returns
    -------

    dataset
        A named tuple with the following elements:

        battery
            Same as the `battery` argument.

        dataset
            Same as the `dataset` argument.

        description
            Contents of the description file.

        data
            Data matrix.

        labels
            A list consisting of the label vectors.

    Examples
    --------

    >>> import os.path
    >>> import clustbench
    >>> # load from a local library (a manually downloaded suite)
    >>> data_path = os.path.join("~", "Projects", "clustering-data-v1")  # up to you
    >>> wut_x2 = clustbench.load_dataset("wut", "x2", path=data_path)
    >>> print(wut_x2.battery, wut_x2.dataset)
    >>> print(wut_x2.description)
    >>> print(wut_x2.data, wut_x2.labels)
    >>> # load from GitHub (slow...):
    >>> data_url = "https://github.com/gagolews/clustering-data-v1/raw/v1.1.0"
    >>> wut_smile = clustbench.load_dataset("wut", "smile", url=data_url)
    >>> print(wut_smile.data, wut_smile.labels)
    """
    if url is not None and path is not None:
        raise ValueError("`url` and `path` are mutually exclusive.")

    if url is not None:
        base_name = url + "/" + battery + "/" + dataset
    else:
        if path is None: path = "."
        base_name = os.path.join(path, battery, dataset)
        if expanduser: base_name = os.path.expanduser(base_name)
        if expandvars: base_name = os.path.expandvars(base_name)

    data_file = base_name + ".data.gz"
    data = np.loadtxt(data_file, ndmin=2)

    if data.ndim != 2:
        raise ValueError("Not a matrix.")

    if preprocess:
        data = preprocess_data(data, random_state=random_state)


    labels = []
    i = 0
    while True:
        try:
            f = base_name + ".labels%d.gz" % i
            l = np.loadtxt(f, dtype="int")
            if l.ndim != 1 or l.shape[0] != data.shape[0]:
                raise ValueError("Incorrect number of labels in '%s'." % f)

            labels.append(l)
            i += 1
        except FileNotFoundError:
            # this could be done better with glob.glob for local files,
            # but not for remote URLs
            break

    with np.DataSource().open(base_name + ".txt", "r") as readme_file:
        description = readme_file.read()

    RetClass = namedtuple(
        "ClusteringBenchmark",
        ["battery", "dataset", "description", "data", "labels"]
    )
    return RetClass(
        battery=battery,
        dataset=dataset,
        description=description,
        data=data,
        labels=labels,
    )
