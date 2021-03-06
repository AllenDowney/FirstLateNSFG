import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import re
import os

class FixedWidthVariables(object):
    """Represents a set of variables in a fixed width file."""

    def __init__(self, variables, index_base=0):
        """Initializes.

        variables: DataFrame
        index_base: are the indices 0 or 1 based?

        Attributes:
        colspecs: list of (start, end) index tuples
        names: list of string variable names
        """
        self.variables = variables

        # note: by default, subtract 1 from colspecs
        self.colspecs = variables[['start', 'end']] - index_base

        # convert colspecs to a list of pair of int
        self.colspecs = self.colspecs.astype(np.int).values.tolist()
        self.names = variables['name']

    def read_fixed_width(self, filename, **options):
        """Reads a fixed width ASCII file.

        filename: string filename

        returns: DataFrame
        """
        df = pd.read_fwf(filename,
                             colspecs=self.colspecs,
                             names=self.names,
                             **options)
        return df


def read_stata_dict(dct_file, **options):
    """Reads a Stata dictionary file.

    dct_file: string filename
    options: dict of options passed to open()

    returns: FixedWidthVariables object
    """
    type_map = dict(byte=int, int=int, long=int, float=float,
                    double=float, numeric=float)

    var_info = []
    with open(dct_file, **options) as f:
        for line in f:
            match = re.search( r'_column\(([^)]*)\)', line)
            if not match:
                continue
            start = int(match.group(1))
            t = line.split()
            vtype, name, fstring = t[1:4]
            name = name.lower()
            if vtype.startswith('str'):
                vtype = str
            else:
                vtype = type_map[vtype]
            long_desc = ' '.join(t[4:]).strip('"')
            var_info.append((start, vtype, name, fstring, long_desc))

    columns = ['start', 'type', 'name', 'fstring', 'desc']
    variables = pd.DataFrame(var_info, columns=columns)

    # fill in the end column by shifting the start column
    variables['end'] = variables.start.shift(-1)
    variables.loc[len(variables)-1, 'end'] = 0

    dct = FixedWidthVariables(variables, index_base=1)
    return dct


def read_stata(dct_name, dat_name, **options):
    """Reads Stata files from the given directory.

    dirname: string

    returns: DataFrame
    """
    dct = read_stata_dict(dct_name)
    df = dct.read_fixed_width(dat_name, **options)
    return df


def read_gss(dirname):
    """Reads GSS files from the given directory.
    
    In general, Pandas can read data in most standard formats, 
    including CSV, Excel, Stata, and SPSS.  
    
    Unfortunately, the current version of Pandas cannot 
    read the data generated by GSS.

    As a workaround, I wrote functions to read the 
    Stata dictionary file and use the information there to 
    read the Stata data file using `pd.read_fwf`,
    which reads fixed-width files.
    
    dirname: string
    
    returns: DataFrame
    """
    dct_file = os.path.join(dirname, 'GSS.dct')
    dct = read_stata_dict(dct_file)
    
    data_file = os.path.join(dirname, 'GSS.dat.gz')
    gss = dct.read_fixed_width(data_file, compression='gzip')
    
    return gss


