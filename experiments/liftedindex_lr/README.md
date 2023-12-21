# Lifted Index Linear Regression Experiment
The easiest machine learning model to experiment with is a linear regression. Let's see if we can train a linear regression model to predict a basic severe weather parameter. I chose the Lifted Index because it is one of the simpler calculations. If we can accurately predict this value, we may be able to predict much more complicated parameters.

## Why Bother
The point of this experiment is to become familiar with IGRA data, the severe weather forecasting process, and learn machine learning techniques. This is a necessary stepping stone before we can dive into more complicated experiments in the future.

tl;dr; - Learn to crawl first

## Lifted Index
The Lifted Index (LI) is a calculation that provides a number that predicts the unstability of the atmosphere. It represents the difference in temperature at 500mb between the actual atomosphere and a parcel of air lifted from the surface to 500mb.

    LI = ActualTemp@500mb - LiftedParcelTemp@500mb

The significance is simple: heat rises. If the lifted parcel's temperature at altitude is greater than the actual temperature, this is an unstable situation. The air will rise, potentially causing a thunderstorm.

There is almost always a temperature inversion lower in the atmosphere. This prevents parcels of air from being lifted. In other words, just because there's a large temperature delta, it does not gaurantee thunderstrorms. Thunderstorms can only happen if there is unstable air aloft, and the temperature inversion can be overcome.

## Interpretation of LI:
The lower the LI, the more unstable the atmosphere is. LI does not take into account the strength of the temperature inversion (cap). A low value therefore does not guarentee a thunderstorm.

- LI > 0: Stable atmosphere, no thunderstorms
- -6 > LI > 0: Unstable, thunderstorms possible
- LI < -6: Very unstable, severe thunderstorms possbile

## Data
Completed the steps in the README file up one level in the /experiments/ folder. Once you have the data, you can proceed.

## Required Python Packages
The notebooks in this section assume the following packages are installed.

### OlieIgra
The olieigra package is necessary to parse the IGRA files. Follow the link for installation instructions.

[OlieIgra Installation Instructions](https://github.com/olievortex/olieigra)

### MetPy
MetPy is used to calculate the Lifted Index.

    # Conda packages
    %conda install -c conda-forge metpy

[MetPy documentation](https://unidata.github.io/MetPy/latest/api/generated/metpy.calc.lifted_index.html)
