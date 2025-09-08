# RedChip's Advertising Impact on Stock Returns

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/yourusername/Campaign-Impact-Analysis)

## Overview

RedChip is an advertising agency that offers services to small-cap public companies. They advertise 
for their clients on TV networks such as Fox, ABC, NBC, and more. You can read more about their advertising here:
https://www.redchip.com/corporate/media_production

I wanted to analyze the impact/correlation of these advertising campaigns with underlying movements in the stock price
after spotting an overlay with a spike in share price. This notebook incorporates some non-parametric 
tests (Mann-Whitney U, Kolmogorov-Smirnov) to test for differences in population distributions (pre vs post campaign);
GARCH fitting and forecasting to compare expected vs realized volatility over the campaign period; aggregate statistics
demonstrating the differences in pre vs post-campaign price movement, and visualizations along the way.

Such findings in the notebook indicate potential trading opportunities, even for the uninformed (those unaware
of an impending advertising campaign). Whether or not the campaigns lead to lasting investor awareness/capital
for the public company is unclear. This project only addresses short-term impacts.

Further analysis could involve aggregating campaign impacts across different advertising companies, assessing the 
effect on derivatives if present (none of the companies in this analysis offered publicly traded options), 
fitting more Conditional Heteroskedastic Models, and assessing intra-day price fluctuations.

If you have any questions about this project or would like to reach out, feel free to do so at ase9pz@virginia.edu

`Campaign_Impact.ipynb` contains the full workflow for running the analysis.
`Scraper.py` and `ticker_configs.py` are used to scrape the RedChip catalog for companies for which they ran campaigns.


## Table of Contents

- [Overview](#overview)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Outputs](#outputs)  
- [License](#license)  

## Installation

Clone the repository and install dependencies:

```bash
git clone <https://github.com/nemmo-ciccone/RedChip-Analysis>
cd Campaign-Impact-Analysis
pip install -r requirements.txt
```
## Usage

Open the Jupyter notebook and run all cells:

```bash
jupyter notebook Campaign_Impact.ipynb
```