def gss_replace_invalid(df):
    """Replace invalid data with NaN.
    
    df: DataFrame
    """
    df.realinc.replace([0], np.nan, inplace=True)                  
    df.educ.replace([98, 99], np.nan, inplace=True)
    # 89 means 89 or older
    df.age.replace([98, 99], np.nan, inplace=True) 
    df.cohort.replace([9999], np.nan, inplace=True)
    df.adults.replace([9], np.nan, inplace=True)
    df.colhomo.replace([0, 8, 9], np.nan, inplace=True)
    df.libhomo.replace([0, 8, 9], np.nan, inplace=True)
    df.cappun.replace([0, 8, 9], np.nan, inplace=True)
    df.gunlaw.replace([0, 8, 9], np.nan, inplace=True)
    df.grass.replace([0, 8, 9], np.nan, inplace=True)
    df.fepol.replace([0, 8, 9], np.nan, inplace=True)
    df.abany.replace([0, 8, 9], np.nan, inplace=True)
    df.prayer.replace([0, 8, 9], np.nan, inplace=True)
    df.sexeduc.replace([0, 8, 9], np.nan, inplace=True)
    df.premarsx.replace([0, 8, 9], np.nan, inplace=True)
    df.xmarsex.replace([0, 8, 9], np.nan, inplace=True)
    df.homosex.replace([0, 5, 8, 9], np.nan, inplace=True)
    df.racmar.replace([0, 8, 9], np.nan, inplace=True)
    df.spanking.replace([0, 8, 9], np.nan, inplace=True)
    df.racpres.replace([0, 8, 9], np.nan, inplace=True)
    df.fear.replace([0, 8, 9], np.nan, inplace=True)
    df.databank.replace([0, 8, 9], np.nan, inplace=True)
    df.affrmact.replace([0, 8, 9], np.nan, inplace=True)
    df.happy.replace([0, 8, 9], np.nan, inplace=True)
    df.hapmar.replace([0, 8, 9], np.nan, inplace=True)
    df.natspac.replace([0, 8, 9], np.nan, inplace=True)
    df.natenvir.replace([0, 8, 9], np.nan, inplace=True)
    df.natheal.replace([0, 8, 9], np.nan, inplace=True)
    df.natcity.replace([0, 8, 9], np.nan, inplace=True)
    df.natcrime.replace([0, 8, 9], np.nan, inplace=True)
    df.natdrug.replace([0, 8, 9], np.nan, inplace=True)
    df.nateduc.replace([0, 8, 9], np.nan, inplace=True)
    df.natrace.replace([0, 8, 9], np.nan, inplace=True)
    df.natarms.replace([0, 8, 9], np.nan, inplace=True)
    df.nataid.replace([0, 8, 9], np.nan, inplace=True)
    df.natfare.replace([0, 8, 9], np.nan, inplace=True)
    df.health.replace([0, 8, 9], np.nan, inplace=True)
    df.life.replace([0, 8, 9], np.nan, inplace=True)
    df.helpful.replace([0, 8, 9], np.nan, inplace=True)
    df.fair.replace([0, 8, 9], np.nan, inplace=True)
    df.trust.replace([0, 8, 9], np.nan, inplace=True)
    df.conclerg.replace([0, 8, 9], np.nan, inplace=True)
    df.coneduc.replace([0, 8, 9], np.nan, inplace=True)
    df.confed.replace([0, 8, 9], np.nan, inplace=True)
    df.conpress.replace([0, 8, 9], np.nan, inplace=True)
    df.conjudge.replace([0, 8, 9], np.nan, inplace=True)
    df.conlegis.replace([0, 8, 9], np.nan, inplace=True)
    df.conarmy.replace([0, 8, 9], np.nan, inplace=True)
    df.spkhomo.replace([0, 8, 9], np.nan, inplace=True)
    df.spkath.replace([0, 8, 9], np.nan, inplace=True)
    df.colath.replace([0, 8, 9], np.nan, inplace=True)
    df.libath.replace([0, 8, 9], np.nan, inplace=True)
    df.spkrac.replace([0, 8, 9], np.nan, inplace=True)
    df.spkcom.replace([0, 8, 9], np.nan, inplace=True)
    df.spkmil.replace([0, 8, 9], np.nan, inplace=True)
    df.satjob.replace([0, 8, 9], np.nan, inplace=True)
    df.satfin.replace([0, 8, 9], np.nan, inplace=True)
    df.finrela.replace([0, 8, 9], np.nan, inplace=True)

    df.union_.replace([0, 8, 9], np.nan, inplace=True)
    df.res16.replace([0, 8, 9], np.nan, inplace=True)

    df.fund.replace([0, 8, 9], np.nan, inplace=True)
    df.memchurh.replace([0, 8, 9], np.nan, inplace=True)
    df.fund16.replace([0, 8, 9], np.nan, inplace=True)
    df.reliten.replace([0, 8, 9], np.nan, inplace=True)
    df.postlife.replace([0, 8, 9], np.nan, inplace=True)
    df.pray.replace([0, 8, 9], np.nan, inplace=True)
    df.sprel16.replace([0, 8, 9], np.nan, inplace=True)
    df.hunt.replace([0, 8, 9], np.nan, inplace=True)
    df.polviews.replace([0, 8, 9], np.nan, inplace=True)

    df.compuse.replace([0, 8, 9], np.nan, inplace=True)

    df.degree.replace([8, 9], np.nan, inplace=True)
    df.padeg.replace([8, 9], np.nan, inplace=True)
    df.madeg.replace([8, 9], np.nan, inplace=True)
    df.spdeg.replace([8, 9], np.nan, inplace=True)
    df.partyid.replace([8, 9], np.nan, inplace=True)

    df.chldidel.replace([-1, 8, 9], np.nan, inplace=True)

    df.attend.replace([9], np.nan, inplace=True)
    df.childs.replace([9], np.nan, inplace=True)
    df.adults.replace([9], np.nan, inplace=True)

    df.divorce.replace([0, 8, 9], np.nan, inplace=True)
    df.agewed.replace([0, 98, 99], np.nan, inplace=True)
    df.relig.replace([0, 98, 99], np.nan, inplace=True)
    df.relig16.replace([0, 98, 99], np.nan, inplace=True)
    df.age.replace([0, 98, 99], np.nan, inplace=True)
    
    # note: sibs contains some unlikely numbers
    df.sibs.replace([-1, 98, 99], np.nan, inplace=True)
    df.educ.replace([97, 98, 99], np.nan, inplace=True)
    df.maeduc.replace([97, 98, 99], np.nan, inplace=True)
    df.paeduc.replace([97, 98, 99], np.nan, inplace=True)
    df.speduc.replace([97, 98, 99], np.nan, inplace=True)

    df.cohort.replace([0, 9999], np.nan, inplace=True)
    df.marcohrt.replace([0, 9999], np.nan, inplace=True)

    df.phone.replace([0, 2, 9], np.nan, inplace=True)
    df.owngun.replace([0, 3, 8, 9], np.nan, inplace=True)
    df.pistol.replace([0, 3, 8, 9], np.nan, inplace=True)
    df.class_.replace([0, 5, 8, 9], np.nan, inplace=True)
    df.pres04.replace([0, 8, 9], np.nan, inplace=True)
    df.pres08.replace([0, 8, 9], np.nan, inplace=True)
    df.pres12.replace([0, 8, 9], np.nan, inplace=True)


