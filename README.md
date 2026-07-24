# The Digital Divide and Economic Performance in the EU-27

**Bachelor thesis project — Mohamed Mohamady**
Business Informatics (*Wirtschaftsinformatik*), Universität Paderborn

> **Research question:** *To what extent do digital infrastructure and digital adoption explain differences in economic performance among EU-27 member states?*

This repository contains the complete empirical pipeline for the thesis, including the source data, data preparation, exploratory clustering, panel regression analysis, generated figures and tables, and the written thesis.

---

## 1. Overview

* **Scope:** EU-27 member states, 2017–2024
* **Unit of analysis:** country-year
* **Observations:** 27 countries × 8 years = **216**
* **Dependent variable:** GDP per capita in Purchasing Power Standards (PPS)
* **Data sources:** Eurostat and the World Bank

The empirical analysis consists of two complementary strands:

1. **K-Means clustering** identifies digital and innovation-related country profiles based on average differences between EU member states.
2. **Two-way fixed-effects panel regressions** examine how changes in digital indicators within countries over time are associated with changes in GDP per capita.

The regression analysis includes country and year fixed effects, country-clustered standard errors, and interaction terms between digital adoption and education.

The study is observational. The cluster analysis describes between-country patterns, while the panel regressions estimate conditional within-country associations. Neither analysis establishes causal effects.

---

## 2. Repository structure

```text
Bachelorarbeit/
├── 01_Data/
│   ├── raw/                           # Original Eurostat and World Bank data
│   └── final/
│       └── master_panel.xlsx          # Raw master panel used as pipeline input
│
├── 02_Code/
│   └── final_notebooks/
│       ├── 01_data_preparation.ipynb  # Cleaning, interpolation and descriptive outputs
│       ├── 02_clustering.ipynb        # K-Means analysis and cluster outputs
│       ├── 03_regression.ipynb        # Models M1–M10, VIF and interaction analysis
│       ├── utils.py                   # Shared functions and configuration
│       └── README.md
│
├── 03_Output/
│   └── final_run/                     # Generated data, figures and tables
│
├── 04_Literature/                     # Literature used for the thesis
│
└── 05_Thesis/
    └── chapters/
        ├── Bachelorarbeit_mohamady.docx
        └── Bachelorarbeit_mohamady.pdf
```

The contents of `04_Literature/` are intended for local academic use and should not be redistributed publicly unless permitted by the respective copyright holders.

---

## 3. Data

| Aspect                   | Detail                                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------------------------ |
| **Countries**            | 27 EU member states                                                                                    |
| **Period**               | 2017–2024                                                                                              |
| **Observations**         | 216 country-years                                                                                      |
| **Dependent variable**   | GDP per capita in PPS                                                                                  |
| **Eurostat variables**   | GDP, internet access, internet use, internet purchases, cloud computing, R&D expenditure and education |
| **World Bank variables** | Fixed broadband, secure internet servers and high-tech exports                                         |

The cleaned analysis panel is generated at:

```text
03_Output/final_run/master_panel_clean.xlsx
```

It contains the following variables:

```text
Country
Year
GDP Per Capita PPS
Internet Access
Internet Use
Internet Purchases
Cloud Computing
Fixed_Broadband
Secure_Servers
HighTech_Exports
R&D expenditure
Education
```

`Education` measures the share of the population aged 15–64 with an educational attainment level of ISCED 3–8.

### Data preparation

* Four isolated missing observations in Internet Access, Internet Use and Internet Purchases are completed through country-specific linear interpolation.
* Digital Skills is excluded because 162 of 216 observations are missing.
* Cloud Computing contains 87 missing observations. Values between observed years are linearly interpolated, while missing values at the beginning or end of a country series are completed using the nearest observed value.
* Because approximately 40% of the Cloud Computing observations are not original measurements, the variable is used only in the exploratory cluster analysis and not in the panel regressions.
* The Internet Purchases series combines Eurostat dataset `isoc_ec_ibuy` up to 2019 with `isoc_ec_ib20` from 2020 onwards. A measurement-related break between 2019 and 2020 cannot be completely excluded.

