# Compartmental herd model

The herd dynamics model is a compartmental model in which herds (livestock populations) are divided by sex and age classes. Each sex class (male and female) is classified into three age groups (neonate, juvenile and adult) resulting in six sex-age groups. The model simulates the herd dynamics based on demographic (birth and death rates) and offtake rates in a monthly time step for one year.

The simulation of the model produces annual production offtakes (live animal, milk, draft power, hides, manure etc.) and their respective monetary values (revenue) based on prices for these production outputs. It also estimates the change in total expenditure on production inputs: feed, labor and animal health care. The revenue and costs from the herd model enable the calculation of gross margins for the simulated populations.

The gross margin is calculated for different scenarios formed by combination of sex-age groups, production systems and incremental improvement in health statuses.

The parameters of the herd dynamics model include:

**Population dynamics**
- Initial population (number of head) for each of the 6 sex-age groups
- Growth rate from neonate to juvenile and from juvenile to adult
- Fertility rate
- Mortality rates for neonates, juveniles, adult females, and adult males
- Cull rates for adult males and females

**Production Values**
- Liveweight conversion for each of the 6 sex-age groups
- Offtake rates for adult males and adult females
- Carcass yield as % of liveweight
- Lactation
    - Proportion of adult females lactating
	- Lactation duration (days)
	- Average daily milk yield (liters)
	- Monetary value of milk
- Draught (cattle only)
    - Castration rate of adult males
	- Draught usage rate
	- Monetary value of draught per head per day
- Monetary value of live animals for each of the 6 sex-age groups
- Hide production rate
- Monetary value of hides
- Manure production rate for each age group (kg per day)
- Monetary value of manure

**Costs**
- Feed requirements and costs
    - Dry matter feed requirements for each of the 6 sex-age groups (proportion of liveweight)
    - Proportion of livestock keepers that purchase feed
    - Dry matter in feed as proportion of weight
    - Feed cost per kg dry matter
- Cost of labor for livestock keepers per head per month
    - Separate for Cattle, Oxen, and Dairy (cattle only)
- Health expenditure per head per month
    - Preventative care
	- Treatment
- Capital costs
    - Interest rate
	- Infrastructure cost per head