def sample_rows(df, nrows, replace=False):
    """Choose a sample of rows from a DataFrame.

    df: DataFrame
    nrows: number of rows
    replace: whether to sample with replacement

    returns: DataDf
    """
    indices = np.random.choice(df.index, nrows, replace=replace)
    sample = df.loc[indices]
    return sample


def resample_rows(df):
    """Resamples rows from a DataFrame.

    df: DataFrame

    returns: DataFrame
    """
    return sample_rows(df, len(df), replace=True)


def resample_rows_weighted(df, column='finalwgt'):
    """Resamples a DataFrame using probabilities proportional to given column.

    df: DataFrame
    column: string column name to use as weights

    returns: DataFrame
    """
    weights = df[column].copy()
    weights /= sum(weights)
    indices = np.random.choice(df.index, len(df), replace=True, p=weights)
    sample = df.loc[indices]
    return sample


def resample_by_year(df, column='finalwgt'):
    """Resample rows within each year.

    df: DataFrame
    column: string name of weight variable

    returns DataFrame
    """
    grouped = df.groupby('year')
    samples = [resample_rows_weighted(group, column)
               for _, group in grouped]
    sample = pd.concat(samples, ignore_index=True)
    return sample


def values(series):
    """Count the values and sort.
    
    series: pd.Series
    
    returns: series mapping from values to frequencies
    """
    return series.value_counts().sort_index()