`master_panel_clean.xlsx` is a generated output. Notebook 01 creates the file, and notebooks 02 and 03 use it as their input.

---

## 4. Methodology

### 4.1 K-Means clustering

The clustering analysis is implemented in:

```text
02_Code/final_notebooks/02_clustering.ipynb
```

K-Means is applied to standardised country averages for seven digital and innovation-related indicators:

* Internet Access
* Internet Use
* Cloud Computing
* Fixed Broadband
* Secure Internet Servers
* High-Tech Exports
* R&D Expenditure

GDP per capita is deliberately excluded from the clustering inputs. The resulting clusters therefore represent digital and innovation-related profiles rather than income groups.

The algorithm is estimated with:

```text
k = 2
random_state = 42
n_init = 10
```

Solutions with two to eight clusters are compared using the elbow method and the silhouette score. The silhouette score is highest at `k = 2` at approximately 0.319, while the elbow plot does not show a clear kink. The two-cluster solution is therefore selected primarily on the basis of the silhouette criterion.

The analysis identifies:

* **Advanced Digital Economies:** 14 member states
* **Catching-up Economies:** 13 member states

The labels reflect differences in the countries’ digital and innovation-related profiles. GDP per capita is compared only after the clusters have been formed.

The two-cluster solution provides a useful representation of the main structure in the data but does not imply that the underlying differences between EU member states are strictly binary rather than gradual.

### 4.2 Panel regression

The regression analysis is implemented in:

```text
02_Code/final_notebooks/03_regression.ipynb
```

The main specification is a two-way fixed-effects model with:

* country fixed effects;
* year fixed effects;
* country-clustered standard errors;
* GDP per capita in PPS as the dependent variable.

The models are estimated with `linearmodels.PanelOLS`.

Ten specifications are reported:

* **M1–M3:** individual internet access and adoption indicators;
* **M4:** diagnostic illustration of multicollinearity between the three internet variables;
* **M5–M6:** interactions between digital adoption and education;
* **M7–M9:** fixed broadband, secure internet servers and high-tech exports;
* **M10:** final combined specification.

M4 is used only to illustrate the consequences of jointly including the highly correlated internet indicators and is not interpreted substantively.

### 4.3 Interaction analysis

The interaction variables are grand-mean centred before the product terms are constructed. The models include both constituent terms alongside the interaction term.

Marginal associations are calculated as a function of education and presented with 95% confidence intervals based on the delta method.

### 4.4 Diagnostics

The correlation matrix shows high correlations between Internet Access, Internet Use and Internet Purchases.

When these variables are included jointly, Internet Use reaches a VIF of 11.63. In the centred final model M10, all VIF values are below 2.7. According to the applied rule of thumb, M10 therefore shows no indication of problematic multicollinearity.

---

## 5. Key results

### 5.1 Cluster analysis

The clustering analysis identifies two distinct digital and innovation-related country profiles.

The Advanced Digital Economies cluster contains 14 countries, while the Catching-up Economies cluster contains 13 countries. The advanced profile displays higher average values across most of the digital and innovation indicators.

Average GDP per capita, which was not used to construct the clusters, differs considerably between the two groups:

* **Advanced Digital Economies:** approximately 43,004 PPS
* **Catching-up Economies:** approximately 25,796 PPS

The result shows that stronger digital and innovation-related country profiles are associated with higher average economic performance. It does not establish that digitalisation causes the observed income difference.

### 5.2 Panel regression

The individual indicators for internet access, internet use, internet purchases, fixed broadband and secure internet servers do not show statistically significant independent associations with GDP per capita in the estimated models.

Three findings are particularly relevant:

