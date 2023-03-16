from IPython.display import Image, display
import pandas as pd
import plotly.express as px
import numpy as np

def variancestats(df, var):
    d = dict()
    d["mean"] = df[var].mean()
    d["std"] = df[var].std()
    d["q25th"] = df[var].quantile(0.25)
    d["q75th"] = df[var].quantile(0.75)

    return d

def zscore(df, var):
    r = variancestats(df, var)
    mean = r["mean"]
    std = r["std"]

    zscorevar = "{}_zscore".format(var)
    outliervar = "{}_zscore_outlier".format(var)

    df[zscorevar] = (df[var] - mean) / std
    df[outliervar] = 0
    df.loc[np.abs(df[zscorevar]) >= 2, outliervar] = 1

    return df

def zscore_analysis(df, var):
    dt = df.copy()
    dt = zscore(dt, var)

    zscorevar = "{}_zscore".format(var)
    outliervar = "{}_zscore_outlier".format(var)

    dt = dt.groupby([var, zscorevar, outliervar]).agg({"c": "sum"})
    dt.reset_index(inplace=True)

    fig = px.scatter(dt, x=var, y="c", color=zscorevar)
    render_fig(fig)

def corr_analysis(df, var, y):
    dt = df.copy()
    dt = zscore(dt, var)

    zscorevar = "{}_zscore".format(var)
    outliervar = "{}_zscore_outlier".format(var)

    dt = dt.groupby([var, zscorevar, outliervar]).agg({y: "avg"})
    dt.reset_index(inplace=True)

    fig = px.scatter(dt, x=var, y=y, color=zscorevar)
    render_fig(fig)


def aggrsimple(df, col, key):
    dgrouped = df.groupby([col, key]).agg({"c": "sum"})
    dgrouped.sort_index()
    dgrouped.reset_index(inplace=True)

    dgrouped_pcts = dgrouped.groupby(col).sum()

    # group two rows with varying Feature "Key" into a single one
    dgrouped = dgrouped.join(dgrouped_pcts, on=col, rsuffix="_")
    # PART = 100% of customers in the group / customers total with "Key"
    dgrouped["PART"] = np.round(100 * dgrouped["c"] / dgrouped["c_"])
    # PCT = PART . '%'
    dgrouped["PCT"] = dgrouped["PART"].astype("str") + "%"

    # total = total number of customers in the dataset
    dgrouped["total"] = dgrouped["c"].sum()

    dgrouped = dgrouped.sort_values(by="PART", ascending =False)
    return dgrouped

# Pivot categories against each other by measures
def pivotYesNo(df, flag, index="MarketingConsent"):
    d1 = aggrsimple(df, flag, index)
    d1.reset_index(inplace=True)

    import seaborn as sns
    cm = sns.light_palette("red", as_cmap = True)

    pt = pd.pivot_table(d1, index, columns=flag, values=["PART", "c"], aggfunc=np.sum, margins=True)
    pt = pt.style.background_gradient(cmap=cm)
    return pt

def createhistogram(df, key, var):
    dgrouped = df.groupby([key, var]).agg({"c": "sum"})
    dgrouped.sort_index()
    dgrouped.reset_index(inplace = True)

    fig = px.histogram(dgrouped, x=key, y="c", color=var, title="{} by{}".format(key, var), barnorm="percent")
    render_fig(fig)

staticrender = False

def render_fig(fig):
    global staticrender

    if staticrender == True:
        display(Image(fig.to_image(format="png")))
        return

    fig.show()

def set_render(static = False):
    global staticrender
    staticrender = static