def count_by_year(gss, varname):
    """Groups by category and year and counts.

    gss: DataFrame
    varname: string variable to group by

    returns: DataFrame with one row per year, one column per category.
    """
    grouped = gss.groupby([varname, 'year'])
    count = grouped[varname].count().unstack(level=0)

    # note: the following is not ideal, because it does not
    # distinguish 0 from NA, but in this dataset the only
    # zeros are during years when the question was not asked.
    count = count.replace(0, np.nan).dropna()
    return count
    
def fill_missing(df, varname, badvals=[98, 99]):
    """Fill missing data with random values.

    df: DataFrame
    varname: string column name
    badvals: list of values to be replaced
    """
    # replace badvals with NaN
    df[varname].replace(badvals, np.nan, inplace=True)

    # get the index of rows missing varname
    null = df[varname].isnull()
    n_missing = sum(null)

    # choose a random sample from the non-missing values
    fill = np.random.choice(df[varname].dropna(), n_missing, replace=True)

    # replace missing data with the samples
    df.loc[null, varname] = fill

    # return the number of missing values replaced
    return n_missing


def round_into_bins(df, var, bin_width, high=None, low=0):
    """Rounds values down to the bin they belong in.

    df: DataFrame
    var: string variable name
    bin_width: number, width of the bins

    returns: array of bin values
    """
    if high is None:
        high = df[var].max()

    bins = np.arange(low, high+bin_width, bin_width)
    indices = np.digitize(df[var], bins)
    return bins[indices-1]


def underride(d, **options):
    """Add key-value pairs to d only if key is not in d.

    d: dictionary
    options: keyword args to add to d
    """
    for key, val in options.items():
        d.setdefault(key, val)

    return d


def decorate(**options):
    """Decorate the current axes.
    Call decorate with keyword arguments like
    decorate(title='Title',
             xlabel='x',
             ylabel='y')
    The keyword arguments can be any of the axis properties
    https://matplotlib.org/api/axes_api.html
    In addition, you can use `legend=False` to suppress the legend.
    And you can use `loc` to indicate the location of the legend
    (the default value is 'best')
    """
    loc = options.pop('loc', 'best')
    if options.pop('legend', True):
        legend(loc=loc)

    plt.gca().set(**options)
    plt.tight_layout()


def legend(**options):
    """Draws a legend only if there is at least one labeled item.
    options are passed to plt.legend()
    https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html
    """
    underride(options, loc='best')

    ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    #TODO: don't draw if there are none
    ax.legend(handles, labels, **options)

from statsmodels.nonparametric.smoothers_lowess import lowess

def make_lowess(series):
    """Use LOWESS to compute a smooth line.

    series: pd.Series

    returns: pd.Series
    """
    endog = series.values
    exog = series.index.values

    smooth = lowess(endog, exog)
    index, data = np.transpose(smooth)

    return pd.Series(data, index=index)

def plot_series_lowess(series, color):
    """Plots a series of data points and a smooth line.

    series: pd.Series
    color: string or tuple
    """
    series.plot(lw=0, marker='o', color=color, alpha=0.5)
    smooth = make_lowess(series)
    smooth.plot(label='_', color=color)

def plot_columns_lowess(df, columns, colors):
    """Plot the columns in a DataFrame.

    df: pd.DataFrame
    columns: list of column names, in the desired order
    colors: mapping from column names to colors
    """
    for col in columns:
        series = df[col]
        plot_series_lowess(series, colors[col])

def anchor_legend(x, y):
    """Put the legend at the given locationself.

    x: axis coordinate
    y: axis coordinate
    """
    plt.legend(bbox_to_anchor=(x, y), loc='upper left', ncol=1)