* **R&D expenditure** shows the most consistent positive association with GDP per capita and is statistically significant across all ten specifications.
* **High-Tech Exports** has a positive and statistically significant coefficient in models M9 and M10.
* The interactions between **digital adoption and education** are positive and statistically significant in the interaction models.

The interaction between Internet Purchases and Education remains positive and significant in the final model M10. This indicates that the estimated association between internet purchases and GDP per capita becomes more positive as the education level increases.

The marginal point estimate becomes positive at an education level of approximately 67%. However, the 95% confidence interval continues to include zero. This value must therefore not be interpreted as a statistically significant threshold.

### 5.3 Final model M10

| Variable                       | Coefficient | p-value |
| ------------------------------ | ----------: | ------: |
| Internet Purchases             |       79.51 |   0.383 |
| High-Tech Exports              |      191.54 |   0.024 |
| R&D Expenditure                |       11.44 |   0.029 |
| Education                      |      487.55 |   0.080 |
| Internet Purchases × Education |        7.69 |   0.045 |
| Within R²                      |      0.5082 |         |
| Observations                   |         216 |         |

Model M10 has the highest within R² among the reported specifications. The value increases from approximately 0.35 in M1 to approximately 0.51 in M10.

A higher within R² indicates that M10 accounts for a larger share of the within-country variation in GDP per capita. It does not by itself demonstrate a superior causal model.

---

## 6. Outputs

All generated outputs are stored in:

```text
03_Output/final_run/
```

### Tables

* T1 — Variable overview
* T2 — Missing values and data treatment
* T3 — Descriptive statistics
* T4 — Model overview
* T5 — VIF results
* T6 — Cluster composition
* T7 — Regression results for M1–M10
* T8 — Detailed results for M10

### Figures

* Correlation matrix
* Elbow and silhouette comparison
* EU cluster map
* Cluster radar diagram
* Cluster heatmap
* GDP per capita by cluster
* Internet-use trend by cluster
* Regression coefficient plot
* Marginal-association plots for M5, M6 and M10
* R&D expenditure and GDP per capita scatter plot
* Within R² model comparison

Figures are rendered as high-resolution PNG files at 300 dpi for inclusion in the thesis.

---

## 7. Reproducing the analysis

### Environment

The project uses Python and Jupyter. The main packages are:

```text
pandas
numpy
matplotlib
statsmodels
linearmodels
scikit-learn
openpyxl
```

The local Jupyter kernel is named:

```text
bachelorarbeit
```

### Execution order

Run the notebooks in the following order:

```bash
# Run from the project root

jupyter nbconvert \
  --to notebook \
  --execute \
  --inplace \
  02_Code/final_notebooks/01_data_preparation.ipynb

jupyter nbconvert \
  --to notebook \
  --execute \
  --inplace \
  02_Code/final_notebooks/02_clustering.ipynb

jupyter nbconvert \
  --to notebook \
  --execute \
  --inplace \
  02_Code/final_notebooks/03_regression.ipynb
```

Notebook 01 reads:

```text
01_Data/final/master_panel.xlsx
```

and writes:

```text
03_Output/final_run/master_panel_clean.xlsx
```

Notebooks 02 and 03 depend on this cleaned panel and generate the remaining figures and tables in `03_Output/final_run/`.

Each notebook is designed to execute cleanly from top to bottom. The workflow is sequential rather than fully independent because notebooks 02 and 03 require the output generated by notebook 01.

The notebooks include verification cells for key results, including:

* cluster sizes and averages;
* M10 coefficients;
* M10 within R² of 0.5082.

The fixed K-Means random state ensures that the clustering results are reproducible.

---

## 8. Thesis document

The written thesis and its rendered PDF are stored in:

```text
05_Thesis/chapters/
```

Files:

```text
Bachelorarbeit_mohamady.docx
Bachelorarbeit_mohamady.pdf
```

The figures and tables included in the thesis are generated by the notebooks and stored in `03_Output/final_run/`.

---

*Data sources: Eurostat and World Bank, 2017–2024. Own calculations. N = 216.*
