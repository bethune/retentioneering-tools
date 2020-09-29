# Copyright (C) 2019 Maxim Godzi, Anatoly Zaytsev, Dmitrii Kiselev
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import itertools
from datetime import datetime


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


from .plot_utils import __save_plot__

@__save_plot__
def step_matrix(data, targets=None, *,
                targets_list=None, plot_name=None,
                title='', centered_position=None, precision=2):

    target_cmaps = itertools.cycle(['BrBG', 'PuOr', 'PRGn', 'RdBu'])

    n_rows = 1 + (len(targets_list) if targets_list else 0)
    n_cols = 1

    grid_specs = ({'wspace': 0.08, 'hspace': 0.04,
                  'height_ratios': [data.shape[0], *list(map(len, targets_list))]}
                 if targets is not None else {})

    f, axs = sns.mpl.pyplot.subplots(n_rows, n_cols, sharex=True,

                                     figsize=(round(data.shape[1] * 0.7),
                                              round((len(data) +
                                                     (len(targets) if targets is not None else 0)) * 0.6)),

                                     gridspec_kw=grid_specs)

    heatmap = sns.heatmap(data,
                          yticklabels=data.index,
                          annot=True,
                          fmt=f'.{precision}f',
                          ax=axs[0] if targets is not None else axs,
                          cmap="RdGy",
                          center=0,
                          cbar=False)

    heatmap.set_title(title, fontsize=16)

    if targets is not None:
        for n, i in enumerate(targets_list):
            sns.heatmap(targets.loc[i],
                        yticklabels=targets.loc[i].index,
                        annot=True,
                        fmt=f'.{precision}f',
                        ax=axs[1 + n],
                        cmap=next(target_cmaps),
                        center=0,
                        vmin=min(pd.core.common.flatten(targets.loc[i].values)),
                        vmax=max(pd.core.common.flatten(targets.loc[i].values)) or 1,
                        cbar=False)

        for ax in axs:
            sns.mpl.pyplot.sca(ax)
            sns.mpl.pyplot.yticks(rotation=0)

            # add vertical lines for central step-matrix
            if centered_position is not None:
                ax.vlines([centered_position-0.02, centered_position+0.98],
                          *ax.get_ylim(),
                          colors='Black',
                          linewidth=0.7)

    else:
        sns.mpl.pyplot.sca(axs)
        sns.mpl.pyplot.yticks(rotation=0)
        # add vertical lines for central step-matrix
        if centered_position is not None:
            axs.vlines([centered_position-0.02, centered_position+0.98],
                       *axs.get_ylim(),
                       colors='Black',
                       linewidth=0.7)

    plot_name = plot_name or 'step_matrix_{}'.format(datetime.now()).replace(':', '_').replace('.', '_') + '.svg'
    plot_name = data.rete.retention_config['experiments_folder'] + '/' + plot_name

    return heatmap, plot_name, None, data.rete.retention_config


